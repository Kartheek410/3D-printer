import tkinter as tk
from tkinter import *
from tkinter import filedialog
import os
import time
from time import sleep
from PIL import Image, ImageTk
from pixtendv2l import PiXtendV2L
import logging
import RPi.GPIO as GPIO

'''LOG_FILENAME = 'Log.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

logging.debug('Debugging')'''


p = PiXtendV2L()

GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)

GPIO.setup(21,GPIO.OUT) # direction
GPIO.setup(20,GPIO.OUT) # step

step_count = 72727  # number of step to run  change this to change where it stops
delay = 0.001

GPIO.output(21, GPIO.HIGH)

# create logger with 'spam_application'
logger = logging.getLogger('log_application')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('Log.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)
# 'application' code
logger.debug('Debugging')
logger.info('User interface up and running')



class Filedialog:
    def directory(self, Stepper):
        content = filedialog.askdirectory()
        return content
        


class Main(Frame):
    
    
    def __init__(self):
        self.opening_times = 0
        self.current_image = 0
        self.images = []
        self.root = Tk()
        self.root.title("H3DP")
        self.root.configure(bg='#DDE2E2')
        self.root.geometry("800x800")
        self.frame = Frame(self.root)
        self.frame.pack(side=RIGHT)
        self.frame = Frame.__init__(self, self.root)
        self.root.bind("<Left>", self.reverse_image)
        self.root.bind("<Right>", self.next_image)
        self.create_widgets()
        self.widgets()
        self.root.mainloop()

        

    def create_widgets(self):

        # -----------------------------------------------------
        # Button for LIGHT
        # -----------------------------------------------------

        self.relayon = Button(self.frame)
        self.relayon["text"] = "ON"
        self.relayon["command"] = self.relay_on
        self.relayon.place(x=5, y=30, width=50, height=20)

        self.relayoff = Button(self.frame)
        self.relayoff["text"] = "OFF"
        self.relayoff["command"] = self.relay_off
        self.relayoff.place(x=5, y=60, width=50, height=20)

        self.light = Label(self.frame)
        self.light["text"] = "Light"
        self.light.place(x=5, y=5, width=50, height=20)
        
        self.clockwise = Button(self.frame)
        self.clockwise["text"] = "25cw"
        self.clockwise["command"] = self.stepper_25cw
        self.clockwise.place(x=65, y=10)   
        
        self.anticlockwise = Button(self.frame)
        self.anticlockwise["text"] = "25ccw"
        self.clockwise["command"] = self.stepper_25ccw
        self.anticlockwise.place(x=65, y=50)
        

    #stepper.setup()    

    def widgets(self):

        self.menu = Menu(self.root)
        self.root.config(menu=self.menu)
        self.filemenu = Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="Open", command=self.open_image)
        self.image_label = Label(self.root)
        self.image_label.place(relx=0.5, rely=0.5, anchor="center")
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Save")
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.onExit)
        self.editmenu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label='Edit', menu=self.editmenu)
        self.editmenu.add_command(label="Undo")
        self.editmenu.add_command(label="Redo")

    def stepper_25cw(self):
        
        delay = 0.001
        GPIO.output(21, GPIO.HIGH)
        print (" Drive CW ", step_count ,"steps")
        for x in range(step_count):
            GPIO.output(20, GPIO.HIGH)
            sleep(delay)
            GPIO.output(20, GPIO.LOW)
            sleep(delay)
        print("Stop")
        sleep(5)
        GPIO.cleanup()


    def stepper_25ccw(self):
        print (" Drive CCW ", step_count ,"steps")
        GPIO.output(21, GPIO.LOW)
        for x in range(step_count):
            GPIO.output(20, GPIO.HIGH)
            sleep(delay)
            GPIO.output(20, GPIO.LOW)
            sleep(delay)

        # end of program
        print("End program")
        GPIO.cleanup()


    def open_image(self):
        self.image_path = Filedialog.directory(self)
        if self.image_path != "":
            for file in os.listdir(self.image_path):
                print(file)
                self.images.append(str(self.image_path) + "/" + str(file))
                self.opening_times = self.opening_times + 1
                if self.opening_times == 1:
                    self.original = PhotoImage(file=str(self.image_path) + "/" + str(file))
                    self.image = self.original.subsample(4, 4)
                    self.image_label.config(image=self.image)
                    self.image_label.update()
                    #img = ImageTk.PhotoImage(Image.open(self.image_path))
                    #panel = tk.Label(self.root, image=img)
                    #panel.pack(side="bottom", fill="both", expand="yes")
        print(self.images)

    def reverse_image(self, event):
        if len(self.images) > 1:
            self.original = PhotoImage(file=str(self.images[self.current_image - 1]))
            self.image = self.original.subsample(4, 4)
            self.image_label.config(image=self.image)
            self.image_label.update()
            self.current_image = self.current_image - 1

    def next_image(self, event):
        if len(self.images) > 1:
            self.original = PhotoImage(file=str(self.images[self.current_image + 1]))
            self.image = self.original.subsample(4, 4)
            self.image_label.config(image=self.image)
            self.image_label.update()
            self.current_image = self.current_image + 1

    def relay_on(self):

        p.relay1 = p.ON

    def relay_off(self):

        p.relay1 = p.OFF

    def relay_on0(self):

        p.relay0 = p.ON

    def relay_off0(self):

        p.relay0 = p.OFF

    def relay_on2(self):

        p.relay2 = p.ON

    def relay_off2(self):

        p.relay2 = p.OFF

    def onExit(self):
        self.quit()



if __name__ == "__main__":
    Main()
