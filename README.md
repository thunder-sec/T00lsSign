# T00lsSign

T00ls自动签到、查域名脚本(搭配云函数使用)

## 使用说明

**1.登录信息修改**

```
# 登录信息
username = ""           # 用户名
password = ""           # 密码，md5 32位小写
question_num = ""       # 密保问题
question_answer = ""    # 密保答案
```

> 密保问题对应值如下
>
> ```
> # 0 = 没有安全提问
> # 1 = 母亲的名字
> # 2 = 爷爷的名字
> # 3 = 父亲出生的城市
> # 4 = 您其中一位老师的名字
> # 5 = 您个人计算机的型号
> # 6 = 您最喜欢的餐馆名称
> # 7 = 驾驶执照的最后四位数字
> ```

**2.打码平台信息修改**

* 如下使用的是图鉴识别 www.ttshitu.com ，注册用户，小额充值，填入用户名和密码即可，一次识别0.008元。

```
# 图鉴识别登录 www.ttshitu.com
TTusername = ""
TTpassword = ""
```

**3.推送设置**

* 推送目前设置了bark、dingding，如何配置自行查找方法。**默认关闭推送**，需要**开启推送**将 `pushServer` 修改为 `1` 即可，并且设置 `pushType` 为相应的推送方式。

```
# 推送设置
pushServer = 0      # 推送开关，0为关闭，1为开启，默认关闭
pushType = ""       # 选择推送方式，目前支持：bark、dingding
```

* bark推送

  bark推送需要设置服务地址以及在app上获取到的key值。

  ```
  # bark data
  bark_server_url = ""    # 示例：https://test.com
  bark_key = ""           # 从bark app上获取
  ```

* dingding推送

  钉钉推送需要创建群机器人，安全选项选“加签”，获取到key值填入下`dingkey`即可，获取到加签的secret添如到`secret`。

  ```
  # dingding data
  dingkey = ""        # webhook key值
  secret = ""         # 安全选项选"加签"，secret值
  ```

## 云函数配置

**1.云函数配置**

* 使用的某讯云函数，注册好之后，创建云函数—>从头开始—>事件函数—>**运行环境选择python3.6**—>**执行方法处写** `index.main` 。

* 高级配置中，将**超时时间设置为最长900s**。

![yun](https://github.com/thunder-sec/T00lsSign/blob/main/yunhanshu.jpg?raw=true)

**2.代码修改**

* 因为云函数的原因，不需要引入`if __name__ == '__main__'`，所以直接将代码修改好放入云函数即可执行。

**3.设置定时触发任务**

可自行设置触发时间，例如每天上午10点触发一次，cron表达式为：`0 0 10 * * * *`

