# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox
from math import cos, sin, pi
from tkinter import ROUND
from random import randint


class NetworkFrame(tk.Canvas):
    """Class inheriting from tkinter.Canvas. It contains the graphic
    representation of the network. Its children (tkinter) are the
    Person(s) and Links

    """

    def __init__(self, master, network_info, disp_options):
        super().__init__(master, bg="bisque")

        self.layout_funcs = {"circular": self.circular,
                             "shell": self.shell_dist}

        # Access to some attributes from these 'friend' classes
        self.info_friend = network_info
        self.display_friend = disp_options

        # Canvas will update automatically if window resizes
        self.bind("<Configure>", lambda event: master.update_app())

        # Access to simu_data attribute and some methods needed
        self.master = master

        #
        self.start_node = None
        self.end_node = None

    def update(self, network, people, *args):
        """draw the canvas objects again"""
        self.delete("all")
        node_size = self.display_friend.node_size.get()
        link_thickness = self.display_friend.link_thickness.get()
        border_adjust = node_size + 20

        # Draw people
        for i in range(len(people)):
            node_geometry = self.layout_funcs[self.display_friend.layout.get()](i, border_adjust, people)
            people[i].draw_person(self, self.master, node_geometry, node_size)

        # Draw links between people
        for i in range(len(network)):
            for j in range(len(network[i])):
                if network[i][j]:
                    network[i][j].draw_link(self, self.master, link_thickness)

    def circular(self, index, border_adjust, people):
        """Represents the network in an oval fashion"""
        major_radius = self.winfo_width() / 2 - border_adjust
        minor_radius = self.winfo_height() / 2 - border_adjust

        # Oval container (decoration)
        self.create_oval(border_adjust,                    # x0
                         border_adjust,                    # y0
                         major_radius * 2 + border_adjust, # x1
                         minor_radius * 2 + border_adjust, # y1
                         dash=(10,))

        angles = 2*pi/len(people)
        angle = angles * (index + 1)
        x_coord = int(major_radius*cos(angle)) + major_radius + border_adjust
        y_coord = int(minor_radius*sin(angle)) + minor_radius + border_adjust
        return x_coord, y_coord

    def shell_dist(self, index, border_adjust, people):
        """Place the people as a seashell in the canvas

        """
        SPIRAL_RESOLUTION = 50

        width = self.winfo_width() - (border_adjust << 1)
        height = self.winfo_height() - (border_adjust << 1)

        # Spiral container (decoration)
        step = 2.0 * pi / (SPIRAL_RESOLUTION)
        for i in range(SPIRAL_RESOLUTION):
            self.create_line(i * step * cos(i) * border_adjust,
                             i * step * sin(i) * border_adjust,
                             i + 1 * step * cos(i + 1) * border_adjust,
                             i + 1 * step * sin(i + 1) * border_adjust)

        step = 2.0 * pi / len(people)
        x_coord, y_coord = (index * step * cos(index) * border_adjust,
                            index * step * sin(index) * border_adjust)
        width_adjust = (width / 2)
        height_adjust = (height / 2) + border_adjust + border_adjust
        x_coord += width_adjust
        y_coord += height_adjust
        return x_coord, y_coord

    # Update names and rumor in NetworkInfo (friend)
    def give_info(self, name, rumor):
        """Updates the info panel"""
        self.info_friend.node_name.set(name)
        if rumor is not None:
            rumor = "#{:06X}".format(rumor)
        self.info_friend.node_rumor.set(rumor)

    def remove_info(self):
        """Updates the info panel """
        self.info_friend.node_name.set("")
        self.info_friend.node_rumor.set("")

    def dnd_start(self, start_node, event):
        """Drag and drop feature"""
        points = (start_node.node_geometry[0],
                  start_node.node_geometry[1],
                  event.x,
                  event.y)
        link_thickness = self.display_friend.link_thickness.get()
        self.delete("dndline")
        self.create_line(points,
                         capstyle=ROUND,
                         width=link_thickness,
                         fill="blue",
                         tags="dndline")

        self.start_node = start_node

    def dnd_end(self, event, tag):
        """Drag and drop feature

        """
        closest = self.find_overlapping(event.x, event.y, event.x, event.y)
        i = 0
        keep = True
        while i < len(self.master.simu_data["people"]) and keep:
            tag_to_search = self.master.simu_data["people"][i].name.replace(" ", "")
            if self.find_withtag(tag_to_search)[0] in closest:
                self.end_node = self.master.simu_data["people"][i]
                keep = False
            i += 1

        if self.end_node is None or self.start_node is None\
           or self.end_node is self.start_node:
            # Means drag and drop was not completed or same person,
            # clean and exit
            self.delete("dndline")
            self.start_node = None
            self.end_node = None
            return
        elif self.end_node.name in self.start_node.friends:
            # Already friends
            self.delete("dndline")
            messagebox.showwarning("Already friends!",
                                   "The two people chosen are already friends")
            self.start_node = None
            self.end_node = None
            return

        # Also add to each other's friends list
        self.start_node.friends.append(self.end_node.name)
        self.end_node.friends.append(self.start_node.name)

        self.start_node = None
        self.end_node = None
        self.master.update_app()
