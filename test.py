import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
import time
#import tensorflow
#import keras
import tkinter as tk
from tkinter import *
import PIL
from PIL import ImageTk

class Tk_Manage(tk.Tk):
     def __init__(self, *args, **kwargs):     
              tk.Tk.__init__(self, *args, **kwargs)
              container = tk.Frame(self)
              container.pack(side="top", fill="both", expand = True)
              container.grid_rowconfigure(0, weight=1)
              container.grid_columnconfigure(0, weight=1)
              self.frames = {}
              for F in (StartPage, TextToSign, SignToText):
                     frame = F(container, self)
                     self.frames[F] = frame
                     frame.grid(row=0, column=0, sticky="nsew")
              self.show_frame(StartPage)

     def show_frame(self, cont):
             frame = self.frames[cont]
             frame.tkraise()

class StartPage(tk.Frame):

       def __init__(self, parent, controller):
              tk.Frame.__init__(self,parent)
              label = tk.Label(self, text="TWO WAY SIGN LANGUAGE TRANSLATOR", font=("Verdana", 14))
              label.pack(pady=30,padx=30)
              button = tk.Button(self, text="TEXT TO SIGN",font=("Verdana", 10),command=lambda: controller.show_frame(TextToSign))
              button.place(x=310,y=80)
              #button.pack(padx=10,pady=10)
              button2 = tk.Button(self, text="SIGN TO TEXT",font=("Verdana", 10),command=lambda: controller.show_frame(SignToText))
              button2.place(x=310,y=120)
              #button2.pack(padx=10,pady=10)
              load = PIL.Image.open("image.png")
              load = load.resize((590, 420))
              render = ImageTk.PhotoImage(load)
              img = Label(self, image=render)
              img.image = render
              img.place(x=100, y=180) 

class TextToSign(tk.Frame):
            def __init__(self, parent, controller):
                cnt=0
                gif_frames=[]
                inputtxt=None
                tk.Frame.__init__(self, parent)
                label = tk.Label(self, text="TEXT TO SIGN", font=("Verdana", 12))
                label.pack(pady=10,padx=10)
                gif_box = tk.Label(self)
              
                button1 = tk.Button(self, text="BACK TO HOME",command=lambda: controller.show_frame(StartPage))
                button1.pack(padx=8,pady=8)
                button2 = tk.Button(self, text="SIGN TO TEXT",command=lambda: controller.show_frame(SignToText))
                button2.pack(padx=8,pady=8)

            '''def gif_stream():
                     global cnt
                     global gif_frames
                     if(cnt==len(gif_frames)):
                            return
                     img = gif_frames[cnt]
                     cnt+=1
                     imgtk = ImageTk.PhotoImage(image=img)
                     gif_box.imgtk = imgtk
                     gif_box.configure(image=imgtk)
                     gif_box.after(50, gif_stream)

            def Take_input():
                     INPUT = inputtxt.get("1.0", "end-1c")
                     print(INPUT)
                     global gif_frames
                     gif_frames=func(INPUT)
                     global cnt
                     cnt=0
                     gif_stream()
                     gif_box.place(x=400,y=140)

            l = tk.Label(self,text = "ENTER TEXT:")
            #l1 = tk.Label(self,text = "OR")
            inputtxt = tk.Text(self, height = 4,width = 25)
            #voice_button= tk.Button(self,height = 2,width = 20, text="Record Voice",command=lambda: hear_voice())
            #voice_button.place(x=50,y=180)
            l.place(x=100, y=200)
            #l1.place(x=115, y=230)
            inputtxt.place(x=100, y=240)
            Display = tk.Button(self, height = 2,width = 20,text ="CONVERT",command = lambda:Take_input())
            Display.place(x=100,y=320)'''

class SignToText(tk.Frame):
    def __init__(self, parent, controller):
              tk.Frame.__init__(self, parent)
              label = tk.Label(self, text="SIGN TO TEXT", font=("Verdana", 12))
              label.pack(pady=10,padx=10)
              button1 = tk.Button(self, text="BACK TO HOME",command=lambda: controller.show_frame(StartPage))
              button1.pack(padx=5,pady=5)
              button2 = tk.Button(self, text="TEXT TO SIGN",command=lambda: controller.show_frame(TextToSign))
              button2.pack(padx=5,pady=5)
              disp_txt = tk.Text(self, height = 4,width = 25)

              def start_video():
                 cap = cv2.VideoCapture(0)
                 detector = HandDetector(maxHands=1)
                 classifier = Classifier("model/keras_model.h5", "model/labels.txt")

                 offset = 20
                 imgSize = 300

                 counter = 0

                 labels = ['A', 'B', 'C', 'D', 'E','F','G','H','I','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y']
                 while True:
                    success, img = cap.read()
                    imgOutput = img.copy()
                    hands, img = detector.findHands(img)
                    if hands:
                        hand = hands[0]
                        x, y, w, h = hand['bbox']


                        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8)*255
                        imgCrop = img[y - offset:y + h + offset, x - offset: x+ w + offset]

                        imgCropShape = imgCrop.shape

                        aspectRatio = h/w

                        if aspectRatio > 1:
                            k = imgSize / h
                            wCal = math.ceil(k * w)
                            imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                            imgResizeShape = imgResize.shape
                            wGap = math.ceil((imgSize - wCal) / 2)
                            imgWhite[:, wGap:wCal + wGap] = imgResize
                            prediction , index = classifier.getPrediction(imgWhite, draw = False)
                            print(prediction, index)

                        else:
                            k = imgSize / w
                            hCal = math.ceil(k * h)
                            imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                            imgResizeShape = imgResize.shape
                            hGap = math.ceil((imgSize - hCal) / 2)
                            imgWhite[hGap:hCal + hGap,:] = imgResize
                            prediction , index = classifier.getPrediction(imgWhite, draw = False)

                        cv2.putText(imgOutput, labels[index], (x, y-20), cv2.FONT_HERSHEY_COMPLEX,2,(255,0,255),2)
                        cv2.rectangle(imgOutput, (x - offset, y - offset), (x + w + offset, y + h + offset), (255,0,255), 4)


                        #cv2.imshow("ImageCrop", imgCrop)
                        #cv2.imshow("ImageWhite", imgWhite)

                    cv2.imshow("Image", imgOutput)
                    cv2.waitKey(1)
              start_vid = tk.Button(self,height = 2,width = 20, text="START VIDEO",command=lambda: start_video())
              start_vid.pack(padx=5,pady=5)

app = Tk_Manage()
app.geometry("800x750")
app.mainloop()