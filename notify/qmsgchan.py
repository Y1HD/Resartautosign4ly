import json
import requests
import datetime
import sys
sys.path.append("..")
import config
from utils import log


class QmsgChan(object):
    def __init__(self):
        self.key = config.config.QMsg_KEY

    @staticmethod
    def form_content(do_sign_list, style):
        log.info('Starting forming qmsg chan content')

        text = ""
        week_list = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']

        success_count = 0
        fail_list = []
        for value in do_sign_list:
            if value["sign_status"] == "已签":
                success_count = success_count + 1
            elif value["sign_status"] == "签到":
                fail_list.append(value["title_sub"])

        tip_time = datetime.datetime.now().strftime('%m-%d')
        days = week_list[datetime.datetime.now().weekday()]
        if style == 'DEFAULT':
            text = text + tip_time + ' ' + days + '\n\n签到结果 \n\n - 成功签到 ' + str(
                success_count) + ' / ' + str(len(do_sign_list))
        elif style == 'DETAIL':
            text = text + tip_time + ' ' + days + '\n\n成功签到 \n\n'
            for value in do_sign_list:
                text = text + '- ' + value['title_level'] + ' ' + value['title_sub'] + '  ✅ \n'

        if len(fail_list) != 0:
            text = text + '\n\n签到失败 \n\n'
        for value in fail_list:
            text = text + '- ' + str(value) + '  ❌ \n'

        return text

    def send(self, content, err):
        log.info('Starting sending qmsg chan message')

        if err != '':
            content = '由于你近期修改过密码，或开启了登录保护，参数失效，请重新获取微博超话签到相关参数'

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'msg': f"{content}"
        }
        url = f"https://qmsg.zendee.cn/send/{self.key}"

        response = requests.post(url, headers=headers, data=data)

        if json.loads(response.text)['success']:
            log.info('Qmsg chan message send success')
