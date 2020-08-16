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
ENTER_BATTLE = 1
ENTER_NONE = 0
ENTER_NEXT = 2

EQUIPED = 1
NOT_EQUIPED = -1
CLEAR_ALL = -2
EXIT = 0


def story():
	tkinit()
	i = 0

	cmd_char = input(_("CHOOSE EPISODE?(NUMBER, 0-10)>"))
	try:
		i = int(cmd_char)
	except ValueError:
		pass
		
	if i > 10 or i == "":
		story()

	story_level = i
	
	while 1:
		i = enter_episode(story_level)
		if i == ENTER_BATTLE:
			if battle_system.main(story_level):
				if story_level != 10:
					print_victory()
					story_level += 1
				else:
					tkmessage("", _("DEA LILIUM was defeated. Your power can make you be the god of this universe. The destiny of the universe are on your hand..."))
					time.sleep(6)
					sys.exit(0)
		elif i == ENTER_NEXT:
			story_level += 1
		else:
			pass

def enter_episode(story_id=0):
	story_path = "./Stories/"

	story = [
		"ep0",
		"ep1",
		"ep2",
		"ep3",
		"ep4",
		"ep5",
		"ep6",
		"ep7",
		"ep8",
		"ep9",
		"ep10"
	]
	
	enemy_id = [
		0,
		1,
		2,
		3,
		4,
		5,
		6,
		7,
		8,
		9,
		10
	]

	storyfile_suffix = ".txt"
	
	
	if not enter_episode.is_shown:
		for i in open(story_path + story[story_id] + _("_en") + storyfile_suffix, encoding='utf-8'):
			if story_id != 10:
				print(i, end="")
				sys.stdout.flush()
			else:
				tkmessage(_("DEA LILIUM"), i)
		print("")
			
	enter_episode.is_shown = True	
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
		if i == SCENE_BATTLE:
			if story_id == 0:
				return ENTER_NEXT
			return ENTER_BATTLE
		elif i == SCENE_INVENTORY:
			print_all_weapons()
			while 1:
				i = choose_weapon()
				if i == EXIT:
					break
		elif not i:
			return ENTER_NONE
		else:
			return ENTER_NONE

enter_episode.is_shown = False
	
def set_inventory(story_id=0):
	if story_id == 1:
		set_weapons([0, 2])
	elif story_id == 2:
		set_weapons([0, 1, 2, 3])
	elif story_id == 3:
		set_weapons([0, 1, 2, 3, 4, 6])
	elif story_id == 4:
		set_weapons([0, 1, 2, 3, 4, 5, 6, 7])
	elif story_id == 5:
		set_weapons([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
	elif story_id == 6:
		set_weapons([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
	elif story_id == 7:
		set_weapons([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
	elif story_id == 8:
		set_weapons([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
	elif story_id == 9:
		set_weapons([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17])
	elif story_id == 10:
		set_weapons([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 22])
		
def set_weapons(weapon_ids):
	for i in weapon_ids:
		Party.add_weapon(i)
		
def auto_equip(story_id):
	weapon_ids = []
	if story_id == 1:
		weapon_ids = [0, 2]
	elif story_id == 2:
		weapon_ids = [0, 1, 2, 3]
	elif story_id == 3:
		weapon_ids = [4, 6, 2, 3]
	elif story_id == 4:
		weapon_ids = [5, 7, 6, 4]
	elif story_id == 5:
		weapon_ids = [9, 8, 7, 6]
	elif story_id == 6:
		weapon_ids = [11, 10, 9, 8]
	elif story_id == 7:
		weapon_ids = [13, 12, 11, 10]
	elif story_id == 8:
		weapon_ids = [14, 15, 13, 12]
	elif story_id == 9:
		weapon_ids = [16, 17, 15, 14]
	elif story_id == 10:
		weapon_ids = [22, 18, 19, 17]
		
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
	print(_("(If disarmed and exit, system will equip recommend weapons.)"))
		
def choose_weapon():
	print_inventory_tips()
	cmd_char = input(_("INVENTORY COMMAND?>"))
	if cmd_char == "0":
		return EXIT
	elif cmd_char == "d":
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
	cmd_char = input(_("COMMAND?>")).lower()
	if cmd_char == "e":
		return SCENE_BATTLE
	elif cmd_char == "i":
		return SCENE_INVENTORY
	else:
		return SCENE_NONE
