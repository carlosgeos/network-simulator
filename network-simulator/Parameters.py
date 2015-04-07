# -*- coding: utf-8 -*-

import tkinter as tk
from Common import Common


class Parameters(tk.Toplevel, Common):
    """Class implementing the top level window that shows all the possible
    modifications to perform on the network

    """
    UPDATE = ("stable", "rewrite", "mixture")
    SELECTION = ("random", "all")
    MODIFICATION = ("none", "incremental", "bitflip")

    DEFAULT_PROBABILITY = 0.5

    def __init__(self, master):
        super().__init__()
        self.title("Parameters")
        tk.Label(self, text="Update Policy").grid(row=0, column=0)
        tk.Label(self, text="Modification Policy").grid(row=0, column=1)
        tk.Label(self, text="Selection Policy").grid(row=0, column=2)

        update_menu = tk.OptionMenu(self, master.simu_data["update_function"],
                                    *self.UPDATE)
        update_menu.grid(row=1, column=0)
        modif_menu = tk.OptionMenu(self, master.simu_data["modif_function"],
                                   *self.MODIFICATION)
        modif_menu.grid(row=1, column=1)
        select_menu = tk.OptionMenu(self, master.simu_data["select_function"],
                                    *self.SELECTION)
        select_menu.grid(row=1, column=2)

        error_scale = tk.Scale(self,
                               label="Modification probability",
                               orient=tk.HORIZONTAL,
                               from_=0.0,
                               to=1.0,
                               tickinterval=0.25,
                               resolution=0.01,
                               length=250,
                               variable=master.simu_data["probability"])
        error_scale.grid(row=2, column=0, columnspan=3)

        # default values
        master.simu_data["update_function"].set(self.UPDATE[0])
        master.simu_data["select_function"].set(self.SELECTION[0])
        master.simu_data["modif_function"].set(self.MODIFICATION[0])
        master.simu_data["probability"].set(self.DEFAULT_PROBABILITY)

        self.resizeable()
