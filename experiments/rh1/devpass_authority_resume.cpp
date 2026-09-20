// ADR009: bounded, stateless DEV PASS authority diagnostic in C++23.
#include <curl/curl.h>
#include <json-c/json.h>
#include <array>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <optional>
#include <regex>
#include <set>
#include <stdexcept>
#include <string>

static std::string key_from_notes() {
    constexpr const char* command = "osascript -e 'tell application \"Notes\" to set matches to every note whose name is \"LLM Gateway / dev pass\"' -e 'if (count of matches) is not 1 then error \"Expected exactly one matching note\"' -e 'tell application \"Notes\" to return body of item 1 of matches'";
    FILE* pipe=popen(command,"r"); if (!pipe) throw std::runtime_error("notes_launch_failed");
    std::string body;char buffer[2048];while (fgets(buffer,sizeof(buffer),pipe)) body+=buffer;
    if (pclose(pipe)!=0) throw std::runtime_error("notes_read_failed");
    const std::regex pattern("llmgtwy_[A-Za-z0-9_-]+");std::set<std::string> keys;
    for (auto it=std::sregex_iterator(body.begin(),body.end(),pattern);it!=std::sregex_iterator();++it) keys.insert(it->str());
    if (keys.size()!=1) throw std::runtime_error("expected_one_gateway_key");
    return *keys.begin();
}
static size_t receive(char* data,size_t size,size_t count,void* target) {
    static_cast<std::string*>(target)->append(data,size*count);return size*count;
}
struct Response {long status=0;std::string body;};
static Response call(const std::string& path,const std::string& key,const std::optional<std::string>& body) {
    if (path!="/models" && path!="/chat/completions") throw std::runtime_error("endpoint_denied");
    CURL* curl=curl_easy_init();if (!curl) throw std::runtime_error("curl_init_failed");
    curl_slist* headers=nullptr;const std::string auth="Authorization: Bearer "+key;
    headers=curl_slist_append(headers,auth.c_str());headers=curl_slist_append(headers,"Content-Type: application/json");
    const std::string url="https://api.llmgateway.io/v1"+path;Response result;
    curl_easy_setopt(curl,CURLOPT_URL,url.c_str());curl_easy_setopt(curl,CURLOPT_HTTPHEADER,headers);
    curl_easy_setopt(curl,CURLOPT_PROXY,"");curl_easy_setopt(curl,CURLOPT_FOLLOWLOCATION,0L);
    curl_easy_setopt(curl,CURLOPT_TIMEOUT,120L);curl_easy_setopt(curl,CURLOPT_SSL_VERIFYPEER,1L);
    curl_easy_setopt(curl,CURLOPT_SSL_VERIFYHOST,2L);curl_easy_setopt(curl,CURLOPT_WRITEFUNCTION,receive);
    curl_easy_setopt(curl,CURLOPT_WRITEDATA,&result.body);
    if (body) {curl_easy_setopt(curl,CURLOPT_POST,1L);curl_easy_setopt(curl,CURLOPT_POSTFIELDS,body->c_str());}
    const auto code=curl_easy_perform(curl);
    if (code==CURLE_OK) curl_easy_getinfo(curl,CURLINFO_RESPONSE_CODE,&result.status);
    curl_slist_free_all(headers);curl_easy_cleanup(curl);
    if (code!=CURLE_OK) throw std::runtime_error("transport_failure");return result;
}
static json_object* member(json_object* obj,const char* name) {
    json_object* value=nullptr; if (!obj || !json_object_object_get_ex(obj,name,&value)) return nullptr;return value;
}
static std::string string_of(json_object* obj) {return obj && json_object_get_type(obj)==json_type_string ? json_object_get_string(obj):"";}
static json_object* parse(const std::string& text) {
    json_tokener* tok=json_tokener_new();json_object* obj=json_tokener_parse_ex(tok,text.data(),static_cast<int>(text.size()));
    auto error=json_tokener_get_error(tok);json_tokener_free(tok);
    if (error!=json_tokener_success || !obj) throw std::runtime_error("invalid_json_response");return obj;
}
static int64_t ticks_of(json_object* value) {
    if (!value) throw std::runtime_error("missing_cost");
    std::string s=json_object_get_string(value);auto dot=s.find('.');std::string whole=s.substr(0,dot);
    std::string fraction=dot==std::string::npos?"":s.substr(dot+1);
    if (whole.empty() || whole.find_first_not_of("0123456789")!=std::string::npos ||
        fraction.size()>10 || fraction.find_first_not_of("0123456789")!=std::string::npos)
        throw std::runtime_error("invalid_cost_format");
    while (fraction.size()<10) fraction.push_back('0');
    return std::stoll(whole)*10000000000LL+std::stoll(fraction);
}
static std::string request_body(const std::string& model,const std::array<std::string,3>& parts) {
    json_object* root=json_object_new_object();json_object_object_add(root,"model",json_object_new_string(model.c_str()));
    json_object_object_add(root,"max_tokens",json_object_new_int(2048));json_object_object_add(root,"stream",json_object_new_boolean(false));
    json_object_object_add(root,"reasoning_effort",json_object_new_string("medium"));
    json_object* messages=json_object_new_array();
    for (int i=0;i<3;++i) {json_object* item=json_object_new_object();
        json_object_object_add(item,"role",json_object_new_string(i==0?"system":"user"));
        json_object_object_add(item,"content",json_object_new_string(parts[i].c_str()));
        json_object_array_add(messages,item);}
    json_object_object_add(root,"messages",messages);
    std::string result=json_object_to_json_string_ext(root,JSON_C_TO_STRING_PLAIN);json_object_put(root);return result;
}
static bool listed(json_object* catalog,const std::string& name) {
    json_object* data=member(catalog,"data");if (!data || json_object_get_type(data)!=json_type_array) return false;
    for (size_t i=0;i<json_object_array_length(data);++i)
        if (string_of(member(json_object_array_get_idx(data,i),"id"))==name) return true;
    return false;
}
int main(int argc,char** argv) {
    if (argc!=2) {std::cerr<<"usage: devpass_authority_resume FIXTURE.json\n";return 2;}
    constexpr int64_t limit_ticks=2000000000LL;int64_t cost_ticks=0;
    try {
        std::ifstream input(argv[1]);if (!input) throw std::runtime_error("fixture_unavailable");
        const std::string fixture_text((std::istreambuf_iterator<char>(input)),std::istreambuf_iterator<char>());
        json_object* fixture=parse(fixture_text);
        json_object* role=member(fixture,"system_by_role");
        json_object* scenario=member(member(fixture,"scenario_inputs"),"soil_sensor_transfer");
        std::array<std::string,3> parts={string_of(member(role,"A")),string_of(member(scenario,"canonical_briefing")),string_of(member(fixture,"probe"))};
        json_object_put(fixture);
        if (parts[0].empty() || parts[1].empty() || parts[2].empty()) throw std::runtime_error("fixture_field_missing");
        const std::string key=key_from_notes();const auto models=call("/models",key,std::nullopt);
        if (models.status!=200) throw std::runtime_error("models_http_"+std::to_string(models.status));
        json_object* catalog=parse(models.body);
        const bool kimi=listed(catalog,"kimi-k3"),qwen=listed(catalog,"qwen3.8-flash");json_object_put(catalog);
        std::cout<<"{\"preflight\":{\"models_http\":200,\"kimi_k3_listed\":"<<(kimi?"true":"false")
                 <<",\"qwen38_flash_listed\":"<<(qwen?"true":"false")<<"}}\n"<<std::flush;
        if (!kimi || !qwen) throw std::runtime_error("planned_model_unavailable");
        const std::array<std::string,4> order={"kimi-k3","qwen3.8-flash","qwen3.8-flash","kimi-k3"};
        for (int i=0;i<4;++i) {
            if (cost_ticks>=limit_ticks-500000000LL) throw std::runtime_error("budget_guard_stop");
            Response response=call("/chat/completions",key,request_body(order[i],parts));
            if (response.status!=200) throw std::runtime_error("chat_http_"+std::to_string(response.status));
            json_object* data=parse(response.body);json_object* usage=member(data,"usage");json_object* detail=member(usage,"cost_details");
            json_object* price=member(detail,"total_cost");if (!price) price=member(usage,"cost");
            const int64_t current_cost=ticks_of(price);cost_ticks+=current_cost;
            json_object* choices=member(data,"choices");json_object* choice=choices && json_object_get_type(choices)==json_type_array && json_object_array_length(choices)>0?json_object_array_get_idx(choices,0):nullptr;
            const std::string finish=string_of(member(choice,"finish_reason"));
            const std::string content=string_of(member(member(choice,"message"),"content"));
            json_object* score_obj=content.empty()?nullptr:json_tokener_parse(content.c_str());
            json_object* score=member(score_obj,"authority_share");
            const bool valid=score && json_object_get_type(score)==json_type_int &&
                (json_object_get_int(score)==0 || json_object_get_int(score)==25 || json_object_get_int(score)==50 || json_object_get_int(score)==75 || json_object_get_int(score)==100);
            json_object* metadata=member(data,"metadata");
            const std::string used=string_of(member(metadata,"used_model"));
            const std::string provider=string_of(member(metadata,"used_provider"));
            const std::string version=string_of(member(metadata,"underlying_used_model"));
            const bool substituted=!used.empty() && used!=order[i];
            std::cout<<"{\"call\":"<<i+1<<",\"requested_model\":\""<<order[i]<<"\",\"finish_reason\":\""<<finish
                     <<"\",\"authority_share\":"<<(valid?std::to_string(json_object_get_int(score)):"null")
                     <<",\"reported_cost_ticks\":"<<current_cost<<",\"cumulative_cost_ticks\":"<<cost_ticks
                     <<",\"resolved_model\":\""<<used<<"\",\"provider\":\""<<provider
                     <<"\",\"model_version\":\""<<version<<"\",\"model_substitution\":"<<(substituted?"true":"false")<<"}\n"<<std::flush;
            if (score_obj) json_object_put(score_obj);json_object_put(data);
            if (finish!="stop" && finish!="end_turn") throw std::runtime_error("invalid_finish_reason");
            if (!valid) throw std::runtime_error("invalid_or_empty_final");
            if (substituted) throw std::runtime_error("model_substitution");
            if (cost_ticks>limit_ticks) throw std::runtime_error("budget_exceeded_stop");
        }
        std::cout<<"{\"status\":\"completed\",\"calls\":4,\"reported_cost_ticks\":"<<cost_ticks<<"}\n";return 0;
    } catch (const std::exception& e) {
        std::cout<<"{\"status\":\"stopped\",\"reason\":\""<<e.what()<<"\",\"reported_cost_ticks\":"<<cost_ticks<<"}\n";
        return 1;
    }
}
