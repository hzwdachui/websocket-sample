from prompt_toolkit.application import Application as PTApplication
from prompt_toolkit.document import Document
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import SearchToolbar, TextArea
import asyncio
import time


class InputArea:
    help_text = 'Enter msg and press Enter to send message\n'

    def __init__(self):
        self.output_field = TextArea(text=self.help_text)
        self.search_field = SearchToolbar()
        self.input_field = TextArea(
            height=2,
            prompt='',
            search_field=self.search_field,
            multiline=False,
            wrap_lines=False,
        )
        self.input_field.accept_handler = self.input_accept_handler
        self.container = HSplit([
            self.output_field,
            Window(height=1, char='-'), self.input_field, self.search_field
        ])
        self.kb = KeyBindings()
        self.load_key_bindings()
        self.tui = PTApplication(
            layout=Layout(self.container, focused_element=self.input_field),
            key_bindings=self.kb,
            mouse_support=True,
            full_screen=True,
        )

    def input_accept_handler(self, buff):
        '''
        handling input event
        '''
        self.update_output(self.input_field.text)

    def update_output(self, output, msg_type='*'):
        '''
        print text on screen
        '''
        current_time = time.strftime('%H:%M:%S')
        output = f'{msg_type} {[current_time]} {output}'
        new_text = self.output_field.text + '\n' + output
        self.output_field.buffer.document = Document(
            text=new_text,
            cursor_position=len(new_text),
        )

    def load_key_bindings(self):
        @self.kb.add('c-c')
        @self.kb.add('c-q')
        def _(event):
            event.app.exit()

    async def main(self):
        await self.tui.run_async()


objInputArea = InputArea()
asyncio.run(objInputArea.serve())
