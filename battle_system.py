import random
import sys
import time

import story_panel
from common import *
from gamedb import *
from gamedb import equiped_weapons

_ = translate

weapons = []
battlers = []
covers = []
status = []
skills = []

def init(story_id):
	global weapons
	for i in WEAPONS:
		weapons.append(Weapon(_(i[0]), i[1], i[2], i[3], i[4], i[5], i[6]))
		
	global covers
	for i in COVERS:
		covers.append(Cover(_(i[0]), i[1], i[2], i[3], i[4]))

	global status
	for i in STATUS:
		status.append(Status(_(i[0]), i[1], i[2], i[3], i[4], i[5]))
	
	global battlers
	battlers.append(Battler(_("You"), HERO[story_id - 1]))
	
	battlers.append(Battler(_(BOSSES[story_id - 1][0]), BOSSES[story_id - 1][1], BOSSES[story_id - 1][2], BOSSES[story_id - 1][3]))
	for i in equiped_weapons:
		battlers[0].equip_weapon(weapons[i])
		
	global skills
	for i in SKILLS:
		if i[3] or i[3] == 0: #if status is none
			skills.append(Skill(_(i[0]), i[1], i[2], status[i[3]], i[4]))
		else:
			skills.append(Skill(_(i[0]), i[1], i[2], None, i[4]))
			
	skills[0].hp_cost = int(battlers[0].hp * 0.03)
	skills[1].hp_cost = -int(battlers[0].hp / 5)
	skills[2].hp_cost = int(battlers[0].hp * 0.04)
	skills[3].hp_cost = -int(battlers[0].hp / 3)
	
	for i in range(0, 4):
		battlers[0].add_skill(skills[i])
		
	if story_id == 1:
		battlers[1].equip_weapon(weapons[1])
		battlers[1].equip_weapon(weapons[3])
		battlers[1].add_status(status[3])
	elif story_id == 2:
		battlers[1].equip_weapon(weapons[4])
		battlers[1].equip_weapon(weapons[6])
		skills[4].hp_cost = int(battlers[1].hp * 0.05)
		battlers[1].add_skill(skills[4])
	elif story_id == 3:
		battlers[1].equip_weapon(weapons[7])
	elif story_id == 4:
		battlers[1].equip_weapon(weapons[9])
		battlers[1].equip_weapon(weapons[8])
		
		

		
	ready_for_next_fire = False
	player_lastturn_is_covered = False
	#enemy_action.hacking = False
	
def reset():
	weapons.clear()
	covers.clear()
	battlers.clear()
	status.clear()
	skills.clear()

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
						print(_("EVAD"), end=" ")
				else:
					print_without_enter(COLORS.BLUE)
					print(_("MISS"), end=" ")
					
					
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
				
			wait_and_flush(1 / rps)
			
			
	return total_hit, total_damage

def show_damage(hit, dmg):
	print("")
	print(_("(%s hit, %s damage)") % (hit, dmg))
	wait_and_flush()
	
def show_covers():
	print_hugebar("COVER")
	print("{:<3} {:<10} {:<6}   {:<6} {:<9} {:<9}".format("ID", _("NAME"), _("HP"), _("MAXHP"), _("HITMAX%"), _("EVADEMAX%")))
	for i, j in enumerate(covers):
		name = j.name
		hp = j.hp
		maxhp = j.maxhp
		hit_bouns = j.hit_bouns
		evade_bouns = j.evade_bouns
		print("{:<3} {:<10} {:<6} / {:<6} {:<9} {:<9}".format(i + 1, name, hp, maxhp, hit_bouns, evade_bouns))
		
	print_hugebar()
	
def choose_covers():
	print(_("[W]:Leave cover, [`][0]:Exit"))
	id = input(_("COVER COMMAND?>"))
	if id is "`" or id is "0":
		return False
	if id is "w":
		if battlers[0].is_covered():
			print(_("[LEAVE COVER]"))
			battlers[0].leave_cover()
			return True
		else:
			print(_("[NOT COVERED]"))
			return False
	
	try:
		id = int(id)
	except ValueError:
		print(_("PLEASE INPUT LEGAL COMMAND"))
		return False
		
	id -= 1
	if covers[id].is_dead():
		print_without_enter(COLORS.RED)
		print(_("[COVER IS NOT USABLE]"))
		print_without_enter(COLORS.ENDC)
		return False
		
	c = covers[id]
	battlers[0].cover_object = c
	print(_("Cover changed to: %s ") % c.name)
	
	if id is 4:
		for j, i in enumerate(battlers[0].status):
			if i.name is status[4].name:
				print(_("Fire was disappeared due to you jumped in sea."))
				remove_status(battlers[0], j)
	
	
	return True
	
def battler_reload(battler):
	print_without_enter(COLORS.GREEN)
	print(_("[RELOADING]"))
	print_without_enter(COLORS.ENDC)
	wp = battler.get_current_weapon()
	wp.reload()
	
def battler_switch_weapon(battler, id):
	wp = battler.get_current_weapon()
	if not battler.is_equip_weapon(id):
		print("[NO WEAPON IN SLOT]")
		return False
	print_without_enter(COLORS.GREEN)
	print(_("[SWITCH WEAPON TO %s]") % battler.weapons[id].name)
	print_without_enter(COLORS.ENDC)
	battler.hold_weapon(id)
	return True
	
def print_playerinfo():
	print_hugebar("INFO")
	print("{:<10}".format(battlers[0].name))
	print_bar("WEAPONS")
	print_currentweapon(battlers[0], True)
	print_bar("SKILLS")
	print_skills(battlers[0])
	
def use_skill(attacker, target, id):
	s = attacker.skills[id]
	if not s.is_cooldown():
		return False
	
	s.set_cooldown()
	attacker.hp_change(-s.hp_cost)
	if s.status:
		target.add_status(s.status)
	
	print_bar("SKILL")
	print_without_enter(COLORS.YELLOW)
	print(_("MP CHANGED: %s") % -s.hp_cost)
	print("%s" % s.name)
	print_without_enter(COLORS.ENDC)
	return True
	
def player_use_skill(id):
	return use_skill(battlers[0], battlers[1], id)
	
def command_perform(cmd_char):
	if cmd_char is "w":
		wp = battlers[0].get_current_weapon()
		if wp.is_magazine_empty():
			print(_(">AMMO OUT<"))
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
		return player_use_skill(0)
	elif cmd_char is "x":
		return player_use_skill(1)
	elif cmd_char is "c":
		return player_use_skill(2)
	elif cmd_char is "v":
		return player_use_skill(3)
	elif cmd_char is "i":
		print_playerinfo()
		return False
	elif cmd_char is "1":
		if battler_switch_weapon(battlers[0], 0):
			return True
		return False
	elif cmd_char is "2":
		if battler_switch_weapon(battlers[0], 1):
			return True
		return False
	elif cmd_char is "3":
		if battler_switch_weapon(battlers[0], 2):
			return True
		return False
	elif cmd_char is "4":
		if battler_switch_weapon(battlers[0], 3):
			return True
		return False
	else:
		return False
		
	return True
	

def enemy_action(story_id):
	if battlers[1].is_movable == False:
		print(_("[SHOCKED]"))
		return
	wp = battlers[1].get_current_weapon()
	
	if story_id == 1:
		if wp.is_magazine_empty():
			wp1 = battlers[1].weapons[0]
			wp2 = battlers[1].weapons[1]
			if wp1.is_magazine_empty() and wp2.is_magazine_empty():
				battlers[1].current_weapon_id = 0
				battler_reload(battlers[1])
				battlers[1].current_weapon_id = 1
				battler_reload(battlers[1])
				return
		
			if battlers[1].current_weapon_id == 0:
				battler_switch_weapon(battlers[1], 1)
			else:
				battler_switch_weapon(battlers[1], 0)
		
	elif story_id == 2:
		if wp.is_magazine_empty():
			battler_reload(battlers[1])
			return
			
		if not enemy_action.ready_for_next_fire:
			if wp.is_magazine_empty():
				battler_reload(battlers[1])
				return
				
			if battlers[0].is_covered():
				battler_switch_weapon(battlers[1], 1)
				enemy_action.ready_for_next_fire = True
				enemy_action.hold_rpg = True
				return
			else:
				if use_skill(battlers[1], battlers[0], 0):
					return
				if enemy_action.hold_rpg:
					battler_switch_weapon(battlers[1], 0)
					enemy_action.hold_rpg = False
					return
		else:
			enemy_action.ready_for_next_fire = False
	elif story_id == 3:
		if wp.is_magazine_empty():
			battler_reload(battlers[1])
			return
		
		if not enemy_action.hacking:
			if battlers[1].hp <= int(battlers[1].maxhp / 3):
				print(_("I have turn on my cheat program!"))
				battlers[1].add_status(status[5])
				enemy_action.hacking = True
				return
	elif story_id == 4:
		if wp.is_magazine_empty():
			battler_reload(battlers[1])
			return
		
	hit, dmg = attack_in_turn(battlers[1], battlers[0])
	show_damage(hit, dmg)
	
enemy_action.ready_for_next_fire = False
enemy_action.hold_rpg = False
enemy_action.hacking = False
	
	
def is_win(battlers):
	if battlers[0].is_dead():
		print_hugebar()
		print(_("You are dead"))
		return -1
	elif battlers[1].is_dead():
		print_hugebar()
		print(_("Enemy down"))
		return 1
	else:
		return 0
		
def check_win():
	party_state = is_win(battlers)
	if party_state < 0:
		print(_("You lose"))
		print_hugebar()
		return False
	elif party_state > 0:
		print(_("You win"))
		print_hugebar()
		return True
		
def check_cover(battler):
	if not battler.is_covered():
		return
	c = battler.cover_object
	if c.is_dead():
		print_without_enter(COLORS.RED)
		print(_("[COVER IS BROKEN]"))
		print_without_enter(COLORS.ENDC)
		battler.leave_cover()
		
def remove_status(battler, id):
	battler.remove_hit_bouns()
	battler.remove_evade_bouns()
	battler.remove_status(id)
		
		
def check_status():
	for i in battlers:
		if not i.status:
			continue
		
		print_bar("STATUS EFFECT")
		for id, j in enumerate(i.status):
			if j.is_dead():
				remove_status(i, id)
				i.is_movable = True
			else:
				hp_change = int(i.maxhp * (j.hp_change_percent / 100))
				i.hp_change(hp_change)
				i.add_hit_bouns(j.hit_bouns)
				i.add_evade_bouns(j.evade_bouns)
				if j.name != status[1].name:
					i.is_movable = j.is_movable
				
				print("%s MP + %s" % (i.name, hp_change))
				
			j.reduce_keep_turn()
			wait_and_flush()
	
	
			
		
def update_skill_cooldown():
	for i in battlers[0].skills:
		if not i.is_cooldown():
			i.reduce_keep_turn()
		
def print_battlersStatus():
	print("{:<}\t\t {:<}\t   {:<}\t {:<}".format(_("NAME"), _("MANA"), _("MAXMN"), _("STATUS")))
	for i in range(2):
		name = battlers[i].name
		hp = battlers[i].hp
		maxhp = battlers[i].maxhp
		
		if hp <= int(maxhp / 2):
			print_without_enter(COLORS.YELLOW)
		elif hp <= int(maxhp / 3):
			print_without_enter(COLORS.RED)	
				
		print("{:<}\t\t {:<}\t / {:<}\t ".format(name, hp, maxhp), end="")
		
		for i in battlers[i].status:
			
			print(i.name, end=" ")
			
		print_without_enter(COLORS.ENDC)
		print("")
		
		
def print_final_percent():
	print(_("HIT%: {:<4} EVADE%: {:<4}").format(get_attacker_final_hit_percent(battlers[0]), get_target_final_evade_percent(battlers[0])))
	
def print_currentweapon(battler, detail=False):
	if detail:
		print("{:<3} {:<15} {:<4} {:<4} {:<5} {:<8} {:<6} {:<6}".format("ID", _("NAME"), "DMG", "DPS", "AMMO", "MAX", "CRIT%", "HIT%"))
	else:
		print("{:<3} {:<15} {:<5} {:<8}".format("ID", _("NAME"), _("AMMO"), _("MAX")))
	for j, i in enumerate(battler.weapons): 
		name = i.name
		dmg = i.dmg
		rps = i.rps
		ammo = i.ammo
		max_ammo = i.max_ammo
		desc = i.desc
		if j is battler.current_weapon_id:
			print(COLORS.GREEN, end="")
		if ammo <= int(max_ammo / 4):
			print_without_enter(COLORS.RED)
	
		if detail:
			print("[{:<1}] {:<15} {:<4} {:<4} {:<5} {:<8} {:<6} {:<6}".format((j + 1), name, dmg, rps, ammo, max_ammo, i.critical_percent, i.hit_percent_bouns))
			print("    " + i.desc)
		else:
			print("[{:<1}] {:<15} {:<5} {:<8}".format((j + 1), name, ammo, max_ammo))
		print(COLORS.ENDC, end="")
		
def print_currentCover(battler):
	print(_("Current cover") + ": ", end="")
	if battler.is_covered():
		c = battler.cover_object
		print("{:<10} {:<6} / {:<6}".format(c.name, c.hp, c.maxhp))
		return
	print_without_enter(COLORS.RED)
	print(" NO COVER")
	print_without_enter(COLORS.ENDC)
	
def print_skills(battler):
	print("{:<10} {:<8}".format(_("NAME"), _("MP COST")))
	for i in battler.skills:
		print("{:<10} {:<8}".format(i.name, i.hp_cost))
		print("    " + i.desc)

def print_commands():
	print("{:<}\t {:<}\t {:<}\t {:<}\t {:<}".format("[1]-[4]", _("Switch weapon"), "", "", ""))
	print("{:<}\t {:<}\t {:<}\t {:<}\t {:<}".format("", "[W]:" + _("FIRE"), "", "[R]:" + _("RELOAD"), "[I]:INFO"))
	print("{:<}\t {:<}\t {:<}\t {:<}\t {:<}".format("", "[S]:" + _("TAKE COVER"), "", "", ""))
	if not battlers[0].skills:
		return
	print("{:<}\t {:<}\t {:<}\t {:<}\t {:<}".format("[Z]:" + skills[0].name,
												"[X]:" + skills[1].name, 
												"[C]:" + skills[2].name,
												"[V]:" + skills[3].name,
												_("SKILLS")))
	print("{:<}\t\t {:<}\t\t {:<}\t\t {:<}\t\t {:<}".format(skills[0].hp_cost,
												skills[1].hp_cost, 
												skills[2].hp_cost,
												skills[3].hp_cost,
												_("MP COST")))
	print_without_enter(COLORS.GREEN)
	print("{:<}\t\t {:<}\t\t {:<}\t\t {:<}\t\t {:<}".format(skills[0].cooldown,
												skills[1].cooldown, 
												skills[2].cooldown,
												skills[3].cooldown,
												_("COOLDOWN")))
	print_without_enter(COLORS.ENDC)

def battle_scene(story_id):
	turn = 0;
	
	while True:
		print_without_enter(COLORS.BOLD)
		print_hugebar("STATUS")
		print_without_enter(COLORS.ENDC)
		print("[" + _("SECOND") + ": %s]" % turn)
		print_battlersStatus()
		print_currentCover(battlers[0])
		print_bar(_("APPROXIMATE HIT/EVADE %"))
		print_final_percent()
		print_hugebar()
		
		print_currentweapon(battlers[0])
		print_hugebar()
		print_commands()
		
		
		while 1:
			cmd = input(_("COMMAND?(LOW CASE)>"))
			if cmd:
				#print_bar("PLAYER ACTION")
				cmd_char = cmd[0]
				if command_perform(cmd_char):
					break
		
		
		if check_win():
			return True
		elif check_win() == False:
			return False
			
		check_cover(battlers[0])
		
		print_bar("ENEMY ACTION")
		enemy_action(story_id)
		
		check_status()
		update_skill_cooldown()

		if check_win():
			return True
		elif check_win() == False:
			return False
			
			
		check_cover(battlers[0])
		
		turn += 1
		print("\n\n\n")
			
		
def main(story_id=1):
	init(story_id)
	if battle_scene(story_id):
		reset()
		return True
	else:
		reset()
		return False
		return alse
	
