import json
import os
import sys
import threading
import requests
import drawMap


class getContent_thread:
    __threadlist = []
    already = 0

    def __init__(self, nums: int):
        self.nums = nums
        self.__getNewestId()

    def __getNewestId(self):
        res = json.loads(requests.get('https://u.xiaouni.com/user-api/content/article/list?size=1').text)
        if (res['code'] == 200):
            self.newestId = res['data']['list'][0]['id']
        else:
            print('无法获取最新帖子ID')
            sys.exit(0)

    def getmsg(self, id):
        # 发送http请求
        url = 'https://u.xiaouni.com/user-api/content/article/info?id=' + str(id)
        response = requests.get(url=url)
        # json格式化
        json_data = json.loads(response.text)
        # 获取状态码，标题和内容
        status_code = json_data['code']
        if status_code == 200:
            title = json_data['data']['title']
            content = json_data['data']['content']
            # 返回标题和内容
            return '[' + title + ']:' + content + '\n'
        else:
            return 'none'

    def run(self):
        if self.nums <= 8:
            for m_thread in range(0, self.nums):
                t = threading.Thread(target=self.__run, args=(m_thread, m_thread, self.nums))
                self.__threadlist.append(t)
                t.start()
        else:
            stringNum: int = int(self.nums / 8)
            for m_thread in range(0, 8):
                t = threading.Thread(target=self.__run,
                                     args=(m_thread, m_thread * stringNum, m_thread * stringNum + stringNum))
                self.__threadlist.append(t)
                t.start()
            if stringNum * 8 < self.nums:
                t = threading.Thread(target=self.__run, args=(8, 8 * stringNum, self.nums - stringNum * 8))
                self.__threadlist.append(t)
                t.start()
        for it in self.__threadlist:
            it.join()
        content_txt = ''
        for i in range(0, 9):
            with open(str(i) + '.txt', 'r', encoding='utf-8') as f:
                try:
                    content_txt += f.read()
                    f.close()
                except IOError as e:
                    print(str(i) + ':', e)
        with open('content.txt', 'w', encoding='utf-8') as f:
            f.write(content_txt)
            f.close()
            for i in range(0, 9):
                try:
                    os.remove(str(i) + '.txt')
                except IOError as e:
                    print(str(i) + '(remove):', e)

    def __run(self, thread_id, begin, end):
        with open(str(thread_id) + ".txt", 'a', encoding='utf-8') as f:
            for i in range(begin, end):
                id = self.newestId - i
                text = self.getmsg(id)
                print(text[0:20], '……')
                if text != 'none':
                    f.write(text)
            f.close()


if __name__ == '__main__':
    num = int(input("输入要获取的帖子数目(建议300条左右)："))
    getContent_thread(num).run()
    print('已完成帖子获取,正在生成词云图……')
    drawMap.draw('wordcloud.png')
    print('词云生成完毕！')
