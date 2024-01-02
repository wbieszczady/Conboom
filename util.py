
MAP = [['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
       ['x', 'o', 'o', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'o', 'o', 'x'],
       ['x', 'o', 'x', 'c', 'x', 'c', 'x', 'c', 'x', 'c', 'x', 'o', 'x'],
       ['x', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'x'],
       ['x', 'c', 'x', 'c', 'x', 'c', 'x', 'c', 'x', 'c', 'x', 'c', 'x'],
       ['x', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'x'],
       ['x', 'c', 'x', 'c', 'x', 'c', 'x', 'c', 'x', 'c', 'x', 'c', 'x'],
       ['x', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'x'],
       ['x', 'c', 'x', 'c', 'x', 'c', 'x', 'c', 'x', 'c', 'x', 'c', 'x'],
       ['x', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'x'],
       ['x', 'o', 'x', 'c', 'x', 'c', 'x', 'c', 'x', 'c', 'x', 'o', 'x'],
       ['x', 'o', 'o', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'o', 'o', 'x'],
       ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']]

CODES = [113,119,101,114,116,121,117,105,111,112,97,115,100,102,103,104,106,107,108,122,120,99,118,98,110,109,32]
CODES_L = [48,49,50,51,52,53,54,55,56,57]
COMMANDS = ['root', 'help', 'settings', 'fullscreen', 'vsync', 'fps counter', 'master volume', 'confirm', 'resolution', '1280x720', '1920x1080', '2560x1440']

def resemblance(string):

       answers = []
       for command in COMMANDS:
              i = 0
              for com, letter in zip(command, string):
                     if com == letter:
                            i += 1
              answers.append(i)

       score = max(answers)

       try:
              string = int(string)
       except:
              pass

       return COMMANDS[answers.index(max(answers))] if score > 2 else string


class Config:
       def __init__(self, game):
              self.game = game

              self.fullscreen = self.get_option_boolean('fullscreen')
              self.vsync = self.get_option_boolean('vsync')
              self.fps_counter = self.get_option_boolean('fps_counter')
              self.width = self.get_option_int('width')
              self.height = self.get_option_int('height')

              self.master_volume = self.get_option_int('master_volume')

       def MASTER_VOLUME(self):
              return f'Master volume: {int(float(self.master_volume)*100)}%\n\n' \
                     f'Enter a number between 0 and 200 to set the master volume.\n' \
                     f'Then type "confirm" to apply.' \

       def RESOLUTION(self):
              return f'Change your window resolution. Current is {self.width}x{self.height}.\n\n' \
                     f' 1280 x 720\n' \
                     f' 1920 x 1080\n' \
                     f' 2560 x 1440'

       def SETTINGS(self):
              return f'Graphics\n' \
                     f' Resolution\n'\
                     f' Fullscreen = {str(self.fullscreen).lower()}\n' \
                     f' Vsync = {str(self.vsync).lower()}\n' \
                     f' FPS counter = {str(self.fps_counter).lower()}\n\n' \
                     f'Audio\n' \
                     f' Master volume\n\n'
       @property
       def master_volume(self):
              return self.get_option_int('master_volume')
       @master_volume.setter
       def master_volume(self, val):
              val = float(val)
              if val >= 0 and val <= 2.0:
                     self.edit_option('master_volume', val)
                     self._master_volume = val

       @property
       def width(self):
              return self.get_option_int('width')

       @width.setter
       def width(self, val):
              self.edit_option('width', val)
              self._width = val

       @property
       def height(self):
              return self.get_option_int('height')
       @height.setter
       def height(self, val):
              self.edit_option('height', val)
              self._height = val

       @property
       def fullscreen(self):
              return self.get_option_boolean('fullscreen')
       @fullscreen.setter
       def fullscreen(self, bool):
              self.edit_option('fullscreen', bool)
              self._fullscreen = bool
              self.game.set_fullscreen(bool)

       @property
       def vsync(self):
              return self.get_option_boolean('vsync')
       @vsync.setter
       def vsync(self, bool):
              self.edit_option('vsync', bool)
              self._vsync = bool
              self.game.set_vsync(bool)

       @property
       def fps_counter(self):
              return self.get_option_boolean('fps_counter')
       @fps_counter.setter
       def fps_counter(self, bool):
              self.edit_option('fps_counter', bool)
              self._fps_counter = bool

       def get_option_boolean(self, option) -> bool:
              with open('options.txt', 'r') as options:
                     for opt in options:
                            a, b = opt.split()
                            if a == option:
                                   return self.convert_to_boolean(b)
       def get_option_int(self, option) -> int:
              with open('options.txt', 'r') as options:
                     for opt in options:
                            a, b = opt.split()
                            if a == option:
                                   return b
       def get_option_index(self, option) -> int:
              with open('options.txt', 'r') as options:
                     for index, opt in enumerate(options):
                            a, b = opt.split()
                            if a == option:
                                   return index
       def edit_option(self, option, value):
              with open('options.txt', 'r') as options:

                     data = [d.replace('\n', '') for d in options.readlines()]
                     index = self.get_option_index(option)
                     data[index] = f'{option} {value}'

              with open('options.txt', 'w') as options:
                     options.writelines([d+'\n' for d in data])
       def convert_to_boolean(self, string):
              lowered = string.lower()
              if lowered == 'true':
                     return True
              elif lowered == 'false':
                     return False
              else:
                     return None


WELCOME = 'Welcome to the terminal!\n\n' \
          'This is where you can change some variables.\n' \
          'Type "help" to get more information...\n\n' \
          'Click "ESC" to leave.'

HELP = 'Options pages:\n\n' \
       ' settings'