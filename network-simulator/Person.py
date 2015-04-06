# -*- coding: utf-8 -*-

from tkinter import colorchooser
from PlatformUtils import PlatformUtils


class Person:
    """Class representing a person in the network"""

    def __init__(self, name, friends=None, rumor=None):
        self.name = name
        if friends is None:
            self.friends = []
        self.rumor = rumor

    def draw_person(self, master, gui, node_geometry, node_radius):
        """Graphic layer to the Person class"""

        # Binds and events occurring on the people
        # Using names as tags
        # Tags do not like names with spaces
        tag = self.name.replace(" ", "")
        print("Hi im being graphically created now")
        print("My tag is:", tag)
        print("And my friends are:", self.friends)
        right_button = str(PlatformUtils.getRightButton())
        master.tag_bind(tag, "<Enter>", lambda event:
                        master.give_info(self.name, self.rumor))
        master.tag_bind(tag, "<Leave>", lambda event:
                        master.remove_info())
        master.tag_bind(tag, "<" + right_button + ">", lambda event:
                        self.get_rumor(master, gui))
        master.tag_bind(tag, "<Double-1>", lambda event:
                        self.delete_node(gui))
        master.tag_bind(tag, "<B1-Motion>", lambda event:
                        master.dnd_start(self, event))
        master.tag_bind(tag, "<ButtonRelease-1>", lambda event:
                        master.dnd_end(event, tag))

        # Drawing
        if self.rumor is None:
            color = "black"
            stipple = "gray25"  # No effect in OS X (Quartz)
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
        """Removes the Person instance from people and from their friends
        list. Since there are no more references to this object, the
        python garbage collector will eliminate it once it is
        appropriate

        """
        for i in range(len(gui.simu_data["people"])):
            my_friends_friends = gui.simu_data["people"][i].friends
            if self.name in my_friends_friends:
                my_friends_friends.remove(self.name)
        gui.simu_data["people"].remove(self)
        gui.update_app()

    def get_rumor(self, master, gui):
        """Sets the 6 digit hex colour value to the rumor of Person in people

        askcolor returns a tuple, whose second element is the string
        value of the color in hexadecimal

        """
        value = colorchooser.askcolor(title="Choose a rumor")
        if value[1] is None:
            return
        self.rumor = int(value[1].replace("#", "0x"), 0)
        self.draw_person(master, gui, self.node_geometry, self.node_radius)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if (other is None):
            return False
        return self.name == other.name
