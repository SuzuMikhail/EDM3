import random
import sys
import time

import story_panel

from gamedb import *

weapons = []
battlers = []
covers = []
status = []
skills = []

def init():
	global weapons
	for i in WEAPONS:
		weapons.append(Weapon(i[0], i[1], i[2], i[3], i[4], i[5], i[6]))
		
	global covers
	for i in COVERS:
		covers.append(Cover(i[0], i[1], i[2], i[3], i[4]))
			
	global battlers
	battlers.append(Battler("You", HERO[0]))
	battlers.append(Battler(BOSSES[0][0], BOSSES[0][1], BOSSES[0][2], BOSSES[0][3]))
	battlers[0].equip_weapon(weapons[0])
	battlers[0].equip_weapon(weapons[2])
	battlers[1].equip_weapon(weapons[1])
	battlers[1].equip_weapon(weapons[3])
	#battlers[1].hold_weapon(0)

	global status
	status.append(Status("BURN", 5, -5, -5, hp_change=-150))
	status.append(Status("SHOCK", 5, -25, -25, False, -20))
	status.append(Status("HEALING", 5, 0, 0, hp_change=100))
	status.append(Status("HEALING+", 600, 0, 0, hp_change=80))

	global skills
	for i in SKILLS:
		if i[3]:
			skills.append(Skill(i[0], i[1], i[2], status[i[3]], i[4]))
		else:
			skills.append(Skill(i[0], i[1], i[2], None, i[4]))
	skills[1].hp_cost = -int(battlers[0].hp / 5)
	skills[3].hp_cost = -int(battlers[0].hp / 3)

	for i in skills:
		battlers[0].add_skill(i)
		
	battlers[1].add_status(status[3])

def print_hugebar(s=""):
	print(s.center(80, "="))
	
def print_bar(s=""):
	print(s.center(80, "-"))

def print_without_enter(s=""):
	print(s, end="")

def attack(target, hp):
	target.hp_change(-hp)
	return True
	
def get_rate():
	return random.randrange(101)
	
def get_attacker_final_hit_percent(attacker):
	attacker_hit_bouns = 0
	wp = attacker.get_current_weapon()
	if attacker.is_covered():
		attacker_hit_bouns += attacker.cover_object.get_hit_bouns()
	return attacker.hit_percent + wp.hit_percent_bouns + attacker_hit_bouns
	
def get_target_final_evade_percent(target):
	target_evade_bouns = 0
	if target.is_covered():
		target_cover = target.cover_object
		target_evade_bouns += target_cover.get_evade_bouns()
	return target.evade_percent + target_evade_bouns
	
def attack_in_turn(attacker, target):
	total_damage = 0
	total_hit = 0
	
	wp = attacker.get_current_weapon()
	rps = wp.rps
	orig_dmg = wp.dmg
	critical_percent = wp.critical_percent
	
	dmg = orig_dmg
	
	target_is_covered = target.is_covered()
	target_cover = None
	
	if target_is_covered:
		target_cover = target.cover_object
	
	if wp:
		for i in range(rps):
			if wp.fire():
				attacker_hit_percent = get_attacker_final_hit_percent(attacker)
				target_evade_percent = get_target_final_evade_percent(target)
	
				if get_rate() <= attacker_hit_percent:
					if get_rate() >= target_evade_percent:
						if get_rate() <= critical_percent:
							dmg *= int(Weapon.CRITICAL_BONUS_PERCENT / 100)
							print_without_enter(COLORS.YELLOW)
							
						print("{:>4} ".format(dmg), end="")
						
						if attack(target, dmg):
							total_hit += 1
							total_damage += dmg
					else:
						print_without_enter(COLORS.CYAN)
						print("EVAD ", end="")
				else:
					print_without_enter(COLORS.BLUE)
					print("MISS ", end="")
					
					
				if target_is_covered: #If evade or missed, cover takes damage
					target_cover.hp_change(-dmg)
			else:
				print_without_enter(COLORS.RED)
				print(">AMMO OUT<")
				print_without_enter(COLORS.ENDC)
				break
				
			print_without_enter(COLORS.ENDC)
			
			dmg = orig_dmg #Clear critical bonus
			
			if (i + 1) % 10 == 0:
				print("", end="\n")
			
	return total_hit, total_damage

def show_damage(hit, dmg):
	print("(%s hit, %s damage)" % (hit, dmg))
	
def show_covers():
	print_hugebar("COVER")
	print("{:<6} {:<10} {:<6}   {:<6} {:<9} {:<9}".format("INDEX", "NAME", "HP", "MAXHP", "HITMAX%", "EVADEMAX%"))
	for i, j in enumerate(covers):
		name = j.name
		hp = j.hp
		maxhp = j.maxhp
		hit_bouns = j.hit_bouns
		evade_bouns = j.evade_bouns
		print("{:<6} {:<10} {:<6} / {:<6} {:<9} {:<9}".format(i + 1, name, hp, maxhp, hit_bouns, evade_bouns))
		
	print_hugebar()
	
def choose_covers():
	print("[W]:Leave cover, [`][0]:Exit")
	id = input("COVER COMMAND:>")
	if id is "`" or id is "0":
		return False
	if id is "w":
		if battlers[0].is_covered():
			print("[LEAVE COVER]")
			battlers[0].leave_cover()
			return True
		else:
			print("[NOT COVERED]")
			return False
		
	id = int(id)
	id -= 1
	if covers[id].is_dead():
		print_without_enter(COLORS.RED)
		print("[COVER IS NOT USABLE]")
		print_without_enter(COLORS.ENDC)
		return False
	
	c = covers[id]
	battlers[0].cover_object = c
	print("Cover changed to: %s " % c.name)
	return True
	
def battler_reload(battler):
	print_without_enter(COLORS.GREEN)
	print("[RELOADING]")
	print_without_enter(COLORS.ENDC)
	wp = battler.get_current_weapon()
	wp.reload()
	
def battler_switch_weapon(battler, id):
	wp = battler.get_current_weapon()
	if not battler.is_equip_weapon(id - 1):
		print("[NO WEAPON IN SLOT]")
		return False
	print_without_enter(COLORS.GREEN)
	print("[SWITCH WEAPON TO %s]" % wp.name)
	print_without_enter(COLORS.ENDC)
	battler.hold_weapon(id - 1)
	return True
	
def print_playerinfo():
	print_hugebar("INFO")
	print("{:<10}".format(battlers[0].name))
	print_bar("WEAPONS")
	print_currentweapon(battlers[0], True)
	print_bar("SKILLS")
	print_skills(battlers[0])
	
def use_skill(id):
	s = battlers[0].skills[id]
	print(s.cooldown)
	print(s.cooldown_turn)
	if not s.is_cooldown():
		return False
	
	s.set_cooldown()
	battlers[0].hp_change(-s.hp_cost)
	if s.status:
		battlers[1].add_status(s.status)
	
	print_bar("SKILL")
	print_without_enter(COLORS.YELLOW)
	print("%s" % s.name)
	print_without_enter(COLORS.ENDC)
	return True
	
def command_perform(cmd_char):
	if cmd_char is "w":
		wp = battlers[0].get_current_weapon()
		if wp.is_magazine_empty():
			print(">AMMO OUT<")
			return False
		else:
			hit, dmg = attack_in_turn(battlers[0], battlers[1])
			show_damage(hit, dmg)
			return True
	elif cmd_char is "s":
		show_covers()
		if choose_covers():
			return True
		return False
	elif cmd_char is "r":
		battler_reload(battlers[0])
		return True
	elif cmd_char is "z":
		return use_skill(0)
	elif cmd_char is "x":
		return use_skill(1)
	elif cmd_char is "c":
		return use_skill(2)
	elif cmd_char is "v":
		return use_skill(3)
	elif cmd_char is "i":
		print_playerinfo()
		return False
	elif cmd_char is "1":
		if battler_switch_weapon(battlers[0], 1):
			return True
		return False
	elif cmd_char is "2":
		if battler_switch_weapon(battlers[0], 2):
			return True
		return False
	elif cmd_char is "3":
		if battler_switch_weapon(battlers[0], 3):
			return True
		return False
	elif cmd_char is "4":
		if battler_switch_weapon(battlers[0], 4):
			return True
		return False
	else:
		return False
		
	return True
	
def enemy_action():
	if battlers[1].is_movable == False:
		print("[SHOCKED]")
		return
	wp = battlers[1].get_current_weapon()
	if wp.is_magazine_empty():
		battler_reload(battlers[1])
		return 
	hit, dmg = attack_in_turn(battlers[1], battlers[0])
	show_damage(hit, dmg)
	
def is_win(battlers):
	if battlers[0].is_dead():
		print("You are dead")
		return -1
	elif battlers[1].is_dead():
		print("Enemy down")
		return 1
	else:
		return 0
		
def check_win():
	party_state = is_win(battlers)
	if party_state < 0:
		print("You lose")
		sys.exit()
	elif party_state > 0:
		print("You win")
		sys.exit()
		
def check_cover(battler):
	if not battler.is_covered():
		return
	c = battler.cover_object
	if c.is_dead():
		print_without_enter(COLORS.RED)
		print("[COVER IS BROKEN]")
		print_without_enter(COLORS.ENDC)
		battler.leave_cover()
		
def check_status():
	for i in battlers:
		if not i.status:
			continue
		
		print_bar("STATUS EFFECT")
		for id, j in enumerate(i.status):
			if j.is_dead():
				i.remove_hit_bouns()
				i.remove_evade_bouns()
				i.is_movable = True
				i.remove_status(id)
			else:
				i.hp_change(j.hp_change)
				i.add_hit_bouns(j.hit_bouns)
				i.add_evade_bouns(j.evade_bouns)
				i.is_movable = j.is_movable
				
				print("%s MP + %s" % (i.name, j.hp_change))
				
			j.reduce_keep_turn()
			
		
def update_skill_cooldown():
	for i in battlers[0].skills:
		if not i.is_cooldown():
			i.reduce_keep_turn()
		
def print_battlersStatus():
	print("{:<20} {:<6}   {:<6} {:<6}".format("NAME", "MANA", "MAXMN", "STATUS"))
	for i in range(2):
		name = battlers[i].name
		hp = battlers[i].hp
		maxhp = battlers[i].maxhp
		
		if hp <= int(maxhp / 3):
				print_without_enter(COLORS.RED)
				
		print("{:<20} {:<6} / {:<6}".format(name, hp, maxhp), end="")
		
		for i in battlers[i].status:
			
			print(i.name, end=" ")
			
		print_without_enter(COLORS.ENDC)
		print("")
		
		
def print_final_percent():
	print("HIT%: {:<4} EVADE%: {:<4}".format(get_attacker_final_hit_percent(battlers[0]), get_target_final_evade_percent(battlers[0])))
	
def print_currentweapon(battler, detail=False):
	if detail:
		print("{:<3} {:<15} {:<4} {:<4} {:<5} {:<8}".format("ID", "NAME", "DMG", "DPS", "AMMO", "MAX"))
	else:
		print("{:<3} {:<15} {:<5} {:<8}".format("ID", "NAME", "AMMO", "MAX"))
	for j, i in enumerate(battler.weapons):
		name = i.name
		dmg = i.dmg
		rps = i.rps
		ammo = i.ammo
		max_ammo = i.max_ammo
		desc = i.desc
		if j is battler.current_weapon_id:
			print(COLORS.GREEN, end="")
		if detail:
			print("[{:<1}] {:<15} {:<4} {:<4} {:<5} {:<8}".format((j + 1), name, dmg, rps, ammo, max_ammo))
			print("    " + i.desc)
		else:
			print("[{:<1}] {:<15} {:<5} {:<8}".format((j + 1), name, ammo, max_ammo))
		print(COLORS.ENDC, end="")
		
def print_currentCover(battler):
	print("Current cover: ", end="")
	if battler.is_covered():
		c = battler.cover_object
		print("{:<10} {:<6} / {:<6}".format(c.name, c.hp, c.maxhp))
		return
	print_without_enter(COLORS.RED)
	print(" NO COVER")
	print_without_enter(COLORS.ENDC)
	
def print_skills(battler):
	print("{:<10} {:<8}".format("NAME", "MP COST"))
	for i in battler.skills:
		print("{:<10} {:<8}".format(i.name, i.hp_cost))
		print("    " + i.desc)

def print_commands():
	print("{:<15} {:<15} {:<15} {:<15} {:<15}".format("[1]-[4]", "Switch weapon", "", "", ""))
	print("{:<15} {:<15} {:<15} {:<15} {:<15}".format("", "[W]:FIRE", "", "[R]:RELOAD", "[I]:INFO"))
	print("{:<15} {:<15} {:<15} {:<15} {:<15}".format("", "[S]:TAKE COVER", "", "", ""))
	if not battlers[0].skills:
		return
	print("{:<15} {:<15} {:<15} {:<15} {:<15}".format("[Z]:" + skills[0].name,
												"[X]:" + skills[1].name, 
												"[C]:" + skills[2].name,
												"[V]:" + skills[3].name,
												"SKILLS"))
	print("{:<15} {:<15} {:<15} {:<15} {:<15}".format(skills[0].hp_cost,
												skills[1].hp_cost, 
												skills[2].hp_cost,
												skills[3].hp_cost,
												"HP COST"))
	print_without_enter(COLORS.GREEN)
	print("{:<15} {:<15} {:<15} {:<15} {:<15}".format(skills[0].cooldown,
												skills[1].cooldown, 
												skills[2].cooldown,
												skills[3].cooldown,
												"COOLDOWN"))
	print_without_enter(COLORS.ENDC)

def battle_scene():
	turn = 0;
	
	while True:
		print_without_enter(COLORS.BOLD)
		print_hugebar("STATUS")
		print_without_enter(COLORS.ENDC)
		print("[Second: %s]" % turn)
		print_battlersStatus()
		print_currentCover(battlers[0])
		#print_bar("APPROXIMATE HIT/EVADE %")
		#print_final_percent()
		print_hugebar()
		
		print_currentweapon(battlers[0])
		print_hugebar()
		print_commands()
		
		
		while 1:
			cmd = input("COMMAND?(LOW CASE)>")	
			if cmd:
				#print_bar("PLAYER ACTION")
				cmd_char = cmd[0]
				if command_perform(cmd_char):
					break
		
		
		check_win()
		check_cover(battlers[0])
		
		print_bar("ENEMY ACTION")
		enemy_action()
		
		check_status()
		update_skill_cooldown()

		check_win()
		check_cover(battlers[0])
		
		turn += 1
		print("\n\n\n")
			
		
def main():
	init()
	battle_scene()
	return
