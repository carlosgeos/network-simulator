# -*- coding: utf-8 -*-
from tkinter import LabelFrame, Label
from tkinter import StringVar, IntVar
from tkinter import NW, W, SW, E, NE, SE
from Common import Common

class NetworkInfo(LabelFrame, Common):
    """Label frame displaying basic information about the network loaded
    or created, like the number of people or their name.

    """
    def __init__(self, master):
        super().__init__(master, text="Network information")

        # Attributes to use (shared with NetworkFrame)
        self.node_name = StringVar()
        self.node_rumor = StringVar()
        self.network_size = IntVar()

        # Widgets inside the frame
        Label(self, text="Network size:").grid(row=0, column=0, sticky=NW)
        Label(self, text="Node name:").grid(row=1, column=0, sticky=W)
        Label(self, text="Node rumor:").grid(row=2, column=0, sticky=SW)

        Label(self, textvariable=self.network_size,
              anchor=E).grid(row=0, column=1, sticky=NE)

        Label(self, textvariable=self.node_name,
              anchor=E,
              width=15).grid(row=1, column=1, sticky=E)
        Label(self, textvariable=self.node_rumor,
              anchor=E).grid(row=2, column=1, sticky=SE)

        self.resizeable()
