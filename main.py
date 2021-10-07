from typing import NoReturn
from kivymd.app import MDApp

from kivy.lang import Builder
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.widget import Widget

from kivymd.uix.button import MDRaisedButton


Config.set("kivy", "exit_on_escape", 0)
Config.set("kivy", "log_level", "warning")
Window.size = (320, 355)
Builder.load_file("main.kv")


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
    a = False

    def clearAll(self):
        self.currentSign = ""
        self.firstNumber = "0"
        self.secondNumber = "0"
        self.ids.calcText.text = "0"

    def delete(self):
        if len(self.ids.calcText.text) >= 2:
            self.ids.calcText.text = self.ids.calcText.text[:-1]
        else:
            self.ids.calcText.text = "0"

        self.secondNumber = self.ids.calcText.text

    def negation(self):
        self.ids.calcText.text = str(numberify(self.ids.calcText.text) * (-1))
        if self.currentSign == "":
            self.firstNumber = str(numberify(self.firstNumber) * (-1))
        else:
            self.secondNumber = str(numberify(self.secondNumber) * (-1))
        

    def changeSign(self, value):
        if self.currentSign != "":
            self.getResult()
            # self.ids.calcText.text = self.firstNumber
        self.currentSign = value
        self.a = True
        self.secondNumber = self.firstNumber


    def addNumber(self, value):
        # if len(self.ids.calcText.text) > 11:
        #     return
            
        # if self.ids.calcText.text == "0":
        #     self.ids.calcText.text = ""

        # if self.currentSign != "":
        #     placeholder = self.ids.calcText.text
        #     if self.firstNumber == "0":
        #         self.ids.calcText.text = ""
        #     self.firstNumber = placeholder

        # self.ids.calcText.text += str(value)
        # self.secondNumber = self.ids.calcText.text

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
        # print(self.firstNumber, self.secondNumber)

    def getResult(self):
        string = self.firstNumber + self.currentSign + self.secondNumber
        if string == "9+10" or string == "10+9":
            result = ["21"]
        else:
            result = str(eval(string)).split(".")

        if len(result[0]) > 12:
            self.ids.calcText.text = "{:E}".format(float(result[0]))
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

        print(self.firstNumber, self.currentSign, self.secondNumber, "=", str(result))
        self.firstNumber = str(eval(string))


class Calculator(MDApp):
    def build(self):
        return CalcWidget()


Calculator().run()
