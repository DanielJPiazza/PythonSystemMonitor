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
        self.font_family = 'Helvetica'
        self.font_size = '9'
        self.font_label = (self.font_family, self.font_size, 'bold')
        self.font_value = (self.font_family, self.font_size)

        # Lists for GUI widgets.
        self.gui_widgets = []
        self.gui_value_widgets = []

        # Variable structure is the same for most widgets.

        # CPU
        self.cpu_label_text = "CPU (%)"
        self.cpu_label = Label(master, text="{}:".format(self.cpu_label_text), font=self.font_label)
        self.cpu_label_value = Label(master, text="{}".format(psu.cpu_percent()), font=self.font_value)
        self.gui_widgets.append(self.cpu_label)
        self.gui_value_widgets.append(self.cpu_label_value)

        # VIRTUAL MEMORY
        self.mem_label_text = "Memory (%)"
        self.virtual_memory_label = Label(master, text="{}:".format(self.mem_label_text), font=self.font_label)
        self.virtual_memory_label_value = Label(master, text="{}".format(psu.virtual_memory()[2]), font=self.font_value)
        self.gui_widgets.append(self.virtual_memory_label)
        self.gui_value_widgets.append(self.virtual_memory_label_value)

        # UPTIME
        self.uptime_text = "Uptime"
        self.uptime_value = str(datetime.now() - boottime())[:-7]
        self.uptime_label = Label(master, text="{}:".format(self.uptime_text), font=self.font_label)
        self.uptime_label_value = Label(master, text=self.uptime_value, font=self.font_value)
        self.gui_widgets.append(self.uptime_label)
        self.gui_value_widgets.append(self.uptime_label_value)

        # BOOT TIME
        self.boottime_text = "Boot Time"
        self.boottime_label = Label(master, text="{}:".format(self.boottime_text), font=self.font_label)
        self.boottime_label_value = Label(master, text="{}".format(boottime().strftime("%b %d %Y, %H:%M:%S")),
                                          font=self.font_value)
        self.gui_widgets.append(self.boottime_label)
        self.gui_value_widgets.append(self.boottime_label_value)

        # SYSTEM CLOCK
        self.time_label_text = "System Clock"
        self.time_label = Label(master, text="{}:".format(self.time_label_text), font=self.font_label)
        self.time_label_value = Label(master, text=datetime.now().strftime("%H:%M:%S"), font=self.font_value)
        self.gui_widgets.append(self.time_label)
        self.gui_value_widgets.append(self.time_label_value)

        # Loop through widgets and add to grid (col 0).
        self.count = 0
        for i in self.gui_widgets:
            i.grid(sticky="w", row=self.count, column=0, padx=(8, 0), pady=(2, 0))
            self.count += 1
        # Loop through widgets and add to grid (col 1).
        self.count = 0
        for i in self.gui_value_widgets:
            i.grid(sticky="w", row=self.count, column=1, padx=(16, 8), pady=(2, 0))
            self.count += 1

        # Create exit button.
        # Doesn't need a value and has custom position; not appended to GUI widget lists.
        self.close_button = Button(master, text="EXIT", font=self.font_value, command=master.quit)
        self.close_button.grid(row=self.count, column=0, sticky="w", padx=(8, 0), pady=(8, 8))

        # Create toggle for "Always On Top" window.
        # Doesn't need a value and has custom position; not appended to GUI widget lists.
        self.on_top_check = IntVar(value=1)  # Defaults to checked.
        self.always_on_top = Checkbutton(master, text="Always On Top", font=self.font_value, variable=self.on_top_check,
                                         command=self.update_on_top)
        self.always_on_top.grid(row=self.count, column=1, sticky="w", padx=(14, 0), pady=(8, 8))

        # Start system metric update loop - calls self.get_metrics().
        master.after(1000, self.get_metrics)

    def get_metrics(self):
        """Update system metric GUI elements once per second."""
        # Gather metrics.
        cpu = psu.cpu_percent()
        memory = psu.virtual_memory()[2]
        uptime_var = str(datetime.now() - boottime())[:-7]
        boottime_var = boottime().strftime("%b %d %Y, %H:%M:%S")
        time = datetime.now().strftime("%H:%M:%S")

        # CPU (red text when >90%)
        self.cpu_label_value.configure(text=cpu)
        if cpu >= 90.0:
            self.cpu_label_value.configure(fg="red")
        else:
            self.cpu_label_value.configure(fg="black")

        # MEMORY (red text when >90%)
        self.virtual_memory_label_value.configure(text=memory)
        if memory >= 90.0:
            self.virtual_memory_label_value.configure(fg="red")
        else:
            self.virtual_memory_label_value.configure(fg="black")

        # UPTIME
        self.uptime_label_value.configure(text=uptime_var)

        # BOOT TIME
        self.boottime_label_value.configure(text=boottime_var)

        # SYSTEM CLOCK
        self.time_label_value.configure(text=time)

        self.master.after(1000, self.get_metrics)  # Continue calling this function every second.

    def update_on_top(self):
        """Set if window is Always On Top (master.attributes('-topmost')) based on checkbox."""
        if self.on_top_check.get() == 1:
            self.master.attributes("-topmost", "true")
        else:
            self.master.attributes("-topmost", "false")
