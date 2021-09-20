import socket
import base64
import hashlib


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


class Server(object):
    config_type = "debug"
    response_tpl = "HTTP/1.1 101 Switching Protocols\r\n" \
                   "Upgrade:websocket\r\n" \
                   "Connection:Upgrade\r\n" \
                   "Sec-WebSocket-Accept:%s\r\n" \
                   "WebSocket-Location:ws://%s%s\r\n\r\n"

    def __init__(self):
        self.load_config(self.config_type)
        pass

    def load_config(self, confit_type="debug"):
        config = configs[confit_type]
        self.headers = config.headers
        self.host = config.host
        self.port = config.port

    def run_server_forever(self):
        '''
        启动 server 的方法，持续监听
        '''

        # 建立连接
        sock = self._build_conn()
        # 等待用户连接 https://segmentfault.com/a/1190000013031253
        self.conn, self.address = sock.accept()  # 接受的数据是请求头
        # 握手
        self._shakehands()
        # 接受数据
        self._recv()

        sock.close()

    def _shakehands(self):
        '''
        处理握手的方法，响应握手信息给客户端
        '''
        if self.conn is not None and self.address is not None:
            # 获取客户端的【握手】信息
            data = self.conn.recv(1024)  # bytes
            self.headers = self._get_headers(data)
            ac = self._encrypt()
            response = self.response_tpl % (
                ac.decode('utf-8'), self.headers['Host'], self.headers['url'])
            self.conn.send(bytes(response, encoding='utf-8'))
            print("发送握手成功")
        else:
            print("握手重试")
            self._shakehands()

    def _encrypt(self):
        '''
        获取 header 中的 Sec-WebSocket-Key 信息，进行加密后返回，完成握手
        加密规则是：Sec-WebSocket-Key 加上一个 magic_string，然后 sha1，然后 base64
        param: string key 请求的时候 header 中的 Sec-WebSocket-Key 公钥
        return: string 握手信息
        '''
        if "Sec-WebSocket-Key" in self.headers:
            magic_string = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
            return base64.b64encode(hashlib.sha1((self.headers["Sec-WebSocket-Key"]+magic_string).encode('utf-8')).digest())
        else:
            pass

    def _get_headers(self, data):
        '''
        https://segmentfault.com/a/1190000013031253
        将请求头格式化成字典
        :param data:
        :return: dict 
        '''
        header_dict = {}
        data = str(data, encoding='utf-8')

        # for i in data.split('\r\n'):    # headers 用 \r\n 分隔
        #     print(i)

        header, body = data.split('\r\n\r\n', 1)
        header_list = header.split('\r\n')
        for i in range(0, len(header_list)):
            if i == 0:
                if len(header_list[i].split(' ')) == 3:
                    header_dict['method'], header_dict['url'], header_dict['protocol'] = header_list[i].split(
                        ' ')
            else:
                k, v = header_list[i].split(':', 1)
                header_dict[k] = v.strip()
        return header_dict

    def _build_conn(self):
        '''
        建立socket
        : return: socket 对象 
        '''
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))
        sock.listen(5)
        print(f"server start listening on {self.host}:{self.port}")
        return sock

    def _recv(self):
        '''
        获取客户端的数据并解包
        对着协议抄就好了
        todo: 无法处理关闭数据包
        '''
        while True:
            try:
                info = self.conn.recv(8096)
            except Exception as e:
                info = None
            if not info:
                break
            payload_len = info[1] & 127
            if payload_len == 126:
                mask = info[4:8]
                decoded = info[8:]
            elif payload_len == 127:
                mask = info[10:14]
                decoded = info[14:]
            else:
                mask = info[2:6]
                decoded = info[6:]

            bytes_list = bytearray()
            for i in range(len(decoded)):
                chunk = decoded[i] ^ mask[i % 4]
                bytes_list.append(chunk)
            print(bytes_list)
            body = str(bytes_list, encoding='utf-8')
            print(body)
            self._send(self.conn, body.encode('utf-8'))

    def _send(self, conn, msg_bytes):
        '''
        WebSocket服务端向客户端发送消息: 【封包】
        对着协议抄就好了
        :param conn: 客户端连接到服务器端的socket对象,即： conn,address = socket.accept()
        :param msg_bytes: 向客户端发送的字节
        '''
        import struct

        token = b"\x81"
        length = len(msg_bytes)
        if length < 126:
            token += struct.pack("B", length)
        elif length <= 0xFFFF:
            token += struct.pack("!BH", 126, length)
        else:
            token += struct.pack("!BQ", 127, length)

        msg = token + msg_bytes
        conn.send(msg)


def main():
    server = Server()
    server.run_server_forever()


if __name__ == "__main__":
    main()
