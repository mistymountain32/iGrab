import json
import time
import requests
import re


def stodic_cookie(str_cookie):
    temp_list = re.findall('[\w|.|,|\-|;]+', str_cookie)
    dic_cookie = {}
    count = 1
    last = ''
    for string in temp_list:
        if count % 2 == 1:
            last = string
        else:
            if string[-1] != ';':
                string += ';'
            dic_cookie[last] = string
        count += 1
    return dic_cookie


def dictos_cookie(dic_cookie):
    str_cookie = str(dic_cookie)
    str_cookie = str_cookie.replace('{', '')
    str_cookie = str_cookie.replace('}', '')
    str_cookie = str_cookie.replace('\'', '')
    str_cookie = str_cookie.replace(',', '')
    str_cookie = str_cookie.replace(': ', '=')
    return str_cookie


def update_cookie(r_cookie, old_cookie):
    old_cookie = stodic_cookie(old_cookie)
    for i in old_cookie:
        for j in r_cookie:
            if i == j:
                old_cookie[i] = r_cookie[j]
    return dictos_cookie(old_cookie)


def write_cookie(json_data):
    with open('./cookie.json', 'w', encoding='utf8') as fp:
        json.dump(json_data, fp)


def main():
    myheaders = {'Host': 'wechat.v2.traceint.com', 'Connection': 'keep-alive', 'Content-Length': '729',
                 'User-Agent': 'Mozilla/5.0 (Linux; Android 11; M2012K11AC Build/RKQ1.200826.002; wv) AppleWebKit/537.36 '
                               '(KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3149 MMWEBSDK/20211001 Mobile '
                               'Safari/537.36 MMWEBID/68 MicroMessenger/8.0.16.2040(0x28001053) Process/toolsmp '
                               'WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64',
                 'Content-Type': 'application/json', 'Accept': '*/*', 'Origin': 'https://web.traceint.com',
                 'X-Requested-With': 'com.tencent.mm', 'Sec-Fetch-Site': 'same-site', 'Sec-Fetch-Mode': 'cors',
                 'Sec-Fetch-Dest': 'empty', 'Referer': 'https://web.traceint.com/web/index.html',
                 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'}
    check_library_body = {"operationName": "list", "query": "query list {\n userAuth {\n reserve {\n libs(libType: -1) {\n "
                                                            "lib_id\n lib_floor\n is_open\n lib_name\n lib_type\n "
                                                            "lib_group_id\n lib_comment\n lib_rt {\n seats_total\n "
                                                            "seats_used\n seats_booking\n seats_has\n reserve_ttl\n "
                                                            "open_time\n open_time_str\n close_time\n close_time_str\n "
                                                            "advance_booking\n }\n }\n libGroups {\n id\n group_name\n }\n "
                                                            "reserve {\n isRecordUser\n }\n }\n record {\n libs {\n "
                                                            "lib_id\n lib_floor\n is_open\n lib_name\n lib_type\n "
                                                            "lib_group_id\n lib_comment\n lib_color_name\n lib_rt {\n "
                                                            "seats_total\n seats_used\n seats_booking\n seats_has\n "
                                                            "reserve_ttl\n open_time\n open_time_str\n close_time\n "
                                                            "close_time_str\n advance_booking\n }\n }\n }\n rule {\n "
                                                            "signRule\n }\n }\n}"}
    while True:
        with open('./cookie.json', 'r', encoding='utf8') as fp:
            json_data = json.load(fp)
        for this_cookie in json_data['cookies']:
            myheaders['Cookie'] = this_cookie['cookie']
            s = requests.session()
            s.headers.clear()
            s.headers.update(myheaders)
            r = s.post("https://wechat.v2.traceint.com/index.php/graphql/",
                       json=check_library_body)
            r_cookie = requests.utils.dict_from_cookiejar(r.cookies)
            this_cookie['cookie'] = update_cookie(r_cookie, this_cookie['cookie'])
        write_cookie(json_data)
        time.sleep(300)


if __name__ == '__main__':
    main()