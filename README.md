# 赛马娘自动育成脚本

#### 介绍
通过adb获取手机屏幕内容，并通过图像识别得出点击策略，然后在手机相应位置模拟点击，以实现自动养马。


#### 使用说明

1.  确保已安装python3，并且带有subprocess、io、time、matplotlib、numpy、random等模块。
2.  进入手机开发者模式，打开USB调试，用数据线连接手机和电脑。
3.  使用以下命令运行脚本：`python3 start.py`
4.  输入训练轮次，刚开始为0，以及目标距离。之后手机上将弹出USB调试申请，请允许调试。
5.  **本脚本适用于分辨率为2340x1080并且刘海高76像素的手机**，如Redmi Note 8 Pro。
6.  其他手机请自行更改代码中的特征识别坐标及颜色。
7.  如果你毫无Python基础，手机也不符合要求，基本可以放弃了。
8.  视频演示： [https://www.bilibili.com/video/BV1qo4y1C7VU/](https://www.bilibili.com/video/BV1qo4y1C7VU/)

#### 责任声明

1.  本代码仅供学习交流，请勿用于商业用途（如淘宝代刷）；
2.  使用脚本违反了部分游戏条约，请自行对账号负责。

By: charlin


