import gamedb

def translate(key):
	if key in gamedb.STR_ZH and gamedb.LANG_ZH:
		return gamedb.STR_ZH[key]
	return key