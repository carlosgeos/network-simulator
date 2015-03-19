# -*- coding: utf-8 -*-
from tkinter import *
from Common import Common


class SimuOptions(LabelFrame, Common):
    """All the variables and modification options for the network
    simulator.

    """
    UPDATE = ("stable", "rewrite", "mixture")
    SELECTION = "random"
    MODIFICATION = ("none", "incremental", "bitflip")

    DEFAULT_PROBABILITY = 0.5

    def __init__(self, master):
        super().__init__(master, text="Simulator Options")

        Label(self, text="Update Policy").grid(row=0, column=0)
        Label(self, text="Modification Policy").grid(row=0, column=1)
        Label(self, text="Selection Policy").grid(row=0, column=2)

        update_menu = OptionMenu(self, master.simu_data["update_function"], *self.UPDATE)
        update_menu.grid(row=1, column=0)
        modif_menu = OptionMenu(self, master.simu_data["modif_function"], *self.MODIFICATION)
        modif_menu.grid(row=1, column=1)
        select_menu = OptionMenu(self, master.simu_data["select_policy"], self.SELECTION)
        select_menu.grid(row=1, column=2)


        error_scale = Scale(self,
                            label="Modification probability",
                            orient=HORIZONTAL,
                            from_=0.0,
                            to=1.0,
                            tickinterval=0.25,
                            resolution=0.01,
                            length=250,
                            variable=master.simu_data["probability"])
        error_scale.grid(row=2, column=0, columnspan=3)

        # default values
        master.simu_data["update_function"].set(self.UPDATE[0])
        master.simu_data["select_policy"].set(self.SELECTION)
        master.simu_data["modif_function"].set(self.MODIFICATION[0])
        master.simu_data["probability"].set(self.DEFAULT_PROBABILITY)

        self.resizeable()
