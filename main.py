import random
import sys

class Battler:
	def __init__(self, name, maxhp):
		self.name = name
		self.hp = maxhp;
		self.maxhp = maxhp
		self.weapons = []
		self.current_weapon_id = 0
		self.cover = 0
		self.hit_percent = 90
		self.evade_percent = 60
		self.cover_object = None
		
	def is_dead(self):
		#print("is_dead(): hp: %s" % self.hp)
		if self.hp <= 0:
			return True
		return False
		
	def hp_change(self, hp):
		self.hp += hp
		
	def get_current_weapon(self):
		wp = self.weapons[self.current_weapon_id]
		if wp:
			return wp;
		return None
		
	def equip_weapon(self, id):
		self.current_weapon = id
		
	def is_covered(self):
		if self.cover_object:
			return True
		return False
		
	def take_cover(self, cover):
		self.cover_object = cover
		
	def leave_cover(self):
		self.cover_object = 0
		
class Weapon:
	CRITICAL_BONUS_PERCENT = 200
	
	def __init__(self, name, dmg, rps, ammo, critical_percent=0, hit_percent_bouns=0):
		self.name = name
		self.dmg = dmg
		self.rps = rps
		self.ammo = ammo
		self.max_ammo = ammo
		self.critical_percent = critical_percent
		self.hit_percent_bouns = hit_percent_bouns
		
	def fire(self):
		if not self.is_magezine_empty():
			self.ammo -= 1
			return True
		return False
			
		
	def is_magezine_empty(self):
		if self.ammo <= 0:
			return True
		return False
		
class Cover:
	def __init__(self, name, maxhp, hit_bouns=100, evade_bouns=100, nodamage=False):
		self.name = name
		self.hp = maxhp
		self.maxhp = maxhp
		self.hit_bouns = hit_bouns
		self.evade_bouns = evade_bouns
		self.nodamage = nodamage
		
	def get_hit_bouns(self):
		return random.randrange(0, self.hit_bouns)
	
	def get_evade_bouns(self):
		return random.randrange(0, self.evade_bouns)
		
	def is_dead(self):
		if self.hp <= 0:
			return True
		return False
	
	def is_nodamage(self):
		return self.nodamage
		
weapons = []
weapons.append(Weapon("5.56x45mm LMG", 8, 15, 300, 4))
weapons.append(Weapon("7.62x39mm LMG", 18, 10, 90, 12, -3))
		
battlers = []
battlers.append(Battler("You", 300))
battlers.append(Battler("Magical girl", 330))
battlers[0].weapons.append(weapons[0])
battlers[1].weapons.append(weapons[1])
battlers[1].equip_weapon(1)

covers = []
covers.append(Cover("Forest", 10000, hit_bouns=-20, evade_bouns=40))
covers.append(Cover("Street", 20000, hit_bouns=-30, evade_bouns=30))
covers.append(Cover("Building", 10000, hit_bouns=-10, evade_bouns=10))
covers.append(Cover("Sun", 99999, hit_bouns=20, evade_bouns=-20, nodamage=True))

def print_hugebar(s=""):
	print(s.center(80, "="))
	
def print_bar(s=""):
	print(s.center(80, "-"))


def attack(target, hp):
	target.hp_change(-hp)
	return True
	
def get_rate():
	return random.randrange(101)
	
def attack_in_turn(attacker, target):
	total_damage = 0
	total_hit = 0
	
	wp = attacker.get_current_weapon()
	rps = wp.rps
	orig_dmg = wp.dmg
	critical_percent = wp.critical_percent
	
	dmg = orig_dmg
	
	weapon_hit_percent = attacker.hit_percent + wp.hit_percent_bouns
	
	if wp:
		for i in range(rps):
			if wp.fire():
				if get_rate() <= weapon_hit_percent:
					if get_rate() >= target.evade_percent:
						if get_rate() <= critical_percent:
							dmg *= int(Weapon.CRITICAL_BONUS_PERCENT / 100)
							print("!CRIT! ", end="")
							
						print("[%s] " % dmg, end="")
						if attack(target, dmg):
							total_hit += 1
							total_damage += dmg
					else:
						print("EVAD ", end="")
				else:
					print("MISS ", end="")
			
			dmg = orig_dmg #Clear critical bonus		
			
	print("")
	return total_hit, total_damage

def show_damage(hit, dmg):
	print("(%s hit, %s damage)" % (hit, dmg))
	
def show_covers():
	print_hugebar("COVER")
	for i, j in enumerate(covers):
		name = j.name
		hp = j.hp
		maxhp = j.maxhp
		hit_bouns = j.hit_bouns
		evade_bouns = j.evade_bouns
		print("[%s] %s, %s / %s, HIT: %s%%, EVADE: %s%%" % (i, name, hp, maxhp, hit_bouns, evade_bouns))
		
	print_hugebar()

def command_perform(cmd_char):
	if cmd_char is "w":
		hit, dmg = attack_in_turn(battlers[0], battlers[1])
		show_damage(hit, dmg)
	elif cmd_char is "s":
		show_covers()
		return False
	else:
		return False
		
	return True
	
def enemy_action():
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
		
def print_batttlerStatus(battler):
	print("%s  MP: %s / %s" % (battler.name, battler.hp, battler.maxhp))
	
def print_currentweapon(battler):
	for j, i in enumerate(battler.weapons):
		name = i.name
		dmg = i.dmg
		rps = i.rps
		ammo = i.ammo
		max_ammo = i.max_ammo
		print("[%s] %s, DMG: %s, RPS: %s, Ammo: %s / %s" % (j + 1,name, dmg, rps, ammo, max_ammo))
		

def battle_scene():
	turn = 0;
	
	while True:
		print_bar("STATUS")
		print("[Second: %s]" % turn)
		#print_hugebar()
		for i in range(2):
			print_batttlerStatus(battlers[i])
		print_hugebar()
		print_currentweapon(battlers[0])
		print("[W]: Fire, [S]: Take cover, [Enter]:Perform")
		
		
		while 1:
			cmd = input("COMMAND?>")	
			if cmd:
				print_bar("PLAYER ACTION")
				cmd_char = cmd[0]
				if command_perform(cmd_char):
					break
		
		check_win()
		
		print_bar("ENEMY ACTION")
		enemy_action()
		
		check_win()
		
			
		turn += 1
			
		
def main():
	battle_scene()
	return
	
main()
