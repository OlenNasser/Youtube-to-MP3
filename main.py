from pytube import YouTube as yt
from tkinter import *
import tkinter as tk
import os, sys

class MAIN:
    def __init__(self):
        pass
    def main(self):
        self.root = Tk()
        self.root.geometry("800x800")
        self.frame = Frame(self.root)
        self.frame.pack()
        

        leftframe = Frame(self.root)
        leftframe.pack(side=LEFT)
        
        rightframe = Frame(self.root)
        rightframe.pack(side=RIGHT)
        
        self.label = Label(self.frame, text = "oBoonkeros Video Downloader", font = ('Arial', 40))
        self.label.pack()

        self.linkLabel = Label(self.frame, text = 'Enter URL below', font = ('Arial', 20))
        self.linkLabel.pack()
        self.link = Entry (self.root, width = 25)
        self.link.pack(pady = 20)

        self.button = Button (self.root, width = 20, text = 'get', command = self.get)
        self.button.pack()

        self.root.title("Video Downloader")
        self.root.mainloop()

    def get(self):
        
        self.linkLabel.pack_forget()
        self.button.pack_forget()
        self.link.pack_forget()

        self.url = self.link.get()
        self.ytu = yt(self.url)

        self.title = Label(self.frame, text = self.ytu.title + '\n' + str(self.ytu.length), font = ('Arial', 20)).pack()

        self.button2 = Button(self.frame, text = 'Download', command = self.download).pack()
        
        self.locLabel = Label(self.frame, text = 'Download Loacation:', font = ('Arial', 20))
        self.locLabel.pack()
        
        
        
        self.location = Entry (self.root)
        self.location.pack()


        
        

    def download(self):
        self.ytu.streams.first().download(self.location.get())

        




main = MAIN()
main.main()