# -*- coding: utf-8 -*-
import tkinter as tk


class TopMenu(tk.Menu):
    """This class contains the Tk Window Menu, which can be seen at the
    top bar of the window.

    """
    def __init__(self, master):
        super().__init__(master)
        master.config(menu=self)
        self.__create_menu(master)

    def __create_menu(self, master):
        filemenu = tk.Menu(self)
        self.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Load network file", command=master.load_file)
        filemenu.add_command(label="Save", command=master.save_file)
        filemenu.add_command(label="Exit", command=master.destroy)
        helpmenu = tk.Menu(self)
        self.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About", command=about_app)


def about_app():
    """Shows about information"""
    tk.messagebox.showinfo("About",
                           "{}\n{}\n{}".format("YAWN",
                                               "Yet Another Network Simulator",
                                               "Carlos Requena López - 2015"))
