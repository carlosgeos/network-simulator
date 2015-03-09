# -*- coding: utf-8 -*-
"""Class representing a person in the network"""

from tkinter import *
from tkinter import colorchooser
from PlatformUtils import PlatformUtils

class Person:
    """Class representing a person in the network"""
    def __init__(self, name, index=None, friends=[], rumor=None):
        self.name = name
        self.friends = friends
        self.rumor = rumor
        # Keeping index in list people for fast access
        self.index = index

    def draw_person(self, master, gui, node_geometry, node_radius):
        """Graphic layer to the Person class"""

        # Binds and events occurring on the people
        # Using names as tags
        # Tags do not like names with spaces
        tag = self.name.replace(" ", "")
        right_button = PlatformUtils.getRightButton()
        master.tag_bind(tag, "<Enter>", lambda event: \
                        master.give_info(self.name, self.rumor))
        master.tag_bind(tag, "<Leave>", lambda event: \
                        master.remove_info())
        master.tag_bind(tag, "<" + str(right_button) + ">", lambda event: \
                        self.get_rumor(master, gui))
        master.tag_bind(tag, "<Double-1>", lambda event:\
                        self.delete_node(gui))
        master.tag_bind(tag, "<B1-Motion>", lambda event:\
                        master.dnd_start(self, event))
        master.tag_bind(tag, "<ButtonRelease-1>", lambda event:\
                        master.dnd_end(event, tag))
                                        
        # Drawing
        if self.rumor is None:
            color = "black"
            stipple = "gray25"  # No effect in OS X (Quartz)?
        else:
            color = "#{:06X}".format(self.rumor)
            stipple = ""
        self.node_geometry = node_geometry
        x_coord = self.node_geometry[0]
        y_coord = self.node_geometry[1]
        self.node_radius = node_radius
        
        master.create_oval(x_coord - node_radius,
                           y_coord + node_radius,
                           x_coord + node_radius,
                           y_coord - node_radius,
                           activeoutline="red",
                           fill=color,
                           stipple=stipple,
                           tags=tag)
        

    def delete_node(self, gui):
        """Removes the Person instance from people"""
        gui.simu_data["people"].remove(self)
        for i in range(len(gui.simu_data["people"])):
            try:
                gui.simu_data["people"][i].friends.remove(self.name)
            except ValueError:
                pass # Not everyone is friends with everyone (nor with
                     # him/herself)
        gui.update_app()

    def get_rumor(self, master, gui):
        """Sets the 6 digit hex colour value to the rumor of Person in
        people

        """
        value = colorchooser.askcolor(title="Choose a rumor")
        self.rumor = int(value[1].replace("#", "0x"), 0)
        self.draw_person(master, gui, self.node_geometry, self.node_radius)

