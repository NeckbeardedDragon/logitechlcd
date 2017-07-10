import ctypes,sys
from .constants import *

if sys.maxsize > 2**32:
    cdll = ctypes.CDLL(__path__[0]+"\\x64\\LogitechLcdEnginesWrapper.dll")
else:
    cdll = ctypes.CDLL(__path__[0]+"\\x86\\LogitechLcdEnginesWrapper.dll")


cdll.LogiLcdInit.restype = bool
cdll.LogiLcdIsConnected.restype = bool
cdll.LogiLcdIsButtonPressed.restype = bool
cdll.LogiLcdUpdate.restype = None
cdll.LogiLcdShutdown.restype = None

cdll.LogiLcdMonoSetBackground.restype = bool
cdll.LogiLcdMonoSetText.restype = bool

cdll.LogiLcdColorSetBackground.restype = bool
cdll.LogiLcdColorSetTitle.restype = bool
cdll.LogiLcdColorSetText.restype = bool

class MonoImage:
    def __init__(self,img=None):
        self.img = bytearray(160*43)
        if img:
            for i in range(160*43):
                self.img[i] = img[i]

    def set(self, img):
        if img:
            for i in range(160*43):
                self.img[i] = img[i]

    @property
    def _as_parameter_(self):
        return (ctypes.c_byte * (160*43))(*self.img)

class ColorImage:
    #TODO & Caveat to the reader: the byte order for each color is BGRA. RGBA is the general standard, so keep this in mind.
    def __init__(self,img=None):
        self.img = bytearray(320*240*4)
        if img:
            for i in range(320*240*4):
                self.img[i] = img[i]

    def set(self, img):
        if img:
            for i in range(320*240*4):
                self.img[i] = img[i]

    @property
    def _as_parameter_(self):
        return (ctypes.c_byte * (320*240*4))(*self.img)

def init(name,*types):
    """Initialize the app.

    name: Name to display in app selector. Used as an identifier, so keep it somewhat unique
    *types: Types of display to initialize. Use TYPE_MONO and/or TYPE_COLOR depending on what LCDs your app is for."""
    res = 0x00000000
    for t in types:
        res = res | t
    return cdll.LogiLcdInit(name,res)

def isConnected(*types):
    """Check if a certain type of display is connected.

    *types: Types of display to check. Use TYPE_MONO and/or TYPE_COLOR depending on what LCDs you're looking for."""
    res = 0x00000000
    for t in types:
        res = res | t
    return cdll.LogiLcdIsConnected(name,res)

def isButtonPressed(*buttons):
    """Check if certain buttons under the display are pressed.

    *buttons: Buttons to check. Use the MONO_BUTTON_[num] and COLOR_BUTTON_[name] constants."""
    res = 0x00000000
    for b in buttons:
        res = res | b
    return cdll.LogiLcdIsButtonPressed(res)

def update():
    """Update the LCD screen. Required after setting the background, text, or title for it to actually show up."""
    cdll.LogiLcdUpdate()

def shutdown():
    """Shuts down the app. Call this before closing your app."""
    cdll.LogiLcdShutdown()

def setMonoBackground(img):
    """Sets the background for a connected Mono display.

    img: Either a MonoImage or something that can be cast as a ctypes.c_byte * (160*43). Contains the bytes to write to the background. 0-127 = dark, 128-255 = light"""
    if type(img) is not MonoImage:
        img = (ctypes.c_byte * (160*43))(*img)
    return cdll.LogiLcdMonoSetBackground(img)

def setMonoText(line,text):
    """Sets the text on the specified line for a Mono display.

    line: int between 0 and 3.
    text: str to write to the screen."""
    return cdll.LogiLcdMonoSetText(line,text)

def setColorBackground(img):
    """Sets the background for a Color display.

    img: Either a ColorImage or something that can be cast as a ctypes.c_byte * (320*240*4). Contains the bytes to write to the background. Each set of 4 bytes is in BGRA order for one pixel."""
    if type(img) is not ColorImage:
        img = (ctypes.c_byte * (320*240*4))(*self.img)
    return cdll.LogiLcdColorSetBackground(img)

def setColorTitle(text,*color):
    """Sets the title for a Color display.

    text: str to set as the title.
    *color: 3 bytes for the color to display the title in, in RGB order."""
    #THIS is in RGB format.
    return cdll.LogiLcdColorSetTitle(text,*color)

def setColorText(line,text,*color):
    """Sets the text on the specified line for a Color display.

    line: int between 0 and 7.
    text: str to write to the screen.
    *color: 3 bytes for the color to display the line in, in RGB order."""
    #THIS is in RGB format.
    return cdll.LogiLcdColorSetText(line,text,*color)