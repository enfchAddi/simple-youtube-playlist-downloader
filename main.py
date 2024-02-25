from pytube import *
from threading import Thread
import tkinter as tk
from tkinter import *
from tkinter import messagebox


def download_video(video, index, update_callback):
    update_callback(index, 'yellow')  # mark as downloading (yellow)
    video.streams.get_audio_only().download()
    update_callback(index, 'green')  # mark as downloaded (green)

def update_listbox_color(index, color):
    # safe way to update gui from another thread
    def task():
        listbox.itemconfig(index, bg=color)
    listbox.after(0, task)

def add_item():
    item = entry.get()
    if item:
        entry.delete(0, tk.END)
        try:
            pl = Playlist(item)
        
            messagebox.showinfo("Collecting...", "Collecting Videos and starting download, this might take a while. Click OK to progress")
            for i, video in enumerate(pl.videos):
                listbox.insert(tk.END, video.title)
                listbox.itemconfig(i, bg='red')  # initial color before download
                # start download in a separate thread
                Thread(target=download_video, args=(video, i, update_listbox_color)).start()
        except Exception:
            messagebox.showerror("", "Most likely bad URL")

def on_entry_click(event):
    if entry.get() =="Playlist URL":
        entry.delete(0, "end")  # delete all the text in the entry
        entry.insert(0, '')  # insert blank for user input
        entry.config(fg='black')

def on_focusout(event):
    
    if entry.get() == '':
        entry.insert(0, 'Playlist URL')
        entry.config(fg='grey')


# main window creation
root = tk.Tk()
root.title("Youtube Playlist Downloader")

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
entry.insert(0, "Playlist URL")
entry.bind('<FocusIn>', on_entry_click)
entry.bind('<FocusOut>', on_focusout)
entry.pack()

add_button = tk.Button(root, text="Download all", command=add_item)
add_button.pack()

root.mainloop()
