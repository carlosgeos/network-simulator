# -*- coding: utf-8 -*-
"""# TOD
"""

from tkinter import *
from Common import Common

class SimuInfo(LabelFrame, Common):
    def __init__(self, master):
        super().__init__(master, text="Simulator information")

        self.stage_number = IntVar()
        self.stage_number.set(0)
        self.still_fool = IntVar()
        self.still_fool.set(0)


        Label(self, text="Stage number:").grid(row=0, column=0, sticky=NW)
        Label(self, text="Still don't know:").grid(row=1, column=0, sticky=SW)

        Label(self, textvariable=self.stage_number,
              anchor=E).grid(row=0, column=1, sticky=NE)
        Label(self, textvariable=self.still_fool,
              anchor=E).grid(row=1, column=1, sticky=SE)

        self.resizeable()
