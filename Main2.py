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
import json
import requests


moto_url = 'http://192.168.40.120:2001'

p = PiXtendV2L()

p.gpio0_ctrl = p.GPIO_INPUT

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



step_count = 91  ##((Steps for 0.025Micrometers))No.of steps for one MicroMeter... number of step to run  change this to change where it stops (72727 steps for 25mm) (72.727 steps for 25 micrometers)bd
delay = 0.001

GPIO.output(21, GPIO.HIGH)


# create logger
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
        
        
        self.GPIOClean = Button(self.frame)
        self.GPIOClean["text"] = "Clean GPIO"
        self.GPIOClean["bg"] = "gray"
        self.GPIOClean["fg"] = "green"
        self.GPIOClean["command"] = self.GPIO
        self.GPIOClean.place(x=5, y=95, width=100, height=20)

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
        self.clockwise["text"] = "25 microm+"
        self.clockwise["command"] = self.stepper_25cw
        self.clockwise.place(x=65, y=30, width=100, height=20)   
        
        self.anticlockwise = Button(self.frame)
        self.anticlockwise["text"] = "25 microm-"
        self.anticlockwise["command"] = self.stepper_25ccw
        self.anticlockwise.place(x=65, y=60, width=100, height=20)
        
        self.clockwise = Button(self.frame)
        self.clockwise["text"] = "50 microm+"
        #self.clockwise["bg"] = "green"
        self.clockwise["command"] = self.stepper_50cw
        self.clockwise.place(x=165, y=30, width=100, height=20)  
        
        self.anticlockwise = Button(self.frame)
        self.anticlockwise["text"] = "50 microm-"
        self.anticlockwise["command"] = self.stepper_50ccw
        self.anticlockwise.place(x=165, y=60, width=100, height=20)

        self.stepper = Label(self.frame)
        self.stepper["text"] = "Stepper Z axis"
        self.stepper.place(x=65, y=5, width=100, height=20)
        
        self.stopping = Button(self.frame)
        self.stopping["text"] = "Aboart"
        self.stopping["command"] = self.stop
        self.stopping.place(x=165, y=5, width=100, height=20)
        
        self.printing = Button(self.frame)
        self.printing["text"] = "Print"
        self.printing["command"] = self.Printprocess
        self.printing.place(x=180, y=180, width=100, height=20)
        
        self.work = Button(self.frame)
        self.work["text"] = "Z-axis Home"
        self.work["command"] = self.stepperhome
        self.work.place(x=200, y=200, width=100, height=20)
        
        self.ma = Button(self.frame)
        self.ma["text"] = "Yo"
        self.ma["command"] = self.motoHome
        self.ma.place(x=220, y=220)
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
        
#step_count has been given in the initial steps which are for the calculation of 25micrometres
############ Note that GPIO.cleanup() has seperate button to clean the GPIO at the end of program or after the usage #####################
    def stepperhome(self):
        delay = 0.001
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(21, GPIO.OUT)
        GPIO.setup(20,GPIO.OUT)
        print("Homing process")
        #if the motor is at the top end switch resting
        if (GPIO.input(19) == False):
            GPIO.output(21, GPIO.HIGH)
            #range is no . of steps to reach the home(reference point)
            for x in range(24600):
                GPIO.output(20, GPIO.HIGH)
                time.sleep(delay)
                GPIO.output(20, GPIO.LOW)
                time.sleep(delay)
                print("Going towards HOME")
        #if the motor is resting at the down end switch
        if (p.gpio0 == 0):
            while True:
                GPIO.output(21, GPIO.LOW)
                GPIO.output(20, GPIO.HIGH)
                time.sleep(delay)
                GPIO.output(20, GPIO.LOW)
                time.sleep(delay)
                print("homing towards top")
                #motor should run until the top end switch and then moving to home reference point
                if (GPIO.input(19) == False):
                    GPIO.output(21, GPIO.HIGH)
                    for x in range(24600):
                        GPIO.output(20, GPIO.HIGH)
                        time.sleep(delay)
                        GPIO.output(20, GPIO.LOW)
                        time.sleep(delay)
                        print("Going towards HOME")
                    break
                    print("homed")
        #If the motor placed niether at the top end nor the bottom end
        else:
            if (p.gpio0 == 1) and (GPIO.input(19) == True):
                GPIO.output(21, GPIO.LOW)
                while True:
                    GPIO.output(20, GPIO.HIGH)
                    time.sleep(delay)
                    print("Going top")
                    GPIO.output(20, GPIO.LOW)
                    time.sleep(delay)
                    if (GPIO.input(19) == False):
                        GPIO.output(21, GPIO.HIGH)
                        for x in range(24640):
                            GPIO.output(20, GPIO.HIGH)
                            time.sleep(delay)
                            GPIO.output(20, GPIO.LOW)
                            time.sleep(delay)
                            print("Going towards HOME")
                        break
                        print("homed")
        
        self.ret = self.request(moto_url, 'motor_enable')
        print(self.ret)
        
        self.ret = self.request(moto_url, 'home')
        print(self.ret)
        time.sleep(3)
    """
    def man(self):
        delay = 0.001
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(21, GPIO.OUT)
        GPIO.setup(20,GPIO.OUT)
        print("Homing process")
        if (GPIO.input(19) == False):
            GPIO.output(21, GPIO.HIGH)
            for x in range(24669):
                GPIO.output(20, GPIO.HIGH)
                time.sleep(delay)
                GPIO.output(20, GPIO.LOW)
                time.sleep(delay)
                print("Going towards HOME")
        print("finish")
    """
    #Stepper movement of 25micrometers(towards down)
    def stepper_25cw(self):
        delay = 0.00025
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(21, GPIO.OUT)
        GPIO.setup(20, GPIO.OUT)
        GPIO.output(21, GPIO.HIGH)
        print (" Drive CW ", 100*step_count ,"steps")
        for x in range(100*step_count):
            GPIO.output(20, GPIO.HIGH)
            sleep(delay)
            GPIO.output(20, GPIO.LOW)
            sleep(delay)
            if p.gpio0 == 0:
                break
            print(x)
        print("Stop")
        sleep(delay)
    #stepper movement of 25 micro meters anti-clockwise(top)
    def stepper_25ccw(self):
        delay = 0.00025
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(21, GPIO.OUT)
        GPIO.setup(20, GPIO.OUT)
        print (" Drive CCW ", 100*step_count ,"steps")
        GPIO.output(21, GPIO.LOW)
        for x in range(100*step_count):
            GPIO.output(20, GPIO.HIGH)
            sleep(delay)
            GPIO.output(20, GPIO.LOW)
            sleep(delay)
            if (GPIO.input(19) == False):
                break
            print(x)
        print("Homed")
        sleep(delay)
        # end of program
        print ("End program")
    
    def stepper_50cw(self):
        delay = 0.001
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(21, GPIO.OUT)
        GPIO.setup(20, GPIO.OUT)
        GPIO.output(21, GPIO.HIGH)
        print (" Drive CW ", 200*step_count ,"steps")
        for x in range(200*step_count):
            GPIO.output(20, GPIO.HIGH)
            sleep(delay)
            GPIO.output(20, GPIO.LOW)
            sleep(delay)
            if p.gpio0 == 0:
                break
        print("Stop")
        sleep(delay)

    def stepper_50ccw(self):
        delay = 0.001
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(21, GPIO.OUT)
        GPIO.setup(20, GPIO.OUT)
        print (" Drive CCW ", 200*step_count ,"steps")
        GPIO.output(21, GPIO.LOW)
        for x in range(200*step_count):
            GPIO.output(20, GPIO.HIGH)
            sleep(delay)
            GPIO.output(20, GPIO.LOW)
            sleep(delay)
            if (GPIO.input(19) == False):
                break
        print("Homed")
        sleep(delay)
        # end of program
        print ("End program")
    
    def request(self, url, method, params={}, timeout=3):
        headers = {'content-type': 'application/json'}
        jsonid = 1

        payload = {
            "method": method,
            "params": params,
            "jsonrpc": "2.0",
            "id": jsonid
        }

        payload = json.dumps(payload).encode()

        try:
            r = requests.post(url,
                            data=payload,
                            headers=headers,
                            timeout=timeout)
        except Exception as e:
            print('error in json rpc request', e)
            return False

        return r.json()
        
    def motoHome(self):
        self.ret = self.request(moto_url, 'motor_enable')
        print(self.ret)
        
        self.ret = self.request(moto_url, 'home')
        print(self.ret)

    def stop(self):#Stop scanning by setting the global flag to False.
        global running
        running = False

    #To turn the Projector on with the Asic_ready
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
        print("end")
        
    #To turn off the projector
    def off(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(26, GPIO.OUT)
        GPIO.setup(16, GPIO.IN)
        GPIO.setup(12, GPIO.IN)
        GPIO.output(26,GPIO.LOW)
        GPIO.input(12) == 0
        GPIO.input(16) == 0
        print("Projector off")
        sleep(1)

    #To turn the projector LED on
    def led1(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(26, GPIO.OUT)
        GPIO.setup(13, GPIO.OUT)
        GPIO.output(13, GPIO.HIGH)
        print("P LED On")
        sleep(1)

    #To turn the projector LED off
    def led2(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(26, GPIO.OUT)
        GPIO.setup(13, GPIO.OUT)
        GPIO.output(13, GPIO.LOW)
        print("P LED Off")
        sleep(1)

    
    #Open and load the image file that we wanted to print(Select a folder)
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
        self.root.destroy()
        exit()
    
    def GPIO(self):#GPIO cleanup has to do manually after the end of program.
        GPIO.cleanup()
        print("GPIO.clean")

    def Printprocess(self):
        if GPIO.output(26, GPIO.HIGH):        # Rakel runter (Endschalter)
            os.system('sudo fbi -a /dev/fb0 -T 2 -1 /home/pi/Pixtenddemo/bilder/0.png')
            GPIO.output(13, GPIO.LOW)
            sleep(10)
            GPIO.output(13, GPIO.HIGH)
            print("something")
            for i in range (99):
                print(i)
                for j in range (500):
                    time = 0.00125
                    GPIO.setmode(GPIO.BCM)
                    GPIO.setup(21, GPIO.OUT)
                    GPIO.setup(20, GPIO.OUT)
                    GPIO.output(21, GPIO.LOW)
                    GPIO.output(20, GPIO.HIGH)
                    sleep(delay)
                    GPIO.output(20, GPIO.LOW)
                else:
                    os.system('sudo fbi -a /dev/fb0 -T 2 -1 /home/pi/Pixtenddemo/bilder/%s.png' % (str(i)))
                    print("else part")
                    for k in range (480):
                        
                        time = 0.00125
                        GPIO.setmode(GPIO.BCM)
                        GPIO.setup(21, GPIO.OUT)
                        GPIO.setup(20, GPIO.OUT)
                        GPIO.output(21, GPIO.HIGH)
                        GPIO.output(20, GPIO.HIGH)
                        sleep(delay)
                        GPIO.output(20, GPIO.LOW)
                        
                    GPIO.output(13, GPIO.LOW)
                    sleep(1.25)
                    GPIO.output(13, GPIO.HIGH)
            #gehe zurück vor Endschalter
            
            while (True):
                GPIO.setup(21, GPIO.OUT)
                GPIO.setup(20, GPIO.OUT)
                GPIO.output(21, GPIO.LOW)
                GPIO.output(20, GPIO.HIGH)
                sleep(delay)
                GPIO.output(20, GPIO.LOW)
                if (GPIO.input(19) == False):
                    break
                
            GPIO.cleanup()


if __name__ == "__main__":
    Main()
    
