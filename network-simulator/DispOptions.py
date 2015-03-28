# -*- coding: utf-8 -*-
import tkinter as tk
from Common import Common


class DispOptions(tk.LabelFrame, Common):
    LAYOUT = ("circular", "random")
    """All the variables and modification options for the network
    simulator.

    """
    def __init__(self, master):
        super().__init__(master, text="Display Options")

        self.layout = tk.StringVar()
        self.layout.set(self.LAYOUT[0])

        self.node_size = tk.IntVar()
        self.node_size.set(20)

        self.link_thickness = tk.IntVar()
        self.link_thickness.set(2)

        self.delay = tk.DoubleVar()
        self.delay.set(0.5)

        tk.Label(self, text="Network Layout").grid(row=0, column=0,
                                                   columnspan=3)
        tk.OptionMenu(self, self.layout, *self.LAYOUT,
                      command=master.update_app).grid(row=1, column=0,
                                                      columnspan=3, pady=8)

        tk.Scale(self,
                 from_=1, to=50, command=master.update_app,
                 label="Person size",
                 variable=self.node_size).grid(row=2, column=0)
        tk.Scale(self,
                 from_=1, to=10, command=master.update_app,
                 label="Link thickness",
                 variable=self.link_thickness).grid(row=2, column=1)
        tk.Scale(self, from_=0, to=3, resolution=0.1,
                 label="Delay",
                 variable=self.delay).grid(row=2, column=2)

        self.resizeable()
