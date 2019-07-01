# IMPORTS
from tkinter import *
from widgets import *
			
# MAIN
def main():
	root = Tk()
	root.geometry("+400+200")		# Window size and position
	root.resizable(False, False)			# Disable window resize
	root.title("sysmon")				# Window title
	root.attributes("-topmost", "true")		# Defaults window to "Always On Top"
	root.iconbitmap('monitor.ico')	# Set window icon
	gui = GUI(root)					# Create GUI object
	root.mainloop()					# Call main event loop
	
if __name__ == "__main__":
	main()