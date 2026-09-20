// ADR009: exact integer-tick verification of the bounded DEV PASS JSONL receipt.
#include <json-c/json.h>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
static json_object* get(json_object* obj,const char* key) {
    json_object* value=nullptr;
    return obj && json_object_object_get_ex(obj,key,&value)?value:nullptr;
}
static std::string str(json_object* obj) {return obj?json_object_get_string(obj):"";}
int main(int argc,char** argv) {
    if (argc!=2) return 2;
    std::ifstream file(argv[1]);if (!file) throw std::runtime_error("receipt_missing");
    constexpr std::array<const char*,4> models={"kimi-k3","qwen3.8-flash","qwen3.8-flash","kimi-k3"};
    constexpr int64_t prior_ticks=76429305407LL,v02_ticks=20000000000LL;
    int count=0;int64_t total=0,kimi=0,qwen=0;bool completed=false;std::string line;
    while (std::getline(file,line)) {
        json_object* obj=json_tokener_parse(line.c_str());if (!obj) throw std::runtime_error("invalid_jsonl");
        if (get(obj,"call")) {
            if (count>=4 || json_object_get_int(get(obj,"call"))!=count+1 ||
                str(get(obj,"requested_model"))!=models[count] ||
                str(get(obj,"resolved_model"))!=models[count] ||
                str(get(obj,"finish_reason"))!="stop" ||
                json_object_get_int(get(obj,"authority_share"))!=25 ||
                json_object_get_boolean(get(obj,"model_substitution")))
                throw std::runtime_error("unexpected_call_receipt");
            const int64_t ticks=json_object_get_int64(get(obj,"reported_cost_ticks"));
            total+=ticks;if (count==0 || count==3) kimi+=ticks;else qwen+=ticks;
            if (total!=json_object_get_int64(get(obj,"cumulative_cost_ticks")))
                throw std::runtime_error("cumulative_cost_mismatch");
            ++count;
        } else if (get(obj,"status")) {
            completed=str(get(obj,"status"))=="completed" &&
                json_object_get_int(get(obj,"calls"))==4 &&
                json_object_get_int64(get(obj,"reported_cost_ticks"))==total;
        }
        json_object_put(obj);
    }
    if (count!=4 || !completed || total!=87325700LL) throw std::runtime_error("incomplete_or_changed_block");
    std::cout<<"valid_calls="<<count<<"\n"
             <<"kimi_scores=25,25\nqwen_scores=25,25\n"
             <<"kimi_cost_ticks="<<kimi<<"\nqwen_cost_ticks="<<qwen<<"\n"
             <<"block_cost_ticks="<<total<<"\n"
             <<"conservative_exposure_ticks="<<prior_ticks+total<<"\n"
             <<"with_v02_reserve_ticks="<<prior_ticks+total+v02_ticks<<"\n";
}
