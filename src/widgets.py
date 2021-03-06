# IMPORTS
from datetime import datetime
from tkinter import *
from functools import partial
import os

import psutil as psu
from uptime import boottime


# WIDGETS
class GUI:
    """Builds main GUI."""
    def __init__(self, master):
        # self.master is a frame that's a child of master for window padding purposes.
        # Widget grid layouts are children of self.master.
        self.master = Frame(master, padx=10, pady=10)
        self.master.grid()

        # Font and other layout variables.
        # font_label is applied to each label in col 0 (metrics).
        # font_value is applied to each label in col 1 (values).
        self.font_family = "Helvetica"
        self.font_size = "9"
        self.font_label = (self.font_family, self.font_size, "bold")
        self.font_value = (self.font_family, self.font_size)
        self.whitespace_height = 12

        # Change time format for different operating systems.
        if os.name == "nt":
            self.time_format = "%#I:%M:%S %p"
        else:
            self.time_format = "%-I:%M:%S %p"

        # Create widget labels and EXIT button.
        self.gui_widget_metrics = [
            Label(self.master, text="CPU (%):", font=self.font_label),          # CPU
            Label(self.master, text="Memory (%):", font=self.font_label),       # MEMORY
            Label(self.master, text="Uptime:", font=self.font_label),           # UPTIME
            Label(self.master, text="System Clock:", font=self.font_label),     # SYSTEM CLOCK
            Label(self.master, text="Boot Time:", font=self.font_label),        # BOOT TIME
            Frame(self.master, height=self.whitespace_height),                  # WHITESPACE
            Button(self.master, text="EXIT", font=self.font_value,
                   bg="white smoke", command=master.quit)                       # EXIT BUTTON
        ]

        # Create initial widget values and ALWAYS ON TOP button.
        self.on_top_check = IntVar(value=1)  # Initial state for ALWAYS ON TOP button. Defaults to checked.
        self.gui_widget_values = [
            Label(self.master, text="{}".format(psu.cpu_percent()), font=self.font_value),         # CPU
            Label(self.master, text="{}".format(psu.virtual_memory()[2]), font=self.font_value),   # MEMORY
            Label(self.master, text=str(datetime.now() - boottime())[:-7], font=self.font_value),  # UPTIME
            Label(self.master, text=datetime.now().strftime("{}".format(self.time_format)),
                  font=self.font_value),                                                           # SYSTEM CLOCK
            Label(self.master, text="{}".format(boottime().strftime("%b %d %Y, {}".format(self.time_format))),
                  font=self.font_value),                                                           # BOOT TIME
            Frame(self.master, height=self.whitespace_height),                                     # WHITESPACE
            Checkbutton(master=self.master, text="Always On Top", font=self.font_value,
                        variable=self.on_top_check, command=partial(self.update_on_top, master))  # ALWAYS ON TOP BUTTON
        ]

        # Loop through widgets and display on grid (col 0 - metrics).
        for index, label in list(enumerate(self.gui_widget_metrics)):
            # if index == EXIT button, center button in cell
            if index == 6:
                label.grid(sticky="nsew", row=index, column=0, padx=(8, 0))
            else:
                label.grid(sticky="w", row=index, column=0, padx=(8, 0), pady=(1, 0))

        # Loop through widgets and display on grid (col 1 - values).
        for index, label in list(enumerate(self.gui_widget_values)):
            # if index == ALWAYS ON TOP checkbox, center checkbox in cell
            if index == 6:
                label.grid(sticky="nsew", row=index, column=1, padx=(16, 8))
            else:
                label.grid(sticky="w", row=index, column=1, padx=(16, 8), pady=(1, 0))

        # Start system metric update loop - calls self.get_metrics().
        master.after(1000, self.get_metrics)

    def get_metrics(self):
        """Update system metric GUI elements once per second."""
        # Gather metrics.
        cpu = psu.cpu_percent()
        memory = psu.virtual_memory()[2]
        uptime_var = (str(datetime.now() - boottime())[:-7])
        time = datetime.now().strftime("{}".format(self.time_format))

        # CPU (red text when >90%)
        self.gui_widget_values[0].configure(text=cpu)
        if cpu >= 90.0:
            self.gui_widget_values[0].configure(fg="red")
        else:
            self.gui_widget_values[0].configure(fg="black")

        # MEMORY (red text when >90%)
        self.gui_widget_values[1].configure(text=memory)
        if memory >= 90.0:
            self.gui_widget_values[1].configure(fg="red")
        else:
            self.gui_widget_values[1].configure(fg="black")

        # UPTIME
        self.gui_widget_values[2].configure(text=uptime_var)

        # SYSTEM CLOCK
        self.gui_widget_values[3].configure(text=time)

        self.master.after(1000, self.get_metrics)  # Continue calling this function every second.

    def update_on_top(self, root):
        """Set if window is Always On Top (master.attributes("-topmost")) based on checkbox."""
        if self.on_top_check.get() == 1:
            root.attributes("-topmost", "true")
        else:
            root.attributes("-topmost", "false")
