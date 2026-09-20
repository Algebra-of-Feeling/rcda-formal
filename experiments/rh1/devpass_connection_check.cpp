#include <curl/curl.h>
#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <optional>
#include <regex>
#include <set>
#include <stdexcept>
#include <string>

static size_t receive(char* data, size_t size, size_t count, void* target) {
    auto* text = static_cast<std::string*>(target);
    text->append(data, size * count);
    return size * count;
}
static std::string note_key() {
    constexpr const char* cmd = "osascript -e 'tell application \"Notes\" to set matches to every note whose name is \"LLM Gateway / dev pass\"' -e 'if (count of matches) is not 1 then error \"Expected exactly one matching note\"' -e 'tell application \"Notes\" to return body of item 1 of matches'";
    FILE* pipe = popen(cmd,"r");
    if (!pipe) throw std::runtime_error("notes_launch_failed");
    std::string body; char chunk[2048];
    while (fgets(chunk,sizeof(chunk),pipe)) body += chunk;
    if (pclose(pipe)!=0) throw std::runtime_error("notes_read_failed");
    std::regex pat("llmgtwy_[A-Za-z0-9_-]+");
    std::set<std::string> keys;
    for (auto it=std::sregex_iterator(body.begin(),body.end(),pat);it!=std::sregex_iterator();++it) keys.insert(it->str());
    if (keys.size()!=1) throw std::runtime_error("expected_one_gateway_key");
    return *keys.begin();
}
struct Response { long status=0; std::string body; };
static Response call(const std::string& path,const std::string& key,const std::optional<std::string>& payload) {
    if (path!="/key" && path!="/models" && path!="/chat/completions") throw std::runtime_error("endpoint_denied");
    CURL* handle=curl_easy_init(); if (!handle) throw std::runtime_error("curl_init_failed");
    Response result; struct curl_slist* headers=nullptr;
    const std::string authorization="Authorization: Bearer "+key;
    headers=curl_slist_append(headers,authorization.c_str());
    headers=curl_slist_append(headers,"Content-Type: application/json");
    const std::string url="https://api.llmgateway.io/v1"+path;
    curl_easy_setopt(handle,CURLOPT_URL,url.c_str());
    curl_easy_setopt(handle,CURLOPT_HTTPHEADER,headers);
    curl_easy_setopt(handle,CURLOPT_PROXY,"");
    curl_easy_setopt(handle,CURLOPT_FOLLOWLOCATION,0L);
    curl_easy_setopt(handle,CURLOPT_TIMEOUT,60L);
    curl_easy_setopt(handle,CURLOPT_SSL_VERIFYPEER,1L);
    curl_easy_setopt(handle,CURLOPT_SSL_VERIFYHOST,2L);
    curl_easy_setopt(handle,CURLOPT_WRITEFUNCTION,receive);
    curl_easy_setopt(handle,CURLOPT_WRITEDATA,&result.body);
    if (payload) {curl_easy_setopt(handle,CURLOPT_POST,1L);curl_easy_setopt(handle,CURLOPT_POSTFIELDS,payload->c_str());}
    const auto status=curl_easy_perform(handle);
    if (status==CURLE_OK) curl_easy_getinfo(handle,CURLINFO_RESPONSE_CODE,&result.status);
    curl_slist_free_all(headers);curl_easy_cleanup(handle);
    if (status!=CURLE_OK) throw std::runtime_error("transport_failure");
    return result;
}
static std::optional<std::string> number(const std::string& body,const std::string& name) {
    std::regex pat("\\\""+name+"\\\"\\s*:\\s*([0-9]+(?:\\.[0-9]+)?)");std::smatch m;
    if (std::regex_search(body,m,pat)) return m[1].str();
    return std::nullopt;
}
int main() {
    try {
        const auto key=note_key();
        const auto status=call("/key",key,std::nullopt);
        std::cout<<"key_http="<<status.status<<'\n';
        if (status.status!=200) return 1;
        const auto models=call("/models",key,std::nullopt);
        std::cout<<"models_http="<<models.status<<'\n';
        if (models.status!=200) return 1;
        const bool kimi=std::regex_search(models.body,std::regex(R"("id"\s*:\s*"kimi-k3")"));
        std::cout<<"kimi_k3_listed="<<(kimi?"true":"false")<<'\n';
        if (!kimi) return 0;
        constexpr const char* payload=R"({"model":"kimi-k3","messages":[{"role":"user","content":"Connection check only. Reply with exactly GATEWAY_OK."}],"max_tokens":256,"stream":false})";
        const auto answer=call("/chat/completions",key,std::string(payload));
        std::cout<<"chat_http="<<answer.status<<'\n';
        if (answer.status!=200) return 1;
        const bool final=answer.body.find("GATEWAY_OK")!=std::string::npos;
        const bool stopped=answer.body.find("\"finish_reason\":\"stop\"")!=std::string::npos ||
                           answer.body.find("\"finish_reason\": \"stop\"")!=std::string::npos;
        std::cout<<"expected_final_present="<<(final?"true":"false")<<'\n';
        std::cout<<"finish_stop="<<(stopped?"true":"false")<<'\n';
        auto price=number(answer.body,"total_cost"); if (!price) price=number(answer.body,"cost");
        std::cout<<"reported_cost_usd="<<(price?*price:"unavailable")<<'\n';
        return final && stopped ? 0:1;
    } catch (const std::exception& exc) {
        std::cerr<<"status="<<exc.what()<<'\n'; return 1;
    }
}
