# -*- coding: utf-8 -*-
"""File containing the file class"""

from tkinter import *

class Link:
    """This class represents the link (friendship) between 2 people. It is
    linked to the network data structure the same way Person is linked
    to people

    """
    def __init__(self, person1, person2, row_position, col_position):
        """Constructor the class, takes 2 parameters of class Person and the
        thickness to represent the link.

        """
        self.person1 = person1
        self.person2 = person2
        # Indexes are kept for fast delete in network matrix
        self.row_position = row_position
        self.col_position = col_position

    def draw_link(self, master, gui, link_thickness):
        """This method will make the class graphical (it will appear on its
        master - the canvas)

        """

        # Events and binds

        # Tag is the two indexes
        tag = (self.person1.name + self.person2.name).replace(" ", "")
        master.tag_bind(tag, "<Double-Button-1>", lambda event:\
                        self.delete_link(gui))

        
        self.link_thickness = link_thickness
        self.points = (self.person1.node_geometry[0],
                       self.person1.node_geometry[1],
                       self.person2.node_geometry[0],
                       self.person2.node_geometry[1])

        master.create_line(self.points,
                           width=self.link_thickness,
                           fill="black",
                           activefill="red",
                           capstyle=ROUND,
                           smooth=True,
                           tags=tag)


    def delete_link(self, gui):
        """A simple access to simu data network in order to set the link at
        that location to False, then update the network

        """
#        print("My row pos is:", self.row_position)
#        print("My col pos is:", self.col_position)
#        gui.simu_data["network"][self.row_position][self.col_position] = False
        gui.simu_data["people"][self.col_position].friends.remove(gui.simu_data["people"][self.row_position].name)
        gui.simu_data["people"][self.row_position].friends.remove(gui.simu_data["people"][self.col_position].name)
        gui.update_app()
