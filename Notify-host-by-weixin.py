#host
import urllib.request
import json
import sys
#以上是导入模块
#创建获取AccessToken的方法
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
#这里是发送消息的方法
def senddata(access_token,notify_str):
    send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + access_token
#传入的参数是一段字符串每个信息用separator连起来，只要再用字符串的split("separator")方法分开信息就可以了。
    notifydata = notify_str.split("separator")
    user = notifydata[0]
    cationtype = notifydata[1]
    name = notifydata[2]
    state = notifydata[3]
    address = notifydata[4]
    output = notifydata[5]
    datatime = notifydata[6]
    content = '###IDCA Host Notification###\n\n类型: ' + cationtype + '\n主机: ' + name + '\n状态: ' + state + '\n地址: ' + address + '\n摘要: ' + output + '\n时间: ' + datatime + '\n'
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
#设置为非ascii解析，使其支持中文
    send_request = urllib.request.Request(send_url, send_data)
    response = urllib.request.urlopen(send_request)
#这个是返回微信公共平台的信息，调试时比较有用
    msg = response.read()
    return msg
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
#经测试nagios只能传入一个参进python，所以把所有包括用户名跟报警主机报警信息放进一个字符串里
notifystr = str(sys.argv[1])
corpid = '**************' 
corpsecret = '****************'
accesstoken = gettoken(corpid,corpsecret)
msg = senddata(accesstoken,notifystr)
print(msg)

