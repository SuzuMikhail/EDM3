# -*- coding: utf-8 -*-

import time
import sys
from gamedb import COLORS
from gamedb import Weapon
from gamedb import WEAPONS
from gamedb import LEVEL_UP_MSG
from gamedb import NEWITEM_MSG
from gamedb import Party
from gamedb import party_weapons
from gamedb import equiped_weapons
import battle_system
from common import *


_ = translate
SCENE_NONE = 0
SCENE_BATTLE = 1
SCENE_INVENTORY = 2

EQUIPED = 1
NOT_EQUIPED = -1
CLEAR_ALL = -2
EXIT = 0


def story():
	story_level = 3
	while 1:
		if enter_episode(story_level):
			if battle_system.main(story_level):
				print_victory()
				story_level += 1
		

def enter_episode(story_id=0):
	story_path = "./Stories/"

	story = [
		"ep0",
		"ep1",
		"ep2",
		"ep3",
	]
	
	enemy_id = [
		0,
		1,
		2,
		3,
	]

	storyfile_suffix = ".txt"
	
	for i in open(story_path + story[story_id] + _("_en") + storyfile_suffix, encoding='utf-8'):
		print(i, end="")
		sys.stdout.flush()
		#time.sleep(.6)
	print("")
	
	inventory_is_ok = False

	while 1:
		if not inventory_is_ok:
			set_inventory(story_id)
			inventory_is_ok = True
			
		if not Party.is_equiped():
			print_without_enter(COLORS.GREEN)
			print(_("[No weapon equiped, weapon was equiped automatically.]"))
			print_without_enter(COLORS.ENDC)
			auto_equip(story_id)
			
		i = main_menu() 
		if i is SCENE_BATTLE:
			if enemy_id[story_id] == 0:
				return False
			return True
		elif i is SCENE_INVENTORY:
			print_all_weapons()
			while 1:
				i = choose_weapon()
				if i is EXIT:
					break
			#return False
		else:
			return False
	
def set_inventory(story_id=0):
	if story_id == 1:
		set_weapons([0, 2])
	elif story_id == 2:
		set_weapons([0, 1, 2, 3])
	elif story_id == 3:
		set_weapons([0, 1, 2, 3, 4, 6])
		
def set_weapons(weapon_ids):
	for i in weapon_ids:
		Party.add_weapon(i)
		
def auto_equip(story_id):
	weapon_ids = []
	if story_id == 1:
		weapon_ids = [0, 2, 5]
	elif story_id == 2:
		weapon_ids = [0, 1, 2, 3]
	elif story_id == 3:
		weapon_ids = [4, 6, 2, 3]
		
	for i in weapon_ids:
		Party.equip_weapon(i)
		
def equip_wp(id):
	i = Party.equiped_weapons_len()
	if i < 4:
		Party.equip_weapon(id)
		return True
	else:
		print_without_enter(COLORS.RED)
		print(_("[SLOT IS FULL]"))
		print_without_enter(COLORS.ENDC)
		return False
		
		
def print_all_weapons():
	print_hugebar("ALL WEAPONS")
	print("%s  %s\t\t %s\t %s\t %s\t %s\t %s" % ("ID", _("NAME"), _("DMG"), _("RPS"), _("AMMO"), _("CRIT%"), _("HIT%")))
	for j, i in enumerate(party_weapons):
		print("%s  %s\t %s\t %s\t %s\t %s\t %s" % (j + 1, _(WEAPONS[i][0]), WEAPONS[i][2], WEAPONS[i][3], WEAPONS[i][4], WEAPONS[i][5], WEAPONS[i][6]))
	print_equiped_weapons()

def print_equiped_weapons():
	print_hugebar("EQUIPED WEAPONS")
	for j, i in enumerate(equiped_weapons):
		print("%s  %s\t %s\t %s\t %s\t %s\t %s" % (j + 1, _(WEAPONS[i][0]), WEAPONS[i][2], WEAPONS[i][3], WEAPONS[i][4], WEAPONS[i][5], WEAPONS[i][6]))

def print_inventory_tips():
	print(_("[NUMBERS]: Equip, [D]: Disarm all, [0]: Exit"))
		
def choose_weapon():
	print_inventory_tips()
	cmd_char = input(_("INVENTORY COMMAND?(LOW CASE)>"))
	if cmd_char is "0":
		return EXIT
	elif cmd_char is "d":
		if equiped_weapons:
			print_without_enter(COLORS.GREEN)
			print(_("All weapon was disarmed."))
			print_without_enter(COLORS.ENDC)
			Party.unequip_all()
			return CLEAR_ALL
	else:
		try:
			i = int(cmd_char)
			if (i - 1) <= len(party_weapons):
				id = party_weapons[i - 1]
				#print("ID ", id)
				if id in party_weapons:
					if equip_wp(id):
						print(_("Equiped %s") % _(WEAPONS[id][0]))
					print_equiped_weapons()
					return EQUIPED
				else:
					print("NOT EQUIPED")
					return NOT_EQUIPED
		except ValueError:
			print(_("PLEASE INPUT LEGAL COMMAND"))
			return NOT_EQUIPED
			
		
	
def print_victory(story_id=0):
	print_hugebar()
	print(_(LEVEL_UP_MSG))
	print(_(NEWITEM_MSG))
	
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