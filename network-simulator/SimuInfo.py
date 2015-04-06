# -*- coding: utf-8 -*-
import tkinter as tk
from Common import Common


class SimuInfo(tk.LabelFrame, Common):
    INIT = 0

    def __init__(self, master):
        super().__init__(master, text="Simulator information")

        self.stage_number = tk.IntVar()
        self.stage_number.set(self.INIT)
        self.rumor_spread = tk.IntVar()
        self.rumor_spread.set(self.INIT)
        self.still_fool = tk.IntVar()
        self.still_fool.set(self.INIT)

        tk.Label(self, text="Stage number:").grid(row=0, column=0,
                                                  sticky=tk.NW)
        tk.Label(self, text="Rumor spread (last stage):").grid(row=1, column=0,
                                                               sticky=tk.W)
        tk.Label(self, text="Still don't know:").grid(row=2, column=0,
                                                      sticky=tk.SW)

        tk.Label(self, textvariable=self.stage_number,
                 anchor=tk.E).grid(row=0, column=1, sticky=tk.NE)
        tk.Label(self, textvariable=self.rumor_spread,
                 anchor=tk.E).grid(row=1, column=1, sticky=tk.E)
        tk.Label(self, textvariable=self.still_fool,
                 anchor=tk.E).grid(row=2, column=1, sticky=tk.SE)

        self.resizeable()
