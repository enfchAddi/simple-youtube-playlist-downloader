from pytube import *
from threading import Thread
import tkinter as tk
from tkinter import messagebox
from moviepy.editor import *
import os

def download_video(video, index, update_callback, format_choice):
    update_callback(index, 'yellow')  # mark as downloading (yellow)
    if format_choice == "audio":
        video.streams.get_audio_only().download()
        update_callback(index, 'green')  # mark as downloaded (green)
    else:  # video download
        video.streams.get_highest_resolution().download()
        update_callback(index, 'green')  # mark as downloaded (green)

def update_listbox_color(index, color):
    # safe way to update gui from another thread
    def task():
        listbox.itemconfig(index, bg=color)
    listbox.after(0, task)

def mp3convert(stream, path):
    file = AudioFileClip(path)
    file.write_audiofile(stream.title + ".mp3", logger=None )
    file.close()
    os.remove(path)

def add_item():
    item = entry.get()
    format_choice = format_var.get()
    
    if item:
        entry.delete(0, tk.END)
        try:
            if "playlist" in item:
                pl = Playlist(item)
                for i, video in enumerate(pl.videos):
                    listbox.insert(tk.END, video.title)
                    listbox.itemconfig(i, bg='red')  # initial color before download
                    if format_choice == "audio":
                        video.register_on_complete_callback(mp3convert)
                    # start download in a separate thread
                    Thread(target=download_video, args=(video, i, update_listbox_color, format_choice)).start()
            else:
                video = YouTube(item)
                listbox.insert(tk.END, video.title)
                listbox.itemconfig(0, bg='red')  # initial color before download
                if format_choice == "audio":
                    video.register_on_complete_callback(mp3convert)
                # start download in a separate thread
                Thread(target=download_video, args=(video, 0, update_listbox_color, format_choice)).start()
        except Exception as e:
            messagebox.showerror("", f"Error: {str(e)}")

def on_entry_click(event):
    if entry.get() == "Playlist or Video URL":
        entry.delete(0, "end")  # delete all the text in the entry
        entry.insert(0, '')  # insert blank for user input
        entry.config(fg='black')

def on_focusout(event):
    if entry.get() == '':
        entry.insert(0, 'Playlist or Video URL')
        entry.config(fg='grey')


# main window creation
root = tk.Tk()
root.title("Youtube Downloader")

root.resizable(False, False)

frame = tk.Frame(root)
frame.pack(pady=20)

scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox = tk.Listbox(frame, width=50, height=15, yscrollcommand=scrollbar.set)
listbox.pack(side=tk.LEFT)

scrollbar.config(command=listbox.yview)

entry = tk.Entry(root, width=53)
entry.pack(pady=10)
entry.insert(0, "Playlist or Video URL")
entry.bind('<FocusIn>', on_entry_click)
entry.bind('<FocusOut>', on_focusout)
entry.pack()

format_var = tk.StringVar(root)
format_var.set("audio")  # default value
format_options = ["audio", "video"]
format_menu = tk.OptionMenu(root, format_var, *format_options)
format_menu.pack(pady=10)

add_button = tk.Button(root, text="Download", command=add_item)
add_button.pack()

root.mainloop()
