# BilibiliUserDownloader
美好虽然转瞬即逝，但依然可以永恒。
## 介绍
该脚本可以按照up主的id来下载up主的全部视频，视频将按照up的id以及视频的标题分类放好。
## 使用方法
**环境：python3**
**需要安装万能的you_get工具包 ```pip3 install you_get```**
### bilibili_downloader.py：按照up主来下载视频（适用于多分p视频）
参照main函数中的方法：
1. 实例化Manager类，传入一个prefix（即前缀路径）。
2. 调用Manager的run方法，传入一个用户id（即为希望下载的up主的id）
3. enjoy
注：该工具附带了断点续传功能，在run方法中加入整形参数kstart即可从指定位置继续传输。e.x.假如一个up主有20个视频，你传到第10个的时候断开了，那么屏幕上会显示10/20，那么接下来重新开始运行脚本时，只需传入kstart=10即可从断开的地方继续传输。
### bilibili_downloader4SingleVideo.py：按照av号（或者bv号）来下载单独的视频（同样适用于多分p视频）
这是一个补充的脚本，比第一个稍微实用一点。
main函数中几乎一目了然了，方法如下：
1. 实例化Manager。
2. 调用Manager的run方法，参数vid是av号或者bv号，mode：av号就填‘av’反之亦然，prefix是路径，kstart是断点续传，与第一个工具使用方法一致。
