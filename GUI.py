#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# INFO-F106 : Projet d'année
# Carlos Requena López

"""Module implementing the graphical user interface of the network
simulator

"""
# --- TkInter libraries --- #
from tkinter import *
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox
import random
# --- GUI main widgets --- #
from NetworkFrame import NetworkFrame
from NetworkInfo import NetworkInfo
from SimuInfo import SimuInfo
from Buttons import Buttons
from TopMenu import TopMenu
from DispOptions import DispOptions
from SimuOptions import SimuOptions
# --- Abstract Classes --- #
from Common import Common       # common widget methods and attributes
from Person import Person
from Link import Link
# --- Simulator functions --- #
import rumorFunctions as rF


class GUI(Tk, Common):

    modif_funcs = {"none": rF.none,
                   "incremental": rF.incremental,
                   "bitflip": rF.bitflip}

    update_funcs = {"stable": rF.stable,
                    "rewrite": rF.rewrite,
                    "mixture": rF.mixture}


    """Instance class defining the Graphical User Interface, more
    specifically, the top level window and root Tk

    """

    def __init__(self):
        super().__init__()      # takes Tk constructor

        self.option_readfile("optionsDB") # .Xresources file
        self.title("Network simulator")
        
        # Root binds / shortcuts
        self.bind("<Control-w>", lambda event: self.destroy())
        self.bind("<Control-q>", lambda event: self.destroy())
        self.bind("<Control-o>", lambda event: self.load_file())

        # Data center
        self.simu_data = {
            "network_file": None,
            "network": [],
            "people": [],
            "dont_tell": False,
            "modif_function": StringVar(),
            "probability": DoubleVar(),
            "update_function": StringVar(),
            "select_policy": StringVar()
        }

        self.create_widgets()
        self.resizeable()



    # --- Widgets initialization --- #
    def create_widgets(self):
        """This method creates and positions all the widgets in the
        window. They become attributes of GUI

        """

        self.top_menu = TopMenu(self)

        self.network_info = NetworkInfo(self)
        self.network_info.grid(row=0, column=0,
                               sticky=N+W+S+E)
        self.simu_info = SimuInfo(self)
        self.simu_info.grid(row=1, column=0,
                            sticky=N+W+S+E)
        self.buttons = Buttons(self)
        self.buttons.grid(row=2, column=0,
                          sticky=N+W+S+E)
        self.disp_options = DispOptions(self)
        self.disp_options.grid(row=2, column=1,
                               sticky=N+W+S+E)
        self.simu_options = SimuOptions(self)
        self.simu_options.grid(row=2, column=2,
                               sticky=N+W+S+E)

        self.canvas = NetworkFrame(self, self.network_info,
                                   self.disp_options)
        self.canvas.grid(row=0, column=1,
                         rowspan=2, columnspan=2,
                         sticky=N+W+S+E)



    # --- Files and errors --- #

    def network_check(self):
        """Method checking if names is empty or not"""
        try:
            if not self.simu_data["people"]:
                raise TclError
        except TclError:
            messagebox.showwarning("No network", "The network is empty!")
            return False 
        else:
            return True

    def load_file(self):
        """Gets the path of network file, and extracts the names, friends and
        friendship network of it. Then updates the class attributes.

        """

        ftypes = [("Network files", ".txt"),
                  ("All files", ".*")]
        self.simu_data["network_file"] = filedialog.askopenfilename(title="Select a network file",
                                                                    filetypes=ftypes)
        

        #try: pensar en hacer exception handling!
        self.simu_data["people"] = rF.load_people(self.simu_data["network_file"])
        self.simu_data["network"] = rF.load_network(self.simu_data["people"])
        self.update_app()


    def reset_all(self):
        self.simu_data["people"] = []
        self.simu_data["network"] = []
        self.simu_info.stage_number.set(0)
        self.simu_info.still_fool.set(0)
        self.update_app()
        
    def save_file(self):
        """Partie 4
        """
        pass

    # --- calls to rumorFunctions and simulator related methods --- #

    def add_friend(self):
        """adds a person to the network"""
        name = simpledialog.askstring("Add a new person",
                                      "Name of person:")
        # TODO: if name.isdigit() --> conflict with canvas object ID's
        index = len(self.simu_data["people"])
        self.simu_data["people"].append(Person(name, index))
        self.simu_data["network"] = rF.load_network(self.simu_data["people"])
        self.update_app()

    def run(self):
        """call propagate for a finite number of times"""
        if self.network_check():
            stages_number = simpledialog.askinteger("Run simulation",
                                                    "Number of stages:")
            delay = int(self.disp_options.delay.get() * 1000)
            for i in range(stages_number):
                self.propagate()
                self.after(delay)
                self.update()
            
    def calc_still_fools(self):
        """Calculates the number of people that still do not know any rumor"""
        counter = 0
        for person in self.simu_data["people"]:
            if person.rumor is None:
                counter += 1
        self.simu_info.still_fool.set(counter)

    def update_app(self, *args):
        """Updates the whole interface, calling other minor updates
        fonctions

        """

        # Update Info label frames
        self.network_info.network_size.set(len(self.simu_data["people"]))
        self.calc_still_fools()

        self.simu_data["network"] = rF.load_network(self.simu_data["people"])
        
        # Update canvas
        self.canvas.update(self.simu_data["network"],
                           self.simu_data["people"])

    def propagate(self):
        if self.network_check():
            modif_func = self.modif_funcs[self.simu_data["modif_function"].get()]
            update_func = self.update_funcs[self.simu_data["update_function"].get()]
            prob = self.simu_data["probability"].get()
            dont_tell = False

            flags = (dont_tell, modif_func, prob, update_func)
        
            spread = rF.update(self.simu_data["network"], self.simu_data["people"], flags)
            self.simu_info.stage_number.set(self.simu_info.stage_number.get() + 1)
            self.update_app()

# --- Main --- #
def main():
    """Main function. Creates an instance of class GUI, which is the
    parent object (tkinter-speaking), and in turn inherits from the
    root window Tk. This way the hierarchy keeps coherence.

    """
    my_gui = GUI()
    my_gui.mainloop()           # Tk watchdog


if __name__ == "__main__":
    main()