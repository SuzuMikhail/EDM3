# -*- coding: utf-8 -*-

import time
import sys
from gamedb import Weapon
from gamedb import WEAPONS
from gamedb import LEVEL_UP_MSG
from gamedb import Party
from gamedb import party_weapons
import battle_system
import common

_ = common.translate
SCENE_NONE = 0
SCENE_BATTLE = 1
SCENE_INVENTORY = 2


def story():
	story_level = 1
	while 1:
		if enter_episode(story_level):
			if battle_system.main(story_level):
				story_level += 1
		

def enter_episode(story_id=0):
	story_path = "./Stories/"

	story = [
		"ep0",
		"ep1",
		"ep2",
	]
	
	enemy_id = [
		0,
		1,
		2,
	]

	storyfile_suffix = ".txt"
	
	for i in open(story_path + story[story_id] + _("_en") + storyfile_suffix, encoding='utf-8'):
		print(i, end="")
		sys.stdout.flush()
		#time.sleep(.6)
	print("")

	while 1:
		set_inventory(story_id)
		if not Party.is_equiped():
			print("No weapon equiped, equiped weapon automatically.")
			auto_equip(story_id)
			
		i = main_menu() 
		if i is SCENE_BATTLE:
			if enemy_id[story_id] == 0:
				return False
			return True
		elif i is SCENE_INVENTORY:
			print_all_weapons()
			return False
		else:
			return False
	
def set_inventory(story_id=0):
	party_weapons = []
	
	if story_id == 1:
		set_weapons([0, 2, 5])
	elif story_id == 2:
		set_weapons([0, 1, 2, 3, 5])
		
def set_weapons(weapon_ids):
	for i in weapon_ids:
		Party.add_weapon(i)
		
def auto_equip(story_id):
	weapon_ids = []
	if story_id == 1:
		weapon_ids = [0, 2, 5]
	elif story_id == 2:
		weapon_ids = [0, 1, 2, 3]
		
	for i in weapon_ids:
		Party.equip_weapon(i)
		
def print_all_weapons():
	print("%s  %s\t\t %s\t %s\t %s\t %s\t %s" % ("ID", _("NAME"), _("DMG"), _("RPS"), _("AMMO"), _("CRIT%"), _("HIT%")))
	for j, i in enumerate(party_weapons):
		print("%s  %s\t %s\t %s\t %s\t %s\t %s" % (j + 1, WEAPONS[i][0], WEAPONS[i][2], WEAPONS[i][3], WEAPONS[i][4], WEAPONS[i][5], WEAPONS[i][6]))
	
def print_victory(story_id=0):
	print(LEVEL_UP_MSG)
	
def print_main_menu():
	print("{:<15} {:<15} {:<15}".format("", "[E]:" + _("NEXT"), "[I]:" + _("INVENTORY")))
	
def main_menu():
	print_main_menu()
	cmd_char = input(_("COMMAND?(LOW CASE)>"))
	if cmd_char is "e":
		return SCENE_BATTLE
	elif cmd_char is "i":
		return SCENE_INVENTORY
	else:
		return SCENE_NONE