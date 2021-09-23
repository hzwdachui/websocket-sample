class DebugConfig(object):
    '''
    development config for server
    '''
    headers = dict()
    host = "127.0.0.1"
    port = "8002"


class ProductionConfig(object):
    '''
    production config for server
    '''
    headers = dict()
    host = "0.0.0.0"
    port = "8002"


configs = {
    "debug": DebugConfig,
    "production": ProductionConfig
}