from module.core import core


# 如果使用云函数，默认指定的运行程序为index.handler 即不需要坐修改。
def handler(event, content):
    core()

# 如果本地自行运行，将如下两行去除注释，从而手动执行脚本
# if __name__ == '__main__':
#     core()
