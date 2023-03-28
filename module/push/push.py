from module.config import config
from module.push.barkpush import bark_push
from module.push.dingdingpush import dingding_push


# 推送函数
def push(message):
    if config.pushType == 'bark':
        bark_push(message)
    elif config.pushType == 'dingding':
        dingding_push(message)
