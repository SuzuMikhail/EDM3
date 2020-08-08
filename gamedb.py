# -*- coding: utf-8 -*-

import random
import common

import os

LANG_ZH = False

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
		
_ = common.translate

STR_ZH = {
	"5.56x45mm LMG": "5.56毫米轻机枪",
	"7.62x39mm LMG": "7.62苏式轻机枪",
	"12.7x99mm HMG": "12.7美式重机枪",
	
	"NAME": "名称",
	"AMMO": "弹药",
	"MAX": "最大",
	
	"MP COST": "消耗魔力",
	
	"NEXT": "下一步",
	"INVENTORY": "仓库"
}
		
WEAPONS = [
	["5.56x45mm LMG",  "A light machinegun made by Belgium", 8, 15, 300, 4,   0],
	["7.62x39mm LMG",  "A light machinegun made by USSR",   18, 10, 300, 12, -5],
	["12.7x99mm HMG",  "A heavy machinegun made by USA",    30, 5, 100, 30, -30],
	["12.7x108mm HMG", "A heavy machinegun made by Russia", 40, 7, 100, 35, -35],
	["9mm Classic SMG", "A submachinegun made by Italy",     5, 50, 800, 2,  10]
]

HERO = [
	3000,
	6000
]

BOSSES = [
	["New world godness", 9000, 95, 25],
	["Happy virus maker", 15000, 85, 15],
	["VR Dominator",     23000, 200, 5],
]

COVERS = [
	["Forest", 10000, -50, 70, False],
	["Street", 20000, -40, 50, False],
	["Building", 10000, 0, 20, False],
	["Sun",     99999, 40, -20, True]
]

SKILLS = [
	["FIRE",      "Burn enemy and keep them burning",        80,   0,  15],
	["ICE POWER", "Heal yourself",                            0, None, 15],
	["BOLT",       "Shock enemy and make them can not move", 100,  1,  23],
	["HEAL",      "Heal yourself",                           0, None, 30]
]

STATUS = [
	["BURN",      5,  -5, -5,   True, -150],
	["SHOCK",     5, -25, -25, False, -20],
    ["HEALING",   5,   0, 0,    True, 100],
    ["HEALING+", 150,  0, 0,    True, 40]
]

LEVEL_UP_MSG = "LEVEL UP!"