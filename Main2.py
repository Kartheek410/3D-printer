import tkinter as tk
from tkinter import *
from tkinter import filedialog, RIGHT
import os
import time
from time import sleep
from PIL import Image, ImageTk
from pixtendv2l import PiXtendV2L
import logging
import RPi.GPIO as GPIO
import webbrowser

'''LOG_FILENAME = 'Log.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

logging.debug('Debugging')'''


p = PiXtendV2L()

GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)

##Stepper signal(One of the end switches)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(21,GPIO.OUT) ##for direction
GPIO.setup(20,GPIO.OUT) ##for step

##projector RESETZ
#GPIO.setup(26, GPIO.OUT)
#GPIO.setup(13, GPIO.OUT)
#GPIO.output(26, GPIO.LOW)
##I2C_BUSY
#GPIO.setup(16, GPIO.OUT)

##ASIC_READY
#GPIO.setup(12, GPIO.OUT)



step_count = 72727  ##number of step to run  change this to change where it stops
delay = 0.001

GPIO.output(21, GPIO.HIGH)



#GPIO.input(26, GPIO.LOW) #projector kept low initially

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

#Redirecting to the web page(Mioto print head) through tkinter button
running = True

class Filedialog:
    def directory(self):
        content = filedialog.askdirectory()
        return content
        


class Main(Frame):
    
    
    def __init__(self):
        self.opening_times = 0
        self.current_image = 0
        self.images = []
        self.root = Tk()
        self.root.title("H3DP")
        self.root.configure(bg='pale turquoise')
        self.root.geometry("800x800")
        self.frame = Frame(self.root)
        self.frame.pack(side=RIGHT)
        self.frame = Frame.__init__(self, self.root)
        self.root.bind("<Left>", self.reverse_image)
        self.root.bind("<Right>", self.next_image)
        self.create_widgets()
        self.widgets()
        self.root.mainloop()
    
    #To open a web browser
    
    def openweb(self):
        url = "https://192.168.40.120"
        webbrowser.open(url)



    def create_widgets(self):

        # -----------------------------------------------------
        # Button for LIGHT
        # -----------------------------------------------------

        self.relayon = Button(self.frame)
        self.relayon["text"] = "ON"
        self.relayon["bg"] = "green"
        self.relayon["command"] = self.relay_on
        self.relayon.place(x=5, y=30, width=50, height=20)

        self.relayoff = Button(self.frame)
        self.relayoff["text"] = "OFF"
        self.relayoff["bg"] = "red"
        self.relayoff["command"] = self.relay_off
        self.relayoff.place(x=5, y=60, width=50, height=20)

        self.light = Label(self.frame)
        self.light["text"] = "Light"
        self.light.place(x=5, y=5, width=50, height=20)

        # -----------------------------------------------------
        # Button for Projector
        # -----------------------------------------------------
        self.projectoron = Button(self.frame)
        self.projectoron["text"] = "Turnon"
        self.projectoron["bg"] = "green"
        self.projectoron["command"] = self.on
        self.projectoron.place(x=125, y=143, width=50, height=20)
        
        self.projectoroff = Button(self.frame)
        self.projectoroff["text"] = "Turnoff"
        self.projectoroff["bg"] = "red"
        self.projectoroff["command"] = self.off
        self.projectoroff.place(x=180, y=143, width=50, height=20)
        
        self.projector = Label(self.frame)
        self.projector["text"] = "Projector"
        self.projector.place(x=125, y=120, width=100, height=20)
        
        self.ledon = Button(self.frame)
        self.ledon["text"] = "Led On"
        self.ledon["bg"] = "green"
        self.ledon["command"] = self.led1
        self.ledon.place(x=125, y=163, width=50, height=20)
        
        self.ledoff = Button(self.frame)
        self.ledoff["text"] = "Led Off"
        self.ledoff["bg"] = "red"
        self.ledoff["command"] = self.led2
        self.ledoff.place(x=180, y=163, width=50, height=20)
        
        # -----------------------------------------------------
        # Button for Z-axis Stepper motor
        # -----------------------------------------------------
        
        self.clockwise = Button(self.frame)
        self.clockwise["text"] = "25 mm+"
        self.clockwise["command"] = self.stepper_25cw
        self.clockwise.place(x=65, y=30, width=100, height=20)   
        
        self.anticlockwise = Button(self.frame)
        self.anticlockwise["text"] = "25 mm-"
        self.anticlockwise["command"] = self.stepper_25ccw
        self.anticlockwise.place(x=65, y=60, width=100, height=20)
        
        self.clockwise = Button(self.frame)
        self.clockwise["text"] = "50 mm+"
        #self.clockwise["bg"] = "green"
        self.clockwise["command"] = self.stepper_50cw
        self.clockwise.place(x=165, y=30, width=100, height=20)  
        
        self.anticlockwise = Button(self.frame)
        self.anticlockwise["text"] = "50 mm-"
        self.anticlockwise["command"] = self.stepper_50ccw
        self.anticlockwise.place(x=165, y=60, width=100, height=20)

        self.stepper = Label(self.frame)
        self.stepper["text"] = "Stepper Z axis"
        self.stepper.place(x=65, y=5, width=100, height=20)
        
        self.stopping = Button(self.frame)
        self.stopping["text"] = "Aboart"
        self.stopping["command"] = self.stop
        self.stopping.place(x=165, y=5, width=100, height=20)
    #stepper.setup()    
        # -----------------------------------------------------
        # Button for Opening Mioto WebUI
        # -----------------------------------------------------
        
        self.webbrowser = Button(self.frame)
        self.webbrowser["text"] = "Mioto WebUI"
        self.webbrowser["command"] = self.openweb
        self.webbrowser.place(x=5, y=140, width=100, height=20)
        
        self.webbrowser = Label(self.frame)
        self.webbrowser["text"] = "Open printhead"
        self.webbrowser.place(x=5, y=120, width=100, height=20)
        
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
        
#step_count has been given in the initial steps which are for the calculation of 25mm in microsteps
    def stepper_25cw(self):
        delay = 0.001
        GPIO.setmode(GPIO.BCM)
        GPIO.output(21, GPIO.HIGH)
        print (" Drive CW ", step_count ,"steps")
        for x in range(step_count):
            GPIO.output(20, GPIO.HIGH)
            sleep(delay)
            GPIO.output(20, GPIO.LOW)
            sleep(delay)
            if p.digital_in0 == p.OFF:
                break
        GPIO.cleanup()
        print("Stop")
        sleep(5)

    def stepper_25ccw(self):
        delay = 0.001
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(21, GPIO.OUT)
        GPIO.setup(20, GPIO.OUT)
        print (" Drive CCW ", step_count ,"steps")
        GPIO.output(21, GPIO.LOW)
        for x in range(step_count):
            GPIO.output(20, GPIO.HIGH)
            sleep(delay)
            GPIO.output(20, GPIO.LOW)
            sleep(delay)
            if (GPIO.input(19) == False):
                break
        print("Homed")
        sleep(delay)
        GPIO.cleanup()
        # end of program
        print ("End program")
    
    def stepper_50cw(self):
        delay = 0.001
        GPIO.setmode(GPIO.BCM)
        GPIO.output(21, GPIO.HIGH)
        print (" Drive CW ", 2*step_count ,"steps")
        for x in range(step_count):
            GPIO.output(20, GPIO.HIGH)
            sleep(delay)
            GPIO.output(20, GPIO.LOW)
            sleep(delay)
            if p.digital_in0 == p.OFF:
                break
        print("Stop")
        sleep(5)
        GPIO.cleanup()

    def stepper_50ccw(self):
        delay = 0.001
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(21, GPIO.OUT)
        GPIO.setup(20, GPIO.OUT)
        print (" Drive CCW ", 2*step_count ,"steps")
        GPIO.output(21, GPIO.LOW)
        for x in range(step_count):
            GPIO.output(20, GPIO.HIGH)
            sleep(delay)
            GPIO.output(20, GPIO.LOW)
            sleep(delay)
            if (GPIO.input(19) == False):
                break

        # end of program
        print ("Homed")
        GPIO.cleanup()
        
    def stop(self):#Stop scanning by setting the global flag to False."""
        global running
        running = False
        
    def on(self):
        GPIO.setup(26, GPIO.OUT)
        GPIO.setup(12, GPIO.IN)
        GPIO.setup(16, GPIO.IN)
        
        GPIO.output(26, GPIO.HIGH)
        if True:
            GPIO.input(12) == 1
            print("ASIC_READY")
            sleep(15)
        print("Projecor ON")

        sleep(1)
        #GPIO.cleanup()
        print("end")
        
    def off(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(26, GPIO.OUT)
        GPIO.setup(16, GPIO.IN)
        GPIO.setup(12, GPIO.IN)
        
        #GPIO.output(12, GPIO.HIGH)
        #if GPIO.input(12, GPIO.HIGH):
        GPIO.output(26,GPIO.LOW)
        print("Projector off")
        sleep(1)
        #GPIO.cleanup()
    
    def led1(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(26, GPIO.OUT)
        GPIO.setup(13, GPIO.OUT)
        if (GPIO.output(26, GPIO.HIGH)):
            GPIO.output(13, GPIO.HIGH)
            print("P LED On")
        sleep(1)
        #GPIO.cleanup()
    
    def led2(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(13, GPIO.OUT)
        if GPIO.output(13, GPIO.HIGH):
            GPIO.output(13, GPIO.LOW)
            print("P LED Off")
        sleep(1)
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
    
