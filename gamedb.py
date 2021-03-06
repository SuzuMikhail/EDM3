# -*- coding: utf-8 -*-

import random
import common
import os

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
		added_hp = self.hp + hp
		if added_hp >= self.maxhp:
			self.hp = self.maxhp
			return
		self.hp += hp
		return
		
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
	def __init__(self, name, keep_turn=0, hit_bouns=0, evade_bouns=0, is_movable=True, hp_change_percent=0):
		self.name = name
		self.hp = keep_turn
		self.keep_turn = keep_turn
		self.hit_bouns = hit_bouns
		self.evade_bouns = evade_bouns
		self.is_movable = is_movable
		self.hp_change_percent = hp_change_percent
		
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

party_weapons = []
equiped_weapons = []
		
class Party:
	@staticmethod
	def add_weapon(id):
		party_weapons.append(id)
	
	@staticmethod
	def remove_weapon(id):
		del party_weapons[id]
		
	@staticmethod
	def clear_weapon():
		party_weapons.clear()
		
	@staticmethod
	def equip_weapon(id):
		equiped_weapons.append(id)
		
	@staticmethod
	def unequip_weapon(id):
		del equiped_weapons[id]
		
	@staticmethod
	def unequip_all():
		equiped_weapons.clear()
		
	@staticmethod
	def equiped_weapons_len():
		i = len(equiped_weapons)
		return i

	@staticmethod
	def is_equiped():
		if equiped_weapons:
			return True
		else:
			return False
		
STR_ZH = {
	"_en" : "_zh",

	"5.56x45mm LMG":   "5.56毫米轻机枪",
	"7.62x39mm LMG":   "7.62苏式轻机枪",
	"12.7x99mm HMG":   "12.7美式重机枪",
	"12.7x108mm HMG": "12.7苏式重机枪",
	"Storm Generator": "风卷残云轻机枪",
	"7.62 Gatling": "轻型加特林机枪",
	"RPG Classic": "经典火箭推进榴弹",
	"20x102 Vulcan": "火神式加特林机炮",
	"Wired Missile": "线导式反坦克导弹",
	"20x102mm CIWS": "20mm 近迫防御系统",
	"105mm Cannon": "105mm 重型加农炮",
	"30x165mm CIWS": "30mm 近迫防御系统",
	"Stone Missile": "岩石式短程导弹",
	"Magical Rifle": "魔法轻型突击步枪",
	"Magic Storm":   "魔法武器疾风暴雨",
	"Jupiter Missile":  "诸神之王中程导弹",
	"Antimatter RFL": "反物质突击步枪",
	"Thor Missile":  "雷神式远程导弹",
	"Antimatter LMG": "反物质轻型机枪",
	"Minute Missile": "一分钟式洲际导弹",
	"Antimatter RAIN": "反物质暴雨狂潮",
	"Meteor Missile":  "小型流星星际导弹",
	"Magic Shotgun":  "小型魔法霰弹枪",
	
	
	"10th magical girl": "第十位魔法少女",
	"New world godness": "新世界女神",
	"Happy virus maker": "乐流感大师",
	"VR Dominator": "ＶＲ支配者",
	"Magical emperor": "魔法之霸王",
	"Magical Berserker": "魔法狂战士",
	"Ubermensch": "超人约伯满取",
	"United souls": "统一的人类灵魂",
	"MAGICA LILIUM": "百合星魔法少女",
	"The New Lord":  "新世界天父",
	"DEA LILIUM":    "百合星神",
	
	"Forest": "森林",
	"Street": "街道",
	"Building": "高楼",
	"Sun": "太阳",
	"Sea": "大海",
	
	"City": "城市",
	"Mountain": "山脉",
	
	"Earth": "地球",
	"Moon":  "月球",
	"Mars":  "火星",
	
	"NAME": "名称",
	"DMG": "伤害",
	"RPS": "射速",
	"AMMO": "弹药",
	"CRIT%": "爆击+",
	"HIT%": "命中+",
	"MAX": "最大",
	"MANA": "魔力",
	"MAXMN": "最大魔力",
	"STATUS": "状态",
	"SECOND": "秒数",
	"Switch weapon": "切换武器",
	
	"(%s hit, %s damage)": "（命中 %s 次, 造成 %s 点伤害）",
	"(Cover: %s damage)": "（掩体：受到 %s 点伤害）",
	"MP CHANGED: %s": "魔力变化了: %s",
	
	"EVAD": "回避",
	"MISS": "失误",
	">AMMO OUT<": ">弹药耗尽<",
	
	"Current cover": "当前掩体",
	
	"HIT%: {:<4} EVADE%: {:<4}": "命中率参考值： {:>4}% 回避率参考值： {:>4}%",
	
	"HP": "耐久",
	"MAXHP": "最大",
	"HITMAX%": "命中加成%",
	"EVADEMAX%": "回避加成%",
	
	"MP COST": "消耗",
	
	"COMMAND?>": "指令？>",
	"COVER COMMAND?>": "掩体指令？>",
	"INVENTORY COMMAND?>": "仓库指令？>",
	"[NUMBERS]: Equip, [D]: Disarm all, [0]: Exit": "[数字]: 装备, [D]: 解除所有装备, [0]: 退出",
	"(If disarmed and exit, system will equip recommend weapons.)": "（如果解除了所有装备并退出，系统会自动装备推荐的装备。）",
	"[No weapon equiped, weapon was equiped automatically.]": "[无武器被装备，已自动装备武器。]",
	"Equiped %s": "装备了 %s",
	"All weapon was disarmed.": "解除了所有装备。",
	
	"NEXT": "下一步",
	"INVENTORY": "仓库",
	"FIRE": "开火",
	"TAKE COVER": "寻求掩体",
	"RELOAD": "装填",
	"INFO": "信息",
	"[COVER IS BROKEN]": "[掩体损坏]",
	"[RELOADING]": "[正在装弹]",
	"[W]:Leave cover, [`][0]:Exit": "[W]:离开掩体, [`][0]:返回",
	"[LEAVE COVER]": "[离开掩体]",
	"[NOT COVERED]": "[无掩体]",
	"[COVER IS NOT USABLE]": "[掩体不可用]",
	"[SLOT IS FULL]": "[槽位已满]",
	"Cover changed to: %s ": "切换至掩体: %s",
	"PLEASE INPUT LEGAL COMMAND": "请输入正确指令",
	"Fire was disappeared due to you jumped in sea.": "由于跳入了海中，身上的火熄灭了。",
	"[SWITCH WEAPON TO %s]": "[切换武器至 %s]",
	
	"FIRE CURSE": "烈火诅咒",
	"ICE HEAL": "寒冰疗愈",
	"BOLT": "雷霆震荡",
	"HEAL": "魔力恢复",
	"CHMICAL FIRE": "化学烈焰",
	"SOUL CURSE": "灵魂诅咒",
	
	"Burn enemy and keep them burning": "燃烧敌人，并使其持续燃烧",
	"Heal yourself": "治疗自身",
	"Shock enemy and reduce hit/evade %": "震撼敌人并降低他们的命中率和回避率",
	
	"BURN": "燃烧",
	"SHOCK": "触电",
	"C.BURN": "化学燃烧",
	"HACKING": "开挂",
	"WANTED": "全球通缉",
	"BERSERK": "狂战",
	"CURSED": "诅咒",
	"YURI": "百合贴贴",
	
	"[SHOCKED]": "触电",
	
	"HEALING+": "无限魔力",
	
	"SKILLS": "技能",
	"COOLDOWN": "冷却秒数",
	
	"You are dead": "你被击败了",
	"You lose": "你输了",
	"Enemy down": "打倒了敌人",
	"You win": "你赢了",
	
	"LEVEL UP!": "等级提升！",
	"New items are in your inventory.": "新的道具已经收进了你的仓库。",
	
	"I have turn on my cheat program!": "傻了吧，爷会开挂！",
	"(BERSERK EFFECT: MP + %s, DAMAGE + %s)": "（狂战效果： 自身魔力恢复 %s, 造成伤害增加 %s）",
	"Why must you let us to disappear!!!!": "你为什么一定要让我们消失啊！！！！",
	"DEA LILIUM was defeated. Your power can make you be the god of this universe. The destiny of the universe are on your hand...": "百合星神被打败了。你的力量已经可以使你成为这个宇宙的神。大宇宙的命运就交给你了……",
	"CHOOSE EPISODE?(NUMBER, 0-10)>": "选关？（数字，0-10）>",
}
		
WEAPONS = [
	["5.56x45mm LMG",  "",     8, 15, 300, 4,   0],
	["7.62x39mm LMG",  "",    18, 10, 300, 12, -5], # boss 1 used
	["12.7x99mm HMG",  "",    30, 8, 100, 30, -30],
	["12.7x108mm HMG", "",    48, 7, 100, 35, -35],
	
	["7.62 Gatling",   "",    22, 45, 800, 2,  -38], # boss 2 used
	["Storm Generator",   "",     8, 200, 2400, 8, -12],
	["RPG Classic",    "",  3000,   1,   15, 5, -25],
	
	["20x102 Vulcan", "" ,    60, 30, 3500,  50, -45], # boss 3 used
	
	["Wired Missile", "",   3500,  1,  1,  5,  -25], # boss 4 used
	["20x102mm CIWS", "",    60,  55, 6000,  50, -20],
	
	["105mm Cannon", "",    4300,  1,  3,   5,  -23], # boss 5 used
	["30x165mm CIWS", "",   100,  50, 8000,  30, -20],
	
	["Stone Missile",  "",  10000,  1,  1,   0,  -25], # boss 6 used
	["Magical Rifle",  "",    700,  10,  140,  8,  5],
	
	["Magic Storm",   "",    300,  35,  500,  2,  10], # boss 7 used
	["Jupiter Missile",  "",   15000,  1,  1,   0,   -25],
	
	["Antimatter RFL",  "",    650, 20,  500,  10,   10], # boss 8
	["Thor Missile",  "",    20000,  1,   1,   0,   -25],
	
	["Antimatter LMG",  "",    650,  40,  1000,  10,  7], # boss 9
	["Minute Missile",  "",  30000,  1,   1,   0,   -25],
	
	["Antimatter RAIN", "",    650, 100,  1000,  0,   0], # boss 10
	["Meteor Missile",  "",  25000,  2,   500,   0,     -25],
	
	["Magic Shotgun",   "",   300,  90,  5000,  4,   10],
]

HERO = [
	3000,
	6000,
	9000,
	
	14000,
	20000,
	25000,
	
	32000,
	48000,
	60000,
	100000
]

BOSSES = [
	["New world godness", 9000, 95, 25],
	["Happy virus maker", 15000, 85, 15],
	["VR Dominator",     9500, 95, 0],
	
	["Magical emperor", 16000, 70,  20],
	["Magical Berserker", 25000, 70, 25],
	["Ubermensch",      40000,  80,  20],
	
	["United souls",    60000,  90, 0],
	["MAGICA LILIUM",   50000,  90, 20],
	["The New Lord",   120000,  90, 20],
	["DEA LILIUM",     300000,  90, 10]
]

COVERS = [
	["Forest", 15000, -50, 70, False],
	["Street", 20000, -40, 50, False],
	["Building", 25000, 0, 20, False],
	["Sun",     99999, 40, -20, True],
	["Sea",    999999, -100, -100, False]
]

COVERS_2 = [
	["City", 60000, -60, 60, False],
	["Mountain", 80000, -30, 30, False],
	["Sun",     99999, 40, -20, True],
]

COVERS_3 = [
	["Earth",  400000, -60, 60, False],
	["Moon",   200000, -45, 45, False],
	["Sun",    900000, -90, 90, False],
	["Mars",   600000, -75, 75, False]
]

SKILLS = [
	["FIRE CURSE",      "Burn enemy and keep them burning",  80,   0,  15],
	["ICE HEAL", "Heal yourself",                            0, None, 15],
	["BOLT",       "Shock enemy and reduce hit/evade %", 40,  1,  10],
	["HEAL",      "Heal yourself",                           0, None, 30],
	["CHMICAL FIRE", "",                                      0,   4,  20],
	["SOUL CURSE",     "",                                   0,    8,  25],
]

STATUS = [
	["BURN",      5,  -5, -5,   True, -3],
	["SHOCK",     5, -25, -25,  True, -1],
	
    ["HEALING+", 150,   0, 0,    True, 2],
    ["HEALING+", 150,  0, 0,    True, 0.5], #boos 1 used
	
	["C.BURN",    20,  -30, -30, True, -6],
	["HACKING",   5, 150, 150,   True, 18],
	
	["WANTED",  150,  -10, -10,  True, -2],
	["BERSERK", 150,  0, 0,     True,   0],
	
	["CURSED",   10, -10, -10,  True,  -5],
	["YURI",    50,  5,  5,  True,   4], #boss 9/10 used
]


LEVEL_UP_MSG = "LEVEL UP!"
NEWITEM_MSG = "New items are in your inventory."
