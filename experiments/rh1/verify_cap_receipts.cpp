// ADR009: exact-integer C++23 verification of the four recorded API receipts.
#include <array>
#include <fstream>
#include <iostream>
#include <map>
#include <optional>
#include <stdexcept>
#include <string>

std::optional<std::string> field(const std::string& line, const std::string& name) {
    const auto key = line.find('"' + name + '"');
    if (key == std::string::npos) return std::nullopt;
    auto start = line.find(':', key);
    if (start == std::string::npos) return std::nullopt;
    start = line.find_first_not_of(" \t", start + 1);
    if (start == std::string::npos) return std::nullopt;
    if (line[start] == '"') {
        const auto end = line.find('"', start + 1);
        if (end == std::string::npos) return std::nullopt;
        return line.substr(start + 1, end - start - 1);
    }
    const auto end = line.find_first_not_of("0123456789.", start);
    if (end == start) return std::nullopt;
    return line.substr(start, end - start);
}

int64_t micros(const std::string& decimal) {
    const auto dot = decimal.find('.');
    const std::string whole = decimal.substr(0, dot);
    std::string fractional = dot == std::string::npos ? "" : decimal.substr(dot+1);
    if (fractional.size() > 6) throw std::runtime_error("Cost precision exceeds micro USD");
    while (fractional.size() < 6) fractional.push_back('0');
    return std::stoll(whole) * 1000000 + std::stoll(fractional);
}

int main(int argc, char** argv) {
    if (argc != 2) { std::cerr << "Usage: verify_cap_receipts RECEIPTS.jsonl\n"; return 2; }
    std::ifstream in(argv[1]);
    if (!in) { std::cerr << "Cannot read receipt file\n"; return 2; }
    struct Group { int attempts=0, nonempty=0, empty=0; };
    std::map<int, Group> groups;
    const std::array<int,4> expected_caps{4096,8192,8192,4096};
    int attempts = 0, violations = 0;
    int64_t cost_micro_usd = 0;
    std::string line;
    while (std::getline(in,line)) {
        if (field(line,"status") != "completed") continue; // Skip duplicate error-event rows.
        const auto call = field(line,"block_call");
        const auto cap = field(line,"max_output_tokens_returned");
        const auto tokens = field(line,"output_tokens");
        const auto price = field(line,"cost_usd");
        if (!call || !cap || !tokens || !price) throw std::runtime_error("Missing receipt field");
        const int index = std::stoi(*call);
        const int limit = std::stoi(*cap);
        const int used = std::stoi(*tokens);
        if (index < 1 || index > 4 || limit != expected_caps[index-1])
            throw std::runtime_error("Unexpected call order or cap");
        if (field(line,"model") != "grok-4.6" || field(line,"temperature_returned") != "1.7" ||
            field(line,"reasoning_effort_returned") != "high")
            throw std::runtime_error("Model, temperature or effort mismatch");
        const auto types_key = line.find("\"output_item_types\"");
        const auto types_start = line.find('[', types_key);
        const auto types_end = line.find(']', types_start);
        if (types_key == std::string::npos || types_start == std::string::npos || types_end == std::string::npos)
            throw std::runtime_error("Missing output types");
        const bool has_message = line.substr(types_start, types_end-types_start).find("\"message\"") != std::string::npos;
        auto& group = groups[limit];
        ++group.attempts;
        if (has_message) {
            if (line.find(R"(authority_share\":25)") == std::string::npos)
                throw std::runtime_error("Unexpected or missing authority score");
            ++group.nonempty;
        } else ++group.empty;
        if (used > limit) ++violations;
        cost_micro_usd += micros(*price);
        ++attempts;
    }
    if (attempts != 4 || groups[4096].attempts != 2 || groups[8192].attempts != 2)
        throw std::runtime_error("Incomplete block");
    if (groups[4096].nonempty != 1 || groups[8192].nonempty != 1 ||
        groups[4096].empty != 1 || groups[8192].empty != 1)
        throw std::runtime_error("Observed outcome counts changed");
    std::cout << "attempts=" << attempts << "\n"
              << "cap4096_nonempty=" << groups[4096].nonempty << " empty=" << groups[4096].empty << "\n"
              << "cap8192_nonempty=" << groups[8192].nonempty << " empty=" << groups[8192].empty << "\n"
              << "reported_tokens_exceed_cap=" << violations << "\n"
              << "cost_micro_usd=" << cost_micro_usd << "\n";
}
