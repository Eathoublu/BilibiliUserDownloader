import requests
import re
import os
import json
import sys
from you_get import common as you_get

class BilibiliDownloader(object):
    def __init__(self):
        pass
    @staticmethod
    def run(dic, urll, kstart=None):
        # kstart is the last number printed on the screen.
        k = 0
        kt = len(urll)
        for u in urll:
            k += 1
            if kstart:
                if k <= kstart:
                    continue
            try:
                sys.argv = ['you-get', '-o', dic, u]
                you_get.main()
            except Exception as e:
                print(e)
                print('*Loss one. The url is:{}'.format(u))
            print('{}/{} done.'.format(k, kt))
        return

class BilibiliVideoManager(object):

    def __init__(self):
        self.rule = re.compile('<span class="cur-page">.*?/(.*?)</span></div>', re.S)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        }
        self.trule = re.compile('eta="true">(.*?)_哔哩哔哩', re.S)
        self.alphabet = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'

    @staticmethod
    def genurl(url, page):
        urls = []
        urls.append(url)
        for idx in range(1, page):
            urls.append('{}?p={}'.format(url, idx+1))
        return urls

    def dec(self, x):
        r = 0
        for i, v in enumerate([11, 10, 3, 8, 4, 6]):
            r += self.alphabet.find(x[v]) * 58 ** i
        return (r - 0x2_0840_07c0) ^ 0x0a93_b324

    def enc(self, x):
        x = (x ^ 0x0a93_b324) + 0x2_0840_07c0
        r = list('BV1**4*1*7**')
        for v in [11, 10, 3, 8, 4, 6]:
            x, d = divmod(x, 58)
            r[v] = self.alphabet[d]
        return ''.join(r)

    def run(self, vid, mode='bv'):
        if mode == 'bv':
            vid = 'av'+str(self.dec(vid))
        url = 'https://www.bilibili.com/video/{}'.format(vid)
        req = requests.get(url, headers=self.headers)
        content = str(req.content, 'utf8')
        wholep = self.rule.findall(content)
        if wholep:
            return self.genurl(url, int(wholep[0]))
        return [url, ]

    def gettitle(self, url):
        c = str(requests.get(url, headers=self.headers).content, 'utf8')
        title = self.trule.findall(c)[0]
        return title

class Manager(object):
    def __init__(self):
        self.bd = BilibiliDownloader()
        self.bvm = BilibiliVideoManager()

    def run(self, vid, prefix='.', mode='bv', kstart=None):
        urll = self.bvm.run(vid, mode)
        tit = self.bvm.gettitle(urll[0])
        self.bd.run(dic=prefix+'/'+tit, urll=urll, kstart=kstart)

if __name__ == '__main__':

    m = Manager()
    m.run('av91882697', mode='av', prefix='.')
