# -*- coding: utf-8 -*-
"""# TO
"""
from tkinter import *
from Common import Common

class Buttons(LabelFrame, Common):
    """This buttons class implements:

    - Propagate: run the simulator 1 unit of time
    - Run: run the simulator n times
    - Add friend: adds a new person to the network
    - Reset: goes back to original state

    """
    def __init__(self, master):
        super().__init__(master, text="Choose an action")

        Button(self, text="Add friend",
               command=lambda: master.add_friend()).pack()
        Button(self, text="Run simulation",
               command=lambda: master.run()).pack()
        Button(self, text="Propagate",
               command=master.propagate).pack()
        Button(self, text="Reset",
               command=lambda: master.reset_all()).pack()

        self.resizeable()



def cbOn():
    print("The checkbutton is on and the variable is YEAH")

