# -*- coding: utf-8 -*-
import tkinter as tk


class Link:
    """This class represents the link (friendship) between 2 people. It is
    linked to the network data structure the same way Person is linked
    to people

    """
    def __init__(self, person1, person2):
        """Constructor the class, takes 2 parameters of class Person and the
        thickness to represent the link.

        """
        self.person1 = person1
        self.person2 = person2

    def draw_link(self, master, gui, link_thickness):
        """This method will make the class graphical (it will appear on its
        master - the canvas)

        """

        # Events and binds
        # Tag is the two indexes
        tag = (self.person1.name + self.person2.name).replace(" ", "")
        print("I have just being created, my Link tag is", tag)
        master.tag_bind(tag, "<Double-Button-1>", lambda event:
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
                           capstyle=tk.ROUND,
                           smooth=True,
                           tags=tag)

    def delete_link(self, gui):
        """Eliminates each others name from the concerned people friend's
        list, then update the simulator to reflect the changes.

        """

        self.person1.friends.remove(self.person2.name)
        self.person2.friends.remove(self.person1.name)
        gui.update_app()
