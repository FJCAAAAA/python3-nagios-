#service
import urllib.request
import json
import sys
 
def gettoken(corp_id,corp_secret):
    gettoken_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=' + corp_id + '&corpsecret=' + corp_secret
    try:
        token_file = urllib.request.urlopen(gettoken_url)
    except urllib.error.HTTPError as e:
        print(e.code)
        print(e.read().decode("utf8"))
    token_data = token_file.read().decode('utf-8')
    token_json = json.loads(token_data)
    token_json.keys()
    token = token_json['access_token']
    return token
 
def senddata(access_token,notify_str):
    send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + access_token
    notifydata = notify_str.split("separator")
    user = notifydata[0]
    cationtype = notifydata[1]
    desc = notifydata[2]
    alias = notifydata[3]
    address = notifydata[4]
    state = notifydata[5]
    output = notifydata[6]
    datatime = notifydata[7]
    content ='###IDCA Service Notification ###\n\n类型: ' + cationtype + '\n\n服务: ' + desc + '\n主机: ' + alias + '\n地址: ' + address + '\n状态: ' + state  + '\n摘要:' + output + '\n时间: ' + datatime + '\n'
    send_values = {
        "touser":user,
        "msgtype":"text",
        "agentid":"1000003",
        "text":{
            "content":content
            },
        "safe":"0"
        }
    send_data = json.dumps(send_values, ensure_ascii=False).encode(encoding='UTF8')
    send_request = urllib.request.Request(send_url, send_data)
    response = urllib.request.urlopen(send_request)
    msg = response.read()
    return msg
 
 
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
notifystr = str(sys.argv[1])
corpid = '****************'
corpsecret = '**************'
accesstoken = gettoken(corpid,corpsecret)
msg = senddata(accesstoken,notifystr)
print(msg) 

