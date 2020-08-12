import gamedb
import time
import sys
from tkinter import Tk
from tkinter import messagebox

root = Tk()
root.withdraw()

def tkinit():
	root = Tk() #tk window
	root.withdraw()
	
def tkmessage(name, msg):
	root.lower()
	root.attributes('-topmost', 1)              
	messagebox.showwarning(name, msg, parent=root)
	root.focus_set()
	#root.tkraise()
		

def print_hugebar(s=""):
	print(s.center(80, "="))
	
def print_bar(s=""):
	print(s.center(80, "-"))

def print_without_enter(s=""):
	print(s, end="")

def translate(key):
	if key in gamedb.STR_ZH and gamedb.LANG_ZH:
		return gamedb.STR_ZH[key]
	return key
	
def wait_and_flush(second=0.03):
	time.sleep(second)
	sys.stdout.flush()