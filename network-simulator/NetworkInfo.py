# -*- coding: utf-8 -*-
import tkinter as tk
from Common import Common


class NetworkInfo(tk.LabelFrame, Common):
    """Label frame displaying basic information about the network loaded
    or created, like the number of people or their name.

    """
    def __init__(self, master):
        super().__init__(master, text="Network information")

        # Attributes to use (shared with NetworkFrame)
        self.node_name = tk.StringVar()
        self.node_rumor = tk.StringVar()
        self.network_size = tk.IntVar()

        # Widgets inside the frame
        tk.Label(self, text="Network size:").grid(row=0, column=0, sticky=tk.NW)
        tk.Label(self, text="Person name:").grid(row=1, column=0, sticky=tk.W)
        tk.Label(self, text="Rumor:").grid(row=2, column=0, sticky=tk.SW)

        tk.Label(self, textvariable=self.network_size,
                 anchor=tk.E).grid(row=0, column=1, sticky=tk.NE)

        tk.Label(self, textvariable=self.node_name,
                 anchor=tk.E,
                 width=15).grid(row=1, column=1, sticky=tk.E)
        tk.Label(self, textvariable=self.node_rumor,
                 anchor=tk.E).grid(row=2, column=1, sticky=tk.SE)

        self.resizeable()
