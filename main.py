import random
import sys

class Battler:
	def __init__(self, name, hp):
		self.name = name
		self.hp = hp;
		self.weapons = 0
		self.current_weapon = 0
		self.cover = 0
		self.hit_percent = 80
		self.evade_percent = 70
		
	def print_batttlerStatus(self):
		print("%s  MP: %s" % (self.name, self.hp))
		
	def is_dead(self):
		#print("is_dead(): hp: %s" % self.hp)
		if self.hp <= 0:
			return True
		return False
		
	def hp_change(self, hp):
		self.hp += hp
		
	def equip_weapon(self, id):
		self.current_weapon = id
		
class Weapon:
	def __init__(self, name, dmg, rps, ammo):
		self.name = name
		self.dmg = dmg
		self.rps = rps
		self.ammo = ammo
		
	def fire(self):
		if not self.is_magezine_empty():
			self.ammo -= 1
			return True
		return False
			
		
	def is_magezine_empty(self):
		if self.ammo < 0:
			return True
		return False
		
battlers = []
battlers.append(Battler("You", 300))
battlers.append(Battler("Magical girl", 330))
battlers[1].equip_weapon(1)

weapons = []
weapons.append(Weapon("5.56x45mm LMG", 10, 15, 300))
weapons.append(Weapon("7.62x39mm LMG", 15, 10, 90))

def attack(target, hp):
	target.hp_change(-hp)
	return True
	
def attack_in_turn(attacker, target):
	total_damage = 0
	total_hit = 0
	rps = weapons[attacker.current_weapon].rps
	dmg = weapons[attacker.current_weapon].dmg
	
	for i in range(rps):
		if random.randrange(100) <= attacker.hit_percent:
			if random.randrange(100) >= target.evade_percent:
				print("%s DMG" % dmg)
				if attack(target, dmg):
					total_hit += 1
					total_damage += dmg
			else:
				print("Evaded")
		else:
			print("MISS")
			
	return total_hit, total_damage

def show_damage(hit, dmg):
	print("(%s hit, %s damage)" % (hit, dmg))

def command_perform(cmd_char):
	if cmd_char is "w":
		hit, dmg = attack_in_turn(battlers[0], battlers[1])
		show_damage(hit, dmg)
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
	
def battle_scene():
	turn = 0;
	empty_str = ""
	while True:
		print("[Second: %s]" % turn)
		print(empty_str.center(80, "="))
		for i in battlers:
			i.print_batttlerStatus()
		print(empty_str.center(80, "="))
		print("[W]: Fire, [S]: Take cover, [Enter]:Perform")
		
		while 1:
			cmd = input("COMMAND?>")	
			if cmd:
				cmd_char = cmd[0]
				if command_perform(cmd_char):
					break
		
		check_win()
		
		print("[Enemy action]")
		enemy_action()
		
		check_win()
		
			
		turn += 1
			
		
def main():
	battle_scene()
	return
	
main()
