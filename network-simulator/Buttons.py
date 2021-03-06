# -*- coding: utf-8 -*-
import tkinter as tk
from Common import Common


class Buttons(tk.LabelFrame, Common):
    """This buttons class implements:

    - Add friend: adds a new person to the network
    - Add network: adds several people at once
    - Propagate: run the simulator 1 unit of time
    - Run: run the simulator n times
    - Reset: goes back to original state

    """
    def __init__(self, master):
        super().__init__(master, text="Choose an action")

        tk.Button(self, text="Add friend",
                  command=master.add_friend).pack()
        tk.Button(self, text="Add network",
                  command=master.add_network).pack()
        tk.Button(self, text="Run simulation",
                  command=master.run).pack()
        tk.Button(self, text="Propagate",
                  command=master.propagate).pack()
        tk.Button(self, text="Reset",
                  command=master.reset_all).pack()

        self.resizeable()
