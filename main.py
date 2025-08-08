from pytubefix import YouTube as yt
from pytubefix import Playlist
from pytubefix.cli import on_progress
from tkinter import *
import tkinter as tk
import os, sys

#This is a simple GUI video downloader using pytube(fix) and tkinter

#GUI stuff
class MAIN:
    def __init__(self):
        pass
    def main(self):
        #Default download location, gets updated when user changes it
        self.ddl = "C:\\Downloads\\"

        self.root = Tk()
        self.root.geometry("800x800")
        self.frame = Frame(self.root)
        self.frame.pack()
        leftframe = Frame(self.root)
        leftframe.pack(side=LEFT)
        
        rightframe = Frame(self.root)
        rightframe.pack(side=RIGHT)
        
        #Title
        self.label = Label(self.frame, text = "oBoonkeros Video Downloader", font = ('Arial', 40))
        self.label.pack()

        self.setup()

    def setup(self):
        
        
        #Link input found at self.link
        self.linkLabel = Label(self.frame, text = 'Enter URL below', font = ('Arial', 20))
        self.linkLabel.pack()
        self.link = Entry (self.root, width = 25)
        self.link.pack(pady = 20)

        #Button to get the link
        self.button = Button (self.root, width = 20, text = 'get', command = self.get)
        self.button.pack()

        #Checkbox to select if the user wants to download a playlist or a single video
        self.playlist = tk.IntVar()
        self.checkbox = Checkbutton(self.root, text = 'Playlist', variable = self.playlist, onvalue=1, offvalue=0)
        self.checkbox.pack()

        self.root.title("Video Downloader")
        self.root.mainloop()

    def get(self):

        #System to remember the last download location
        try:
            self.file = open (os.getcwd() + '\\Directory.txt', 'r+')
            self.ddl = self.file.read()
            self.file.close()

        except:
            self.file = open (os.getcwd() + '\\Directory.txt', 'w')
            self.file.write(self.ddl)
            self.file.close()
        
        #Clearing the frame, probably not the best way to do it but it works
        self.linkLabel.pack_forget()
        self.button.pack_forget()
        self.link.pack_forget()
        self.checkbox.pack_forget()

        self.url = self.link.get()

        #No idea why it was done like this but I don't want to touch it, this part hasn't been touched in years
        # if the user wants to download a playlist or a single video it will display different information or let user know url is invalid
        if self.playlist.get()==0:
            try:
                self.ytu = yt(self.url)
                self.title = Label(self.frame, text = self.ytu.title + '\n' + str(self.ytu.length), font = ('Arial', 20))
                self.title.pack()
                self.button2 = Button(self.frame, text = 'Download', command = self.download)
                self.button2.pack()
                
                self.locLabel = Label(self.frame, text = 'Download Loacation:', font = ('Arial', 20))
                self.locLabel.pack()
                
                self.audio = tk.IntVar()
                self.checkforvideo = Checkbutton(self.root, text = 'Only Audio', variable = self.audio, onvalue=1, offvalue=0)
                self.checkforvideo.pack()
                
                self.location = Entry (self.root)
                self.location.insert(0, self.ddl)
                self.location.pack()
            except Exception as e:
                print (e)
                self.title = Label(self.frame, text = "Invalid URL", font = ('Arial', 30))
                self.title.pack()

        elif self.playlist.get()==1:
            try:
                self.ytu = Playlist(self.url)
                self.title = Label(self.frame, text = self.ytu.title + '\n' + str(len(self.ytu.video_urls)), font = ('Arial', 20))
                self.title.pack()
                self.button2 = Button(self.frame, text = 'Download', command = self.download)
                self.button2.pack()

                self.audio = tk.IntVar()
                self.checkforvideo = Checkbutton(self.root, text = 'Only Audio', variable = self.audio, onvalue=1, offvalue=0)
                self.checkforvideo.pack()

                self.locLabel = Label(self.frame, text = 'Download Loacation:', font = ('Arial', 20))
                self.locLabel.pack()
                
                
                
                self.location = Entry (self.root)
                self.location.insert(0, self.ddl)
                self.location.pack()
            except:
                self.title = Label(self.frame, text = "Invalid URL (Make sure playlist is public)", font = ('Arial', 30))
                self.title.pack()


        

        

        self.button3 = Button(self.frame, text = 'Back', command = self.back)
        self.button3.pack()


        
        
    #Actual download function via pytube(fix)
    def download(self):
        #self.ytu.streams.first().download(self.location.get())

        self.file = open(os.getcwd() + '\\Directory.txt', 'r+')
        self.file.truncate(0)
        self.file.write(self.location.get())
        self.file.close()
        #If not playlist download video if it is download all videos via for loop running through the playlist
        #Also downloads captions if available (functionality doesn't work on song lyrics as of now)
        if self.playlist.get()==0:
            url = self.url
            dir = self.location.get()

            #Added use_oauth and allow_oauth_cache to handle OAuth authentication due to some issues with Youtube API calling for age restrictions but this can be removed if not needed as it is annoying
            vid = yt(url, use_oauth=True, allow_oauth_cache=True, on_progress_callback=on_progress)

            #If only audio or not checked through the checkbox
            if self.audio.get()==1:
                ys = vid.streams.get_audio_only()
            else:
                ys = vid.streams.get_highest_resolution()
            ys.download(output_path=dir)

            title = vid.title
            try:
                caption = vid.captions['a.en']
                caption.download(output_path=dir)
                caption.save_captions(title + "_captions.txt")
            except:
                print("No captions available for " + title + ".") 
        
        else:
            url = self.url
            dir = self.location.get()

            pl = Playlist(url)
            for vid in pl.videos:
                if self.audio.get()==1:
                    ys = vid.streams.get_audio_only()
                else:
                    ys = vid.streams.get_highest_resolution()
                ys.download(output_path=dir)

                title = vid.title
                try:
                    caption = vid.captions['a.en']
                    caption.download(output_path=dir)
                    caption.save_captions(title + ".lrc")
                except:
                    print("No captions available for this video.")
            

#old code that used to work but doesn't anymore, left for reference as it might be useful in the future
        """try:
            if self.playlist.get()==0:
                try:    
                    if self.audio.get()==0:
                        highresvid = self.ytu.streams.get_highest_resolution()
                        highresvid.download(self.location.get())
                    elif self.audio.get()==1:
                        highresvid = self.ytu.streams.filter(only_audio=True).first()
                        highresvid.download(self.location.get())
                except:
                    print("ERROR: " +video.title)

            elif self.playlist.get()==1:
                for video in self.ytu.videos:
                    try:
                        if self.audio.get()==0:
                            highresvid = video.streams.first()
                            highresvid.download(self.location.get())
                        elif self.audio.get()==1:
                            highresvid = video.streams.get_audio_only()
                            highresvid.download(self.location.get())
                        print (video.title)
                    except:
                        print("ERROR: " + video.title)
                    
                    

        except Exception as e:
            print (e)
"""

    #Back function to go back to the main menu (must be a better way)
    def back(self):
        try:
            self.title.pack_forget()
            self.button2.pack_forget()
            self.locLabel.pack_forget()
            self.location.pack_forget()
            self.checkforvideo.pack_forget()
        finally:
            self.button3.pack_forget()
            self.setup()

        




main = MAIN()
main.main()