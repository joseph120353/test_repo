#! /usr/bin/python3


import subprocess
import optparse
import cv2
import numpy 
import time
import os


class Hide:
    def __init__(self):
        values = self.get_arguments()
        self.values = values 
        self.data = ""
        if self.values.hide:
            image = self.encode_image()
            encoded_image = self.hide_data(image)
            self.hidden_data(encoded_image)
        elif self.values.show:
            dt = self.start()
            print("Hidden data: " + dt)
            time.sleep(3)
            
            
    def get_arguments(self):
        parser = optparse.OptionParser()
        parser.add_option("-d","--hide",dest="hide",help="Choose this if you want to hide data(type --hide or -d + 'yes'")
        parser.add_option("-i","--image",dest="image",help="Pass me the image you want to hide data in it")
        parser.add_option("-s","--show",dest="show",help="Choose this is if you want to read a secret info in image(type -s or --show + yes")
        user_val = parser.parse_args()[0]
        if user_val.hide and not user_val.show and not user_val.image:
            parser.error("You have to choose --hide or --show + --image option(full_path of your image file),type --help for more info")
    
        elif not user_val.hide and not user_val.show and user_val.image:
            parser.error("Choose one from this options:--hide or --show ")
        elif not user_val.hide and not user_val.show and not user_val.image:
            parser.error("Type --help for more info")
        else:
            return user_val
    
    def encode_image(self):
        print("Type the data that you want to hide in the image..")
        user_data = input()
        if len(user_data) == 0:
                print("Zero data...")
                print("Exiting...")
                time.sleep(3)
                os.sys.exit(0)
        else:
            user_data = user_data + "////"
            self.data = user_data
            print("Starting process...")
            print("Image reading....")
            time.sleep(3)
            image = cv2.imread(self.values.image)
            print("Done...")
            print("Continue...")
            time.sleep(3)
            return image
    
    def to_binary(self,dt):
        if type(dt) == int or type(dt) == numpy.uint8:
            return format(dt,"08b")       
        if type(dt) == str:
            return [format(ord(i),"08b") for i in dt]
        if type(dt) == bytes or type(dt) == numpy.ndarray:
            return [format(i,"08b") for i in dt]
    
    def hide_data(self,image):
        print("Starting process to hide the data in the last significant bit..")
        time.sleep(2)
        width = image.shape[0]
        height = image.shape[1]
        image_size = width * height * 3//8
        encoded_data = self.to_binary(self.data)
        if image_size < len(encoded_data):
            print("Error size of picture too small for this data...")
            print("Exiting...")
            time.sleep(2)
            os.sys.exit(0)
        else:
            pointer = 0
            for values in image:
                for pixel in values:      
                    red,green,blue = self.to_binary(pixel)
                    if pointer < len(encoded_data):
                        pixel[0] = int(red[:-1] + encoded_data[pointer])
                        pointer = pointer + 1
                    if pointer < len(encoded_data):
                        pixel[1] = int(green[:-1] + encoded_data[pointer])
                        pointer = pointer + 1
                    if pointer <len(encoded_data):
                        pixel[2] = int(blue[:-1] + encoded_data[pointer])
                        pointer = pointer + 1
                    if pointer >= len(encoded_data):
                        break
            return image

    def hidden_data(self,image):
        print("Starting the process to save your image..")
        print("Type the file in which you want to save the image(png extension))")
        filename = input()
        extension = filename.split(".")[-1]
        extension = "." + extension
    
        
        result = cv2.imwrite(filename,image)
        
        if result:
            print("Image saved!!")
            time.sleep(2)
            os.sys.exit(0)
        else:
            print("Error at saving the image")
            print("Exiting...")
            time.sleep(2)
            os.sys.exit(0)
    
    def start(self):
        print("Starting process...")
        print("Please wait..")
        time.sleep(2)
        print("Type the path of the encoded image...")
        path  = input()
        if os.path.exists(path):
            print("Ok lets continue...")
            im = cv2.imread(path)
            p = 0
            extracted_dt = ""
            for i in im:
                for px in i:
                    red,green,blue = self.to_binary(px)
                    extracted_dt = extracted_dt + red[-1]
                    extracted_dt = extracted_dt + green[-1]
                    extracted_dt = extracted_dt + blue[-1]
        
            data = [extracted_dt[x:x+8] for x in range(0,len(extracted_dt),8)]
            info = ""            
            for i in data:
                info = info + chr(int(i,base=2))
                if i[-4:] == "////":
                    break
            return info[:-4]
        else:
            print("Path doesnt exist...")
            print("Exiting...")
            time.sleep(2)
            os.sys.exit(0)
        
start = Hide()



        

     
    
    
       
        
    
