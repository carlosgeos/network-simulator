#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# INFO-F106 : Projet d'année
# Carlos Requena López

"""Module implementing the graphical user interface of the network
simulator.

"""
# --- Libraries --- #
import json
# --- TkInter libraries --- #
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox
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
# from Link import Link
# --- Simulator functions --- #
import rumorFunctions as rF


class GUI(tk.Tk, Common):
    """Instance class defining the Graphical User Interface, more
    specifically, the top level window and root Tk

    """

    modif_funcs = {"none": rF.none,
                   "incremental": rF.incremental,
                   "bitflip": rF.bitflip}

    update_funcs = {"stable": rF.stable,
                    "rewrite": rF.rewrite,
                    "mixture": rF.mixture}

    def __init__(self):
        super().__init__()      # takes Tk constructor

        self.option_readfile("optionsDB")  # .Xresources file
        self.title("Network simulator")

        # Root binds / shortcuts
        self.bind("<Control-w>", lambda event: self.destroy())
        self.bind("<Control-q>", lambda event: self.destroy())
        self.bind("<Control-o>", lambda event: self.load_file())

        # Data to manipulate
        self.simu_data = {
            "network_file": None,
            "network": [],
            "people": [],
            "dont_tell": False,
            "modif_function": tk.StringVar(),
            "probability": tk.DoubleVar(),
            "update_function": tk.StringVar(),
            "select_policy": tk.StringVar()
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
                               sticky=tk.N+tk.W+tk.S+tk.E)
        self.simu_info = SimuInfo(self)
        self.simu_info.grid(row=1, column=0,
                            sticky=tk.N+tk.W+tk.S+tk.E)
        self.buttons = Buttons(self)
        self.buttons.grid(row=2, column=0,
                          sticky=tk.N+tk.W+tk.S+tk.E)
        self.disp_options = DispOptions(self)
        self.disp_options.grid(row=2, column=1,
                               sticky=tk.N+tk.W+tk.S+tk.E)
        self.simu_options = SimuOptions(self)
        self.simu_options.grid(row=2, column=2,
                               sticky=tk.N+tk.W+tk.S+tk.E)

        self.canvas = NetworkFrame(self, self.network_info,
                                   self.disp_options)
        self.canvas.grid(row=0, column=1,
                         rowspan=2, columnspan=2,
                         sticky=tk.N+tk.W+tk.S+tk.E)

    # --- Files and errors --- #
    def network_check(self):
        """Method checking if names is empty or not"""
        try:
            if not self.simu_data["people"]:
                raise tk.TclError
        except tk.TclError:
            messagebox.showwarning("No network", "The network is empty!")
            return False
        else:
            return True

    def file_present(self):
        if self.simu_data["network_file"] is None:
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
        if not self.simu_data["network_file"]:
            return

        self.simu_data["people"] = rF.load_people(self.simu_data["network_file"])
        self.update_app()

    def load_pickled_file(self):
        """Decodes a pickled file containing the people and the friendship
        matrix, then updates the attributes and the GUI

        """
        ftypes = [("Pickled network files", ".p"),
                  ("All files", ".*")]
        self.simu_data["network_file"] = filedialog.askopenfilename(title="Select a network file",
                                                                    filetypes=ftypes)
        if not self.simu_data["network_file"]:
            return

        self.simu_data["people"] = rF.load_pickled_file(self.simu_data["network_file"])
        self.update_app()

    def save_file(self):
        """Takes a snapshot of the current state of the network and saves it
        to a file. The file format is readable by this program using
        the load_file method.

        It uses the pickle library

        """
        self.simu_data["network_file"] = filedialog.asksaveasfilename(title="Select a file to save the data to:",
                                                                      defaultextension=".p")
        if not self.simu_data["network_file"]:
            return
        rF.save_file(self.simu_data)

    def reset_all(self):
        """Resets the network to the initial state
        """
        self.simu_data["people"] = []
#        self.simu_data["network"] = []
        self.simu_info.stage_number.set(0)
        self.simu_info.still_fool.set(0)
        self.update_app()

    # --- calls to rumorFunctions and simulator related methods --- #
    def add_friend(self):
        """adds a person to the network"""
        name = simpledialog.askstring("Add a new person",
                                      "Name of person:")
        if name is None or not name:
            # Cancel button or empty name
            return
        elif len(list(filter(lambda person: name == person.name, self.simu_data["people"]))) > 0:
            # Name already given
            tk.messagebox.showerror("Existing name",
                                    "This name is already given")
            return

        self.simu_data["people"].append(Person(name))
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

        # Compute the network
        self.simu_data["network"] = rF.load_network(self.simu_data["people"])
        # rF.print_matrix(self.simu_data["network"])

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
            self.simu_info.rumor_spread.set(spread)
            self.update_app()


# --- Main --- #
def main():
    """Main function. Creates an instance of class GUI, which is the
    tkinter parent object, and in turn inherits from the root window
    Tk. This way the hierarchy keeps coherence.

    """
    my_gui = GUI()
    my_gui.mainloop()           # Tk watchdog


if __name__ == "__main__":
    main()
