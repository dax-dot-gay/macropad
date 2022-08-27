from adafruit_macropad import MacroPad, Keycode
from usb_cdc import data
from jsondb import JsonDb
import os
import json


class ModPad:
    def __init__(self, db="data.json") -> None:
        self.pad = MacroPad()
        db = f"data/{db}"
        if not db in os.listdir("data"):
            with open(db, "w") as f:
                json.dump({
                    "modes": [
                        {
                            "name": "Media1",
                            "keys": [
                                None,
                                {
                                    "code": " VOL+ ",
                                    "color": [0, 128, 0]
                                },
                                None,
                                {
                                    "code": " PREV ",
                                    "color": [128, 0, 0]
                                },
                                {
                                    "code": " PL/P ",
                                    "color": [0, 0, 128]
                                },
                                {
                                    "code": " NEXT ",
                                    "color": [0, 128, 0]
                                },
                                None,
                                {
                                    "code": " VOL- ",
                                    "color": [128, 0, 0]
                                },
                                None
                            ]
                        }
                    ],
                    "mode": 0
                }, f)
        self.db = JsonDb(db)

        self.lines = [f"Current Mode: {self.mode['name']}",
                      "====== ====== ======", "====== ====== ======", "====== ====== ======"]
        
        self.display = self.pad.display_text(title="")
        for l in range(len(self.lines)):
            self.display[l].text = self.lines[l]
        
        self.display.show()
        self.last_pressed = None
        self.pad.pixels.brightness = 0.2
        self.pressed_actions = []

    def update_text(self, lines: list[str]):
        updt = False
        for l in range(len(lines)):
            if not lines[l] == self.lines[l]:
                self.display[l].text = lines[l]
                self.lines[l] = lines[l]
                updt = True
        
        if updt:
            self.display.show()

    def key_events(self):
        evt = self.pad.keys.events.get()
        if evt and evt.pressed and self.last_pressed != evt.key_number:
            self.last_pressed = evt.key_number

            if evt.key_number == 0:
                if self.db["mode"] > 0:
                    self.db["mode"] -= 1

            if evt.key_number == 1:
                self.pad.keyboard.press(Keycode.ALT, Keycode.D)
                self.pad.keyboard.release_all()
            
            if evt.key_number == 2:
                if self.db["mode"] < (len(self.db["modes"]) - 1):
                    self.db["mode"] += 1

        elif evt and evt.released:
            self.last_pressed = None
        
        if evt and evt.key_number >= 3:
            keys = []
            for k in range(9):
                try:
                    l = self.mode["keys"][k]["code"]
                except:
                    l = "======"

                if evt.pressed and evt.key_number - 3 == k:
                    l = "[" + l[1:-1] + "]"
                    self.pressed_actions.append(evt.key_number - 3)
                elif evt.released and evt.key_number - 3 == k and k in self.pressed_actions:
                    self.pressed_actions.remove(k)
                elif k in self.pressed_actions:
                    l = "[" + l[1:-1] + "]"
                keys.append(l)
        else:
            keys = []
            for k in range(9):
                try:
                    l = self.mode["keys"][k]["code"]
                except:
                    l = "======"

                if k in self.pressed_actions:
                    l = "[" + l[1:-1] + "]"
                keys.append(l)

        self.update_text(
            [f"Current Mode: {self.mode['name']}", " ".join(keys[:3]), " ".join(keys[3:6]), " ".join(keys[6:])])
    
    def update_lights(self):
        self.pad.pixels[1] = (0, 0, 255)
        if self.db["mode"] == 0:
            self.pad.pixels[0] = (255, 0, 0)
        else:
            self.pad.pixels[0] = (0, 255, 0)

        if self.db["mode"] >= (len(self.db["modes"]) - 1):
            self.pad.pixels[2] = (255, 0, 0)
        else:
            self.pad.pixels[2] = (0, 255, 0)
        
        for r in range(9):
            if len(self.mode["keys"]) - 1 >= r and self.mode["keys"][r]:
                self.pad.pixels[3+r] = self.mode["keys"][r]["color"]
            else:
                self.pad.pixels[3+r] = (0, 0, 0)


    def loop(self):
        while True:
            self.key_events()
            self.update_lights()
    
    @property
    def mode(self):
        return self.db['modes'][self.db['mode']]



pad = ModPad()
pad.loop()
