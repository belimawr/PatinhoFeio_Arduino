# (c) 2017 Tiago Queiroz <https://github.com/belimawr>
# (c) 2017 Felipe Correa da Silva Sanches <juca@members.fsf.org>
# Licensed under the GNU General Public License, version 2 (or later)

# Buttons commands
# 8-bit codes, hexadecimal
# 0x10 ~ 0x1F -> Panel data
# 0x30 ~ 0x3F -> Mode
# 0x40 -> Espera
# 0x41 -> Interrupcao
# 0x42 -> Preparacao
# 0x43 -> Partida

add_library('serial')
import math

SMALL_LED = 8
SMALL_INC = 15

BIG_LED = 12
BIG_INC = 46

RED_ON = (255, 0, 0)

GREEN_ON =(0, 255, 0)

WHITE_ON = (255, 255, 255)

buff = []
leds = []
buttons = []

myPort = None

class Led(object):
  def __init__(self, x, y, size, colour):
    self._x = x
    self._y = y
    self._size = size
    self._colour = colour
    self._state  = False

  def draw(self):
    if self._state == True:
      fill(*self._colour)
    else:
      fill(*map(lambda x: x/2, self._colour))
    ellipse(self._x , self._y, self._size, self._size)

  def set_value(self, value):
    self._state = value
    self.draw()


class Button(Led):
  def __init__(self, x, y, size, colour, cmd):
    super(Button, self).__init__(x, y, size, colour)
    self._cmd = cmd

  def clicked(self, x, y):
    d = math.sqrt((self._x - x)**2 + (self._y - y)**2)

    if d <= self._size/2.0:
      self._state = not self._state
      self._send_pressed()

    return self._state

  def _send_pressed(self):
    global myPort
    myPort.write("I:")
    myPort(self._cmd)

  def __repr__(self):
    return str(self._x) + ' ' + str(self._y)


class Partida(Button):
  def draw(self):
      fill(*self._colour)
      rect(self._x, self._y, 24, 19)

  def clicked(self, x, y):
    if ((x >= self._x) and (x <= self._x + 24)) and ((y >= self._y) and (y <= self._y + 19)):
      self._send_pressed()

def dados_painel(val):
    global leds
    i = 0
    for a, b in enumerate(range(11, -1, -1)):
        bool_value = ((val & (1 << a)) == (1 << a))
        leds[i + b].set_value(bool_value)

def vai_um(val):
    leds[12].set_value(val)

def transbordo(val):
    leds[13].set_value(val)

def parado(val):
    leds[14].set_value(val)

def externo(val):
    leds[15].set_value(val)

#ci -> Endreço de Instrução
def ci(val):
    global leds
    i = 16
    for a, b in enumerate(range(11, -1, -1)):
        bool_value = ((val & (1 << a)) == (1 << a))
        leds[i+b].set_value(bool_value)

# re -> Endereço na Memória
def re(val):
    global leds
    i = 28
    for a, b in enumerate(range(11, -1, -1)):
        bool_value = ((val & (1 << a)) == (1 << a))
        leds[i+b].set_value(bool_value)


# rd -> Dados da Memória
def rd(val):
    global leds
    i = 40
    for a, b in enumerate(range(7, -1, -1)):
        bool_value = ((val & (1 << a)) == (1 << a))
        leds[i+a].set_value(bool_value)

# ri -> Código de Instrução
def ri(val):
    global leds
    i = 48
    for a, b in enumerate(range(7, -1, -1)):
        bool_value = ((val & (1 << a)) == (1 << a))
        leds[i+a].set_value(bool_value)

# acc -> Acumulador
def acc(val):
    global leds
    i = 56
    for a, b in enumerate(range(7, -1, -1)):
        bool_value = ((val & (1 << a)) == (1 << a))
        leds[i+a].set_value(bool_value)

# TODO: FASE

def modo(val):
    global leds
    i = 71
    for a in range(6):
        bool_value = ((val & (1 << a)) == (1 << a))
        leds[i+a].set_value(bool_value)

def espera(val):
    leds[77].set_value(val)

def interrupcao(val):
    leds[78].set_value(val)

def preparacao(val):
    leds[79].set_value(val)

def setup():
    global myPort
    # dados_painel - 1
    x, y = 434, 277
    inc = SMALL_INC
    for i in range(12):
      leds.append(Led(x + inc * i,
                      y,
                      SMALL_LED,
                      RED_ON,
      ))

      # vai_um
    x, y = 600, 170
    leds.append(Led(x, y, SMALL_LED, RED_ON))

    # transbordo
    x, y = 436, 170
    leds.append(Led(x, y, SMALL_LED, RED_ON))

    # parado
    x, y = 340, 378
    leds.append(Led(x, y, BIG_LED, WHITE_ON))

    # externo
    x, y = 401, 378
    leds.append(Led(x, y, BIG_LED, WHITE_ON))

    # ci -> Endreço de Instrução
    x, y = 434, 121
    inc = SMALL_INC
    for i in range(12):
      leds.append(Led(x + inc * i,
                      y,
                      SMALL_LED,
                      RED_ON,
      ))

    # re -> Endereço na Memória
    x, y = 434, 57
    inc = SMALL_INC
    for i in range(12):
      leds.append(Led(x + inc * i,
                      y,
                      SMALL_LED,
                      RED_ON,
      ))

    # rd -> Dados da Memória
    x, y = 146, 250
    inc = SMALL_INC
    for i in range(8):
      leds.append(Led(x + inc * i,
                      y,
                      SMALL_LED,
                      RED_ON,
      ))

    # ri -> Código de Instrução
    x, y = 146, 185
    inc = SMALL_INC
    for i in range(8):
      leds.append(Led(x + inc * i,
                      y,
                      SMALL_LED,
                      RED_ON,
      ))

    # acc -> Acumulador
    x, y = 146, 120
    inc = SMALL_INC
    for i in range(8):
      leds.append(Led(x + inc * i,
                      y,
                      SMALL_LED,
                      RED_ON,
      ))

    # TODO: FASE
    for i in range(7):
      leds.append(Led(0, 0, 0, GREEN_ON))

    # modo
    x, y = 79, 566
    inc = 58
    for i in range(6):
      leds.append(Button(x + inc * i,
                         y,
                         19,
                         GREEN_ON,
                         0x40 + i,
      ))

    # espera
    x, y = 525, 566
    leds.append(Button(x, y, 19, GREEN_ON, 0x40))

    # interrupcao
    x, y = 584, 566
    leds.append(Button(x, y, 19, GREEN_ON, 0x41))

    # preparacao
    x, y = 640, 620
    leds.append(Button(x, y, 19, GREEN_ON, 0x42))

    # Buttons
    # Painel
    for i in range(12):
      x, y = 109, 474
      buttons.append(Button(x + BIG_INC * i,
                            y,
                            BIG_LED,
                            RED_ON,
                            0x10 + i,
      ))

    # Partida
    buttons.append(Partida(628, 556, 18, (255, 255, 255), 0x43))

    # Other buttons
    for led in leds:
      if isinstance(led, Button):
        buttons.append(led)

    #noStroke()
    size(729, 665)
    dados_painel(11)
    portName = '/dev/ttyACM0'
    try:
      myPort = Serial(this, portName, 115200)
      myPort.bufferUntil(10)
    except:
      pass
    
    pato = loadImage("pato.png")
    image(pato, 0, 0)

def mouseClicked():
    for b in buttons:
      b.clicked(mouseX, mouseY)

def draw():
    global buff
    for b in buttons:
      b.draw()

    if len(buff) == 80:
        update_panel(buff)
    else:
        print ('There is not enough data to update panel. len={}'.format(len(buff)))
    
def serialEvent(evt):
    global buff
    data = evt.readString()
    if data.startswith('LEDS:'):
        split = data.split(':')
        if len(split) == 2:
            buff = split[1].strip()
    elif data.startswith('TTY:'):
        split = data.split(':')
        if len(split) == 2:
            print 'Teletype: ', split[1].strip()
    else:
      print("Unknown: " + data)


def binary_str_to_int(lst):
    if not lst:
        return 0
    return reduce(lambda x,y:x+y, [int(v)<<i for i, v in enumerate(lst)])


def update_panel(status):
    global leds
    dados_painel(binary_str_to_int(status[0:12]))
    vai_um(int(status[12]))
    transbordo(int(status[13]))
    parado(int(status[14]))
    externo(int(status[15]))
    ci(binary_str_to_int(status[16:28]))
    re(binary_str_to_int(status[28:40]))
    rd(binary_str_to_int(status[40:8]))
    ri(binary_str_to_int(status[48:56]))
    acc(binary_str_to_int(status[56:64]))
    modo(binary_str_to_int(status[71:77]))
    espera(int(status[77]))
    interrupcao(int(status[78]))
    preparacao(int(status[79]))
