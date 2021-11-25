# 导入模块
import requests
import json
import time
import reserve_quickly


def main():
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
    with open("./cookie.json", "r", encoding="utf8") as fp:
        json_data_file = json.load(fp)
        nickname = input("请输入昵称：")
        ok = False
        for item in json_data_file["cookies"]:
            if item["nickname"] == nickname:
                ok = True
                myheaders['Cookie'] = item['cookie']
                break
        if not ok:
            raise Exception("无效的昵称!")
    print("楼层\t\t\t代号")
    print("三楼\t\t\t716")
    print("四楼\t\t\t730")
    print("五楼\t\t\t737")
    print("六楼\t\t\t765")
    print("七楼\t\t\t744")
    print("八楼\t\t\t786")
    print("九楼\t\t\t751")
    print("十楼\t\t\t758")
    print("十一楼\t\t772")
    print("十二楼\t\t779")
    print("图东环楼三楼\t793")
    print("图东环楼四楼\t800")
    print("自带电脑学习区\t114074")
    print("电子阅览室\t118707")
    libnum = int(input("请输入想抢的楼层代号："))
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
    s = requests.session()
    s.headers.clear()
    s.headers.update(myheaders)
    count = 0
    ''',proxies={'https': 'http://127.0.0.1:8888'}, verify=False'''
    while True:
        r = s.post("https://wechat.v2.traceint.com/index.php/graphql/", json=check_library_body)
        json_data = r.json(), reserve_quickly.write_and_update(s, item, json_data_file, myheaders)
        ok = True
        try:
            for lib in json_data[0]['data']['userAuth']['reserve']['libs']:
                if lib['lib_id'] == libnum:
                    if lib['is_open'] and lib['lib_rt']['seats_has'] != 0:
                        break
                    else:
                        ok = False
        except:
            print("request library error")
            break
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
            json_data = r.json(), reserve_quickly.write_and_update(s, item, json_data_file, myheaders)
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
                json_data = r.json(), reserve_quickly.write_and_update(s, item, json_data_file, myheaders)
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
