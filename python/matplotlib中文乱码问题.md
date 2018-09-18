折腾了一天,终于搞定了.
系统Ubuntu16.04
Python版本:3.5.2

第一步:下载字体:msyh.ttf (微软雅黑)
放在系统字体文件夹下:
/usr/share/fonts

同时我也复制了下放在matplotlib的字体文件夹下了(不知道这一步是不是必须)
/usr/local/lib/python3.5/dist-packages/matplotlib/mpl-data/fonts/ttf/

第二步：修改matplotlib配置文件：
sudo vim /usr/local/lib/python3.5/dist-packages/matplotlib/mpl-data/matplotlibrc
删除font.family和font.sans-serif两行前的#，并在font.sans-serif后添加中文字体
Microsoft YaHei, ...(其余不变)

第三步：删除~/.cache/matplotlib下文件fontList.py3k.cache

作者：司毅

链接：https://www.zhihu.com/question/25404709/answer/128171562

来源：知乎

著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。