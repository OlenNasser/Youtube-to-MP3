from pytubefix import YouTube as yt
from pytubefix import Playlist
from pytubefix.cli import on_progress
from tkinter import *
import tkinter as tk
import os, sys

#This is a simple GUI video downloader using pytube(fix) and tkinter

class MAIN:
    def __init__(self):
        pass
    def main_c(self):
        self.ddl = 'c:\\Downloads' 
        print("Welcome to oBoonkero's Video Downloader!\n")
        print("Press p or s to select if you want to download a playlist or a single video: ")
        temp = input() #get input from user
        if (temp.lower() == 'p'):
            self.playlist = 1
        else:
            self.playlist = 0

        print("Enter the URL of the video/playlist you want to download: ")
        self.url = input()
        self.get()
        print("Would you like audio only? (y/n): ")
        if (input().lower() == 'y'):
            self.audio = 1
        else:
            self.audio = 0
        print("Enter the download location (current is " + self.ddl + "press enter to keep): ")
        loc = input()
        if loc != '':
            self.ddl = loc
        self.download()
        print("Download complete, press enter to restart or ctrl+c to exit")
        input()
        self.main_c()


    
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
        

        #No idea why it was done like this but I don't want to touch it, this part hasn't been touched in years
        # if the user wants to download a playlist or a single video it will display different information or let user know url is invalid
        if self.playlist==0:
            try:
                self.ytu = yt(self.url)
                print(self.ytu.title + '\n' + str(self.ytu.length))
                
                
            except Exception as e:
                print (e)
                print("\nInvalid URL\n")
                self.main_c()

        elif self.playlist==1:
            try:
                self.ytu = Playlist(self.url)
                print(self.ytu.title + '\n' + str(len(self.ytu.video_urls)) + " videos in playlist")
                
            except:
                print("\nInvalid URL (Make sure playlist is public)\n")
                self.main_c()


        



        
        
    #Actual download function via pytube(fix)
    def download(self):
        #self.ytu.streams.first().download(self.location.get())

        self.file = open(os.getcwd() + '\\Directory.txt', 'r+')
        self.file.truncate(0)
        self.file.write(self.ddl)
        self.file.close()
        #If not playlist download video if it is download all videos via for loop running through the playlist
        #Also downloads captions if available (functionality doesn't work on song lyrics as of now)
        if self.playlist==0:
            url = self.url
            dir = self.location()

            #Added use_oauth and allow_oauth_cache to handle OAuth authentication due to some issues with Youtube API calling for age restrictions but this can be removed if not needed as it is annoying
            vid = yt(url, use_oauth=True, allow_oauth_cache=True, on_progress_callback=on_progress)

            #If only audio or not checked through the checkbox
            if self.audio==1:
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
                pass
        else:
            url = self.url
            dir = self.ddl

            pl = Playlist(url)
            downloaded = 0
            for vid in pl.videos:
                #little progress bar I thought was cool
                progress = "Downloading("
                progress += "." * downloaded
                progress += " " * (len(pl.video_urls) - downloaded - 1)
                progress += f") {downloaded+1}/{len(pl.video_urls)} {vid.title}"
                print(progress, end='\r', flush=True)
                downloaded += 1

                if self.audio==1:
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
                    pass





main = MAIN()
main.main_c()
