# -*- coding: utf-8 -*-
from tkinter import Button
from tkinter import LabelFrame
from Common import Common

class Buttons(LabelFrame, Common):
    """This buttons class implements:

    - Propagate: run the simulator 1 unit of time
    - Run: run the simulator n times
    - Add friend: adds a new person to the network
    - Reset: goes back to original state


    These are the options available to perform on the network

    """
    def __init__(self, master):
        super().__init__(master, text="Choose an action")

        Button(self, text="Add friend",
               command=master.add_friend).pack()
        Button(self, text="Run simulation",
               command=master.run).pack()
        Button(self, text="Propagate",
               command=master.propagate).pack()
        Button(self, text="Reset",
               command=master.reset_all).pack()

        self.resizeable()
