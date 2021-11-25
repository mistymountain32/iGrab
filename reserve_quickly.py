# 导入模块
import requests
import json
import time
import cookie_loop


def write_and_update(s, item, json_data, myheaders):
    item['cookie'] = cookie_loop.update_cookie(requests.utils.dict_from_cookiejar(s.cookies), item['cookie'])
    cookie_loop.write_cookie(json_data)
    myheaders['Cookie'] = item['cookie']
    s.headers.clear(), s.headers.update(myheaders)


def main():
    # 准备工作：输入昵称，初始化不变部分
    nickname = input("请输入昵称: ")
    myheaders = {'Host': 'wechat.v2.traceint.com', 'Connection': 'keep-alive', 'Content-Length': '729',
                 'User-Agent': 'Mozilla/5.0 (Linux; Android 11; M2012K11AC Build/RKQ1.200826.002; wv) AppleWebKit/537.36 '
                               '(KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3149 MMWEBSDK/20211001 Mobile '
                               'Safari/537.36 MMWEBID/68 MicroMessenger/8.0.16.2040(0x28001053) Process/toolsmp '
                               'WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64',
                 'Content-Type': 'application/json', 'Accept': '*/*', 'Origin': 'https://web.traceint.com',
                 'X-Requested-With': 'com.tencent.mm', 'Sec-Fetch-Site': 'same-site', 'Sec-Fetch-Mode': 'cors',
                 'Sec-Fetch-Dest': 'empty', 'Referer': 'https://web.traceint.com/web/index.html',
                 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
                 }
    check_library_body = {"operationName": "list",
                          "query": "query list {\n userAuth {\n reserve {\n libs(libType: -1) {\n "
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
    count = 0
    # 开始循环，反复尝试抢座
    while True:
        # 针对特定用户，读入cookie
        with open("./cookie.json", "r", encoding="utf8") as fp:
            json_data_file = json.load(fp)
            ok = False
            for item in json_data_file["cookies"]:
                if item["nickname"] == nickname:
                    ok = True
                    myheaders['Cookie'] = item['cookie']
                    break
            if not ok:
                raise Exception("无效的昵称!")
        s = requests.session()
        s.headers.clear(), s.headers.update(myheaders)
        ''',proxies={'https': 'http://127.0.0.1:8888'}, verify=False'''
        r = s.post("https://wechat.v2.traceint.com/index.php/graphql/", json=check_library_body)
        json_data = r.json(), write_and_update(s, item, json_data_file, myheaders)
        libnum = ''
        ok = True
        try:
            for lib in json_data[0]['data']['userAuth']['reserve']['libs']:
                if lib['is_open'] and lib['lib_rt']['seats_has'] != 0:
                    libnum = lib['lib_id']
                    break
        except:
            print("request library error")
            break
        if libnum == '':
            ok = False
        if ok:
            check_floor_body = {"operationName": "libLayout",
                                "query": "query libLayout($libId: Int, $libType: Int) {\n userAuth "
                                         "{\n reserve {\n libs(libType: $libType, libId: $libId) {"
                                         "\n lib_id\n is_open\n lib_floor\n lib_name\n lib_type\n "
                                         "lib_layout {\n seats_total\n seats_booking\n "
                                         "seats_used\n max_x\n max_y\n seats {\n x\n y\n key\n "
                                         "type\n name\n seat_status\n status\n }\n }\n }\n }\n "
                                         "}\n}", "variables": {"libId": libnum}}
            r = s.post("https://wechat.v2.traceint.com/index.php/graphql/", json=check_floor_body)
            json_data = r.json(), write_and_update(s, item, json_data_file, myheaders)
            seatkey = ''
            try:
                for seat in json_data[0]['data']['userAuth']['reserve']['libs'][0]['lib_layout']['seats']:
                    if seat['seat_status'] == 1:
                        seatkey = seat['key']
                        break
            except:
                print("request seats error")
                break
            if seatkey == '': ok = False
            if ok:
                reserve_body = {"operationName": "reserveSeat",
                                "query": "mutation reserveSeat($libId: Int!, $seatKey: String!, "
                                         "$captchaCode: String, $captcha: String!) {\n userAuth {\n "
                                         "reserve {\n reserveSeat(\n libId: $libId\n seatKey: "
                                         "$seatKey\n captchaCode: $captchaCode\n captcha: $captcha\n "
                                         ")\n }\n }\n}", "variables": {"seatKey": seatkey,
                                                                       "libId": libnum,
                                                                       "captchaCode": "",
                                                                       "captcha": ""}}
                r = s.post("https://wechat.v2.traceint.com/index.php/graphql/", json=reserve_body)
                json_data = r.json(), write_and_update(s, item, json_data_file, myheaders)
                try:
                    if json_data[0]['data']['userAuth']['reserve']['reserveSeat']:
                        print("Congratulations!")
                        break
                except:
                    print("reserve seats error")
                    break
        count += 1
        print("you have tried %d times" % count)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
