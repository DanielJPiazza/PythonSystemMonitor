from datetime import datetime
from tkinter import *
import psutil as psu

class GUI:
	def __init__(self, master):
		# Create GUI object.
		self.master = master
		
		# Lists for GUI widgets.
		self.gui_widgets = []
		self.gui_value_widgets = []
				
		# Get CPU percentage and apply it to a tkinter label.
		# Variable structure is the same for most widgets.
		self.cpu_label_text = "CPU"
		self.cpu_label = Label(master, text="{}:".format(self.cpu_label_text))
		self.cpu_label_value = Label(master, text="{}%".format(psu.cpu_percent()))
		self.gui_widgets.append(self.cpu_label)
		self.gui_value_widgets.append(self.cpu_label_value)
		
		# Get virtual memory percentage and apply it to a tkinter label.
		self. mem_label_text = "Virtual Memory"
		self.virtual_memory_label = Label(master, text="{}:".format(self.mem_label_text))
		self.virtual_memory_label_value = Label(master, text="{}%".format(psu.virtual_memory()[2]))
		self.gui_widgets.append(self.virtual_memory_label)
		self.gui_value_widgets.append(self.virtual_memory_label_value)
		
		# Get system time and apply it to a tkinter label.
		self.time_label_text = "System Clock"
		self.time_label = Label(master, text="{}:".format(self.time_label_text))
		self.time_label_value = Label(master, text=datetime.now().strftime("%H:%M:%S"))
		self.gui_widgets.append(self.time_label)
		self.gui_value_widgets.append(self.time_label_value)
		
		# Loop through widgets and add to grid (col 0).
		self.count = 0
		for i in self.gui_widgets:
			i.grid(sticky="w", row=self.count, column=0, padx=2, pady=2)
			self.count += 1
		# Loop through widgets and add to grid (col 1).
		self.count = 0
		for i in self.gui_value_widgets:
			i.grid(sticky="w", row=self.count, column=1, padx=10, pady=2)
			self.count += 1
			
		# Create an exit button.
		# Doesn't need a value and has custom position; not appended to GUI widget lists.
		self.close_button = Button(master, text="EXIT", command=master.quit)
		self.close_button.grid(row=self.count, column=0, sticky="w", padx=4)
		
		# Start system metric update loop - calls self.get_metrics().
		root.after(1000, self.get_metrics)
		
	def get_metrics(self):
		"""Update system metric GUI elements once per second."""
		self.cpu_label_value.configure(text="{}%".format(psu.cpu_percent()))
		self.virtual_memory_label_value.configure(text="{}%".format(psu.virtual_memory()[2]))
		self.time_label_value.configure(text=datetime.now().strftime("%H:%M:%S"))
		root.after(1000, self.get_metrics)	# Continue to call this function every second.	
		
# Create tkinter root / GUI object and call the main event loop.
root = Tk()
root.geometry("200x106+400+200")	# Window size and position
root.resizable(False, False)		# Disable window resize
root.title("sm.py")					# Window title
gui = GUI(root)
root.mainloop()