import time
import sys
import battle_system


def story():
	story_level = 1
	while 1:
		if enter_episode(story_level):
			battle_system.main()
		story_level += 1
		

def enter_episode(story_id=0):
	story_path = "./Stories/"

	story = [
		"ep0",
		"ep1"
	]
	
	enemy_id = [
		0,
		1,
	]

	storyfile_suffix = ".txt"
	
	for i in open(story_path + story[story_id] + storyfile_suffix):
		#print(i, end="")
		sys.stdout.write(i)
		sys.stdout.flush()
		#time.sleep(.6)
	print("")

	while 1:
		if main_menu():
			if enemy_id[story_id] == 0:
				return False
			return True
	
def print_main_menu():
	print("{:<15} {:<15} {:<15}".format("", "[E]:Next", "[I]:Inventory"))
	
def main_menu():
	print_main_menu()
	cmd_char = input("COMMAND?>")
	if cmd_char is "e":
		return True
	elif cmd_char is "i":
		return False
	else:
		return False