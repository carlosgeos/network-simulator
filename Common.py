# -*- coding: utf-8 -*-

class Common:
    """Abstract class containing common methods that most if not all
    widgets will use

    """
    def resizeable(self):
        """Making window/frame resizeable to work with sticky options.

        grid_size()[0] is the number of columns and grid_size()[1] is
        the number of rows in the widget's grid system

        """

        for column in range(self.grid_size()[0]):
            self.columnconfigure(column, weight=1)
        for row in range(self.grid_size()[1]):
            self.rowconfigure(row, weight=1)
