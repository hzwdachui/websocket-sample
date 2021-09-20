from prompt_toolkit.application import Application as PTApplication
from prompt_toolkit.document import Document
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import SearchToolbar, TextArea
import asyncio
import time
import websockets


class InputArea:
    help_text = '''
        #########################################################
        #           Welcome to the anonymous chatroom v0.1      #
        #       Enter message and press Enter to send message   #
        #########################################################
    '''

    def __init__(self, websocket):
        self.ws = websocket
        self._load_config()
        self.input_ui = PTApplication(
            layout=Layout(self._container, focused_element=self._input_field),
            key_bindings=self._kb,
            mouse_support=True,
            full_screen=True,
        )

    def _load_config(self):
        '''
        load components for the prompt toolkit input application
        '''
        self._output_field = TextArea(text=self.help_text)
        self._search_field = SearchToolbar()
        self._input_field = TextArea(
            height=2,
            prompt='',
            search_field=self._search_field,
            multiline=False,
            wrap_lines=False,
            accept_handler=self._input_accept_handler
        )
        self._container = HSplit([
            self._output_field,
            Window(height=1, char='-'), self._input_field, self._search_field
        ])
        self._kb = KeyBindings()
        self._load_key_bindings()

    def _print(self, text, msg_type='*'):
        '''
        print text on screen with format
        @param: text  string text to be outputed
        '''
        current_time = time.strftime('%H:%M:%S')
        output_text = self._output_field.text + '\n' + \
            f'{msg_type} {[current_time]} {text}'
        self._output_field.buffer.document = Document(
            text=output_text,
            cursor_position=len(output_text),
        )

    def _load_key_bindings(self):
        '''
        bind key of prompt_toolkit input area 
        '''
        @self._kb.add('c-c')
        @self._kb.add('c-q')
        def _(event):
            event.app.exit()

    def _input_accept_handler(self, buff):
        '''
        handling input event
        '''
        asyncio.create_task(self._ws_send(self._input_field.text))

    async def _recv_handler(self):
        '''
        creating a coroutine receiving msg from the server
        '''
        # recv_task = asyncio.create_task(self.ws_recv())
        # await recv_task   # warning: don't run it now
        asyncio.create_task(self._ws_recv())

    async def _ws_send(self, msg):
        '''
        sending msg to ws server
        @param: msg string msg to be sent
        '''
        try:
            await self.ws.send(msg)
        except websockets.exceptions.ConnectionClosedOK:
            # close normally
            self._print("lost connection...")
        except websockets.exceptions.ConnectionClosedError:
            self._print("connection failed abnormally...")
        except Exception as err:
            msg = f'{type(err).__name__}: {err}'
            self._print(msg)

    async def _ws_recv(self):
        '''
        receiving msg from server forever
        '''
        self._print("start receiving...")
        while True:
            try:
                text = await self.ws.recv()
                self._print(f"{text}")
            except websockets.exceptions.ConnectionClosedOK:
                # close normally
                self._print("lost connection...")
                break
            except websockets.exceptions.ConnectionClosedError:
                # close abnormally
                self._print("connection failed abnormally...")
                break
            except Exception as err:
                msg = f'{type(err).__name__}: {err}'
                self._print(msg)
                break

    async def recv(self):
        '''
        runing the receive handler
        '''
        await self._recv_handler()

    async def serve(self):
        '''
        entry point
        '''
        await self.recv()   # handling receiving
        await self.input_ui.run_async()  # handling input


async def action(websocket):
    '''
    the handler after connecting the server
    '''
    objInputArea = InputArea(websocket)
    await objInputArea.serve()


async def main():
    '''
    communicating with server
    '''
    host = input("host:")
    port = input("port:")
    username = input("username:")
    uri = f"ws://{host}:{port}/{username}"
    try:
        async with websockets.connect(uri) as websocket:
            await action(websocket)
    except Exception as err:
        err_msg = f'{type(err).__name__}: {err}'
        print(f"lost connection: {err_msg}")
        quit()

asyncio.run(main())
