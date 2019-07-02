# IMPORTS
from datetime import datetime
from tkinter import *

import psutil as psu
from uptime import boottime


# WIDGETS
class GUI:
    def __init__(self, master):
        self.master = master

        # Font variables.
        # font_label is applied to each label in col 0 (metrics).
        # font_value is applied to each label in col 1 (values).
        self.font_family = 'Helvetica'
        self.font_size = '9'
        self.font_label = (self.font_family, self.font_size, 'bold')
        self.font_value = (self.font_family, self.font_size)

        # Create widget labels and EXIT button.
        self.gui_widget_metrics = [
            Label(master, text="CPU (%):", font=self.font_label),                   # CPU
            Label(master, text="Memory (%):", font=self.font_label),                # MEMORY
            Label(master, text="Uptime:", font=self.font_label),                    # UPTIME
            Label(master, text="Boot Time:", font=self.font_label),                 # BOOT TIME
            Label(master, text="System Clock:", font=self.font_label),              # SYSTEM CLOCK
            Button(master, text="EXIT", font=self.font_value, command=master.quit)  # EXIT BUTTON
        ]

        # Create initial widget values and ALWAYS ON TOP button.
        self.on_top_check = IntVar(value=1)  # Initial state for ALWAYS ON TOP button. Defaults to checked.
        self.gui_widget_values = [
            Label(master, text="{}".format(psu.cpu_percent()), font=self.font_value),           # CPU
            Label(master, text="{}".format(psu.virtual_memory()[2]), font=self.font_value),     # MEMORY
            Label(master, text=str(datetime.now() - boottime())[:-7], font=self.font_value),    # UPTIME
            Label(master, text="{}".format(boottime().strftime("%b %d %Y, %H:%M:%S")),          # BOOT TIME
                  font=self.font_value),
            Label(master, text=datetime.now().strftime("%H:%M:%S"), font=self.font_value),      # SYSTEM CLOCK
            Checkbutton(master, text="Always On Top", font=self.font_value,                     # ALWAYS ON TOP BUTTON
                        variable=self.on_top_check, command=self.update_on_top)
        ]

        # Loop through widgets and display on grid (col 0 - metrics).
        for index, label in list(enumerate(self.gui_widget_metrics)):
            label.grid(sticky="w", row=index, column=0, padx=(8, 0), pady=(2, 0))

        # Loop through widgets and display on grid (col 1 - values).
        for index, label in list(enumerate(self.gui_widget_values)):
            label.grid(sticky="w", row=index, column=1, padx=(16, 8), pady=(2, 0))

        # Start system metric update loop - calls self.get_metrics().
        master.after(1000, self.get_metrics)

    def get_metrics(self):
        """Update system metric GUI elements once per second."""
        # Gather metrics.
        cpu = psu.cpu_percent()
        memory = psu.virtual_memory()[2]
        uptime_var = str(datetime.now() - boottime())[:-7]
        time = datetime.now().strftime("%H:%M:%S")

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

        # CLOCK
        self.gui_widget_values[4].configure(text=time)

        self.master.after(1000, self.get_metrics)  # Continue calling this function every second.

    def update_on_top(self):
        """Set if window is Always On Top (master.attributes('-topmost')) based on checkbox."""
        if self.on_top_check.get() == 1:
            self.master.attributes("-topmost", "true")
        else:
            self.master.attributes("-topmost", "false")
