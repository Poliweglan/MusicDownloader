import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror, showwarning, showinfo
from pytube import YouTube, Playlist
import os


class UrlLenZeroError(Exception):
    pass


class Combobox(ttk.Combobox):
    def __init__(self, parent):
        super().__init__(parent)
        self.__formatVar = tk.StringVar()
        self.__list = ['mp3', 'mp4', 'mkv']

        self.config(
            textvariable=self.__formatVar,
            values=self.__list,
            state='readonly',
            justify='center',
            width=5,
        )

        self.set(self.__list[0])

    def get(self):
        return self.__formatVar.get()

    def set(self, value):
        self.__formatVar.set(value)


class Checkbutton(ttk.Checkbutton):
    def __init__(self, parent):
        super().__init__(parent)
        self.__CheckbuttonVar = tk.BooleanVar()

        self.config(
            text='Playlist',
            variable=self.__CheckbuttonVar,
            onvalue=True,
            offvalue=False,
        )

        self.set(False)

    def get(self):
        return self.__CheckbuttonVar.get()

    def set(self, value):
        self.__CheckbuttonVar.set(value)


class Entry(ttk.Entry):
    def __init__(self, parent):
        super().__init__(parent)
        self.__text = tk.StringVar()
        self.config(
            textvariable=self.__text
        )

    def get(self):
        return self.__text.get()

    def set(self, value):
        self.__text.set(value)


class Button(ttk.Button):
    def __init__(self, parent, text, command):
        super().__init__(parent)
        self.config(
            command=command,
            text=text,
        )


class MainFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.format_file = 'MP3'
        self.playlist = False
        self.url = ''
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.config(
            padding=5
        )

        self.__create_widgets()

        self.combobox.bind('<<ComboboxSelected>>', self.__format_changed)

    def __download_single_file(self):
        # solo       https://www.youtube.com/watch?v=dQw4w9WgXcQ
        # solo       https://www.youtube.com/watch?v=eCyMy9ZStnM |||
        # playlst    https://www.youtube.com/watch?v=EPUVstUH22k&list=OLAK5uy_lgySQEqAIqdWtjzKZi3k1BfQgy4gaJSbw
        try:
            yt = YouTube(self.url)
            video = yt.streams.get_audio_only()
            title = self.__repair_name(video.title)
            file_name = title + f'.{self.format_file}'
            video.download(filename=file_name)
        except Exception as e:
            showerror(
                title="ANY ERROR!",
                message=str(e)
            )
        else:
            showinfo(
                title="Success!",
                message=f"Download song\n{file_name}\nCompleted successfully"
            )
            self.entry.set('')

    def __download_multi_file(self):
        try:
            yt = Playlist(self.url)
            pl_title = self.__repair_name(yt.title)
            check_folder = os.path.exists(pl_title)
            if not check_folder:
                os.mkdir(pl_title)
            for song in yt.videos:
                song_title = self.__repair_name(song.title) + f'.{self.format_file}'
                song.streams.get_audio_only().download(filename=f'{pl_title}\\{song_title}')
        except Exception as e:
            showerror(
                title="ANY ERROR!",
                message=str(e)
            )
        else:
            showinfo(
                title="Success!",
                message=f"Download playlist\n{pl_title}\nCompleted successfully"
            )
            self.entry.set('')

    def __repair_name(self, name):
        new_name = ''
        for letter in name:
            # \/:*?"<>|
            if letter not in ('\\', '//', ':', '*', '?', '"', '<', '>', '|'):
                new_name += letter
        return new_name

    def __format_changed(self, event):
        print("Combobox set:", self.combobox.get())

    def __cancel_button(self):
        self.parent.quit()

    def __download_button(self):
        try:
            self.format_file = self.combobox.get()
            self.playlist = self.checkbutton.get()
            self.url = self.entry.get()
            if len(self.url) == 0:
                raise UrlLenZeroError
        except UrlLenZeroError:
            showwarning(
                title='length url alert!',
                message='Incorrect or missing url!')
            self.url = ''
        else:
            if self.playlist:
                self.__download_multi_file()
            else:
                self.__download_single_file()

    def __create_widgets(self):
        self.combobox = Combobox(self)
        self.combobox.grid(row=0, column=0, sticky='NEWS')

        self.checkbutton = Checkbutton(self)
        self.checkbutton.grid(row=0, column=1, sticky='NS')

        self.entry = Entry(self)
        self.entry.grid(row=1, column=0, columnspan=2, sticky='NEWS', pady=3)

        self.button_cancel = Button(self, text='Cancel', command=self.__cancel_button)
        self.button_cancel.grid(row=2, column=0, sticky='NEWS')

        self.button_download = Button(self, text='Download', command=self.__download_button)
        self.button_download.grid(row=2, column=1, sticky='NEWS')


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('MusicDownloader')
        self.geometry('300x100')
        self.maxsize(500, 150)
        self.minsize(300, 100)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.mainframe = MainFrame(self)
        self.mainframe.grid(row=0, column=0, sticky='NEWS')


if __name__ == "__main__":
    app = App()
    app.mainloop()
