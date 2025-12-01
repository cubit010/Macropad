# KMK firmware example for Seeed RP2040 macropad
# Columns: GPIO29, GPIO6, GPIO7 (pins 4,5,6)
# Rows: GPIO26, GPIO27, GPIO28 (pins 1,2,3)
import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation


keyboard = KMKKeyboard()

# Pin definitions
keyboard.row_pins = (board.GP29, board.GP6, board.GP7)
keyboard.col_pins = (board.GP26, board.GP27, board.GP28)
keyboard.diode_orientation = DiodeOrientation.ROW2COL


# Rotary Encoder
from kmk.modules.encoder import EncoderHandler
encoder_handler = EncoderHandler()
keyboard.modules.append(encoder_handler)
encoder_handler.pins = ((2, 1),)
encoder_handler.switch_pin = 0
encoder_handler.map = [((KC.VOLU,), (KC.VOLD,))]

# OLED Display
from kmk.extensions.display import Oled
keyboard.extensions.append(
    Oled(
        width=128,
        height=32,
        i2c_num=0,
        sda=board.GP4,
        scl=board.GP3,
    )
)

# Custom Volume Bar UI
from kmk.extensions.display import Oled, Canvas

class VolumeUI(Canvas):
    def __init__(self):
        super().__init__(128, 32)
        self.level = 50

    def draw(self, display):
        display.fill(0)
        bar_width = int((self.level / 100) * 120)
        display.rect(4, 12, 120, 8, 1)
        display.fill_rect(4, 12, bar_width, 8, 1)
        display.text(f"Vol {self.level}", 4, 0, 1)
        display.show()

vol_ui = VolumeUI()

oled = Oled(
    width=128,
    height=32,
    i2c_num=0,
    sda=4,
    scl=3,
    display=vol_ui,
)
keyboard.extensions.append(oled)

# Update encoder mapping to change volume level
encoder_handler.map = [
    ((lambda: setattr(vol_ui, "level", min(100, vol_ui.level + 1)),),
     (lambda: setattr(vol_ui, "level", max(0, vol_ui.level - 1)),))
]

# Simple 3x3 keymap
keyboard.keymap = [
    [KC.A, KC.B, KC.C],
    [KC.D, KC.E, KC.F],
    [KC.G, KC.H, KC.I],
]

if __name__ == '__main__':
    keyboard.go()
