import random
import sys
import time

import story_panel

class COLORS:
	ENDC = '\033[0m'
	RED = '\033[91m'
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	BLUE = '\033[94m'
	MAGENTA = '\033[95m'
	CYAN = '\033[96m'
	BOLD = '\033[01m'

class Battler:
	def __init__(self, name, maxhp, orig_hit_percent=95, orig_evade_percent=30):
		self.name = name
		self.hp = maxhp;
		self.maxhp = maxhp
		self.orig_hit_percent = orig_hit_percent
		self.orig_evade_percent = orig_evade_percent
		self.hit_percent = orig_hit_percent
		self.evade_percent = orig_evade_percent
		self.weapons = []
		self.current_weapon_id = 0
		self.cover = 0
		self.cover_object = None
		self.status = []
		self.skills = []
		self.is_movable = True
		
	def is_dead(self):
		if self.hp <= 0:
			return True
		return False
		
	def hp_change(self, hp):
		current_hp = self.hp + hp
		if current_hp > self.maxhp:
			return
		self.hp += hp
		
	def get_current_weapon(self):
		wp = self.weapons[self.current_weapon_id]
		if wp:
			return wp;
		return None
		
	def hold_weapon(self, id):
		self.current_weapon_id = id
		
	def equip_weapon(self, weapon):
		self.weapons.append(weapon)
		
	def is_equip_weapon(self, id):
		if id > (len(self.weapons) - 1):
			return False
		return True
	
	def remove_weapon(self, id):
		del self.weapons[id]
		
	def add_skill(self, skill):
		self.skills.append(skill)
	
	def remove_skill(self, id):
		del self.skills[id]
		
	def is_covered(self):
		if self.cover_object:
			return True
		return False
		
	def take_cover(self, cover):
		self.cover_object = cover
		
	def leave_cover(self):
		self.cover_object = None
		
	def add_status(self, status):
		self.status.append(status)
	
	def remove_status(self, id):
		del self.status[id]
		
	def add_hit_bouns(self, value):
		self.hit_percent += value
		
	def remove_hit_bouns(self):
		self.hit_percent = self.orig_hit_percent
		
	def add_evade_bouns(self, value):
		self.evade_percent += value
		
	def remove_evade_bouns(self):
		self.evade_percent = self.orig_evade_percent
		
		
		
class Weapon:
	CRITICAL_BONUS_PERCENT = 200
	
	def __init__(self, name, desc, dmg, rps, ammo, critical_percent=0, hit_percent_bouns=0):
		self.name = name
		self.desc = desc
		self.dmg = dmg
		self.rps = rps
		self.ammo = ammo
		self.max_ammo = ammo
		self.critical_percent = critical_percent
		self.hit_percent_bouns = hit_percent_bouns
		
	def fire(self):
		if not self.is_magazine_empty():
			self.ammo -= 1
			return True
		return False
				
	def is_magazine_empty(self):
		if self.ammo <= 0:
			return True
		return False
		
	def reload(self):
		self.ammo = self.max_ammo
		
class Cover:
	def __init__(self, name, maxhp, hit_bouns=100, evade_bouns=100, nodamage=False):
		self.name = name
		self.hp = maxhp
		self.maxhp = maxhp
		self.hit_bouns = hit_bouns
		self.evade_bouns = evade_bouns
		self.nodamage = nodamage
		
	def get_hit_bouns(self):
		hit_bouns = self.hit_bouns
		if self.hit_bouns == 0:
			return 0

		if self.hit_bouns < 0:
			hit_bouns = -self.hit_bouns
			
		i = random.randrange(0, hit_bouns)
		
		if self.hit_bouns < 0:
			return -i
		return i
	
	def get_evade_bouns(self):
		evade_bouns = self.evade_bouns
		if self.evade_bouns == 0:
			return 0
		if self.evade_bouns < 0:
			evade_bouns = -self.evade_bouns
			
		i = random.randrange(0, evade_bouns)
		
		if self.evade_bouns < 0:
			return -i
		return i
		
	def is_dead(self):
		if self.hp <= 0:
			return True
		return False
	
	def is_nodamage(self):
		return self.nodamage
		
	def hp_change(self, hp):
		if self.is_nodamage():
			return False
		self.hp += hp
		return True
		
class Status:
	def __init__(self, name, keep_turn=0, hit_bouns=0, evade_bouns=0, is_movable=True, hp_change=0):
		self.name = name
		self.hp = keep_turn
		self.keep_turn = keep_turn
		self.hit_bouns = hit_bouns
		self.evade_bouns = evade_bouns
		self.is_movable = is_movable
		self.hp_change = hp_change
		
	def reduce_keep_turn(self):
		self.hp -= 1
		
	def is_dead(self):
		if self.hp != 0:
			return False
		self.hp = self.keep_turn
		return True
		
		
class Skill:
	def __init__(self, name, desc="", hp_cost=0, status=None, cooldown_turn=0):
		self.name = name
		self.desc = desc
		self.cooldown = 0
		self.hp_cost = hp_cost
		self.status = status
		self.shield = None
		self.cooldown_turn = cooldown_turn
		
	def addShield(self, hp, hit_bouns=0, evade_bouns=0):
		self.shield = Shield(hp, hit_bouns, evade_bouns)
		
	def reduce_keep_turn(self):
		self.cooldown -= 1
		
	def set_cooldown(self):
		self.cooldown = self.cooldown_turn
		
	def is_cooldown(self):
		if self.cooldown != 0:
			return False
		return True
	
	
		
class Shield:
	def __init__(self, hp, hit_bouns=0, evade_bouns=0):
		self.hp = hp
		self.hit_bouns = 0
		self.evade_bouns = 0
	
weapons = []
battlers = []
covers = []
status = []
skills = []

def init():
	weapons.append(Weapon("5.56x45mm LMG", "A light machinegun made by Belgium", 8, 15, 300, 4))
	weapons.append(Weapon("7.62x39mm LMG", "A light machinegun made by USSR", 18, 10, 300, 12, -5))
	weapons.append(Weapon("12.7x99mm HMG", "A heavy machinegun made by USA", 30, 5, 100, 30, -30))
	weapons.append(Weapon("12.7x108mm HMG", "A heavy machinegun made by Russia", 40, 7, 100, 35, -35))
			

	battlers.append(Battler("You", 3000))
	battlers.append(Battler("New world godness", 9000, orig_evade_percent=25))
	battlers[0].equip_weapon(weapons[0])
	battlers[0].equip_weapon(weapons[2])
	battlers[1].equip_weapon(weapons[1])
	battlers[1].equip_weapon(weapons[3])
	#battlers[1].hold_weapon(0)


	covers.append(Cover("Forest", 10000, hit_bouns=-50, evade_bouns=70))
	covers.append(Cover("Street", 20000, hit_bouns=-40, evade_bouns=50))
	covers.append(Cover("Building", 10000, hit_bouns=0, evade_bouns=20))
	covers.append(Cover("Sun", 99999, hit_bouns=40, evade_bouns=-20, nodamage=True))


	status.append(Status("BURN", 5, -5, -5, hp_change=-150))
	status.append(Status("SHOCK", 5, -25, -25, False, -20))
	status.append(Status("HEALING", 5, 0, 0, hp_change=100))
	status.append(Status("HEALING+", 600, 0, 0, hp_change=80))

	skills.append(Skill("FIRE", "Burn enemy and keep them burning", 80, status[0], 18))
	skills.append(Skill("ICE POWER", "Heal yourself", 0, cooldown_turn=15))
	skills.append(Skill("BOLT", "Shock enemy and make them can not move", 100, status[1], 1))
	skills.append(Skill("HEAL", "Heal yourself", 0, cooldown_turn=30))
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
		print("[COVER IS NOT USABLE]")
		return False
	
	c = covers[id]
	battlers[0].cover_object = c
	print("Cover changed to: %s " % c.name)
	return True
	
def battler_reload(battler):
	print("[RELOADING]")
	wp = battler.get_current_weapon()
	wp.reload()
	
def battler_switch_weapon(battler, id):
	wp = battler.get_current_weapon()
	if not battler.is_equip_weapon(id - 1):
		print("[NO WEAPON IN SLOT]")
		return False
	print("[SWITCH WEAPON TO %s]" % wp.name)
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
	if not s.is_cooldown():
		return False
	
	s.set_cooldown()
	battlers[0].hp_change(-s.hp_cost)
	if s.status:
		battlers[1].add_status(s.status)
	
	print_bar("SKILL")
	print("%s" % s.name)
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
		print("[COVER IS BROKEN]")
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
		print("{:<20} {:<6} / {:<6}".format(name, hp, maxhp), end="")
		for i in battlers[i].status:
			print(i.name, end=" ")
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
	print(" NO COVER")
	
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
	print("BATTLE MAIN")
	init()
	battle_scene()
	return
