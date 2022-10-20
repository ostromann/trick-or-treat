# game setup
WIDTH = 1920#1280
HEIGHT = 1080#720
FPS = 60
TILESIZE = 64
HITBOX_OFFSET = {
	'player': -26,
	'objects': -40,
	'grass': -10,
	'invisible': 0}
INPUT = 'ps4'

# graphics
STRETCH_SIZE = 6
STRETCH_FREQUENCY = 100 #TODO: Convert to real frequency

# ui 
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 40
UI_FONT = 'graphics/font/joystix.ttf'
UI_FONT_SIZE = 18

# general colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

# ui colors
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
EXP_COLOR = 'green'
UI_BORDER_COLOR_ACTIVE = 'gold'

# upgrade menu
TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'

# damage indicator
DAMAGE_INDICATOR_FONT = 'graphics/font/Silkscreen-Bold.ttf'
DAMAGE_INDICATOR_TEXT_COLOR = 'white'
DAMAGE_INDICATOR_FONT_SIZE = 20
DAMAGE_INDICATOR_FADEOUT_TIME = 1.5

DAMAGE_INDICATOR_CRIT_TEXT_COLOR = 'gold'
DAMAGE_INDICATOR_CRIT_FONT_SIZE = 28
DAMAGE_INDICATOR_CRIT_FADEOUT_TIME = 2.5

# level up settings
BASE_EXP_THRESHOLD = 5
BASE_EXP_INCREASE = 10

# player data
player_data = {
	'normalo': {
		'health': 100, 
		'attack': 10,
		'attack_factor': 1,
		'crit_chance': 0.5,
		'crit_damage': 1.5,
		'speed': 10,
		'range': 1,
		'projectile_speed': 1,
		'projectile_queuing_radius': 50,
		'item_pull_range': 100,
		'item_pull_force': 5,
		'projectiles': ['candy','popcorn']},
}

# weapons
weapon_data = {
	'sword': {'cooldown': 100, 'damage': 15,'graphic':'graphics/weapons/sword/full.png'},
	'lance': {'cooldown': 400, 'damage': 30,'graphic':'graphics/weapons/lance/full.png'},
	'axe': {'cooldown': 300, 'damage': 20, 'graphic':'graphics/weapons/axe/full.png'},
	'rapier':{'cooldown': 50, 'damage': 8, 'graphic':'graphics/weapons/rapier/full.png'},
	'sai':{'cooldown': 80, 'damage': 10, 'graphic':'graphics/weapons/sai/full.png'}}

# magic
magic_data = {
	'flame': {'strength': 5,'cost': 20,'graphic':'graphics/particles/flame/fire.png'},
	'heal' : {'strength': 20,'cost': 10,'graphic':'graphics/particles/heal/heal.png'}}

# enemy
MONSTER_SPAWN_DURATION = 1.0
monster_data = {
	'cauldron': {
		'health': 120, 
		'exp': 1, 
		'damage': 40, 
		'attack_type': 'slash', 
		'attack_sound': 
		'audio/attack/slash.wav', 
		'speed':1, 
		'resistance': 6, 
		'attack_radius': 50, 
		'notice_radius': 300,
		'precharge_duration': 0.3},
	'mushroom': {
		'health': 120, 
		'exp': 1, 
		'damage': 40, 
		'attack_type': 'slash', 
		'attack_sound': 
		'audio/attack/slash.wav', 
		'speed':1, 
		'resistance': 6, 
		'attack_radius': 50, 
		'notice_radius': 300,
		'precharge_duration': 0.3},
	# 'squid': {'health': 100,'exp':100,'damage':20,'attack_type': 'slash', 'attack_sound':'audio/attack/slash.wav', 'speed': 3, 'resistance': 6, 'attack_radius': 80, 'notice_radius': 360},
	# 'raccoon': {'health': 300,'exp':250,'damage':40,'attack_type': 'claw',  'attack_sound':'audio/attack/claw.wav','speed': 2, 'resistance': 6, 'attack_radius': 120, 'notice_radius': 400},
	# 'spirit': {'health': 100,'exp':110,'damage':8,'attack_type': 'thunder', 'attack_sound':'audio/attack/fireball.wav', 'speed': 4, 'resistance': 6, 'attack_radius': 60, 'notice_radius': 350},
	# 'bamboo': {'health': 70,'exp':120,'damage':6,'attack_type': 'leaf_attack', 'attack_sound':'audio/attack/slash.wav', 'speed': 3, 'resistance': 6, 'attack_radius': 50, 'notice_radius': 300}
	}

# projectiles
projectile_data = {
	'candy': {'damage': 50, 'attack_type': 'slug', 'attack_sound': 'audio/attack/slash.wav', 'speed': 20, 'return_speed': 10, 'range': 300, 'cooldown': 200},
	'popcorn': {'damage': 80, 'attack_type': 'slug', 'attack_sound': 'audio/attack/claw.wav', 'speed': 15, 'return_speed': 10, 'range': 300, 'cooldown': 600},
}
