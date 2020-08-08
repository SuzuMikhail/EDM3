# -*- coding: utf-8 -*-

import time
import sys
from gamedb import LEVEL_UP_MSG
import battle_system
import common

_ = common.translate

def story():
	story_level = 1
	while 1:
		if enter_episode(story_level):
			if battle_system.main():
				story_level += 1
		

def enter_episode(story_id=0):
	story_path = "./Stories/"

	story = [
		"ep0",
		"ep1"
	]
	
	enemy_id = [
		0,
		1,
	]

	storyfile_suffix = ".txt"
	
	for i in open(story_path + story[story_id] + _("_en") + storyfile_suffix, encoding='utf-8'):
		print(i, end="")
		sys.stdout.flush()
		time.sleep(.6)
	print("")

	while 1:
		if main_menu():
			if enemy_id[story_id] == 0:
				return False
			return True
	
def print_victory(story_id=0):
	print(LEVEL_UP_MSG)
	
def print_main_menu():
	print("{:<15} {:<15} {:<15}".format("", "[E]:" + _("NEXT"), "[I]:" + _("INVENTORY")))
	
def main_menu():
	print_main_menu()
	cmd_char = input(_("COMMAND?(LOW CASE)>"))
	if cmd_char is "e":
		return True
	elif cmd_char is "i":
		return False
	else:
		return False