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
    def run(dic, urll):
        for u in urll:
            # try:
            sys.argv = ['you-get', '-o', dic, u]
            you_get.main()
            # except Exception as e:
            #     print(e)
        return

class BilibiliVideoManager(object):

    def __init__(self):
        self.rule = re.compile('<span class="cur-page">.*?/(.*?)</span></div>', re.S)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        }
        self.trule = re.compile('eta="true">(.*?)_哔哩哔哩', re.S)

    @staticmethod
    def genurl(url, page):
        urls = []
        urls.append(url)
        for idx in range(1, page):
            urls.append('{}?p={}'.format(url, idx+1))
        return urls

    def run(self, bv):

        # url = 'https://api.bilibili.com/x/space/arc/search?mid=12473905&ps=30&tid=0&pn=1&keyword=&order=pubdate&jsonp=jsonp'
        # url = 'https://www.bilibili.com/video/BV1Ez411b7jR'
        url = 'https://www.bilibili.com/video/{}'.format(bv)
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

class BilibiliUserManager(object):
    def __init__(self, prefix):
        # 12473905
        self.prefix = prefix
        self.burl2 = 'https://space.bilibili.com/{}'
        self.i2url = 'https://api.bilibili.com/x/relation/stat?vmid={}'
        self.burl = 'https://api.bilibili.com/x/space/acc/info?mid={}&jsonp=jsonp'
        self.surl = 'https://api.bilibili.com/x/space/arc/search?mid={}&pn={}&ps=25&jsonp=jsonp'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        }
        self.uid = None
        self.alphabet = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'

    def run(self, uid):
        uid = str(uid)
        self.uid = uid
        abspath = self.prefix + '/' + uid
        if not os.path.exists(abspath):
            os.mkdir(abspath)
            os.mkdir(abspath+'/profile')
            os.mkdir(abspath+'/video')
        jsoninfo0 = str(self.request(self.i2url.format(uid)), 'utf8')
        # print(jsoninfo0)
        jif = json.loads(jsoninfo0)
        follower = jif['data']['follower']
        following = jif['data']['following']

        jsoninfo1 = str(self.request(self.burl.format(uid)), 'utf8')
        jif = json.loads(jsoninfo1)
        name = jif['data']['name']
        sex = jif['data']['sex']
        avataru = jif['data']['face']
        rank = jif['data']['rank']
        level = jif['data']['level']
        birthday = jif['data']['birthday']
        sign = jif['data']['sign']
        with open(abspath+'/profile/basic.txt', 'w') as f:
            f.write('name: {} sex:{} rank:{} level:{} birthday:{} sign:{} follower:{} following:{}'.format(name, sex, rank, level, birthday, sign, follower, following))
            f.close()
        avatar = self.request(avataru)
        with open(abspath+'/profile/avatar.jpg', 'wb') as f:
            f.write(avatar)
            f.close()

        with open(abspath+'/profile/source.txt', 'w') as f:
            f.write('{};;{}'.format(jsoninfo0, jsoninfo1))
            f.close()

    def searchlist(self):
        videol = []
        pn = 1
        while True:
            sres = str(self.request(self.surl.format(self.uid, pn)), 'utf8')
            sl = self.parselist(json.loads(sres))
            if sl:
                videol += sl
            else:
                break
            pn += 1
        return videol

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

    @staticmethod
    def parselist(jso, mode='a'):
        vlist = jso['data']['list']['vlist']
        idl = []
        if not vlist:
            return False
        for v in vlist:
            if mode=='b':
                idl.append(v['bvid'])
            else:
                idl.append(v['bvid'])
        return idl

    def request(self, url):
        return requests.get(url, headers=self.headers).content

class Manager(object):
    def __init__(self, prefix='.'):
        self.prefix = prefix
        self.bum = BilibiliUserManager(prefix=prefix)
        self.bvm = BilibiliVideoManager()
        self.bd = BilibiliDownloader()
        self.fall_list = []

    def run(self, uid, startk=None):
        self.fall_list = []
        self.bum.run(uid=uid)
        vlist= self.bum.searchlist()
        vbase = self.prefix+'/'+str(uid)+'/video/'
        k = 0
        tk = len(vlist)
        for v in vlist:
            k += 1
            if startk:
                if k < startk:
                    continue
            print('{}/{}'.format(k, tk))

            svl = self.bvm.run(v)
            tit = str(self.bvm.gettitle(svl[0])).replace('/', '\\')
            if os.path.exists(vbase+str(k)+'_'+tit):
                pass
            else:
                os.mkdir(vbase+str(k)+'_'+tit)
            try:
                # print(svl)
                self.bd.run(vbase+str(k)+'_'+tit, svl)
            except:
                print('Fall one. k={}, svl={}'.format(k, svl))
                self.fall_list.append(svl)

        if self.fall_list:
            print('All Fall:{}'.format(self.fall_list))
        print('Finish!')

if __name__ == '__main__':

    m = Manager(prefix='.')
    m.run(uid='')





