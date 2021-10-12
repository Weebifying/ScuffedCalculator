import string
import os, sys
from typing import NoReturn
from math import sqrt
from kivy.resources import resource_find, resource_add_path

from kivymd.app import MDApp

from kivy.lang import Builder
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.widget import Widget

from kivymd.uix.button import MDRaisedButton


Config.set("kivy", "exit_on_escape", 0)
Config.set("kivy", "log_level", "warning")
Window.size = (320, 355)
if hasattr(sys, "_MEIPASS"):
    resource_add_path(os.path.join(sys._MEIPASS))
filename = "main.kv"
filename = resource_find(filename) or filename
Builder.load_file(filename)

def numberify(*args):
    owo = []
    for w in range(0, len(args)):
        try:
            owo.append(int(args[w]))
        except ValueError:
            owo.append(float(args[w]))
    return owo if len(owo) > 1 else owo[0]


class MDRaisedButtonFixed(MDRaisedButton):
    def on_width(self, instance_button, width: float) -> NoReturn:
        pass


class CalcWidget(Widget):
    currentSign = ""
    firstNumber = "0"
    secondNumber = "0"
    # secondNumber input mode
    a = False
    # result mode
    b = False

    def clearAll(self):
        self.currentSign = ""
        self.firstNumber = "0"
        self.secondNumber = "0"
        self.ids.calcText.text = "0"
        self.a = False
        self.b = False

    def delete(self):
        if len(self.ids.calcText.text) >= 2:
            self.ids.calcText.text = self.ids.calcText.text[:-1]
        else:
            self.ids.calcText.text = "0"

        self.secondNumber = self.ids.calcText.text

    def negation(self):
        try:
            string = str(numberify(self.ids.calcText.text) * (-1))
            result = str(round(eval(string), 12)).split(".")

            if abs(eval(string)) < 0.00000000001:
                self.ids.calcText.text = "{:E}".format(float(eval(string)))
                self.firstNumber = str(eval(string))

            elif len(result[0]) > 12:
                self.ids.calcText.text = "{:E}".format(float(result[0]))
                self.firstNumber = str(round(eval(string), 12))
            else:
                try:
                    num = result[0]
                    dec = result[1]
                    if dec == "0":
                        self.ids.calcText.text = num
                    else:
                        if len(num) + len(dec) > 13:
                            a = 12 - len(num)
                            dec = dec[:a]

                        self.ids.calcText.text = num + "." + dec

                except IndexError:
                    self.ids.calcText.text = num

            if self.currentSign == "":
                self.firstNumber = str(numberify(self.firstNumber) * (-1))
            else:
                self.secondNumber = str(numberify(self.secondNumber) * (-1))

        except NameError:
            pass

    def squareRoot(self):
        try:
            string = str(round(sqrt(numberify(self.ids.calcText.text)), 12))
            result = str(round(eval(string), 12)).split(".")

            if abs(eval(string)) < 0.00000000001:
                self.ids.calcText.text = "{:E}".format(float(eval(string)))
                self.firstNumber = str(eval(string))

            elif len(result[0]) > 12:
                self.ids.calcText.text = "{:E}".format(float(result[0]))
                self.firstNumber = str(round(eval(string), 12))
            else:
                try:
                    num = result[0]
                    dec = result[1]
                    if dec == "0":
                        self.ids.calcText.text = num
                    else:
                        if len(num) + len(dec) > 13:
                            a = 12 - len(num)
                            dec = dec[:a]

                        self.ids.calcText.text = num + "." + dec

                except IndexError:
                    self.ids.calcText.text = num

            if self.currentSign == "":
                self.firstNumber = str(round(sqrt(numberify(self.firstNumber)), 12))
            else:
                self.secondNumber = str(round(sqrt(numberify(self.secondNumber)), 12))
        except ValueError:
            self.ids.calcText.text = "NaN"
            if self.currentSign == "":
                self.firstNumber = "0"
            else:
                self.secondNumber = "0"
        except NameError:
            pass

    def changeSign(self, value):
        if self.currentSign != "" and (not self.a):
            self.getResult(False)
        self.b = False
        self.currentSign = value
        self.secondNumber = self.firstNumber
        self.a = True

    def addDot(self):
        if "." in self.ids.calcText.text:
            return
        else:
            if self.b:
                self.firstNumber = "0."
                self.ids.calcText.text = "0."
            else:
                if self.currentSign == "":
                    self.firstNumber += "."
                else:
                    self.secondNumber += "."
                self.ids.calcText.text += "."

            self.b = False

    def addNumber(self, value):
        if (
            self.currentSign == ""
            and len(self.firstNumber.translate(str.maketrans("", "", "."))) > 12
        ):
            return
        if (
            self.currentSign != ""
            and len(self.secondNumber.translate(str.maketrans("", "", "."))) > 12
        ):
            return

        if ("E" in self.ids.calcText.text) or (self.ids.calcText.text == "INF"):
            self.firstNumber = "0"
            self.ids.calcText.text = "0"

        if self.ids.calcText.text == "0":
            self.ids.calcText.text = ""

        if self.currentSign != "":
            if self.a:
                self.ids.calcText.text = ""
                self.secondNumber = "0"

            if self.secondNumber == "0":
                self.secondNumber = ""

            self.secondNumber += str(value)
        else:
            if self.firstNumber == "0":
                self.firstNumber = ""

            self.firstNumber += str(value)

        self.ids.calcText.text += str(value)
        self.a = False

    def getResult(self, value):
        xd = False
        string = self.firstNumber + self.currentSign + self.secondNumber
        if string == "9+10" or string == "10+9":
            result = ["21"]
        else:
            try:
                result = str(round(eval(string), 12)).split(".")
            except NameError:
                result = [self.ids.calcText.text]

        try:
            if abs(eval(string)) < 0.00000000001:
                self.ids.calcText.text = "{:E}".format(float(eval(string)))
                self.firstNumber = str(eval(string))

            elif len(result[0]) > 12:
                self.ids.calcText.text = "{:E}".format(float(result[0]))
                self.firstNumber = str(round(eval(string), 12))
            else:
                try:
                    num = result[0]
                    dec = result[1]
                    if dec == "0":
                        self.ids.calcText.text = num
                    else:
                        if len(num) + len(dec) > 12:
                            a = 12 - len(num)
                            dec = dec[:a]

                        self.ids.calcText.text = num + "." + dec

                except IndexError:
                    self.ids.calcText.text = num
                    xd = True

        except NameError:
            pass

        print(self.firstNumber, self.currentSign, self.secondNumber, "=", str(result))
        if xd:
            self.firstNumber = str(round(eval(string), 12))
            xd = False
        if value:
            self.b = True
        self.a = False


class Calculator(MDApp):
    def build(self):
        self.icon = "calc.png"
        return CalcWidget()


Calculator().run()
