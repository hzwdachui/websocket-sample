class DebugConfig(object):
    '''
    测试环境 server 配置
    '''
    headers = dict()
    host = "127.0.0.1"
    port = 8002


class ProductionConfig(object):
    '''
    生产环境 server 配置
    '''
    headers = dict()
    host = "127.0.0.1"
    port = 8002


configs = {
    "debug": DebugConfig,
    "production": ProductionConfig
}