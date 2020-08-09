import gamedb
import time
import sys

def print_hugebar(s=""):
	print(s.center(80, "="))
	
def print_bar(s=""):
	print(s.center(80, "-"))


def translate(key):
	if key in gamedb.STR_ZH and gamedb.LANG_ZH:
		return gamedb.STR_ZH[key]
	return key
	
def wait_and_flush(second=0.03):
	time.sleep(second)
	sys.stdout.flush()