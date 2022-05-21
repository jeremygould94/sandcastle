# -------------------------------------------- Sandcastle: main code ---------------------------------------------------
#                                 ________________________________________________
#                                |                                                |
#                                |     oOOOoo   oOoo         |           oOoo     |
#                                |   oOOo                   -O-      oOOo   oOo   |
#                                |                           |                    |
#                                |                                                |
#                                |                xxxX        Xxxx                |
#                                |-------------xxXx              xXxx-------------|
#                                |----------xxXx                    xXxx----------|
#                                |-------xxXx        SANDCASTLE:       xXxx-------|
#                                |-----xXx  A GAME ABOUT THE NEAR FUTURE  xXx-----|
#                                |---xXx                                    xXx---|
#                                |-xXx                                        xXx-|
#                                |xXx..|.||.|...||.||.||..|..|.||...|.||...||..xXx|
#                                |                                                |
#                                |________________________________________________|
#
# ------------------------------------------------ Random Notes --------------------------------------------------------

# Aim for 48 characters for text length on screen.
# A function can have an input as per the definition, and you can then later call the function.
# Success at random combat encounters and so on should deposit loot directly into inventory, or send player to
# > loot screen, so we can then return to same page afterwards
# > Could modify subscriptions so basic is just basic and premium is everything but basic is 100% free on basic etc

# ------------------------------------------------- Import shit --------------------------------------------------------

import time
import datetime
import random
import webbrowser
import string
from os import system, name

# -------------------------------- Declare initial variables and smaller dictionaries ----------------------------------

# Set random seed as using system time
random.seed()

# Initial read delays - leave these as variables because they are used so frequently and have their own function
read_speed_choice = 1
text_delay = 3
error_delay = 1.5
med_delay = 1
short_delay = 0.10

# Status counters - leave alone for now, as used already
drunk_counter = 0
drugged_counter = 0  # not for sol, for when player is drugged by someone etc
health = 100
ad_shield_counter = 0  # max score can be 1, as needs instant decay unless reapplied by page status
temp_ad_blocker_counter = 0
subscription_charge_counter = 0

# status counter dict
status_counters = {
    "drunk_counter": 0,
    "drugged_counter": 0,
    "health": 100,
    "ad_shield_counter": 0,
    "temp_ad_blocker_counter": 0,
    "subscription_charge_counter": 0,
    "hungover_counter": 0,
    "blind_counter": 0,
    "deaf_counter": 0,
    "turn_counter": 0,
    "sol_effect_counter": 0,
    "sol_addict_counter": 0,
    "can_sleep_counter": 20,
    "overdraft_counter": 0
}

# vague info - look up backup for more clarity
# sol drug named for city, boost speech and combat scores by plus 20, will not stack with itself
# increased by 10 with every use of sol, at 50-100 will reduce all scores by 10, at 100+ by 20.
# must hit zero before can sleep in bed again, tick down once per turn
# +1 every turn in overdraft if reaches 50 then sent to work camp
# ad_bomb_counter = 0  # temporarily bombards player with ads by increasing ad rate - removed for moment
# ARC_temp_disabled_counter = 0 - might scrap this idea


# Allegiances
# > Need reb and gov score separate for quest requirement logic
# > Just make sure any action that raises one also decreases the other
# > Banished score will be independent of others

alleg_dict = {
    "reb_sc": random.randint(4, 7),
    "gov_sc": random.randint(1, 3),
    "banished_sc": 1
}

# Romance scores dict - max will be 10
rom_scores = {
    "ash_rom_sc": 2 + int(alleg_dict["reb_sc"] * 0.3),
    "bmarket_rom_sc": 1
}

# Friendship scores dict - max will be 10
fren_scores = {
    "ash_fr_sc": 1 + int(alleg_dict["reb_sc"] * 0.3),
    "bmarket_fr_sc": 2
}

# Criminal record dict
criminal_hist = {
    "fine_if_arrest": 0
}

# Money - can keep this as a variable, I think
current_balance = random.randint(650, 999)

# Subscriptions - any subscriptions fees are charged at purchase and then every 50 turns
sub_fees = {
    "prem_flav":       4000,
    "deluxe_flav":     2000,  # applies to all food and drink, 20 % of regular price at purchase
    "basic_flav":       300,  # applies to basic food and drink, 50 % of regular price at purchase
    "deluxe_ad_block": 5000,  # reduce ads by 60 %
    "basic_ad_block":   600   # reduce ads by 20 %
}

# Perks and binary statuses
perks_and_bools = {
    "sub_prem_flav": False,
    "sub_deluxe_flav": False,
    "sub_basic_flav": False,
    "sub_deluxe_ad_block": False,
    "sub_basic_ad_block": False,
    "hacked_prem_flav": False,
    "hacked_prem_ad_block": False,
    "ARC_disabled": False,
    "wearing_the_glasses": False,
    "voided": False,
    "carrying_minor_illegal_concealed": False,
    "carrying_minor_illegal_open": False,
    "carrying_major_illegal_concealed": False,
    "carrying_major_illegal_open": False,
    "minor_illegal_mod": False,
    "major_illegal_mod": False,
    "minor_scan_blocker": False,
    "major_scan_blocker": False,
    "guard_attack_on_sight": False,
    "guard_arrest_on_sight": False,
    "predator_mode": False,
    "night_vision": False,
    "dark_area": False,
    "big_dim_text": False,
    "small_dim_text": False,
    "ARC_overload_avail": False,
    "in_prison": False,  # may make own prison dict or something, but leave for now
    "game_over": False
}

# Market info - move bools to dictionary, leave lists and dicts as they are
bmarket_unlocked = False
bmarket_avail = False
bmarket_major_unlocked = False
bmarket_accessed_before = False
bmarket_last_accessed_datetime = datetime.datetime.now()
bmarket_instock_items = []
bmarket_instock_num2item_dict = {}
bmarket_instock_item2num_dict = {}
player_invent_avail = False
ARC_menu_avail = False
appt_storage_avail = False
hackbase_storage_avail = False

market_status = {
    "bmarket_unlocked": False,
    "bmarket_avail": False,
    "bmarket_major_unlocked": False,
    "bmarket_accessed_before": False,
    "player_invent_avail": False,
    "ARC_menu_avail": False,
    "appt_storage_avail": False,
    "hackbase_storage_avail": False
}

# Characters met
char_met = {
    "ash_met": False,
    "ash_brother_met": False,
    "bmarket_dealer_met": False,
    "work_friend_met": False,
    "work_boss_met": False,
    "rebel_leader_met": False
}

# Characters dead
char_dead = {
    "ash_dead": False,
    "ash_brother_dead": False,
    "bmarket_dealer_dead": False,
    "work_friend_dead": False,
    "work_boss_dead": False,
    "rebel_leader_dead": False
}

# Skills - 1 to 100
skills = {
    "speech_sc": random.randint(1, 25),
    "stealth_sc": random.randint(1, 25),
    "combat_sc": random.randint(1, 25),
    "hacking_sc": random.randint(1, 25),
    "aim_sc": random.randint(1, 25),
    "science_sc": random.randint(1, 5),
    "fame": 1,  # can be used to access central/political districti, instead of cash, depended on level
    "notoriety": 1  # for accessing underworld missions (which give high cash rewards but lots of danger)
}

# Equipment
equipment = {
    "weapon":    "none",
    "head":      "none",
    "torso":     "none",
    "legs":      "none",
    "shoes":     "none",
    "accessory": "none"
}

# Personal inventory
player_invent = {}

# Appartment storage
appt_storage = {}

# Hacker base storage
hackbase_storage = {}

# All item full names - write all full names as 23 characters - 1st 4 letters of fname should match sname, to sort
all_item_fnames = {
    #                  aaaaaaaaaaaaaaaaaaaaaaa
    "none":           "none",
    "9mm_hand":       "9mm handgun            ",
    "comb_knife":     "combat knife           ",
    "crowbar":        "crowbar                ",
    "cyber_kat":      "cyber katana           ",
    "eagle_sniper":   "eagle-eye sniper rifle ",
    "flip_knife":     "flip knife             ",
    "hammer":         "hammer                 ",
    "lead_pipe":      "lead pipe              ",
    "mils_pred_mod":  "milspec predator module",
    "screw_dr":       "screw driver           ",
    "ar_chick_head":  "AR chicken head        ",
    "ar_chick_tors":  "AR chicken torso       ",
    "ar_chick_legs":  "AR chicken legs        ",
    "ar_chick_feet":  "AR chicken feet        ",
    "ar_chick_tail":  "AR chicken tail        ",
    "ar_croc_head":   "AR crocodile head      ",
    "ar_croc_tors":   "AR crocodile torso     ",
    "ar_croc_legs":   "AR crocodile legs      ",
    "ar_croc_feet":   "AR crocodile feet      ",
    "ar_croc_tail":   "AR crocodile tail      "
}

# All item contraband info
all_item_contra = {
    #                  aaaaa
    "none":           "na",
    "9mm_hand":       "major",
    "comb_knife":     "major",
    "crowbar":        "minor",
    "cyber_kat":      "major",
    "eagle_sniper":   "major",
    "flip_knife":     "minor",
    "hammer":         "minor",
    "lead_pipe":      "minor",
    "mils_pred_mod":  "major",
    "screw_dr":       "minor",
    "ar_chick_head":  "na",
    "ar_chick_tors":  "na",
    "ar_chick_legs":  "na",
    "ar_chick_feet":  "na",
    "ar_chick_tail":  "na",
    "ar_croc_head":   "na",
    "ar_croc_tors":   "na",
    "ar_croc_legs":   "na",
    "ar_croc_feet":   "na",
    "ar_croc_tail":   "na"
}

# All item type info
all_item_type = {
    "none":           "na",
    "9mm_hand":       "weapon",
    "comb_knife":     "weapon",
    "crowbar":        "weapon",
    "cyber_kat":      "weapon",
    "eagle_sniper":   "weapon",
    "flip_knife":     "weapon",
    "hammer":         "weapon",
    "lead_pipe":      "weapon",
    "mils_pred_mod":  "weapon",
    "screw_dr":       "weapon",
    "ar_chick_head":  "head",
    "ar_chick_tors":  "torso",
    "ar_chick_legs":  "legs",
    "ar_chick_feet":  "shoes",
    "ar_chick_tail":  "accessory",
    "ar_croc_head":   "head",
    "ar_croc_tors":   "torso",
    "ar_croc_legs":   "legs",
    "ar_croc_feet":   "shoes",
    "ar_croc_tail":   "accessory"
}

# Fines for contraband - flat fine for major/minor
contra_fines = {
    "major": 5000,
    "minor":  500,
    "na":       0
}

# Black market available items - govern price, availability, short contra, chance of appearing in shop
black_market_items = {
    "9mm_hand":      {"id": 0, "ps": "",   "price": 1200, "icat": "ma", "rr": 0.32},
    "cyber_kat":     {"id": 1, "ps": "",   "price": 8000, "icat": "ma", "rr": 0.02},
    "mils_pred_mod": {"id": 2, "ps": "",   "price": 9999, "icat": "ma", "rr": 0.01},
    "comb_knife":    {"id": 3, "ps": "",   "price": 1000, "icat": "ma", "rr": 0.15},
    "eagle_sniper":  {"id": 4, "ps": "",   "price": 7500, "icat": "ma", "rr": 0.03},
    "crowbar":       {"id": 5, "ps": " ",  "price":  800, "icat": "mi", "rr": 0.60},
    "flip_knife":    {"id": 6, "ps": " ",  "price":  350, "icat": "mi", "rr": 0.70},
    "lead_pipe":     {"id": 7, "ps": " ",  "price":  200, "icat": "mi", "rr": 0.97},
    "hammer":        {"id": 8, "ps": " ",  "price":  180, "icat": "mi", "rr": 0.80},
    "screw_dr":      {"id": 9, "ps": "  ", "price":   75, "icat": "mi", "rr": 0.70}
}

# Weapon info
# contains:
# md = melee damage, rd = ranged damage, ignr = ignore armour Y/N, sk = related skill for accuracy scaling,
# s_bns = stealth bonus multiplier, mel_s = chance of melee success, rng_s = chance of ranged attacked success.
# for melee weapons, range success relates to thrown chance of hit
# stealth bonus applies to a 1st attack on an unaware enemy, is listed as multiplier, doesn't affect guns
# skill does not affect damage, (apart from stealh bonus) it affects chance of success.
# only the related skill will boost the success, so you can't improve melee chance for a gun etc.
# "aim" skill weapons, i.e. guns and maybe throwing knives if I add them should have 10% to quad dmg from a headshot
# ^^^ this applies to the player as well

weapon_info = {
    "9mm_hand":     {"md":  20, "rd":  70, "ignr": 0, "sk": "aim",    "s_bns": 1.00, "mel_s": 0.35, "rng_s": 0.70},
    "comb_knife":   {"md":  70, "rd":  65, "ignr": 0, "sk": "combat", "s_bns": 2.00, "mel_s": 0.85, "rng_s": 0.50},
    "crowbar":      {"md":  50, "rd":  45, "ignr": 0, "sk": "combat", "s_bns": 1.20, "mel_s": 0.60, "rng_s": 0.20},
    "cyber_kat":    {"md": 100, "rd": 100, "ignr": 1, "sk": "combat", "s_bns": 3.00, "mel_s": 0.85, "rng_s": 0.70},
    "eagle_sniper": {"md":  25, "rd": 100, "ignr": 1, "sk": "aim",    "s_bns": 1.00, "mel_s": 0.15, "rng_s": 0.85},
    "flip_knife":   {"md":  45, "rd":  40, "ignr": 0, "sk": "combat", "s_bns": 1.20, "mel_s": 0.65, "rng_s": 0.55},
    "hammer":       {"md":  40, "rd":  35, "ignr": 0, "sk": "combat", "s_bns": 1.20, "mel_s": 0.65, "rng_s": 0.35},
    "lead_pipe":    {"md":  55, "rd":  50, "ignr": 0, "sk": "combat", "s_bns": 1.30, "mel_s": 0.65, "rng_s": 0.15},
    "screw_dr":     {"md":  65, "rd":  10, "ignr": 0, "sk": "combat", "s_bns": 1.40, "mel_s": 0.65, "rng_s": 0.20}
}

# Illegal categories short to long - keep this
illegal_cat = {
    "ma": "major",
    "mi": "minor",
    "na": "legal"
}

# Page counters and info - many of these are initialized here for the page reader func later
# may redo this logic, leave for now
current_chapter = "intro_appt"
return_chapter = "intro_appt"
current_page = 0
return_page = 0
current_disp_text_list = []
current_disp_choices = []
dest_for_choices = {}
dest_chap_for_choices = {}
current_page_minigame = ""
current_page_minigame_param = {}
current_page_minigame_dest = {}
current_page_need_return = ""
current_page_is_game_over = ""
current_page_game_over_msg = []  # using this for prologue atm (and possible for main)
current_page_updates = {}
current_page_mkets_avail = {}
current_page_ARC_menu_avail = ""
current_page_related_quest = ""  # update quest progress at end of turn based on dest page, with function

# Ad info
regular_ad_rate = 1.0
ads = {                                                # aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    0:  {"product": "prem_flav_sub",          "ad": {0: ["AD: Prem flav sub! One!"],
                                                     1: ["AD: Prem flav sub! Two!"],
                                                     2: ["AD: Prem flav sub! Three!"]}},
    1:  {"product": "deluxe_flav_sub",        "ad": {0: ["AD: Deluxe flav sub! One!"],
                                                     1: ["AD: Deluxe flav sub! Two!"],
                                                     2: ["AD: Deluxe flav sub! Three!"]}},
    2:  {"product": "basic_flav_sub",         "ad": {0: ["AD: Basic flav sub! One!"],
                                                     1: ["AD: Basic flav sub! Two!"],
                                                     2: ["AD: Basic flav sub! Three!"]}},
    3:  {"product": "aug_tux_and_gown",       "ad": {0: ["AD: Tux and gown! One!"],
                                                     1: ["AD: Tux and gown! Two!"],
                                                     2: ["AD: Tux and gown! Three!"]}},
    4:  {"product": "aug_tan",                "ad": {0: ["AD: Aug tan! One!"],
                                                     1: ["AD: Aug tan! Two!"],
                                                     2: ["AD: Aug tan! Three!"]}},
    5:  {"product": "nat_prid_mus",           "ad": {0: ["AD: Show that you are a true patriot!\n",
                                                         "Visit the Museum of National Pride today!"],
                                                     1: ["AD: Discover the rich history of Sol City!\n",
                                                         "Visit the Museum of National Pride today!"],
                                                     2: ["AD: Discover the story of how President Hyde\n",
                                                         "saved the world! Visit the Museum of National\n",
                                                         "Pride today!"]}},
    6:  {"product": "aug_shoes",              "ad": {0: ["AD: Get yourself some new aug trainers!\n",
                                                         "Visit the ARC store today and check out the\n",
                                                         "20th century collection."],
                                                     1: ["AD: Aug shoes! Two!"],
                                                     2: ["AD: Aug shoes! Three!"]}},
    7:  {"product": "aug_body_height",        "ad": {0: ["AD: Have you always been insecure about your\n",
                                                         "stubby legs? Visit the ARC store today and\n",
                                                         "update your aug height!"],
                                                     1: ["AD: Are you too tall?! Two!"],
                                                     2: ["AD: Aug body phys! Three!"]}},
    8:  {"product": "aug_body_phys",          "ad": {0: ["AD: Aug body phys! One!"],
                                                     1: ["AD: Aug body phys! Two!"],
                                                     2: ["AD: Aug body phys! Three!"]}},
    9:  {"product": "aug_pet",                "ad": {0: ["AD: Aug pet! One!"],
                                                     1: ["AD: Aug pet! Two!"],
                                                     2: ["AD: Aug pet! Three!"]}},
    10: {"product": "aug_friends",            "ad": {0: ["AD: Aug_friend_group! One!"],
                                                     1: ["AD: Aug_friend_group! Two!"],
                                                     2: ["AD: Aug_friend_group! Three!"]}},
    11: {"product": "aug_companion_no_phys",  "ad": {0: ["AD: Aug comp no phys! One!"],
                                                     1: ["AD: Aug comp no phys! Two!"],
                                                     2: ["AD: Aug comp no phys! Three!"]}},
    12: {"product": "aug_companion_yes_phys", "ad": {0: ["AD: Aug comp yes phys! One!"],
                                                     1: ["AD: Aug comp yes phys! Two!"],
                                                     2: ["AD: Aug comp yes phys! Three!"]}},
    13: {"product": "aug_body_mod",           "ad": {0: ["AD: Get aug body mod! One!"],
                                                     1: ["AD: Get aug body mod! Two!"],
                                                     2: ["AD: Get aug body mod! Three!"]}},
    14: {"product": "new_construction",       "ad": {0: ["AD: New Construction! One!"],
                                                     1: ["AD: New Construction! Two!"],
                                                     2: ["AD: New Construction! Three!"]}},
    15: {"product": "leak_rumours",           "ad": {0: ["AD: There is no leak! One!"],
                                                     1: ["AD: There is no leak! Two!"],
                                                     2: ["AD: There is no leak! Three!"]}},
    16: {"product": "mayor_good",             "ad": {0: ["AD: Mayor Good! One!"],
                                                     1: ["AD: Mayor Good! Two!"],
                                                     2: ["AD: Mayor Good! Three!"]}},
    17: {"product": "consume_good",           "ad": {0: ["AD: Consume Good! One!"],
                                                     1: ["AD: Consume Good! Two!"],
                                                     2: ["AD: Consume Good! Three!"]}},
    18: {"product": "rebel_warning_1",        "ad": {0: ["AD: Rebel Warning_1! One!"],
                                                     1: ["AD: Rebel Warning_1! Two!"],
                                                     2: ["AD: Rebel Warning_1! Three!"]}},
    19: {"product": "rebel_warning_2",        "ad": {0: ["AD: Rebel Warning_2! One!"],
                                                     1: ["AD: Rebel Warning_2! Two!"],
                                                     2: ["AD: Rebel Warning_2! Three!"]}},
    20: {"product": "sun_access",             "ad": {0: ["AD: Sun access! One!"],
                                                     1: ["AD: Sun access! Two!"],
                                                     2: ["AD: Sun access! Three!"]}},
    21: {"product": "consumable_food",        "ad": {0: ["AD: Buy Food! One!"],
                                                     1: ["AD: Buy Food! Two!"],
                                                     2: ["AD: Buy Food! Three!"]}},
    22: {"product": "consumable_drink",       "ad": {0: ["AD: Buy drink! One!"],
                                                     1: ["AD: Buy drink! Two!"],
                                                     2: ["AD: Buy drink! Three!"]}}
}

# Work process info - move to dict
regular_work_tasknum = 10  # controls frequency of regular work tasks, must get 10 right to finish work
regular_work_comp = 300  # 300 credits awarded after 10 correct answers
overtime_work_rate = 15  # how often overtime work tasks are given if opted into overtime
overtime_comp = 50  # 50 credits awarded for every correct overtime task completed
work_difficulty_cap = 3  # could increase within function
imprisoned_diff_min = 6
imprisoned_diff_max = 10
imprisoned_damage_penalty = 2  # deduct 2 hp for every wrong answer if imprisoned in slave camp

work_info = {
    "regular_work_tasknum":     10,  # controls frequency of regular work tasks, must get 10 right to finish work
    "regular_work_comp":       300,  # 300 credits awarded after 10 correct answers
    "overtime_work_rate":       15,  # how often overtime work tasks are given if opted into overtime
    "overtime_comp":            50,  # 50 credits awarded for every correct overtime task completed
    "work_difficulty_cap":       3,  # could increase within function
    "imprisoned_diff_min":       6,
    "imprisoned_diff_max":      10,
    "imprisoned_damage_penalty": 2   # deduct 2 hp for every wrong answer if imprisoned in slave camp
}

# ARC store items

arc_store_subs = {
    "prem_flav_sub":   {"id": 0, "name": "premium flav sub",      "price": 4000},
    "deluxe_flav_sub": {"id": 1, "name": "deluxe flav sub",       "price": 2000},
    "basic_flav_sub":  {"id": 2, "name": "basic flav sub",        "price":  300},
    "deluxe_ad_block": {"id": 3, "name": "deluxe ad blocker sub", "price": 5000},
    "basic_ad_block":  {"id": 4, "name": "basic ad blocker sub",  "price":  600}
}

arc_store_consumables = {
    "temp_ad_block": {"id": 0, "name": "temporary ad blocker", "price": 9999, "rr": 1.00},
    "aug_tux":       {"id": 1, "name": "aug tuxedo",           "price": 9999, "rr": 0.33},
    "aug_eve_gown":  {"id": 2, "name": "aug evening gown",     "price": 9999, "rr": 0.33},
    "aug_tan":       {"id": 3, "name": "aug tan",              "price": 9999, "rr": 0.33},
}

# Repeat discoverable items
rp_disc_items = {
    "hammer": {"id": 0, "name": "the glasses", "ill_cat": "na", "rr": 1.00}
}

# Unique discoverable items
uni_disc_items = {
    "the_glasses": {"id": 0, "name": "the glasses", "ill_cat": "na"}  # see the world as it is, blocks ads when worn
}

# Food

food_prices = {
    "unflav_paste": {"id": 0,  "name": "unflavoured food paste", "full_price":   0, "cat": "basic",  "rr": 1.00},
    "ortolan":      {"id": 1,  "name": "ortolan",                "full_price":   0, "cat": "luxury", "rr": 0.66},
    "caviar":       {"id": 2,  "name": "caviar",                 "full_price": 199, "cat": "luxury", "rr": 0.66},
    "lobster":      {"id": 3,  "name": "lobster",                "full_price": 199, "cat": "luxury", "rr": 0.66},
    "coq_au_vin":   {"id": 4,  "name": "coq au vin",             "full_price": 199, "cat": "luxury", "rr": 0.66},
    "sashimi":      {"id": 5,  "name": "sashimi",                "full_price": 199, "cat": "luxury", "rr": 0.66},
    "wagyu":        {"id": 6,  "name": "wagyu steak",            "full_price": 199, "cat": "luxury", "rr": 0.66},
    "burger":       {"id": 7,  "name": "greasy burger",          "full_price": 199, "cat": "basic",  "rr": 0.66},
    "mac_n_cheese": {"id": 8,  "name": "mac n cheese",           "full_price": 199, "cat": "basic",  "rr": 0.66},
    "crisps":       {"id": 9,  "name": "crisps",                 "full_price": 199, "cat": "basic",  "rr": 0.66},
    "noodles":      {"id": 10, "name": "instant noodles",        "full_price": 199, "cat": "basic",  "rr": 0.66},
    "pizza":        {"id": 11, "name": "pizza",                  "full_price": 199, "cat": "basic",  "rr": 0.66},
    "beans":        {"id": 12, "name": "beans",                  "full_price": 199, "cat": "basic",  "rr": 0.66}
}

# need to reformat reactions to 48 characters
food_reaction = {
    "unflav_paste": {"id": 0,  "react": {1: "As you bite into the insect paste, you feel something still moving.",
                                         2: "You make it two mouthfuls before you are holding back vomit.",
                                         3: "It's got to be at least 60 % cockcroach."}},
    "ortolan":      {"id": 1,  "react": {1: "Even chickens have been extinct for 10 years, let alone this thing.",
                                         2: "An overwhelming sense of shame falls upon you.",
                                         3: "Is it supposed to be this crunchy?"}},
    "caviar":       {"id": 2,  "react": {1: "The best that money can buy. But underneath it's all the same.",
                                         2: "Was it worth it?",
                                         3: "What came first? The fish or the egg?"}},
    "lobster":      {"id": 3,  "react": {1: "Apparently, lobsters never die of old age. We'd never let them anyway.",
                                         2: "Is a lobster a kind of crab? Or is a crab a kind of lobster?",
                                         3: "In Cambodia, you can get a lobster dinner for like a dollar."}},
    "coq_au_vin":   {"id": 4,  "react": {1: "Not actually a cock, but it is chicken.",
                                         2: "How much wine is in this?",
                                         3: "Cock. Balls. Chicken."}},
    "sashimi":      {"id": 5,  "react": {1: "Is sashimi a kind of sushi? Or is sushi a kind of sashimi?",
                                         2: "California rolls FTW.",
                                         3: "Hmmm octopus..."}},
    "wagyu":        {"id": 6,  "react": {1: "Mooooo!!",
                                         2: "Supposedly, the mayor has a private supply of real cows. I think it's BS.",
                                         3: "Hmmm steak..."}},
    "burger":       {"id": 7,  "react": {1: "No cheese, but it is royally tasty.",
                                         2: "Bap. Blap. Brrap.",
                                         3: "Burger. Burger. Burger."}},
    "mac_n_cheese": {"id": 8,  "react": {1: "I like cheese. I like pasta.",
                                         2: "Mac! Cheese! Mac n Cheese!",
                                         3: "Yup."}},
    "crisps":       {"id": 9,  "react": {1: "This is what you get turned into after retirement.",
                                         2: "Soilent green! Do ya know what I mean!",
                                         3: "Crispy crisps."}},
    "noodles":      {"id": 10, "react": {1: "Not spaghetti.",
                                         2: "Ramen in my tumin.",
                                         3: "Why are they called chop sticks? What do you chop with them?"}},
    "pizza":        {"id": 11, "react": {1: "A little slice of happiness to keep the pain away.",
                                         2: "Controversial take: Hawaiian is the best kind of pizza.",
                                         3: "It's not a pie. Why is always called pie?"}},
    "beans":        {"id": 12, "react": {1: "Good for your heart. And that's about it.",
                                         2: "Maybe they're actually just overgrown maggots.",
                                         3: "The cornerstone of any nutritious breakfast, lunch, or dinner."}}
}

# Drink

drink_reaction = {

}

drink_prices = {
    "unflav_water": {"id": 0, "name": "unflavoured water", "full_price":   0, "cat": "basic",  "rr": 1.00},
    "champagne":    {"id": 1, "name": "champagne",         "full_price":   0, "cat": "basic",  "rr": 0.66},
    "martini":      {"id": 2, "name": "martini",           "full_price":   0, "cat": "basic",  "rr": 0.66},
    "cola":         {"id": 7, "name": "cola",              "full_price": 199, "cat": "basic",  "rr": 0.66}
}

# Misc - NR
# need to have a function or something to check if pages already read and returning to page
# could do this by speeding up read speed and then setting back at the end or maybe something better
already_read_page = False
possible_options = []  # controls player options
choice_checked_for_error = False  # does this need to be global? check and remove if not

# ------------------------------------------- Biome Dictionaries ----------------------------------------- IN PROGRESS

# General Biome info - leave this as separate stuff
# (cur tile is below because of map list)
cur_biome = "sol_overworld"  # start in sol overworld at player appt
cur_loc_row = 10  # start at player appt tile
cur_loc_col = 18  # start at player appt tile
cur_shop_list = []  # initialize
cur_building = ""  # initialize
cur_ow_quest_list = []  # initialize
cur_move_dict = {  # initialize
    "w": {"disp": "up",    "command": "north"},
    "s": {"disp": "down",  "command": "south"},
    "a": {"disp": "left",  "command": "east"},
    "d": {"disp": "right", "command": "west"}
}
cur_ow_disp_text = []  # initialize
cur_ow_option_dict = {}  # initialize


# ---------- Sol ----------
# will need to modify sol bio to allow travel to invictus at some point, using minus x coords at certain y values
# co-ordinate system only works as navigation through overworld for middle and industrial districts
# at various points, there will be doors to certain areas e.g. the prison camp or central district
# larger facilities will therefor show as building, rather than nope, with the player prompted to go around
# nope will print "you have reached a boundary, you cannot proceed etc"
# trying to move into building will print "you can't get in this way, try to find an entrance"
# our could be more specific, e.g. "CD_border" will prompt "entrances are at N,E,S, and W"
# could then check either surroundings to determine which areas door is for

# prison camp may want to be a tardis area, to make it more unique, like walking around NESW isn't going to be
# so interesting. May just want 1. go to yard, 2. go to work station etc. Make prison smaller and farm bigger

a = "player_apartment"
b = "border"
c = "central_district"
d = "door"
e = "exit"
f = "farm"
g = "gate"
h = "hacker_base"
i = "industrial_district"
j = "job"
k = "kasino_town"
# l skipped because ambiguous for some reason
m = "middle_district"
n = "nope"
o = "police_base"
p = "political_district"
q = "gang1_territory"
r = "gang2_territory"
s = "slums"
t = "tram"
u = "museum"
v = "power_station"
w = "waste_centre"
x = ""
y = ""
z = "prison_camp"

# Movement direction option info
move_opt_info = {
    "none": "Blocked",
    "player_apartment": "Your Apartment",
    "border": "Blocked",
    "central_district": "Central District",
    "door": "Door",
    "exit": "Exit",
    "farm": "Farm",
    "gate": "Gate",
    "hacker_base": "Hacker Base",
    "industrial_district": "Industrial District",
    "job": "Work",
    "kasino_town": "Kasino Town",
    "middle_district": "Middle District",
    "nope": "You've reached the edge",
    "police_base": "Enforcer Base",
    "political_district": "Political District",
    "gang1_territory": "Gang1 Territory",
    "gang2_territory": "Gang2 Territory",
    "slums": "Slums",
    "tram": "Tram Station",
    "museum": "Museum of National Pride",
    "power_station": "Power Station",
    "waste_centre": "Waste Centre",
    "prison_camp": "Prison Camp"
}

# List controlling sol overworld map. Single character variables act as tiles.
# ROWs (on right) then COLs (along top)
sol_overworld_biome_list = [
 #   0 1 2 3 4 5 6 7 8 9 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 3 3 3 3 3 3 3 3 3 3 4 4 4 4 4 4 4 4 4 4 5
 #                       0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0
    [n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n],  # 0
    [n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,s,s,s,s,s,s,s,s,s,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n],  # 1
    [n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,s,s,s,s,s,s,s,s,s,s,s,s,s,s,i,i,i,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n],  # 2
    [n,n,n,n,n,n,n,n,n,n,n,n,n,n,s,s,s,s,s,s,s,s,s,i,i,s,s,s,s,s,s,i,i,i,b,v,v,n,n,n,n,n,n,n,n,n,n,n,n,n,n],  # 3
    [n,n,n,n,n,n,n,n,n,n,n,n,s,s,s,s,s,s,s,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,b,v,v,v,v,n,n,n,n,n,n,n,n,n,n,n,n],  # 4
    [n,n,n,n,n,n,n,n,n,n,s,s,s,s,s,s,s,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,b,v,v,v,v,v,v,n,n,n,n,n,n,n,n,n,n],  # 5
    [n,n,n,n,n,n,n,n,n,s,s,s,s,s,s,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,b,v,v,v,v,v,v,v,n,n,n,n,n,n,n,n,n],  # 6
    [n,n,n,n,n,n,n,n,s,s,s,s,s,s,i,i,i,i,i,i,i,i,i,i,i,i,i,t,i,i,h,i,i,i,g,v,v,v,v,v,v,v,b,n,n,n,n,n,n,n,n],  # 7
    [n,n,n,n,n,n,n,i,i,i,s,s,s,s,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,b,v,v,v,v,v,v,v,b,i,n,n,n,n,n,n,n],  # 8
    [n,n,n,n,n,n,i,i,i,i,i,s,s,i,i,i,i,i,i,i,i,i,m,m,m,m,m,m,m,i,i,i,i,i,b,v,v,v,v,v,v,v,b,i,i,n,n,n,n,n,n],  # 9
    [n,n,n,n,n,i,i,i,i,i,i,i,i,i,i,i,i,i,a,m,m,m,m,m,m,m,m,m,m,m,m,m,m,i,b,v,v,v,v,v,v,v,g,i,i,i,n,n,n,n,n],  # 10
    [n,n,n,n,n,i,i,i,i,i,i,i,i,i,i,i,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,b,v,v,v,v,v,v,v,b,i,i,i,n,n,n,n,n],  # 11
    [n,n,n,n,i,i,i,i,i,i,i,i,i,i,m,m,m,m,t,m,m,m,m,m,m,m,m,j,j,j,m,m,m,m,b,v,v,v,v,v,v,v,b,i,i,i,i,n,n,n,n],  # 12
    [n,n,n,n,i,i,i,i,i,i,i,i,i,m,m,m,m,m,m,u,m,m,m,m,m,m,m,j,j,j,m,m,m,m,b,b,g,b,b,b,b,b,b,i,i,i,i,n,n,n,n],  # 13
    [n,n,n,i,i,i,i,t,i,i,i,i,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,j,j,j,m,m,m,m,m,m,m,m,m,i,i,i,i,i,i,i,i,i,n,n,n],  # 14
    [n,n,n,i,i,i,i,i,i,i,i,i,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,i,i,i,t,i,i,i,i,i,n,n,n],  # 15
    [n,n,n,i,i,j,j,j,i,i,i,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,t,m,m,m,m,m,j,j,j,m,m,m,i,i,i,i,i,i,i,i,n,n,n],  # 16
    [n,n,i,i,i,j,j,j,i,i,i,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,j,j,j,m,m,m,i,i,i,j,j,j,i,i,i,n,n],  # 17
    [n,n,i,i,i,j,j,j,i,i,m,m,m,j,j,j,m,m,m,m,m,m,b,b,b,g,b,b,b,m,m,m,m,m,j,j,j,m,m,m,m,i,i,j,j,j,i,i,i,n,n],  # 18
    [n,n,i,i,i,i,i,i,i,i,m,m,m,j,j,j,m,m,m,m,b,b,b,c,c,c,c,c,b,b,b,m,m,m,m,m,m,m,m,m,m,i,i,j,j,j,i,i,i,n,n],  # 19
    [n,n,i,i,i,i,i,i,i,i,m,m,m,j,j,j,m,m,b,b,b,c,c,c,c,c,c,c,c,c,b,b,b,m,m,m,m,m,m,m,m,i,i,i,i,i,i,i,i,n,n],  # 20
    [n,i,i,i,i,i,i,i,i,i,m,m,m,m,m,m,m,b,b,c,c,c,c,c,c,c,c,c,c,c,c,c,b,b,m,m,m,m,m,m,m,i,i,i,i,i,i,i,i,i,n],  # 21
    [n,i,i,i,i,i,i,i,i,m,m,m,m,m,m,m,b,b,c,c,c,c,c,b,b,g,b,b,c,c,c,c,c,b,b,m,m,m,m,m,m,m,i,i,i,i,i,i,i,i,n],  # 22
    [n,i,i,i,i,i,i,i,i,m,m,m,m,m,m,b,b,c,c,c,c,c,b,b,p,p,p,b,b,c,c,c,c,c,b,b,m,m,b,b,b,b,b,b,g,b,b,b,b,b,n],  # 23
    [n,i,i,i,i,i,i,i,i,m,m,m,m,m,m,b,c,c,c,c,c,c,b,p,p,p,p,p,b,c,c,c,c,c,c,b,m,m,b,f,f,f,f,f,f,f,f,f,f,f,n],  # 24
    [g,i,i,i,i,i,i,i,i,m,m,m,m,m,m,g,c,c,c,c,c,c,g,p,p,p,p,p,g,c,c,c,c,c,c,g,m,m,b,f,f,f,f,f,f,f,f,f,f,f,n],  # 25
    [n,i,i,i,i,i,i,i,i,m,m,m,m,m,m,b,c,c,c,c,c,c,b,p,p,p,p,p,b,c,c,c,c,c,c,b,m,m,b,f,f,f,f,f,f,f,f,f,f,f,n],  # 26
    [n,i,i,i,t,i,i,i,i,m,m,t,m,m,m,b,b,c,c,c,c,c,b,b,p,p,p,b,b,c,c,c,c,c,b,b,m,m,b,f,f,f,f,f,f,f,f,f,f,f,n],  # 27
    [n,i,i,i,i,i,i,i,i,m,m,m,m,m,m,m,b,b,c,c,c,c,c,b,b,g,b,b,c,c,c,c,c,b,b,m,m,m,g,f,f,f,f,f,f,f,f,f,f,f,n],  # 28
    [n,i,i,j,j,j,i,i,i,i,m,m,m,m,m,m,m,b,b,c,c,c,c,c,c,c,c,c,c,c,c,c,b,b,m,m,m,m,b,f,f,f,f,f,f,f,f,f,f,f,n],  # 29
    [n,n,i,j,j,j,i,i,i,i,m,m,m,m,m,m,m,m,b,b,b,c,c,c,c,c,c,c,c,c,b,b,b,m,m,m,m,m,b,f,f,f,f,f,f,f,f,f,f,n,n],  # 30
    [n,n,i,j,j,j,i,i,i,k,k,k,k,k,m,t,m,m,m,m,b,b,b,c,c,c,c,c,b,b,b,m,m,m,m,m,m,m,b,f,f,f,f,f,f,f,f,f,f,n,n],  # 31
    [n,n,i,i,i,i,i,i,k,k,k,k,k,k,k,k,m,m,m,m,m,m,b,b,b,g,b,b,b,m,m,m,m,m,m,m,m,m,b,f,f,f,f,f,f,f,f,f,f,n,n],  # 32
    [n,n,i,i,i,i,i,i,k,k,k,k,k,k,k,k,k,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,b,b,b,b,b,b,b,b,b,b,b,n,n],  # 33
    [n,n,n,i,i,i,i,i,k,k,k,k,k,k,k,k,k,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,m,t,m,m,m,m,b,z,z,z,z,z,z,z,z,n,n,n],  # 34
    [n,n,n,i,i,i,i,i,i,k,k,k,k,k,k,k,m,m,j,j,j,m,m,b,b,g,b,b,b,m,m,m,m,m,m,m,m,m,m,g,z,z,z,z,z,z,z,z,n,n,n],  # 35
    [n,n,n,i,i,q,q,q,i,i,k,k,k,k,m,m,m,m,j,j,j,m,m,b,o,o,o,o,b,b,b,b,b,m,m,m,m,m,m,b,z,z,z,z,z,z,z,z,n,n,n],  # 36
    [n,n,n,n,q,q,q,q,q,i,i,i,i,m,m,m,m,m,j,j,j,m,m,b,o,o,o,o,o,o,o,o,b,m,m,m,b,g,b,b,z,z,z,z,z,z,z,n,n,n,n],  # 37
    [n,n,n,n,q,q,q,q,q,q,q,q,i,i,m,m,m,m,m,m,m,m,m,g,o,o,o,o,o,o,o,o,g,m,m,m,b,w,w,b,z,z,z,z,z,z,z,n,n,n,n],  # 38
    [n,n,n,n,n,q,q,q,q,q,q,q,i,i,i,i,m,m,m,m,m,m,m,b,o,o,o,o,o,o,o,o,b,m,m,i,b,w,w,b,b,z,z,z,z,z,n,n,n,n,n],  # 39
    [n,n,n,n,n,q,q,q,q,q,q,q,q,i,i,i,i,i,m,m,m,m,m,b,o,o,o,o,o,o,o,o,b,i,i,i,b,w,w,w,b,b,z,z,z,z,n,n,n,n,n],  # 40
    [n,n,n,n,n,n,q,q,q,q,q,q,q,r,r,i,i,i,i,i,i,i,m,b,b,b,b,g,b,b,b,b,b,i,i,i,b,w,w,w,w,b,b,z,z,n,n,n,n,n,n],  # 41
    [n,n,n,n,n,n,n,q,q,q,q,q,q,r,r,r,r,i,i,t,i,i,i,i,i,i,i,i,i,i,i,i,i,t,i,i,b,w,w,w,w,w,b,b,n,n,n,n,n,n,n],  # 42
    [n,n,n,n,n,n,n,n,q,q,q,q,r,r,r,r,r,r,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,g,w,w,w,w,w,w,n,n,n,n,n,n,n,n],  # 43
    [n,n,n,n,n,n,n,n,n,q,q,q,r,r,r,r,r,r,i,i,i,i,i,s,s,i,i,i,i,s,s,s,s,i,i,i,b,w,w,w,w,w,n,n,n,n,n,n,n,n,n],  # 44
    [n,n,n,n,n,n,n,n,n,n,q,q,r,r,r,r,r,r,r,i,i,i,s,s,s,s,i,i,s,s,s,s,s,s,i,i,b,w,w,w,w,n,n,n,n,n,n,n,n,n,n],  # 45
    [n,n,n,n,n,n,n,n,n,n,n,n,r,r,r,r,r,r,r,i,i,i,s,s,s,s,s,s,s,s,s,s,s,s,s,s,b,w,w,n,n,n,n,n,n,n,n,n,n,n,n],  # 46
    [n,n,n,n,n,n,n,n,n,n,n,n,n,n,r,r,r,r,r,r,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,b,n,n,n,n,n,n,n,n,n,n,n,n,n,n],  # 47
    [n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,r,r,r,s,s,s,s,s,s,s,s,s,s,s,s,s,s,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n],  # 48
    [n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,s,s,s,s,s,s,s,s,s,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n],  # 49
    [n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n]   # 50
]


# list to generate "you are here small" map
# will need to be updated with any changes to above sol_overworld_biome_list
full_small_map_list = [
 #     0 1 2 3 4 5 6 7 8 9 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 3 3 3 3 3 3 3 3 3 3 4 4 4 4 4 4 4 4 4 4 5
 #                         0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0
 #     012345678911111111112222222222333333333344444444445555555555666666666677777777778888888888999999999911
 #               01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678900
 #                                                                                                         01
     ["                                        x x x x x x x x x x x                                         "],  # 0
     ["                                x x x x x ~ ~ ~ ~ ~ ~ ~ ~ ~ x x x x x                                 "],  # 1
     ["                          x x x x ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ , , , x x x x                           "],  # 2
     ["                      x x x ~ ~ ~ ~ ~ ~ ~ ~ ~ , , ~ ~ ~ ~ ~ ~ , , , Δ v   x x x                       "],  # 3
     ["                  x x x ~ ~ ~ ~ ~ ~ ~ , , , , , , , , , , , , , , , Δ   v   v x x x                   "],  # 4
     ["                x x ~ ~ ~ ~ ~ ~ ~ , , , , , , , , , , , , , , , , , Δ v   v   v   x x                 "],  # 5
     ["              x x ~ ~ ~ ~ ~ ~ , , , , , , , , , , , , , , , , , , , Δ   v   v   v   x x               "],  # 6
     ["            x x ~ ~ ~ ~ ~ ~ , , , , , , , , , , , , , t , , h , , , = v   v   v   v Δ x x             "],  # 7
     ["          x x , , , ~ ~ ~ ~ , , , , , , , , , , , , , , , , , , , , Δ   v   v   v   Δ , x x           "],  # 8
     ["        x x , , , , , ~ ~ , , , , , , , , , . . . . . . . , , , , , Δ v   v   v   v Δ , , x x         "],  # 9
     ["        x , , , , , , , , , , , , , a . . . . . . . . . . . . . . , Δ   v   v   v   = , , , x         "],  # 10
     ["      x x , , , , , , , , , , , . . . . . . . . . . . . . . . . . . Δ v   v   v   v Δ , , , x x       "],  # 11
     ["      x , , , , , , , , , , . . . . t . . . . . . . . j j j . . . . Δ   v   v   v   Δ , , , , x       "],  # 12
     ["    x x , , , , , , , , , . . . . . . u . . . . . . . j j j . . . . Δ Δ = Δ Δ Δ Δ Δ Δ , , , , x x     "],  # 13
     ["    x , , , , t , , , , . . . . . . . . . . . . . . . j j j . . . . . . . . . , , , , , , , , , x     "],  # 14
     ["    x , , , , , , , , , . . . . . . . . . . . . . . . . . . . . . . . . . . . , , , t , , , , , x     "],  # 15
     ["  x x , , j j j , , , . . . . . . . . . . . . . . . . . t . . . . . j j j . . . , , , , , , , , x x   "],  # 16
     ["  x , , , j j j , , , . . . . . . . . . . . . . . . . . . . . . . . j j j . . . , , , j j j , , , x   "],  # 17
     ["  x , , , j j j , , . . . j j j . . . . . . Δ Δ Δ = Δ Δ Δ . . . . . j j j . . . . , , j j j , , , x   "],  # 18
     ["  x , , , , , , , , . . . j j j . . . . Δ Δ Δ - - - - - Δ Δ Δ . . . . . . . . . . , , j j j , , , x   "],  # 19
     ["x x , , , , , , , , . . . j j j . . Δ Δ Δ - - - - - - - - - Δ Δ Δ . . . . . . . . , , , , , , , , x x "],  # 20
     ["x , , , , , , , , , . . . . . . . Δ Δ - - - - - - - - - - - - - Δ Δ . . . . . . . , , , , , , , , , x "],  # 21
     ["x , , , , , , , , . . . . . . . Δ Δ - - - - - Δ Δ = Δ Δ - - - - - Δ Δ . . . . . . . , , , , , , , , x "],  # 22
     ["x , , , , , , , , . . . . . . Δ Δ - - - - - Δ Δ | | | Δ Δ - - - - - Δ Δ . . Δ Δ Δ Δ Δ Δ = Δ Δ Δ Δ Δ x "],  # 23
     ["x , , , , , , , , . . . . . . Δ - - - - - - Δ | | | | | Δ - - - - - - Δ . . Δ ⁄   ⁄   ⁄   ⁄   ⁄   ⁄ x "],  # 24
     ["= , , , , , , , , . . . . . . = - - - - - - = | | | | | = - - - - - - = . . Δ   ⁄   ⁄   ⁄   ⁄   ⁄   x "],  # 25
     ["x , , , , , , , , . . . . . . Δ - - - - - - Δ | | | | | Δ - - - - - - Δ . . Δ ⁄   ⁄   ⁄   ⁄   ⁄   ⁄ x "],  # 26
     ["x , , , t , , , , . . t . . . Δ Δ - - - - - Δ Δ | | | Δ Δ - - - - - Δ Δ . . Δ   ⁄   ⁄   ⁄   ⁄   ⁄   x "],  # 27
     ["x , , , , , , , , . . . . . . . Δ Δ - - - - - Δ Δ = Δ Δ - - - - - Δ Δ . . . = ⁄   ⁄   ⁄   ⁄   ⁄   ⁄ x "],  # 28
     ["x , , j j j , , , , . . . . . . . Δ Δ - - - - - - - - - - - - - Δ Δ . . . . Δ   ⁄   ⁄   ⁄   ⁄   ⁄   x "],  # 29
     ["x x , j j j , , , , . . . . . . . . Δ Δ Δ - - - - - - - - - Δ Δ Δ . . . . . Δ ⁄   ⁄   ⁄   ⁄   ⁄   x x "],  # 30
     ["  x , j j j , , , k k k k k . t . . . . Δ Δ Δ - - - - - Δ Δ Δ . . . . . . . Δ   ⁄   ⁄   ⁄   ⁄   ⁄ x   "],  # 31
     ["  x , , , , , , k k k k k k k k . . . . . . Δ Δ Δ = Δ Δ Δ . . . . . . . . . Δ ⁄   ⁄   ⁄   ⁄   ⁄   x   "],  # 32
     ["  x , , , , , , k k k k k k k k k . . . . . . . . . . . . . . . . . . . . . Δ Δ Δ Δ Δ Δ Δ Δ Δ Δ Δ x   "],  # 33
     ["  x x , , , , , k k k k k k k k k . . . . . . . . . . . . . . . . . t . . . . Δ ҂ ҂ ҂ ҂ ҂ ҂ ҂ ҂ x x   "],  # 34
     ["    x , , , , , , k k k k k k k . . j j j . . Δ Δ = Δ Δ Δ . . . . . . . . . . = ҂ ҂ ҂ ҂ ҂ ҂ ҂ ҂ x     "],  # 35
     ["    x , , q q q , , k k k k . . . . j j j . . Δ ! ! ! ! Δ Δ Δ Δ Δ . . . . . . Δ ҂ ҂ ҂ ҂ ҂ ҂ ҂ ҂ x     "],  # 36
     ["    x x q q q q q , , , , . . . . . j j j . . Δ ! ! ! ! ! ! ! ! Δ . . . Δ = Δ Δ ҂ ҂ ҂ ҂ ҂ ҂ ҂ x x     "],  # 37
     ["      x q q q q q q q q , , . . . . . . . . . = ! ! ! ! ! ! ! ! = . . . Δ w   Δ ҂ ҂ ҂ ҂ ҂ ҂ ҂ x       "],  # 38
     ["      x x q q q q q q q , , , , . . . . . . . Δ ! ! ! ! ! ! ! ! Δ . . , Δ   w Δ Δ ҂ ҂ ҂ ҂ ҂ x x       "],  # 39
     ["        x q q q q q q q q , , , , , . . . . . Δ ! ! ! ! ! ! ! ! Δ , , , Δ w   w Δ Δ ҂ ҂ ҂ ҂ x         "],  # 40
     ["        x x q q q q q q q r r , , , , , , , . Δ Δ Δ Δ = Δ Δ Δ Δ Δ , , , Δ   w   w Δ Δ ҂ ҂ x x         "],  # 41
     ["            x q q q q q q r r r r , , t , , , , , , , , , , , , , t , , Δ w   w   w Δ Δ x x           "],  # 42
     ["            x x q q q q r r r r r r , , , , , , , , , , , , , , , , , , =   w   w   w x x             "],  # 43
     ["              x x q q q r r r r r r , , , , , ~ ~ , , , , ~ ~ ~ ~ , , , Δ w   w   w x x               "],  # 44
     ["                x x q q r r r r r r r , , , ~ ~ ~ ~ , , ~ ~ ~ ~ ~ ~ , , Δ   w   w x x                 "],  # 45
     ["                  x x x r r r r r r r , , , ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ Δ w   x x x                   "],  # 46
     ["                      x x x r r r r r r ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ Δ x x x                       "],  # 47
     ["                          x x x x r r r ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ x x x x                           "],  # 48
     ["                                x x x x x ~ ~ ~ ~ ~ ~ ~ ~ ~ x x x x x                                 "],  # 49
     ["                                       x x x x x x x x x x x                                          "]   # 50
]


# Dictionary which is populated by procedural functions and can enter any fixed info, e.g. buildings.
# > "Shops" are procedural could be entered if specific shops are required.
# > Contains building locations
# > Don't store quests here. Scripted quests should have their own dictionary with locations.
# > Store specific overworld disp text here. Otherwise, pull from generic disp by tile type. DO NOT Store as fixed.
# > Overworld disp text should probably be short enough that screen doesn't need clearing.

sol_overworld_biome_dict = {
    10: {18: {"building": "player_appt_buil",
              #            aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
              "ow_disp": ["!SHORTPAUSE!",
                          "Outside player appt disp 1",
                          "!PAUSE!",
                          "Outside player appt disp 2"]}}
}

# Set probabilities for spawing shops as per tile types
sol_ow_shop_probs = {
    "player_apartment": {
                         "food_stall": 0.8,
                         "bar": 0.4,
                         "cafe": 0.3,
                         "restaurant": 0.1
                        },
    "border": {},
    "central_district": {},
    "door": {},
    "exit": {},
    "farm": {},
    "gate": {},
    "hacker_base": {},
    "industrial_district": {},
    "job": {},
    "kasino_town": {},
    "middle_district": {
                        "food_stall": 0.8,
                        "bar": 0.4,
                        "cafe": 0.3,
                        "restaurant": 0.1
                        },
    "nope": {},
    "police_base": {},
    "political_district": {},
    "gang1_territory": {},
    "gang2_territory": {},
    "slums": {},
    "tram": {},
    "museum": {},
    "power_station": {},
    "waste_centre": {},
    "prison_camp": {}
}

# Shop proper names
shop_fullnames = {
    "bar": "bar",
    "cafe": "café",
    "food_stall": "food stall",
    "restaurant": "restaurant"
}

# Generic overworld disp text dictionary
# > Role dice later with get current disp text based on this info. Don't overdo it. So only like 1 in 5 tiles should
#   display text etc. Also, only look here if there is no fixed disp text for that tile.
ow_gen_disp_dict = {
    "player_apartment": {},
    "border": {},
    "central_district": {},
    "door": {},
    "exit": {},
    "farm": {},
    "gate": {},
    "hacker_base": {},
    "industrial_district": {},
    "job": {},
    "kasino_town": {},
    "middle_district": {
        #                     aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
                         1: ["> In mid district disp 1"],
                         2: ["> In mid district disp 2"],
                         3: ["> In mid district disp 3"]
                        },
    "nope": {},
    "police_base": {},
    "political_district": {},
    "gang1_territory": {},
    "gang2_territory": {},
    "slums": {},
    "tram": {},
    "museum": {},
    "power_station": {},
    "waste_centre": {},
    "prison_camp": {}
}

# Current tile type
cur_tile = sol_overworld_biome_list[cur_loc_row][cur_loc_col]

# Building proper names
building_fullnames = {
    "player_appt_buil": "your apartment"
}

# ----------------------------------------- Scripted Quest Dictionaries ------------------------------------------------
# NOTE: could add a "key decisions" dict to track big forks. This could then be added as another requirement.
# Shouldn't be too hard to slap on.


# Manage quest content: display text, options, etc.

quests = {
    "ash_main_q1_meet_at_bar": {
                                0: {"Disp_text": [],
                                    "Disp_choices": ["1 | Do a thing",
                                                     "2 | Do a different thing"],
                                    "Dest": {1: 3, 2: 4},
                                    "Minigame": "N",
                                    "Minigame_param": {"Mini_par": "N"},
                                    "Minigame_dest": {"W": "", "L": "", "D": ""},
                                    "Need return ref": "N",
                                    "Is_game_over": "N",
                                    "Game_over_msg": "",
                                    "Updates": {},
                                    "Mket_store_avail": {"ARC_menu": "Y",
                                                         "Pinvent": "Y"},
                                    "ARC_menu_avail": "Y",
                                    "related_quest": "N"},
                                1: {"Disp_text": [],
                                    "Disp_choices": ["1 | Do a thing",
                                                     "2 | Do a different thing"],
                                    "Dest": {1: 3, 2: 4},
                                    "Minigame": "N",
                                    "Minigame_param": {"Mini_par": "N"},
                                    "Minigame_dest": {"W": "", "L": "", "D": ""},
                                    "Need return ref": "N",
                                    "Is_game_over": "N",
                                    "Game_over_msg": "",
                                    "Updates": {},
                                    "Mket_store_avail": {"ARC_menu": "Y",
                                                         "Pinvent": "Y"},
                                    "ARC_menu_avail": "Y",
                                    "related_quest": "N"}
                                },
    "go_to_work_q1":           {
                                    #              aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
                                0: {"Disp_text": ["!PAUSE!",
                                                  "> Going to work disp text 1"],
                                    "Disp_choices": ["1 | Do a thing",
                                                     "2 | Do a different thing"],
                                    "Dest": {1: 3, 2: 4},
                                    "Minigame": "N",
                                    "Minigame_param": {"Mini_par": "N"},
                                    "Minigame_dest": {"W": "", "L": "", "D": ""},
                                    "Need return ref": "N",
                                    "Is_game_over": "N",
                                    "Game_over_msg": "",
                                    "Updates": {},
                                    "Mket_store_avail": {"ARC_menu": "Y",
                                                         "Pinvent": "Y"},
                                    "ARC_menu_avail": "Y",
                                    "related_quest": "N"},
                                1: {"Disp_text": [],
                                    "Disp_choices": ["1 | Do a thing",
                                                     "2 | Do a different thing"],
                                    "Dest": {1: 3, 2: 4},
                                    "Minigame": "N",
                                    "Minigame_param": {"Mini_par": "N"},
                                    "Minigame_dest": {"W": "", "L": "", "D": ""},
                                    "Need return ref": "N",
                                    "Is_game_over": "N",
                                    "Game_over_msg": "",
                                    "Updates": {},
                                    "Mket_store_avail": {"ARC_menu": "Y",
                                                         "Pinvent": "Y"},
                                    "ARC_menu_avail": "Y",
                                    "related_quest": "N"}
                                }
}

# Manage quest progress

quest_prog = {
    "ash_main_q1_meet_at_bar":        {"pos": 0,
                                       "prog": "not_started"},
    "ash_main_q2_meet_at_hackerbase": {"pos": 0,
                                       "prog": "not_started"},
    "go_to_work_q1":                  {"pos": 0,
                                       "prog": "not_started"},
    "go_to_work_q2":                  {"pos": 0,
                                       "prog": "not_started"}
}

# Manage quest requirements
# > By default, completed quests will not appear in overworld. No need to specify for every case.
# > For any quests where we want an endless loop at the end, e.g. sunlight balcony quest in apartment, just don't set
#   the prog status in quest_prog to "comp", etc. This will be handled by the specific quest function.

quest_req = {
    "ash_main_q1_meet_at_bar":        {
                                       "char_met": {},
                                       "char_dead": {"ash_dead": False},
                                       "char_rom": {},
                                       "char_fren": {},
                                       "alleg": {},
                                       "skills": {},
                                       "quest_prog": {}
                                       },
    "ash_main_q2_meet_at_hackerbase": {
                                       "char_met": {},
                                       "char_dead": {"ash_dead": False},
                                       "char_rom": {},
                                       "char_fren": {},
                                       "alleg": {},
                                       "skills": {},
                                       "quest_prog": {"ash_main_q1_meet_at_bar": "comp"}
                                       },
    "go_to_work_q1":                  {
                                       "char_met": {},
                                       "char_dead": {"work_friend_dead": False},
                                       "char_rom": {},
                                       "char_fren": {},
                                       "alleg": {},
                                       "skills": {},
                                       "quest_prog": {}
                                       },
    "go_to_work_q2":                  {
                                       "char_met": {},
                                       "char_dead": {"work_friend_dead": False},
                                       "char_rom": {},
                                       "char_fren": {},
                                       "alleg": {},
                                       "skills": {},
                                       "quest_prog": {"go_to_work_q1": "comp"}
                                       }
}

# Manage scripted quest locations in the overworld.
# > ONLY FOR QUESTS directly in the overworld. Handle quests inside buildings separatly.
# > First key is row ref. Second key is col ref.

ow_quest_loc = {
    12: {18: ["go_to_work_q1",
              "go_to_work_q2"]}
}

# Manage text prompts for quest options. Need to keep these as short as possible.
# May need to suplement with some conditional display text. Can handle this with building functions etc, based on
# quest performance, as could get a bit niche.

quest_opt_text = {
    #                                      aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    "ash_main_q1_meet_at_bar":            "A band is setting up for a gig. Check it out.",
    "ash_main_q2_meet_at_hackerbase":     "Blah. knock on hackerbase door idk.",
    "go_to_work_q1":                      "A work colleague is by the station. Say hi.",
    "go_to_work_q2":                      "Your friend is back. Go over to him."
}


# ------------------------------------------------- Functions ----------------------------------------------------------

# ----- Drunk text ----- NR
# Apply function to any printed text (inside the print), this will corrupt if the player gets drunk
# drunk_text_test = "This is a sentence about being a sentence! Hope I don't get too drunk!"
# drunk_counter = 10

def drunk_filter(text):
    drunkness = min(10, drunk_counter) * 0.25 / 10
    drunk_text = []
    words = text.split(' ')
    for word in words:
        new_word = []
        for wo in word:
            outcome = random.random()
            if outcome <= drunkness:
                wo = random.choice(string.ascii_letters)
            else:
                wo = wo
            new_word.append(wo)
        new_word = "".join(new_word)
        drunk_text.append(new_word)

    drunk_text = " ".join(drunk_text)

    return drunk_text

# print(drunk_filter(drunk_text_test))


# ----- Drugged text ----- NR
# Apply function to any printed text (inside the print, outside drunk), this will mix up text if player is drugged
# drugged_text_test = "This is a sentence about being a sentence! Hope I don't get drugged!"
# drugged_counter = 10

def drugged_filter(text):
    druggedness = min(10, drugged_counter) * 0.3 / 10
    drugged_text = []
    words = text.split(' ')
    for word in words:
        outcome = random.random()
        if outcome <= druggedness:
            drugged_text.insert(0, word)
        else:
            drugged_text.append(word)

    drugged_text = " ".join(drugged_text)

    return drugged_text

# print(drugged_filter(drugged_text_test))


# ----- Generate work question ----- NR
# Returns tuple with question and answer.
# Difficulty of standard work questions is easier. Will be harder for prison work.

def gen_work():
    if not perks_and_bools["in_prison"]:
        num1 = random.randint(2, work_difficulty_cap * 5)
        num2 = random.randint(2, work_difficulty_cap * 5)
    else:
        num1 = random.randint(imprisoned_diff_min * 2, imprisoned_diff_max * 9)
        num2 = random.randint(imprisoned_diff_min * 2, imprisoned_diff_max * 9)
    symbol = random.randint(1, 5)
    add_sub_mod = random.randint(1, 5)
    if symbol == 1:
        w_question = "What is " + str(num1 * add_sub_mod) + " + " + str(num2 * add_sub_mod) + "?"
        w_answer = num1 * add_sub_mod + num2 * add_sub_mod
    elif symbol == 2:
        w_question = "What is " + str(num1 * add_sub_mod) + " - " + str(num2 * add_sub_mod) + "?"
        w_answer = num1 * add_sub_mod - num2 * add_sub_mod
    elif symbol == 3 and num1 > num2 and num1 % num2 != 0:
        w_question = "What is the remainder of " + str(num1) + " ÷ " + str(num2) + "?"
        w_answer = num1 % num2
    else:
        w_question = "What is " + str(num1) + " × " + str(num2) + "?"
        w_answer = num1 * num2

    new_tuple = (w_question, w_answer)

    return new_tuple

# for testing
# work_example = gen_work()
# print(work_example)


# ----- Produce ad ----- GFN
# return rather than print, so we can fix before a loop and freeze ad in cases of wrong inputs

def produce_ad():
    if perks_and_bools["hacked_prem_ad_block"]:
        advert_blocked = True
    elif perks_and_bools["wearing_the_glasses"]:
        advert_blocked = True
    elif perks_and_bools["voided"]:
        advert_blocked = True
    elif status_counters["ad_shield_counter"] > 0:
        advert_blocked = True
    elif perks_and_bools["sub_deluxe_ad_block"]:
        if random.randint(1, 10) <= 6:
            advert_blocked = True
        else:
            advert_blocked = False
    elif perks_and_bools["sub_basic_ad_block"]:
        if random.randint(1, 10) <= 2:
            advert_blocked = True
        else:
            advert_blocked = False
    else:
        advert_blocked = False
    # select ad subject and ad within that subject
    if not advert_blocked:
        ad_id = random.randint(0, max(ads.keys()))
        ad_num = random.randint(0, 2)
        advert = ads[ad_id]["ad"][ad_num]
        advert = "(" + " ".join(advert) + ")"
    else:
        advert = "(AD: Ad Blocked)"
    # return rather than print
    return advert


# testing
# produce_ad()  # for testing
# time.sleep(20)  # for testing


# ----- Update Counters at End of Turn ----- NR
# commented out until cba to remap to dict
# def end_turn_counter_update():
#     # -1 at end of turn, subscription charge handled independently
#     global drunk_counter
#     drunk_counter = max(0, drunk_counter - 1)
#     global drugged_counter
#     drugged_counter = max(0, drugged_counter - 1)
#     global hungover_counter
#     hungover_counter = max(0, hungover_counter - 1)
#     global blind_counter
#     blind_counter = max(0, blind_counter - 1)
#     global deaf_counter
#     deaf_counter = max(0, deaf_counter - 1)
#     global temp_ad_blocker_counter
#     temp_ad_blocker_counter = max(0, temp_ad_blocker_counter - 1)
#     global ad_shield_counter
#     ad_shield_counter = max(0, ad_shield_counter - 1)
#     global ARC_temp_disabled_counter
#     ARC_temp_disabled_counter = max(0, ARC_temp_disabled_counter - 1)
#     global ad_bomb_counter
#     ad_bomb_counter = max(0, ad_bomb_counter - 1)
#     global sol_effect_counter
#     sol_effect_counter = max(0, sol_effect_counter - 1)
#     global sol_addict_counter
#     sol_addict_counter = max(0, sol_addict_counter - 1)
#     global can_sleep_counter
#     can_sleep_counter = max(0, can_sleep_counter - 1)
#     # regain +2 health at end of turn
#     global health
#     health = min(100, health + 2)
#     # update overdraft counter - just the counter, sending to camp handled separately
#     global overdraft_counter
#     if current_balance < 0:
#         overdraft_counter = min(50, overdraft_counter + 1)
#     else:
#         overdraft_counter = 0


# ----- work out subscription charge amount ----- NR
# commented out for now until i cba to remap to dict
# def sub_charge_amount():
#     if sub_prem_flav:
#         flav_amount = 4000
#     elif sub_deluxe_flav:
#         flav_amount = 2000
#     elif sub_basic_flav:
#         flav_amount = 300
#     else:
#         flav_amount = 0
#     if sub_deluxe_ad_block:
#         ad_block_amount = 5000
#     elif sub_basic_ad_block:
#         ad_block_amount = 600
#     else:
#         ad_block_amount = 0
#     sub_charge_total = flav_amount + ad_block_amount
#
#     return sub_charge_total


# ----- subscription charge ----- NR
# handled separately from other counters as more complicated
# run at end of turn

# commented out for now until i cba to remap to dict
# def subscription_charge():
#     global subscription_charge_counter
#     global current_balance
#     if subscription_charge_counter == 50:
#         current_balance -= sub_charge_amount()
#         subscription_charge_counter = 0
#     else:
#         subscription_charge_counter = min(50, subscription_charge_counter + 1)


# ----- clear function ----- GFN

def clear():
    # for windows the os.name is "nt"
    if name == "nt":
        _ = system("cls")
    # for mac and linux the os.name is 'posix'
    else:
        _ = system("clear")


# Then, whenever you want to clear the screen, just use this clear function as:
# clear()


# ----- control read speed ----- NR

def read_speed(speed=1):
    global text_delay
    global error_delay
    global med_delay
    global short_delay
    # normal speed
    if speed == 1:
        text_delay = 3
        error_delay = 1.5
        med_delay = 1
        short_delay = 0.10
    # quick
    elif speed == 2:
        text_delay = 1.1
        error_delay = 0.75
        med_delay = 0.5
        short_delay = 0.10
    # superfast
    elif speed == 3:
        text_delay = 0.10
        error_delay = 0.10
        med_delay = 0.10
        short_delay = 0.10
    # for re-reading
    elif speed == 4:
        text_delay = 0
        med_delay = 0
    else:
        text_delay = 3
        error_delay = 1.5
        med_delay = 1
        short_delay = 0.10


# ----- banner text and printing ----- GFN

def banner_text(text):
    space_counter = int((48 - len(text)) * 0.5)
    spacer = " " * space_counter
    print("")  # leave blank for hp and bank info
    print("________________________________________________")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print(spacer + text)
    print("")
    print("")
    print("")
    print("")
    print("")
    print("________________________________________________")


def empty_banner():
    print("")  # leave blank for hp and bank info
    print("________________________________________________")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("________________________________________________")


def print_middle(text):
    space_count = int((48 - len(text)) / 2)
    spacer = " " * space_count
    print(spacer + text)


# ----- print display text ----- NR for main, used for prologue as is
# If page has already been read and need to flip back, will nerf delays and then reset after printing

def print_disp_text(disp_list):
    global already_read_page
    global text_delay
    global med_delay
    if already_read_page:
        text_delay = 0
        med_delay = 0
    for disp_section in disp_list:
        if disp_section == "!PAUSE!":
            time.sleep(text_delay)
        elif disp_section == "!ENDPAGE!":
            time.sleep(text_delay)
            time.sleep(med_delay)
            clear()
        else:
            print(drugged_filter(drunk_filter(disp_section)))
    read_speed(read_speed_choice)
    already_read_page = True


# ----- get current date time ----- GFN

def current_datetime():
    what_is_the_datetime = datetime.datetime.now()
    return what_is_the_datetime


# ----- get min difference between 2 datetimes as integer ----- GFN
#    print(time_delta.total_seconds()) - use this logic to get seconds difference
#    print(time_delta.total_seconds() / 60 ** 2) - and this one to get hours

def min_diff_int(datetime_1, datetime_2):
    time_delta = datetime_2 - datetime_1
    raw_min_diff = time_delta.total_seconds() / 60
    int_min_diff = int(raw_min_diff)
    return int_min_diff


# ----- hp and bank balance header ----- GFN
# Use hp_spacer to make sure hp doesn't move, then balance should increase to the left

def hp_bank_header():
    # aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    if health == 100:
        hp_spacer = ""
    elif 10 <= health <= 99:
        hp_spacer = " "
    else:
        hp_spacer = "  "
    health_and_spacer = "  HP: " + hp_spacer + str(health) + "/100"
    balance_disp = str(current_balance) + " cR  "
    middle_spacer_size = 48 - len(health_and_spacer) - len(balance_disp)
    middle_spacer = " " * middle_spacer_size
    print(health_and_spacer + middle_spacer + balance_disp)
#   print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")


# ----- balance change animation ----- GFN
# print bank balance, wait, then scroll to new balance, wait, then clear

def balance_chng_animation(up=0, down=0):
    global current_balance
    delta = up - down
    original_balance = current_balance
    new_balance = current_balance + delta
    clear()
    banner_text("Account Balance: " + str(current_balance) + " cR")
    time.sleep(med_delay)
    time.sleep(med_delay)
    while up - down != 0 and current_balance != new_balance:
        if delta > 0:
            if 0 <= (new_balance - current_balance) < 100:
                current_balance += 1
            elif 100 <= (new_balance - current_balance) < 200:
                current_balance += random.randint(5, 7)
            elif 200 <= (new_balance - current_balance) < 500:
                current_balance += random.randint(13, 17)
            elif 500 <= (new_balance - current_balance) < 1000:
                current_balance += random.randint(23, 27)
            elif 1000 <= (new_balance - current_balance) < 3000:
                current_balance += random.randint(33, 37)
            elif 3000 <= (new_balance - current_balance) < 5000:
                current_balance += random.randint(43, 47)
            else:
                current_balance += random.randint(93, 97)
            clear()
            banner_text("Account Balance: " + str(current_balance) + " cR")
            time.sleep(0.0000001)
        elif delta < 0:
            if 0 <= (current_balance - new_balance) < 100:
                current_balance -= 1
            elif 100 <= (current_balance - new_balance) < 200:
                current_balance -= random.randint(5, 7)
            elif 200 <= (current_balance - new_balance) < 500:
                current_balance -= random.randint(13, 17)
            elif 500 <= (current_balance - new_balance) < 1000:
                current_balance -= random.randint(23, 27)
            elif 1000 <= (current_balance - new_balance) < 3000:
                current_balance -= random.randint(33, 37)
            elif 3000 <= (current_balance - new_balance) < 5000:
                current_balance -= random.randint(43, 47)
            else:
                current_balance -= random.randint(93, 97)
            clear()
            banner_text("Account Balance: " + str(current_balance) + " cR")
            time.sleep(0.0000001)
        else:
            print("Test: that wasn't supposed to happen")
    clear()
    banner_text("Account Balance: " + str(current_balance) + " cR")
    time.sleep(med_delay)
    time.sleep(med_delay)


# ---------- draw maps ---------- IN PROGRESS
# ----- draw big sol map -----
# Maybe have "you are here" functionality, but initially just draw the map

def draw_big_sol_map():
    #           baaaababababbabbbbabbbbaabbbbabbbbabbabababaaaab
    print(" __________________________________________________________")
    print("|                                 F2                       |")
    print("|           ,              xxxxxx/                         |")
    print("|                        XXXXXXXXXX             ,     ,    |")
    print("|    ,     ,        XXXXX          XXXXX                   |")
    print("|                XXXX                  XXXX         ,      |")
    print("|             XXXX                        XXXX             |")
    print("|           XXX              ..              XXX       ,   |")
    print("|         XXX         .              .         XXX         |")
    print("|        XX                                      XX        |")
    print("|  ,    XX        .          xx          .        XX       |")
    print("|      XX               x   .  .   x               XX      |")
    print("|     XX       .     x                x     .       XX     |")
    print("|     XX           x .      .  .      . x           XX     |")
    print("|xxxXXXX     .    x       .      .       x    .     XX     |")
    print("|xxxXXXX     .    x       .  PD  .       x    .     XX     |")
    print("|    /XX           x .      .  .      . x           XX     |")
    print("|  F1 XX       .     x       CD       x     .       XX     |")
    print("|      XX               x  .    .  x               XX      |")
    print("|  ,    XX        .          xx          .        XX       |")
    print("|        XX                                      XX     ,  |")
    print("|         XXX          .     MD      .         XXX         |")
    print("|    ,     XXX               ..              XXX           |")
    print("|            XXXX                         XXXXXX     ,     |")
    print("|                XXXX        ID        XXXX   XX-F3        |")
    print("|                   XXXXX          XXXXX                   |")
    print("|    ,        ,          XXXXXXXXXX               ,        |")
    print("|                                           ,              |")
    print("|        ,                SOL CITY                     ,   |")
    print("|__________________________________________________________|")
    print("")
    print("  PD | Political District    F1 | Tunnel to Invictus ruins")
    print("  CD | Central District      F2 | Tidal Power Facility")
    print("  MD | Midddle District      F3 | Waste Disposal Chute")
    print("  ID | Industrial District")
    print("")
    #        baaaababababbabbbbabbbbaabbbbabbbbabbabababaaaab


# ----- quick access big sol map -----

def quick_big_sol_map():
    big_map_choice = 1  # initialize
    while big_map_choice != 0:
        clear()
        draw_big_sol_map()
        print("")
        print("0 | Back")
        print("")
        try:
            big_map_choice = int(input())
        except ValueError:
            print(drunk_filter("Please choose one of the options..."))  # leave drug filter off
            time.sleep(error_delay)
            clear()
            continue
        if big_map_choice == 0:
            time.sleep(med_delay)
            clear()
            continue
        else:
            print(drunk_filter("Please choose one of the options..."))  # leave drug filter off
            time.sleep(error_delay)
            clear()
            continue


# ----- draw full small sol map -----
# > create a copy of the map so that isn't changed
# > pull out the row the player is in, go in the list for that row, replace character in string with player symbol,
#   then put new row back into copied map list and display

def draw_full_small_sol_map():
    you_are_here_list = full_small_map_list[:]
    youarehere_row = you_are_here_list[cur_loc_row]
    youarehere_col_ref = cur_loc_col * 2
    here_string = youarehere_row[0]
    player_replacement = "P"
    here_string = here_string[0:youarehere_col_ref] + player_replacement + here_string[youarehere_col_ref+1:]
    # print(here_string)
    here_mini_list = [here_string]
    # print(here_mini_list)
    you_are_here_list[cur_loc_row] = here_mini_list[:]
    for row in you_are_here_list:
        print(row[0])


# ----- print section of small sol map -----

def print_small_sol_map():
    # generate "you are here" map list
    you_are_here_list = full_small_map_list[:]
    youarehere_row = you_are_here_list[cur_loc_row]
    youarehere_col_ref = cur_loc_col * 2
    here_string = youarehere_row[0]
    player_replacement = "P"
    here_string = here_string[0:youarehere_col_ref] + player_replacement + here_string[youarehere_col_ref+1:]
    # print(here_string)
    here_mini_list = [here_string]
    # print(here_mini_list)
    you_are_here_list[cur_loc_row] = here_mini_list[:]
    # get row ranges for display section
    small_row_start = max(0,cur_loc_row - 5)
    small_row_end = min(50, cur_loc_row + 7)
    if small_row_start == 0:
        small_row_end = 11
    if small_row_end == 50:
        small_row_start = 39
    # get column ranges for display section
    small_col_start = max(0, (cur_loc_col - 12) * 2)
    small_col_end = min(101, (cur_loc_col + 12) * 2)
    if small_col_start == 0:
        small_col_end = 48
    if small_col_end == 101:
        small_col_start = 54
    # print selection of map and allow exit
    map_choice = 1  # initialize
    while map_choice != 0:
        clear()
        hp_bank_header()
        print("________________________________________________")
        for row in you_are_here_list[small_row_start:small_row_end]:
            if small_col_end == 101:
                print(row[0][small_col_start:])
            else:
                print(row[0][small_col_start:small_col_end])
        print("________________________________________________")
        print("")
        print_middle("P = You")
        print("")
        print("0 | Back")
        print("")
        try:
            map_choice = int(input())
        except ValueError:
            print(drunk_filter("Please choose one of the options..."))  # leave drug filter off
            time.sleep(error_delay)
            clear()
            continue
        if map_choice == 0:
            time.sleep(med_delay)
            clear()
        else:
            print(drunk_filter("Please choose one of the options..."))  # leave drug filter off
            time.sleep(error_delay)
            clear()


# ----- section of small sol map as banner -----

def sol_map_banner():
    # generate "you are here" map list
    you_are_here_list = full_small_map_list[:]
    youarehere_row = you_are_here_list[cur_loc_row]
    youarehere_col_ref = cur_loc_col * 2
    here_string = youarehere_row[0]
    player_replacement = "P"
    here_string = here_string[0:youarehere_col_ref] + player_replacement + here_string[youarehere_col_ref+1:]
    # print(here_string)
    here_mini_list = [here_string]
    # print(here_mini_list)
    you_are_here_list[cur_loc_row] = here_mini_list[:]
    # get row ranges for display section
    small_row_start = max(0,cur_loc_row - 5)
    small_row_end = min(50, cur_loc_row + 7)
    if small_row_start == 0:
        small_row_end = 11
    if small_row_end == 50:
        small_row_start = 39
    # get column ranges for display section
    small_col_start = max(0, (cur_loc_col - 12) * 2)
    small_col_end = min(101, (cur_loc_col + 12) * 2)
    if small_col_start == 0:
        small_col_end = 48
    if small_col_end == 101:
        small_col_start = 54
    # print selection of map as banner
    print("________________________________________________")
    for row in you_are_here_list[small_row_start:small_row_end+1]:
        if small_col_end == 101:
            print(row[0][small_col_start:])
        else:
            print(row[0][small_col_start:small_col_end])
    print("________________________________________________")


# ---------- Add/remove items from inventory/storage ---------- GFN
# ----- add "n" of specified item to player inventory ----- GFN

def add_item_inventory(item, num=1):
    global player_invent
    if item in player_invent:
        player_invent[item] += num
    else:
        player_invent[item] = num


# ----- remove "n" of specified item from player inventory ----- GFN

def remove_item_inventory(item, num=1):
    global player_invent
    global equipment
    if player_invent and item in player_invent:
        if player_invent[item] > num:
            player_invent[item] -= num
        elif player_invent[item] == num:
            if item == equipment["weapon"]:
                equipment["weapon"] = "none"
            elif item == equipment["head"]:
                equipment["head"] = "none"
            elif item == equipment["torso"]:
                equipment["torso"] = "none"
            elif item == equipment["legs"]:
                equipment["legs"] = "none"
            elif item == equipment["accessory"]:
                equipment["accessory"] = "none"
            del player_invent[item]


# ----- add "n" of specified item to apartment storage ----- GFN

def add_item_appt_storage(item, num=1):
    global appt_storage
    if item in appt_storage:
        appt_storage[item] += num
    else:
        appt_storage[item] = num


# ----- remove "n" of specified item from apartment storage ----- GFN

def remove_item_appt_storage(item, num=1):
    global appt_storage
    global equipment
    if appt_storage and item in appt_storage:
        if appt_storage[item] > num:
            appt_storage[item] -= num
        elif appt_storage[item] == num:
            if item == equipment["weapon"]:
                equipment["weapon"] = "none"
            elif item == equipment["head"]:
                equipment["head"] = "none"
            elif item == equipment["torso"]:
                equipment["torso"] = "none"
            elif item == equipment["legs"]:
                equipment["legs"] = "none"
            elif item == equipment["shoes"]:
                equipment["shoes"] = "none"
            elif item == equipment["accessory"]:
                equipment["accessory"] = "none"
            del appt_storage[item]


# ----- add "n" of specified item to hackerbase storage ----- GFN

def add_item_hackbase_storage(item, num=1):
    global hackbase_storage
    if item in hackbase_storage:
        hackbase_storage[item] += num
    else:
        hackbase_storage[item] = num


# ----- remove "n" of specified item from hackerbase storage ----- GFN

def remove_item_hackbase_storage(item, num=1):
    global hackbase_storage
    global equipment
    if hackbase_storage and item in hackbase_storage:
        if hackbase_storage[item] > num:
            hackbase_storage[item] -= num
        elif hackbase_storage[item] == num:
            if item == equipment["weapon"]:
                equipment["weapon"] = "none"
            elif item == equipment["head"]:
                equipment["head"] = "none"
            elif item == equipment["torso"]:
                equipment["torso"] = "none"
            elif item == equipment["legs"]:
                equipment["legs"] = "none"
            elif item == equipment["shoes"]:
                equipment["shoes"] = "none"
            elif item == equipment["accessory"]:
                equipment["accessory"] = "none"
            del hackbase_storage[item]


# --------------- Access ARC menu --------------- IN PROGRESS

# ---------- arc equipment ---------- GFN

# ----- equipment weapon ----- GFN
add_item_inventory("hammer")     # for testing
add_item_inventory("lead_pipe")  # for testing
add_item_inventory("screw_dr")   # for testing
add_item_inventory("crowbar")    # for testing


def arc_equip_weapon():
    print("arc equip weapon")  # for testing
    time.sleep(0.2)  # for testing
    global equipment
    equip_weapon_choice = 1
    weapon_equipped = False
    equip_weapon_list = []
    equip_weapon_list_ref = 0
    for item in player_invent:
        if all_item_type[item] == "weapon":
            equip_weapon_list.append(item)
    if equipment["weapon"] in player_invent:
        equip_weapon_list.remove(equipment["weapon"])
    print(equip_weapon_list)  # for testing
    time.sleep(0.2)  # for testing
    equip_weapon_list.sort()
    print(equip_weapon_list)  # for testing
    time.sleep(0.2)  # for testing
    while equip_weapon_choice != 0 and not weapon_equipped:  # if player goes back or equips weapon kick back
        if equip_weapon_list:
            one_message = "  1 | Equip "
        elif equipment["weapon"] == "none":
            one_message = " No weapons in inventory"
        else:
            one_message = ""
        if equip_weapon_list:
            display_name = all_item_fnames[equip_weapon_list[equip_weapon_list_ref]].rstrip()
            name_space_count = int((42 - len(display_name)) / 2)
            name_spacer = " " * name_space_count
        else:
            display_name = ""
            name_spacer = ""
        if equipment["weapon"] != "none":
            two_message = "  2 | Unequip " + all_item_fnames[equipment["weapon"]]
        else:
            two_message = ""
        if equip_weapon_list:
            weapon_counter = str(equip_weapon_list_ref + 1) + "/" + str(len(equip_weapon_list))
            weapon_counter_space_count = int((48 - len(weapon_counter)) / 2)
            weapon_counter_spacer = " " * weapon_counter_space_count
        else:
            weapon_counter = ""
            weapon_counter_spacer = ""
        clear()
        hp_bank_header()
        print("________________________________________________")
        print("")
        print("                  CHOOSE WEAPON                 ")
        print("")
        #      aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
        print("   Equipping a weapon may attract attention...")
        print("")
        if equip_weapon_list:
            print(name_spacer + ">> " + display_name + " <<")
            print(weapon_counter_spacer + weapon_counter)
        if len(equip_weapon_list) > 1:
            #      aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
            print("  3                                          4  ")
            print("  <<                                        >>  ")
        print("")
        print("")
        if equip_weapon_list:
            print(one_message + display_name)
        elif equipment["weapon"] == "none":
            print(one_message)
        if equipment["weapon"] != "none":
            print(two_message)
        print("")
        print("  0 | Back")
        print("")
        try:
            equip_weapon_choice = int(input())
        except ValueError:
            print(drunk_filter("Please choose one of the options..."))  # leave drug filter off
            time.sleep(error_delay)
            clear()
            continue
        # equip selected
        if equip_weapon_list and equip_weapon_choice == 1:
            equipment["weapon"] = equip_weapon_list[equip_weapon_list_ref]
            weapon_equipped = True
            print(display_name + " equipped...")
            time.sleep(med_delay)
        # unequip current weapon
        elif equipment["weapon"] != "none" and equip_weapon_choice == 2:
            equipment["weapon"] = "none"
            weapon_equipped = True
        # view previous weapon if player has more than 1 weapon
        elif len(equip_weapon_list) > 1 and equip_weapon_choice == 3:
            if equip_weapon_list_ref == 0:
                equip_weapon_list_ref = len(equip_weapon_list) - 1
            else:
                equip_weapon_list_ref -= 1
        # view next weapon if player has more than 1 weapon
        elif len(equip_weapon_list) > 1 and equip_weapon_choice == 4:
            if equip_weapon_list_ref == len(equip_weapon_list) - 1:
                equip_weapon_list_ref = 0
            else:
                equip_weapon_list_ref += 1
        # player backs out
        elif equip_weapon_choice == 0:
            time.sleep(med_delay)
        # some other unsupported option is attempted
        else:
            print(drunk_filter("Please choose one of the options..."))  # leave drug filter off
            time.sleep(error_delay)
            clear()


# ----- equipment head ----- GFN
add_item_inventory("ar_croc_head")   # for testing
add_item_inventory("ar_chick_head")  # for testing


def arc_equip_head():
    print("arc equip headgear")  # for testing
    time.sleep(0.2)  # for testing
    global equipment
    equip_head_choice = 1
    head_equipped = False
    equip_head_list = []
    equip_head_list_ref = 0
    for item in player_invent:
        if all_item_type[item] == "head":
            equip_head_list.append(item)
    if equipment["head"] in player_invent:
        equip_head_list.remove(equipment["head"])
    print(equip_head_list)  # for testing
    time.sleep(0.2)  # for testing
    equip_head_list.sort()
    print(equip_head_list)  # for testing
    time.sleep(0.2)  # for testing
    while equip_head_choice != 0 and not head_equipped:  # if player goes back or equips weapon kick back
        if equip_head_list:
            one_message = "  1 | Equip "
        elif equipment["head"] == "none":
            one_message = " No headgear in inventory"
        else:
            one_message = ""
        if equip_head_list:
            display_name = all_item_fnames[equip_head_list[equip_head_list_ref]].rstrip()
            name_space_count = int((42 - len(display_name)) / 2)
            name_spacer = " " * name_space_count
        else:
            display_name = ""
            name_spacer = ""
        if equipment["head"] != "none":
            two_message = "  2 | Unequip " + all_item_fnames[equipment["head"]]
        else:
            two_message = ""
        if equip_head_list:
            head_counter = str(equip_head_list_ref + 1) + "/" + str(len(equip_head_list))
            head_counter_space_count = int((48 - len(head_counter)) / 2)
            head_counter_spacer = " " * head_counter_space_count
        else:
            head_counter = ""
            head_counter_spacer = ""
        clear()
        hp_bank_header()
        print("________________________________________________")
        print("")
        print("                CHOOSE HEAD GEAR                ")
        print("")
        #      aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
        print("")
        if equip_head_list:
            print(name_spacer + ">> " + display_name + " <<")
            print(head_counter_spacer + head_counter)
        if len(equip_head_list) > 1:
            #      aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
            print("  3                                          4  ")
            print("  <<                                        >>  ")
        print("")
        print("")
        if equip_head_list:
            print(one_message + display_name)
        elif equipment["head"] == "none":
            print(one_message)
        if equipment["head"] != "none":
            print(two_message)
        print("")
        print("  0 | Back")
        print("")
        try:
            equip_head_choice = int(input())
        except ValueError:
            print(drunk_filter("Please choose one of the options..."))  # leave drug filter off
            time.sleep(error_delay)
            clear()
            continue
        # equip selected
        if equip_head_list and equip_head_choice == 1:
            equipment["head"] = equip_head_list[equip_head_list_ref]
            head_equipped = True
            print(display_name + " equipped...")
            time.sleep(med_delay)
        # unequip current headgear
        elif equipment["head"] != "none" and equip_head_choice == 2:
            equipment["head"] = "none"
            head_equipped = True
        # view previous headgear if player has more than 1 headgear
        elif len(equip_head_list) > 1 and equip_head_choice == 3:
            if equip_head_list_ref == 0:
                equip_head_list_ref = len(equip_head_list) - 1
            else:
                equip_head_list_ref -= 1
        # view next headgear if player has more than 1 headgear
        elif len(equip_head_list) > 1 and equip_head_choice == 4:
            if equip_head_list_ref == len(equip_head_list) - 1:
                equip_head_list_ref = 0
            else:
                equip_head_list_ref += 1
        # player backs out
        elif equip_head_choice == 0:
            time.sleep(med_delay)
        # some other unsupported option is attempted
        else:
            print(drunk_filter("Please choose one of the options..."))  # leave drug filter off
            time.sleep(error_delay)
            clear()


# ----- equipment torso ----- GFN
add_item_inventory("ar_croc_tors")   # for testing
add_item_inventory("ar_chick_tors")  # for testing


def arc_equip_torso():
    print("arc equip torso gear")  # for testing
    time.sleep(0.2)  # for testing
    global equipment
    equip_torso_choice = 1
    torso_equipped = False
    equip_torso_list = []
    equip_torso_list_ref = 0
    for item in player_invent:
        if all_item_type[item] == "torso":
            equip_torso_list.append(item)
    if equipment["torso"] in player_invent:
        equip_torso_list.remove(equipment["torso"])
    print(equip_torso_list)  # for testing
    time.sleep(0.2)  # for testing
    equip_torso_list.sort()
    print(equip_torso_list)  # for testing
    time.sleep(0.2)  # for testing
    while equip_torso_choice != 0 and not torso_equipped:  # if player goes back or equips weapon kick back
        if equip_torso_list:
            one_message = "  1 | Equip "
        elif equipment["torso"] == "none":
            one_message = " No torso gear in inventory"
        else:
            one_message = ""
        if equip_torso_list:
            display_name = all_item_fnames[equip_torso_list[equip_torso_list_ref]].rstrip()
            name_space_count = int((42 - len(display_name)) / 2)
            name_spacer = " " * name_space_count
        else:
            display_name = ""
            name_spacer = ""
        if equipment["torso"] != "none":
            two_message = "  2 | Unequip " + all_item_fnames[equipment["torso"]]
        else:
            two_message = ""
        if equip_torso_list:
            torso_counter = str(equip_torso_list_ref + 1) + "/" + str(len(equip_torso_list))
            torso_counter_space_count = int((48 - len(torso_counter)) / 2)
            torso_counter_spacer = " " * torso_counter_space_count
        else:
            torso_counter = ""
            torso_counter_spacer = ""
        clear()
        hp_bank_header()
        print("________________________________________________")
        print("")
        print("                CHOOSE TORSO GEAR                ")
        print("")
        #      aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
        print("")
        if equip_torso_list:
            print(name_spacer + ">> " + display_name + " <<")
            print(torso_counter_spacer + torso_counter)
        if len(equip_torso_list) > 1:
            #      aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
            print("  3                                          4  ")
            print("  <<                                        >>  ")
        print("")
        print("")
        if equip_torso_list:
            print(one_message + display_name)
        elif equipment["torso"] == "none":
            print(one_message)
        if equipment["torso"] != "none":
            print(two_message)
        print("")
        print("  0 | Back")
        print("")
        try:
            equip_torso_choice = int(input())
        except ValueError:
            print(drunk_filter("Please choose one of the options..."))  # leave drug filter off
            time.sleep(error_delay)
            clear()
            continue
        # equip selected
        if equip_torso_list and equip_torso_choice == 1:
            equipment["torso"] = equip_torso_list[equip_torso_list_ref]
            torso_equipped = True
            print(display_name + " equipped...")
            time.sleep(med_delay)
        # unequip current torso gear
        elif equipment["torso"] != "none" and equip_torso_choice == 2:
            equipment["torso"] = "none"
            torso_equipped = True
        # view previous torso gear if player has more than 1 torso gear
        elif len(equip_torso_list) > 1 and equip_torso_choice == 3:
            if equip_torso_list_ref == 0:
                equip_torso_list_ref = len(equip_torso_list) - 1
            else:
                equip_torso_list_ref -= 1
        # view next torso gear if player has more than 1 torso gear
        elif len(equip_torso_list) > 1 and equip_torso_choice == 4:
            if equip_torso_list_ref == len(equip_torso_list) - 1:
                equip_torso_list_ref = 0
            else:
                equip_torso_list_ref += 1
        # player backs out
        elif equip_torso_choice == 0:
            time.sleep(med_delay)
        # some other unsupported option is attempted
        else:
            print(drunk_filter("Please choose one of the options..."))  # leave drug filter off
            time.sleep(error_delay)
            clear()


# ----- equipment legs ----- GFN
add_item_inventory("ar_croc_legs")   # for testing
add_item_inventory("ar_chick_legs")  # for testing


def arc_equip_legs():
    print("arc equip legs gear")  # for testing
    time.sleep(0.2)  # for testing
    global equipment
    equip_legs_choice = 1
    legs_equipped = False
    equip_legs_list = []
    equip_legs_list_ref = 0
    for item in player_invent:
        if all_item_type[item] == "legs":
            equip_legs_list.append(item)
    if equipment["legs"] in player_invent:
        equip_legs_list.remove(equipment["legs"])
    print(equip_legs_list)  # for testing
    time.sleep(0.2)  # for testing
    equip_legs_list.sort()
    print(equip_legs_list)  # for testing
    time.sleep(0.2)  # for testing
    while equip_legs_choice != 0 and not legs_equipped:  # if player goes back or equips weapon kick back
        if equip_legs_list:
            one_message = "  1 | Equip "
        elif equipment["legs"] == "none":
            one_message = " No legs gear in inventory"
        else:
            one_message = ""
        if equip_legs_list:
            display_name = all_item_fnames[equip_legs_list[equip_legs_list_ref]].rstrip()
            name_space_count = int((42 - len(display_name)) / 2)
            name_spacer = " " * name_space_count
        else:
            display_name = ""
            name_spacer = ""
        if equipment["legs"] != "none":
            two_message = "  2 | Unequip " + all_item_fnames[equipment["legs"]]
        else:
            two_message = ""
        if equip_legs_list:
            legs_counter = str(equip_legs_list_ref + 1) + "/" + str(len(equip_legs_list))
            legs_counter_space_count = int((48 - len(legs_counter)) / 2)
            legs_counter_spacer = " " * legs_counter_space_count
        else:
            legs_counter = ""
            legs_counter_spacer = ""
        clear()
        hp_bank_header()
        print("________________________________________________")
        print("")
        print("                CHOOSE LEG GEAR                 ")
        print("")
        #      aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
        print("")
        if equip_legs_list:
            print(name_spacer + ">> " + display_name + " <<")
            print(legs_counter_spacer + legs_counter)
        if len(equip_legs_list) > 1:
            #      aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
            print("  3                                          4  ")
            print("  <<                                        >>  ")
        print("")
        print("")
        if equip_legs_list:
            print(one_message + display_name)
        elif equipment["legs"] == "none":
            print(one_message)
        if equipment["legs"] != "none":
            print(two_message)
        print("")
        print("  0 | Back")
        print("")
        try:
            equip_legs_choice = int(input())
        except ValueError:
            print(drunk_filter("Please choose one of the options..."))  # leave drug filter off
            time.sleep(error_delay)
            clear()
            continue
        # equip selected
        if equip_legs_list and equip_legs_choice == 1:
            equipment["legs"] = equip_legs_list[equip_legs_list_ref]
            legs_equipped = True
            print(display_name + " equipped...")
            time.sleep(med_delay)
        # unequip current legs gear
        elif equipment["legs"] != "none" and equip_legs_choice == 2:
            equipment["legs"] = "none"
            legs_equipped = True
        # view previous legs gear if player has more than 1 legs gear
        elif len(equip_legs_list) > 1 and equip_legs_choice == 3:
            if equip_legs_list_ref == 0:
                equip_legs_list_ref = len(equip_legs_list) - 1
            else:
                equip_legs_list_ref -= 1
        # view next legs gear if player has more than 1 legs gear
        elif len(equip_legs_list) > 1 and equip_legs_choice == 4:
            if equip_legs_list_ref == len(equip_legs_list) - 1:
                equip_legs_list_ref = 0
            else:
                equip_legs_list_ref += 1
        # player backs out
        elif equip_legs_choice == 0:
            time.sleep(med_delay)
        # some other unsupported option is attempted
        else:
            print(drunk_filter("Please choose one of the options..."))  # leave drug filter off
            time.sleep(error_delay)
            clear()
            
            
# ----- equipment shoes ----- GFN
add_item_inventory("ar_croc_feet")   # for testing
add_item_inventory("ar_chick_feet")  # for testing


def arc_equip_shoes():
    print("arc equip shoes gear")  # for testing
    time.sleep(0.2)  # for testing
    global equipment
    equip_shoes_choice = 1
    shoes_equipped = False
    equip_shoes_list = []
    equip_shoes_list_ref = 0
    for item in player_invent:
        if all_item_type[item] == "shoes":
            equip_shoes_list.append(item)
    if equipment["shoes"] in player_invent:
        equip_shoes_list.remove(equipment["shoes"])
    print(equip_shoes_list)  # for testing
    time.sleep(0.2)  # for testing
    equip_shoes_list.sort()
    print(equip_shoes_list)  # for testing
    time.sleep(0.2)  # for testing
    while equip_shoes_choice != 0 and not shoes_equipped:  # if player goes back or equips weapon kick back
        if equip_shoes_list:
            one_message = "  1 | Equip "
        elif equipment["shoes"] == "none":
            one_message = " No shoes gear in inventory"
        else:
            one_message = ""
        if equip_shoes_list:
            display_name = all_item_fnames[equip_shoes_list[equip_shoes_list_ref]].rstrip()
            name_space_count = int((42 - len(display_name)) / 2)
            name_spacer = " " * name_space_count
        else:
            display_name = ""
            name_spacer = ""
        if equipment["shoes"] != "none":
            two_message = "  2 | Unequip " + all_item_fnames[equipment["shoes"]]
        else:
            two_message = ""
        if equip_shoes_list:
            shoes_counter = str(equip_shoes_list_ref + 1) + "/" + str(len(equip_shoes_list))
            shoes_counter_space_count = int((48 - len(shoes_counter)) / 2)
            shoes_counter_spacer = " " * shoes_counter_space_count
        else:
            shoes_counter = ""
            shoes_counter_spacer = ""
        clear()
        hp_bank_header()
        print("________________________________________________")
        print("")
        print("                CHOOSE FOOT GEAR                ")
        print("")
        #      aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
        print("")
        if equip_shoes_list:
            print(name_spacer + ">> " + display_name + " <<")
            print(shoes_counter_spacer + shoes_counter)
        if len(equip_shoes_list) > 1:
            #      aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
            print("  3                                          4  ")
            print("  <<                                        >>  ")
        print("")
        print("")
        if equip_shoes_list:
            print(one_message + display_name)
        elif equipment["shoes"] == "none":
            print(one_message)
        if equipment["shoes"] != "none":
            print(two_message)
        print("")
        print("  0 | Back")
        print("")
        try:
            equip_shoes_choice = int(input())
        except ValueError:
            print(drunk_filter("Please choose one of the options..."))  # leave drug filter off
            time.sleep(error_delay)
            clear()
            continue
        # equip selected
        if equip_shoes_list and equip_shoes_choice == 1:
            equipment["shoes"] = equip_shoes_list[equip_shoes_list_ref]
            shoes_equipped = True
            print(display_name + " equipped...")
            time.sleep(med_delay)
        # unequip current shoes gear
        elif equipment["shoes"] != "none" and equip_shoes_choice == 2:
            equipment["shoes"] = "none"
            shoes_equipped = True
        # view previous shoes gear if player has more than 1 shoes gear
        elif len(equip_shoes_list) > 1 and equip_shoes_choice == 3:
            if equip_shoes_list_ref == 0:
                equip_shoes_list_ref = len(equip_shoes_list) - 1
            else:
                equip_shoes_list_ref -= 1
        # view next shoes gear if player has more than 1 shoes gear
        elif len(equip_shoes_list) > 1 and equip_shoes_choice == 4:
            if equip_shoes_list_ref == len(equip_shoes_list) - 1:
                equip_shoes_list_ref = 0
            else:
                equip_shoes_list_ref += 1
        # player backs out
        elif equip_shoes_choice == 0:
            time.sleep(med_delay)
        # some other unsupported option is attempted
        else:
            print(drunk_filter("Please choose one of the options..."))  # leave drug filter off
            time.sleep(error_delay)
            clear()
            

# ----- equipment accessory ----- GFN
add_item_inventory("ar_croc_tail")   # for testing
add_item_inventory("ar_chick_tail")  # for testing


def arc_equip_accessory():
    print("arc equip accessory gear")  # for testing
    time.sleep(0.2)  # for testing
    global equipment
    equip_accessory_choice = 1
    accessory_equipped = False
    equip_accessory_list = []
    equip_accessory_list_ref = 0
    for item in player_invent:
        if all_item_type[item] == "accessory":
            equip_accessory_list.append(item)
    if equipment["accessory"] in player_invent:
        equip_accessory_list.remove(equipment["accessory"])
    print(equip_accessory_list)  # for testing
    time.sleep(0.2)  # for testing
    equip_accessory_list.sort()
    print(equip_accessory_list)  # for testing
    time.sleep(0.2)  # for testing
    while equip_accessory_choice != 0 and not accessory_equipped:  # if player goes back or equips weapon kick back
        if equip_accessory_list:
            one_message = "  1 | Equip "
        elif equipment["accessory"] == "none":
            one_message = " No accessory gear in inventory"
        else:
            one_message = ""
        if equip_accessory_list:
            display_name = all_item_fnames[equip_accessory_list[equip_accessory_list_ref]].rstrip()
            name_space_count = int((42 - len(display_name)) / 2)
            name_spacer = " " * name_space_count
        else:
            display_name = ""
            name_spacer = ""
        if equipment["accessory"] != "none":
            two_message = "  2 | Unequip " + all_item_fnames[equipment["accessory"]]
        else:
            two_message = ""
        if equip_accessory_list:
            accessory_counter = str(equip_accessory_list_ref + 1) + "/" + str(len(equip_accessory_list))
            accessory_counter_space_count = int((48 - len(accessory_counter)) / 2)
            accessory_counter_spacer = " " * accessory_counter_space_count
        else:
            accessory_counter = ""
            accessory_counter_spacer = ""
        clear()
        hp_bank_header()
        print("________________________________________________")
        print("")
        print("                CHOOSE ACCESSORY                ")
        print("")
        #      aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
        print("")
        if equip_accessory_list:
            print(name_spacer + ">> " + display_name + " <<")
            print(accessory_counter_spacer + accessory_counter)
        if len(equip_accessory_list) > 1:
            #      aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
            print("  3                                          4  ")
            print("  <<                                        >>  ")
        print("")
        print("")
        if equip_accessory_list:
            print(one_message + display_name)
        elif equipment["accessory"] == "none":
            print(one_message)
        if equipment["accessory"] != "none":
            print(two_message)
        print("")
        print("  0 | Back")
        print("")
        try:
            equip_accessory_choice = int(input())
        except ValueError:
            print(drunk_filter("Please choose one of the options..."))  # leave drug filter off
            time.sleep(error_delay)
            clear()
            continue
        # equip selected
        if equip_accessory_list and equip_accessory_choice == 1:
            equipment["accessory"] = equip_accessory_list[equip_accessory_list_ref]
            accessory_equipped = True
            print(display_name + " equipped...")
            time.sleep(med_delay)
        # unequip current accessory gear
        elif equipment["accessory"] != "none" and equip_accessory_choice == 2:
            equipment["accessory"] = "none"
            accessory_equipped = True
        # view previous accessory gear if player has more than 1 accessory gear
        elif len(equip_accessory_list) > 1 and equip_accessory_choice == 3:
            if equip_accessory_list_ref == 0:
                equip_accessory_list_ref = len(equip_accessory_list) - 1
            else:
                equip_accessory_list_ref -= 1
        # view next accessory gear if player has more than 1 accessory gear
        elif len(equip_accessory_list) > 1 and equip_accessory_choice == 4:
            if equip_accessory_list_ref == len(equip_accessory_list) - 1:
                equip_accessory_list_ref = 0
            else:
                equip_accessory_list_ref += 1
        # player backs out
        elif equip_accessory_choice == 0:
            time.sleep(med_delay)
        # some other unsupported option is attempted
        else:
            print(drunk_filter("Please choose one of the options..."))  # leave drug filter off
            time.sleep(error_delay)
            clear()
            
            
# ----- equipment main access ----- GFN

def arc_equipment():
    print("arc equipment")  # for testing
    time.sleep(0.2)  # for testing
    equip_choice1 = 1
    while equip_choice1 != 0:
        clear()
        hp_bank_header()
        print("________________________________________________")
        print("")
        print("                   EQUIPMENT                    ")
        print("")
        print("1 |             Weapon: " + all_item_fnames[equipment["weapon"]])
        print("2 |           Headgear: " + all_item_fnames[equipment["head"]])
        print("3 |              Torso: " + all_item_fnames[equipment["torso"]])
        print("4 |               Legs: " + all_item_fnames[equipment["legs"]])
        print("5 |              Shoes: " + all_item_fnames[equipment["shoes"]])
        print("6 |          Accessory: " + all_item_fnames[equipment["accessory"]])
        print("")
        print("0 | Back")
        print("")
        try:
            equip_choice1 = int(input())
        except ValueError:
            print(drunk_filter("Please choose one of the options..."))  # leave drug filter off
            time.sleep(error_delay)
            clear()
            continue
        if equip_choice1 == 1:
            print("weapon")  # for testing
            time.sleep(0.2)  # for testing
            arc_equip_weapon()
            continue
        elif equip_choice1 == 2:
            print("head")  # for testing
            time.sleep(0.2)  # for testing
            arc_equip_head()
            continue
        elif equip_choice1 == 3:
            print("torso")  # for testing
            time.sleep(0.2)  # for testing
            arc_equip_torso()
            continue
        elif equip_choice1 == 4:
            print("legs")  # for testing
            time.sleep(0.2)  # for testing
            arc_equip_legs()
            continue
        elif equip_choice1 == 5:
            print("shoes")  # for testing
            time.sleep(0.2)  # for testing
            arc_equip_shoes()
            continue
        elif equip_choice1 == 6:
            print("accessory")  # for testing
            time.sleep(0.2)  # for testing
            arc_equip_accessory()
            continue
        elif equip_choice1 == 0:
            time.sleep(med_delay)
            clear()
            continue
        else:
            print(drunk_filter("Please choose one of the options..."))  # leave drug filter off
            time.sleep(error_delay)
            clear()
            continue


# ---------- ARC store ---------- IN PROGRESS

def arc_store():
    print("arc store")  # for testing
    time.sleep(5)  # for testing


# ---------- view map ---------- IN PROGRESS

def arc_view_map():
    print("arc view map")  # for testing
    time.sleep(2)  # for testing
    view_map_choice = 1
    while view_map_choice != 0:
        clear()
        hp_bank_header()
        print("________________________________________________")
        print("")
        print("1 | View map of Sol City")
        print("2 | View local map")
        print("")
        print("0 | Back")
        print("")
        try:
            view_map_choice = int(input())
        except ValueError:
            print(drunk_filter("Please choose one of the options..."))  # leave drug filter off
            time.sleep(error_delay)
            clear()
            continue
        if view_map_choice == 1:
            big_map_choice = 1
            while big_map_choice != 0:
                clear()
                # add options for player to get info about places on big map
                # have local map here but also for when player presses "m" on other screens
                draw_big_sol_map()
                print("")
                print("0 | Back")
                print("")
                try:
                    big_map_choice = int(input())
                except ValueError:
                    print(drunk_filter("Please choose one of the options..."))  # leave drug filter off
                    time.sleep(error_delay)
                    clear()
                    continue
                if big_map_choice == 0:
                    continue
                else:
                    print(drunk_filter("Please choose one of the options..."))  # leave drug filter off
                    time.sleep(error_delay)
                    clear()
                    continue
            continue
        elif view_map_choice == 2:
            print("show local map")
            time.sleep(5)
            continue
        elif view_map_choice == 0:
            time.sleep(med_delay)
            continue
        else:
            print(drunk_filter("Please choose one of the options..."))  # leave drug filter off
            time.sleep(error_delay)
            clear()
            continue


# ---------- manage subs ---------- IN PROGRESS

def arc_mng_subs():
    print("arc manage subs")  # for testing
    time.sleep(5)  # for testing


# ---------- manage debt ---------- IN PROGRESS

def arc_mng_debt():
    print("arc manage debt")  # for testing
    time.sleep(5)  # for testing


# ---------- about you ---------- IN PROGRESS

def arc_about_you():
    print("arc about you")  # for testing
    time.sleep(5)  # for testing


# ---------- about others ---------- IN PROGRESS

def arc_about_others():
    print("arc about others")  # for testing
    time.sleep(5)  # for testing


# ---------- arc settings menu ---------- IN PROGRESS

def arc_settings():
    print("arc settings")  # for testing
    time.sleep(5)  # for testing


# ---------- main access ARC menu ---------- IN PROGRESS

def access_arc_menu():
    print("access ARC menu")  # for testing
    time.sleep(2)  # for testing
    arc_menu_choice = 1  # initialize
    freeze_ad = produce_ad()  # this way the ad doesn't change on wrong input
    while arc_menu_choice != 0:
        clear()
        hp_bank_header()
        print("________________________________________________")
        print("                                                ")
        print("                          Ʌɼʗ v208919.919.69145 ")
        print("")
        print(freeze_ad)
        print("                                                ")
        print("1 | Equipment")
        print("2 | ARC Store")
        print("3 | View map")
        print("4 | Manage subs")
        print("5 | Manage debt")
        print("6 | About you")
        print("7 | About others")
        print("8 | Settings")
        print("")
        print("0 | Exit ARC Menu")
        print("")
        try:
            arc_menu_choice = int(input())
        except ValueError:
            print(drunk_filter("Please choose one of the options..."))  # leave drug filter off
            time.sleep(error_delay)
            clear()
            continue
        if arc_menu_choice == 1:
            arc_equipment()
            continue
        elif arc_menu_choice == 2:
            arc_store()
            continue
        elif arc_menu_choice == 3:
            arc_view_map()
            continue
        elif arc_menu_choice == 4:
            arc_mng_subs()
            continue
        elif arc_menu_choice == 5:
            arc_mng_debt()
            continue
        elif arc_menu_choice == 6:
            arc_about_you()
            continue
        elif arc_menu_choice == 7:
            arc_about_others()
            continue
        elif arc_menu_choice == 8:
            arc_settings()
        elif arc_menu_choice == 0:
            time.sleep(med_delay)
            continue
        else:
            print(drunk_filter("Please choose one of the options..."))  # leave drug filter off
            time.sleep(error_delay)
            clear()
            continue


# access_arc_menu()  # for testing
# time.sleep(20)  # for testing


# ---------- personal inventory ---------- GFN
# ----- personal inventory display item info ----- GFN
# display any info for items in inventory, e.g. shop blurb text, will probably need to write up a dictionary with
# info on every item and lookup based on name
# if I'm feeling generous, could add images for every item, but just do name and description from a dict etc. first.

def invent_item_info(invent_item):
    info_choice = 1
    while info_choice != 0:
        print("item info")
        display_name = all_item_fnames[invent_item].rstrip()
        clear()
        hp_bank_header()
        print("________________________________________________")
        print("")
        print(display_name + " info")
        print("")
        if invent_item == "apple":
            #      aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
            print("apple")
        elif invent_item == "donut":
            print("donut")
        print("")
        print("0 | Back")
        print("")
        try:
            info_choice = int(input())
        except ValueError:
            print(drunk_filter("Please choose one of the options..."))  # leave drug filter off
            time.sleep(error_delay)
            clear()
            continue
        if info_choice == 0:
            time.sleep(med_delay)
            clear()
            continue
        else:
            print(drunk_filter("Please choose one of the options..."))  # leave drug filter off
            time.sleep(error_delay)
            clear()
            continue


# ----- personal inventory inspect item ----- GFN
# when scrolling through inventory items give option to... (have these options as fixed numbers)
# > display info,
# > discard item (not drop, permanently discard, should warn player,
# > if applicable (check bool etc.), transfer item to appt or hacker base storage
# 1 | Display info
# 2 | Permanently discard item
# 3 | Transfer to apartment storage
# 4 | Transfer to base storage
# 0 | Back to inventory

def invent_inspect_item(invent_item):
    inspect_choice = 1
    item_removed = False
    display_name = all_item_fnames[invent_item].rstrip()  # remove trailing spaces from temp variable
    while inspect_choice != 0 and not item_removed:
        clear()
        hp_bank_header()
        print("________________________________________________")
        print("")
        print(" " + display_name)
        print("")
        print("1 | Item Info")
        print("2 | Discard (Permanent)")
        if appt_storage_avail:
            print("3 | Transfer to apartment storage")
        if hackbase_storage_avail:
            print("4 | Transfer to base storage")
        print("")
        print("0 | Back")
        print("")
        try:
            inspect_choice = int(input())
        except ValueError:
            print(drunk_filter("Please choose one of the options..."))  # leave drug filter off
            time.sleep(error_delay)
            clear()
            continue
        if inspect_choice == 1:
            print("show item info")  # for testing
            time.sleep(2)  # for testing
            invent_item_info(invent_item)
        # discard choice
        elif inspect_choice == 2:
            # if player tries to discard item, confirm choice as this is permanent
            # if they discard, kick them back to start of access inventory
            discard_choice = 2  # initialize
            while discard_choice != 1 and discard_choice != 0:
                clear()
                hp_bank_header()
                print("________________________________________________")
                print("")
                print("Are you sure you want to permanently discard")
                print(display_name + "?")
                print("")
                print("This cannot be undone.")
                print("")
                print("1 | Yes, discard " + display_name)
                print("")
                print("0 | No, take me back")
                print("")
                try:
                    discard_choice = int(input())
                except ValueError:
                    print(drunk_filter("Please choose one of the options..."))  # leave drug filter off
                    time.sleep(error_delay)
                    clear()
                    continue
                if discard_choice == 1:
                    remove_item_inventory(invent_item)
                    print(display_name + " discarded...")
                    item_removed = True
                    time.sleep(med_delay)
                    continue
                elif discard_choice == 0:
                    time.sleep(med_delay)
                    continue
                else:
                    print(drunk_filter("Please choose one of the options..."))  # leave drug filter off
                    time.sleep(error_delay)
                    clear()
                    continue
        # transfer item to apartment storage
        elif appt_storage_avail and inspect_choice == 3:
            # if player tries to transfer item, confirm choice
            # if they transfer, kick them back to start of access inventory
            appt_storage_choice = 2  # initialize
            while appt_storage_choice != 1 and appt_storage_choice != 0:
                clear()
                print("________________________________________________")
                print("")
                print("Are you sure you want to transfer")
                print(display_name)
                print("to apartment storage?")
                print("")
                print("1 | Yes, transfer " + display_name)
                print("")
                print("0 | No, take me back")
                print("")
                try:
                    appt_storage_choice = int(input())
                except ValueError:
                    print(drunk_filter("Please choose one of the options..."))  # leave drug filter off
                    time.sleep(error_delay)
                    clear()
                    continue
                if appt_storage_choice == 1:
                    add_item_appt_storage(invent_item)
                    remove_item_inventory(invent_item)
                    print(display_name + " transfered to storage...")
                    item_removed = True
                    time.sleep(med_delay)
                    continue
                elif appt_storage_choice == 0:
                    time.sleep(med_delay)
                    continue
                else:
                    print(drunk_filter("Please choose one of the options..."))  # leave drug filter off
                    time.sleep(error_delay)
                    clear()
                    continue
        # transfer item to hackerbase storage
        elif hackbase_storage_avail and inspect_choice == 4:
            # if player tries to transfer item, confirm choice
            # if they transfer, kick them back to start of access inventory
            hackbase_storage_choice = 2  # initialize
            while hackbase_storage_choice != 1 and hackbase_storage_choice != 0:
                clear()
                print("________________________________________________")
                print("")
                print("Are you sure you want to transfer")
                print(display_name)
                print("to base storage?")
                print("")
                print("1 | Yes, transfer " + display_name)
                print("")
                print("0 | No, take me back")
                print("")
                try:
                    hackbase_storage_choice = int(input())
                except ValueError:
                    print(drunk_filter("Please choose one of the options..."))  # leave drug filter off
                    time.sleep(error_delay)
                    clear()
                    continue
                if hackbase_storage_choice == 1:
                    add_item_hackbase_storage(invent_item)
                    remove_item_inventory(invent_item)
                    print(display_name + " transfered to storage...")
                    item_removed = True
                    time.sleep(med_delay)
                    continue
                elif hackbase_storage_choice == 0:
                    time.sleep(med_delay)
                    continue
                else:
                    print(drunk_filter("Please choose one of the options..."))  # leave drug filter off
                    time.sleep(error_delay)
                    clear()
                    continue
        elif inspect_choice == 0:
            time.sleep(med_delay)
            clear()
            continue
        else:
            print(drunk_filter("Please choose one of the options..."))  # leave drug filter off
            time.sleep(error_delay)
            clear()
            continue


# invent_inspect_item("comb_knife")  # for testing

# ----- main access personal inventory ----- GFN
# don't want a cap on inventory storage.
# want to display ref, item name, cat, vol
# create a list using inventory dict, then order all items alphabetically.

def access_personal_inventory():
    # might have an issue if the player removes an item from their inventory, if it tries to find the ref
    # probably need a break or pass or whatever to kick someone all the way out to the start here if exit the
    # view item screen!! think that should fix as refs_to_view etc is remade.
    global player_invent
    all_invent_choice = 1  # initialize
    while all_invent_choice != 0:
        clear()
        print("access inventory")  # for testing
        # create list for inventory items and order alphabetically
        inventory_list = []
        new_invent_dict = {}
        new_invent_dict_ref = 1
        for invent_item in player_invent.keys():
            inventory_list.append(invent_item)
        print(inventory_list)  # for testing
        time.sleep(0.1)  # for testing
        inventory_list.sort()
        print(inventory_list)  # for testing
        time.sleep(0.1)  # for testing
        # create new dictionary with number, fill in cat later using dict of all item ill cats
        for invent_item2 in inventory_list:
            new_invent_dict[new_invent_dict_ref] = {"shortname": invent_item2,
                                                    "full_name": all_item_fnames[invent_item2],
                                                    "illcat": all_item_contra[invent_item2],
                                                    "vol": player_invent[invent_item2]}
            new_invent_dict_ref += 1
        print(new_invent_dict)  # for testing
        time.sleep(0.1)  # for testing
        # create list for up to 7 refs to view per page
        min_ref = 1
        max_ref = len(new_invent_dict.keys())
        print(min_ref)  # for testing
        print(max_ref)  # for testing
        time.sleep(0.1)  # for testing
        seven_or_max_dict = min(7, max_ref)  # set refs as dict length or seven if length > 7
        print("seven or max is " + str(seven_or_max_dict))
        # create refs to view list of dict length or max 7 if dict length > 7
        refs_to_view = []
        refs_to_view_num = 1
        while len(refs_to_view) < seven_or_max_dict:
            refs_to_view.append(refs_to_view_num)
            refs_to_view_num += 1
        print(refs_to_view)  # for testing
        time.sleep(0.1)  # for testing
        # loop until player exits inventory
        while all_invent_choice != 0:
            clear()
            hp_bank_header()
            print("________________________________________________")
            print("")
            print("                   INVENTORY                    ")
            print("")
            print("     item                     contraband    vol")
            #      1    aaaaaaaaaaaaaaaaaaaaaaa      aaaaa      a
            print("")
            for ref in refs_to_view:
                if min_ref <= ref <= max_ref:
                    # full name max as 28 characters and illcat max as 10
                    # print up to 7 items per page as max ref is established
                    ref_space_count = max(0, 3 - len(str(ref)))
                    ref_spacer = " " * ref_space_count
                    full_name_space_count = max(0, 23 - len(new_invent_dict[ref]["full_name"]))
                    full_name_spacer = " " * full_name_space_count
                    illcat_space_count = max(0, 13 - len(new_invent_dict[ref]["illcat"]))
                    illcat_spacer = " " * illcat_space_count
                    invent_row = [str(ref),
                                  ref_spacer,
                                  new_invent_dict[ref]["full_name"],
                                  full_name_spacer,
                                  new_invent_dict[ref]["illcat"],
                                  illcat_spacer,
                                  str(new_invent_dict[ref]["vol"])]

                    invent_row_string = " ".join(invent_row)
                    print(invent_row_string)
            print("")
            if player_invent and min_ref not in refs_to_view:  # if inventory not empty then dict true else false
                print("U | Page up")
            else:
                print("")
            if player_invent and max_ref not in refs_to_view:
                print("D | Page down")
            else:
                print("")
            print("0 | Exit Inventory")
            print("")
            time.sleep(0.1)  # for testing
            up = ["U", "u", "UP", "up", "Up"]
            down = ["D", "d", "DOWN", "down", "Down"]
            all_invent_choice = input()
            if player_invent and min_ref not in refs_to_view and all_invent_choice in up:
                refs_to_view = [xo - 7 for xo in refs_to_view]
                print(refs_to_view)  # for testing
                time.sleep(0.1)  # for testing
                continue
            elif player_invent and max_ref not in refs_to_view and all_invent_choice in down:
                refs_to_view = [xo + 7 for xo in refs_to_view]
                print(refs_to_view)  # for testing
                time.sleep(0.1)  # for testing
                continue
            try:
                all_invent_choice = int(all_invent_choice)
            except ValueError:
                print(drunk_filter("Please choose one of the options..."))  # leave drug filter off
                time.sleep(error_delay)
                clear()
                continue
            if all_invent_choice == 0:
                print("Good bye")  # for testing
                time.sleep(error_delay)
                clear()
                break  # think break is right
            elif all_invent_choice in refs_to_view and all_invent_choice <= max_ref:
                print("Go to invent item page")  # for testing
                print(new_invent_dict[all_invent_choice]["shortname"])  # for testing
                time.sleep(2)  # for testing
                invent_inspect_item(new_invent_dict[all_invent_choice]["shortname"])
                break  # think break is right as want to force redraw, even if player loses place in screen
            else:
                print(drunk_filter("Please choose one of the options..."))  # leave drug filter off
                time.sleep(error_delay)
                clear()
                continue


# access_personal_inventory()  # for testing


# ---------- apartment storage ---------- IN PROGRESS
# ----- apartment item info -----
# ----- apartment inspect item -----
# ----- access appt storage -----

def access_appt_storage():
    print("access appt storage")


# ---------- hacker base storage ---------- IN PROGRESS
# ----- hacker base item info -----
# ----- hacker base inspect item -----
# ----- access hacker base storage -----

def access_hackbase_storage():
    print("access hacker base storage")

# ---------- Black market ----------

# ----- refresh black market stock ----- GFN
# refresh black market stock and list items that are in stock
# generate list for minor and major separately
# then check if major is allowed, if not then remove items from major list
# combine lists into total new list
# then run this refresh function in both the not been before part of access bmarket and the if min > 10


def refresh_bmarket_stock():
    # refresh instock items
    global bmarket_instock_items
    global bmarket_instock_num2item_dict
    global bmarket_instock_item2num_dict
    bmarket_instock_items.clear()
    bmarket_minor_instock = []
    bmarket_major_instock = []
    for bm_item in black_market_items.keys():
        if random.random() < black_market_items[bm_item]["rr"] and black_market_items[bm_item]["icat"] == "mi":
            bmarket_minor_instock.append(bm_item)
    for bm_item in black_market_items.keys():
        if random.random() < black_market_items[bm_item]["rr"] and black_market_items[bm_item]["icat"] == "ma":
            bmarket_major_instock.append(bm_item)
    if not bmarket_major_unlocked:
        bmarket_major_instock.clear()
    bmarket_instock_items = bmarket_minor_instock + bmarket_major_instock

    # create num2item and item2num dictionaries to go with list
    bmarket_instock_num2item_dict.clear()
    bmarket_instock_item2num_dict.clear()
    bm_item2num_ref = 1
    bm_num2item_ref = 1
    for bm_item in bmarket_instock_items:
        bmarket_instock_item2num_dict[bm_item] = bm_item2num_ref
        bm_item2num_ref += 1
    for bm_item in bmarket_instock_items:
        bmarket_instock_num2item_dict[bm_num2item_ref] = bm_item
        bm_num2item_ref += 1


# refresh_bmarket_stock()
# print(bmarket_instock_item2num_dict)
# print(bmarket_instock_num2item_dict)
# time.sleep(10)


# ----- black market store banner ----- GFN

def bmarket_banner():
    print("________________________________________________")
    print("                       ._____|__________        ")
    print("                       |OOOOO|vvvvvvvvvV  ._.   ")
    print("     BLACK                   |            |X|   ")
    print("        MARKET       ._/____________||    |X|   ")
    print(" ._____________L    Z|//// |__|      |D   |X|   ")
    print("D|___________/..|    |______________/   __|X|__ ")
    print("           |j|..|   /xxx/L|               <||   ")
    print("             |..|  /xxx/        o         <||   ")
    print("      ==>    |__| /xxx/       /XXX    o   <||   ")
    print("     /./         /xxx/       / XXX  /XXX  <||   ")
    print("    /./ ==>      /./           XXX / XXX  <||   ")
    print("   /_/ ==>     _/./_                 XXX   V    ")
    print("________________________________________________")


# ----- black market buy screen ----- GFN
# Call function with black market short item name and will display info and allow player to buy if enough cash

def bmarket_buy_screen(bm_item):
    buy_menu_choice = 1  # initialize
    item_bought = False
    while buy_menu_choice != 0 and not item_bought:

        if black_market_items[bm_item]["price"] <= current_balance:
            message = "You want this? or something else?"
        else:
            message = "You don't have enough cRedits"
        display_name = all_item_fnames[bm_item]
        if bm_item == "comb_knife":
            clear()
            hp_bank_header()
            print("________________________________________________")
            print("                                                ")
            print("     ._.     COMBAT KNIFE")
            print("     |X|                                        ")
            print("     |X|     CONTRABAND CATEGORY: MAJOR         ")
            print("     |X|                                        ")
            print("   __|X|__   > Pointy pointy. Stabby Stabby.    ")
            print("     <||     > Effective for buttering toast    ")
            print("     <||       and murder.                      ")
            print("     <||                                        ")
            print("     <||    " + str(black_market_items[bm_item]["price"]) + " cR")
            print("     <||                                        ")
            print("      V     " + message)
            print("________________________________________________")
            print("")
        elif bm_item == "screw_dr":
            clear()
            hp_bank_header()
            print("________________________________________________")
            print("                                                ")
            print("     ._.     SCREW DRIVER")
            print("     |X|                                        ")
            print("     |X|     CONTRABAND CATEGORY: MINOR")
            print("     |X|                                        ")
            print("    _|X|_    > More than just a weapon.         ")
            print("      |      > Always comes in handy.           ")
            print("      |                                         ")
            print("      |                                         ")
            print("      |     " + str(black_market_items[bm_item]["price"]) + " cR")
            print("      |                                         ")
            print("      V     " + message)
            print("________________________________________________")
            print("")
        elif bm_item == "hammer":
            clear()
            hp_bank_header()
            print("________________________________________________")
            print("                                                ")
            print("     ._.     HAMMER")
            print("   D=| |=>                                      ")
            print("     | |     CONTRABAND CATEGORY: MINOR")
            print("     | |                                        ")
            print("     |_|     > To a hammer, everything is just  ")
            print("     |X|       another thing to be hammered.    ")
            print("     |X|     > You want a hammer-sandwich?      ")
            print("     |X|                                        ")
            print("     |X|    " + str(black_market_items[bm_item]["price"]) + " cR")
            print("     |_|                                         ")
            print("            " + message)
            print("________________________________________________")
            print("")
        elif bm_item == "lead_pipe":
            clear()
            hp_bank_header()
            print("________________________________________________")
            print("        _                                       ")
            print("      /|_|   LEAD PIPE")
            print("     |_|                                        ")
            print("     |_|     CONTRABAND CATEGORY: MINOR")
            print("     | |                                        ")
            print("     | |     > Pipe down, you!                  ")
            print("     | |     > Yeah, that's about all I got...  ")
            print("     | |                                        ")
            print("     | |                                        ")
            print("     | |    " + str(black_market_items[bm_item]["price"]) + " cR")
            print("     |_|                                         ")
            print("            " + message)
            print("________________________________________________")
            print("")
        elif bm_item == "flip_knife":
            clear()
            hp_bank_header()
            print("________________________________________________")
            print("                                                ")
            print("      /|     FLIP KNIFE")
            print("     / |                                        ")
            print("     | |     CONTRABAND CATEGORY: MINOR")
            print("     | |                                        ")
            print("     |_|     > Flippedy do-da! Stabbety face!   ")
            print("     )o|     > My oh my, you'll wish you still  ")
            print("     )x|       had your face!                   ")
            print("     |x|                                        ")
            print("     |x|    " + str(black_market_items[bm_item]["price"]) + " cR")
            print("     (_)                                         ")
            print("            " + message)
            print("________________________________________________")
            print("")
        elif bm_item == "crowbar":
            clear()
            hp_bank_header()
            print("________________________________________________")
            print("        _                                       ")
            print("      /|_    CROWBAR")
            print("     / |                                        ")
            print("     | |     CONTRABAND CATEGORY: MINOR")
            print("     | |                                        ")
            print("     | |     > Trusty.                          ")
            print("     | |     > Goes well with orange and blood. ")
            print("     | |                                        ")
            print("     | |                                        ")
            print("     | |    " + str(black_market_items[bm_item]["price"]) + " cR")
            print("    _/_/                                         ")
            print("            " + message)
            print("________________________________________________")
            print("")
        elif bm_item == "eagle_sniper":
            clear()
            hp_bank_header()
            print("________________________________________________")
            print("      _                                         ")
            print("      |      EAGLE-EYE SNIPER RIFLE")
            print("      |                                         ")
            print("     .|.     CONTRABAND CATEGORY: MAJOR")
            print("  __ | |__                                      ")
            print("  ||_| |__|  > You'll shoot your eye out!       ")
            print("  ||_| |     > Pew pew!                         ")
            print("  || | |L _                                     ")
            print("  ^^ | |_|_|                                    ")
            print("     | |    " + str(black_market_items[bm_item]["price"]) + " cR")
            print("    /|_|                                         ")
            print("            " + message)
            print("________________________________________________")
            print("")
        elif bm_item == "9mm_hand":
            clear()
            hp_bank_header()
            print("________________________________________________")
            print("                                                ")
            print("             9mm HANDGUN")
            print("                                                ")
            print("             CONTRABAND CATEGORY: MAJOR")
            print("     _                                          ")
            print("    | |      > Bang! And your face is gone!     ")
            print("    | |_     > A cap in all your asses          ")
            print("    | |L|_                                      ")
            print("   >|_|_|_|                                     ")
            print("            " + str(black_market_items[bm_item]["price"]) + " cR")
            print("                                                ")
            print("            " + message)
            print("________________________________________________")
            print("")
        elif bm_item == "cyber_kat":
            clear()
            hp_bank_header()
            print("________________________________________________")
            print("    ..                                          ")
            print("    ||       CYBER KATANA")
            print("    ||                                          ")
            print("   _||_      CONTRABAND CATEGORY: MAJOR")
            print("    ||                                          ")
            print("    ||       > Have you studied the blade?      ")
            print("    ||       > There was always going to be     ")
            print("    ||         a katana :)                      ")
            print("    ||                                          ")
            print("    ||      " + str(black_market_items[bm_item]["price"]) + " cR")
            print("    ||                                          ")
            print("    /       " + message)
            print("________________________________________________")
            print("")
        elif bm_item == "mils_pred_mod":
            clear()
            hp_bank_header()
            print("________________________________________________")
            print("                                                ")
            print("             MIL-SPEC ARC PREDATOR MODULE")
            print("                                                ")
            print("             CONTRABAND CATEGORY: MAJOR")
            print("   _|__|_                                       ")
            print("   |X||X|    > When equipped, boosts Stealth,   ")
            print("   |X||X|      Combat and Aim abilities to MAX  ")
            print("   |X||X|    > Time to save the world           ")
            print("    z  z                                        ")
            print("            " + str(black_market_items[bm_item]["price"]) + " cR")
            print("                                                ")
            print("            " + message)
            print("________________________________________________")
            print("")
        else:
            clear()
            print("Oops, that wasn't supposed to happen")
        if message == "You want this? or something else?":
            print("1 | Buy")
        print("")
        print("0 | Look at something else")
        print("")

        # Check buy menu choice
        try:
            buy_menu_choice = int(input())
        except ValueError:
            print(drunk_filter("Please choose one of the options..."))  # leave drug filter off
            time.sleep(error_delay)
            clear()
            continue
        if buy_menu_choice == 0:
            time.sleep(med_delay)
            clear()
            continue
        elif buy_menu_choice == 1 and message == "You want this? or something else?":
            print("Add item to inventory and set item bought to true")
            item_bought = True
            print(player_invent)  # for testing
            add_item_inventory(bm_item)
            print(player_invent)  # for testing
            time.sleep(0.1)  # for testing
            print("Remove item from bmstock")
            ref_to_remove = bmarket_instock_item2num_dict[bm_item]
            item_to_remove = bm_item
            # Remove item from bm in stock list
            print(bmarket_instock_items)  # for testing
            bmarket_instock_items.remove(item_to_remove)
            print(bmarket_instock_items)  # for testing
            time.sleep(0.1)  # for testing
            # Remove ref from num2item dict
            print(bmarket_instock_num2item_dict)  # for testing
            del bmarket_instock_num2item_dict[ref_to_remove]
            print(bmarket_instock_num2item_dict)  # for testing
            print("remove num2item ref")  # for testing
            time.sleep(0.1)  # for testing
            # Remove item from item2ref dict
            print(bmarket_instock_item2num_dict)
            del bmarket_instock_item2num_dict[item_to_remove]
            print(bmarket_instock_item2num_dict)
            time.sleep(0.1)  # for testing
            # Play buy animation and charge player balance for bmarket item
            print("Play buy animation")
            time.sleep(0.1)  # for testing
            clear()
            balance_chng_animation(down=black_market_items[bm_item]["price"])
            continue
        else:
            print(drunk_filter("Please choose one of the options..."))  # leave drug filter off
            time.sleep(error_delay)
            clear()
            continue


# ----- access black market ----- GFN

def access_black_market():
    # Check if been to black market before or last time was here to refresh stock if needed
    global bmarket_last_accessed_datetime
    global bmarket_accessed_before
    if not bmarket_accessed_before:
        min_since_bmarket = 0
        bmarket_last_accessed_datetime = current_datetime()
        refresh_bmarket_stock()
        print("test: not been here before")
    else:
        min_since_bmarket = min_diff_int(bmarket_last_accessed_datetime, current_datetime())
        print("test: have been here before")
        print(min_since_bmarket)
    if min_since_bmarket > 10:
        refresh_bmarket_stock()
        print("test: it's been more than 10 minutes since i been here")

    time.sleep(1)  # remove when done testing

    bmarket_accessed_before = True
    bmarket_last_accessed_datetime = current_datetime()

    # Black market graphic intro
    clear()
    empty_banner()
    time.sleep(med_delay)
    clear()
    banner_text("Entering black market...")
    time.sleep(text_delay)
    clear()
    banner_text("All sales are final...")
    time.sleep(text_delay)
    clear()
    empty_banner()
    time.sleep(med_delay)

    bmarket_menu_choice = 1  # initialize, just something that isn't zero

    while bmarket_menu_choice != 0:
        # Black market shop menu - wrap in while loop until player exits shop
        clear()
        hp_bank_header()
        bmarket_banner()
        print("")
        #      aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
        #          item                    contraband    price
        print("    item                    contraband    price")
        #      1 | lead pipe               minor         200 cR
        print("")

        # print black market menu
        for bm_item in bmarket_instock_items:
            contra_space_count = 10 - len(all_item_contra[bm_item])
            contra_spacer = " " * contra_space_count
            price_space_count = 4 - len(str(black_market_items[bm_item]["price"]))
            price_spacer = " " * price_space_count
            #      aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
            bmarket_row = [str(bmarket_instock_item2num_dict[bm_item]),
                           "|",
                           all_item_fnames[bm_item],
                           all_item_contra[bm_item],
                           contra_spacer,
                           price_spacer,
                           str(black_market_items[bm_item]["price"]),
                           "cR"]

            bmarket_row_string = " ".join(bmarket_row)
            print(bmarket_row_string)
        print("")
        print("0 | Exit")
        print("")
        try:
            bmarket_menu_choice = int(input())
        except ValueError:
            print(drunk_filter("Please choose one of the options..."))  # leave drug filter off
            time.sleep(error_delay)
            continue
        if bmarket_menu_choice == 0:
            time.sleep(med_delay)
            clear()
            banner_text("See you soon...")
            time.sleep(med_delay)
            continue
        elif bmarket_menu_choice in bmarket_instock_num2item_dict.keys():
            print("Test: Yes")
            bmarket_item_of_interest = bmarket_instock_num2item_dict[bmarket_menu_choice]
            print(bmarket_item_of_interest)
            time.sleep(1)  # remove sleep when done testing
            bmarket_buy_screen(bmarket_item_of_interest)
        else:
            print(drunk_filter("Please choose one of the options..."))  # leave drug filter off
            time.sleep(error_delay)
            continue


# ---------- reset bools at end of turn ----------
# be careful about how to implement and when
# may want to handle things like black market no available on exit of shop


# ------------------------------------------------- Minigames ----------------------------------------------------------
# ---------- Kasino games ----------
# ----- AI deathmatch (non-quest) -----
# ----- Roulette -----

def roulette():
    print("play roulette")  # for testing
    time.sleep(2)  # for testing
    roul_seq = [0,32,15,19,4,21,2,25,17,34,6,27,13,36,11,30,8,23,10,5,24,16,33,1,20,14,31,9,22,18,29,7,28,12,35,3,26]
    roul_colour = {
        0:  "G",
        1:  "R",
        2:  "B",
        3:  "R",
        4:  "B",
        5:  "R",
        6:  "B",
        7:  "R",
        8:  "B",
        9:  "R",
        10: "B",
        11: "B",
        12: "R",
        13: "B",
        14: "R",
        15: "B",
        16: "R",
        17: "B",
        18: "R",
        19: "R",
        20: "B",
        21: "R",
        22: "B",
        23: "R",
        24: "B",
        25: "R",
        26: "B",
        27: "R",
        28: "B",
        29: "B",
        30: "R",
        31: "B",
        32: "R",
        33: "B",
        34: "R",
        35: "B",
        36: "R"
    }
    roul_choice = 1  # initialize
    while roul_choice != 0 and current_balance > 0:
        bet_on_single = False  # initialize
        bet_on_red = False     # initialize
        bet_on_black = False   # initialize
        bet_on_even = False    # initialize
        bet_on_odd = False     # initialize
        roul_win = False       # initialize
        win_amount = 0         # initialize
        bet_amount = 0         # initialize
        roul_single_num = 1    # initialize
        clear()
        hp_bank_header()
        print("________________________________________________")
        print("")
        print("                    ROULETTE                    ")
        print("")
        print("1 | Bet on single                 O O O         ")
        print("2 | Bet on red                  O   |   O       ")
        print("3 | Bet on black              O     |     O     ")
        print("4 | Bet on even               O --- X --- O     ")
        print("5 | Bet on odd                O     |     O     ")
        print("                                O   |   O       ")
        print("0 | Leave                         O O O         ")
        print("")
        try:
            roul_choice = int(input())
        except ValueError:
            print(drunk_filter("Please choose one of the options..."))  # leave drug filter off
            time.sleep(error_delay)
            continue
        # bet on single - don't let player out once bet chosen
        if roul_choice == 1:
            bet_on_single = True
            roul_single_num_checked = False
            while not roul_single_num_checked:
                clear()
                hp_bank_header()
                print("________________________________________________")
                print("")
                print("                    ROULETTE                    ")
                print("")
                print("                                  O O O         ")
                print("    Enter a number between      O   |   O       ")
                print("    0 and 36...               O     |     O     ")
                print("                              O --- X --- O     ")
                print("                              O     |     O     ")
                print("                                O   |   O       ")
                print("                                  O O O         ")
                print("")
                try:
                    roul_single_num = int(input())
                except ValueError:
                    print(drunk_filter("Please choose one of the options..."))  # leave drug filter off
                    time.sleep(error_delay)
                    continue
                if 0 <= roul_single_num <= 36:
                    roul_single_num_checked = True
                else:
                    print(drunk_filter("Please choose one of the options..."))  # leave drug filter off
                    time.sleep(error_delay)
                    continue
        # other betting choices
        elif roul_choice == 2:
            bet_on_red = True
        elif roul_choice == 3:
            bet_on_black = True
        elif roul_choice == 4:
            bet_on_even = True
        elif roul_choice == 5:
            bet_on_odd = True
        elif roul_choice == 0:
            time.sleep(med_delay)
            continue
        else:
            print(drunk_filter("Please choose one of the options..."))  # leave drug filter off
            time.sleep(error_delay)
            continue

        # ask for bet amount and check
        bet_checked = False
        while not bet_checked:
            clear()
            hp_bank_header()
            print("________________________________________________")
            print("")
            print("                    ROULETTE                    ")
            print("")
            print("                                  O O O         ")
            print("    Enter bet of at least       O   |   O       ")
            print("    1 cR...                   O     |     O     ")
            print("                              O --- X --- O     ")
            print("                              O     |     O     ")
            print("                                O   |   O       ")
            print("                                  O O O         ")
            print("")
            try:
                bet_amount = int(input())
            except ValueError:
                print(drunk_filter("Please enter an amount of at least 1..."))  # leave drug filter off
                time.sleep(error_delay)
                continue
            if bet_amount > current_balance:
                print(drunk_filter("That's more than you have..."))  # leave drug filter off
                time.sleep(error_delay)
            elif 0 < bet_amount <= current_balance:
                clear()
                balance_chng_animation(down=bet_amount)
                bet_checked = True
            else:
                print(drunk_filter("Please enter an amount of at least 1..."))  # leave drug filter off
                time.sleep(error_delay)

        # generate spin
        min_spin_steps = random.randint(200, 350)

        # list for spin
        roul_spin_list = []
        while len(roul_spin_list) < min_spin_steps:
            roul_spin_list += roul_seq

        # get bet info for spin screen
        if bet_on_single:
            bet_info_end = str(roul_single_num)
        elif bet_on_red:
            bet_info_end = "red"
        elif bet_on_black:
            bet_info_end = "black"
        elif bet_on_even:
            bet_info_end = "even"
        else:
            bet_info_end = "odd"
        bet_info = "You bet " + str(bet_amount) + " cR on " + bet_info_end

        # print spin
        for spin_num in roul_spin_list:
            clear()
            hp_bank_header()
            print("________________________________________________")
            print("")
            print("                    ROULETTE                    ")
            print("")
            print("                     O O O                      ")
            print("                   O   |   O                    ")
            print("                 O     |     O                  ")
            print("                 O --- X --- O                  ")
            print("                 O     |     O                  ")
            print("                   O   |   O                    ")
            print("                     O O O                      ")
            print("")
            print_middle(str(spin_num))
            print("")
            print_middle(bet_info)
            time.sleep(0.0000001)

        # check result
        roul_answer = roul_spin_list[-1]
        if bet_on_single:
            if roul_single_num == roul_answer:
                roul_win = True
                win_amount = bet_amount * 37
        elif bet_on_red:
            if roul_colour[roul_answer] == "R":
                roul_win = True
                win_amount = bet_amount * 2
        elif bet_on_black:
            if roul_colour[roul_answer] == "B":
                roul_win = True
                win_amount = bet_amount * 2
        elif bet_on_even:
            if roul_answer % 2 == 0:
                roul_win = True
                win_amount = bet_amount * 2
        elif bet_on_odd:
            if roul_answer % 2 == 1:
                roul_win = True
                win_amount = bet_amount * 2

        # hold result on screen for a moment
        time.sleep(text_delay)

        # show info for number
        if roul_colour[roul_answer] == "R":
            num_colour = "red"
        elif roul_colour[roul_answer] == "B":
            num_colour = "black"
        else:
            num_colour = "green"
        if roul_answer % 2 == 0:
            oddeven = "even"
        else:
            oddeven = "odd"
        clear()
        banner_text(str(roul_answer) + " is " + num_colour + " and " + oddeven)
        time.sleep(text_delay)

        # show win or loose result
        if roul_win and win_amount > 0:
            clear()
            banner_text("You won " + str(win_amount) + " cR!!")
            time.sleep(text_delay)
            clear()
            balance_chng_animation(up=win_amount)
        else:
            clear()
            banner_text("YOU LOSE")
            time.sleep(text_delay)
            clear()
            banner_text("BETTER LUCK NEXT TIME ;)")
            time.sleep(text_delay)

    # If no money, don't let player play
    if current_balance <= 0:
        clear()
        banner_text("Come back when you got some credits...")
        time.sleep(text_delay)
        clear()


# roulette()  # for testing


# ----- Slot machine -----

def slot_machine():
    print("play slot machine")  # for testing
    time.sleep(2)  # for testing
    slot_mach_dict = {
        0:  {"thing": "sand",          "count": 50, "thresh":  50},
        1:  {"thing": "bone",          "count": 37, "thresh":  87},
        2:  {"thing": "square",        "count": 20, "thresh": 107},
        3:  {"thing": "green",         "count": 15, "thresh": 122},
        4:  {"thing": "red",           "count": 12, "thresh": 134},
        5:  {"thing": "water",         "count": 11, "thresh": 145},
        6:  {"thing": "grass",         "count": 10, "thresh": 155},
        7:  {"thing": "fish",          "count":  9, "thresh": 164},
        8:  {"thing": "flower",        "count":  8, "thresh": 172},
        9:  {"thing": "racoon",        "count":  7, "thresh": 179},
        10: {"thing": "microphone",    "count":  6, "thresh": 185},
        11: {"thing": "clown",         "count":  5, "thresh": 190},
        12: {"thing": "elephant",      "count":  4, "thresh": 194},
        13: {"thing": "dinosaur",      "count":  3, "thresh": 197},
        14: {"thing": "space station", "count":  2, "thresh": 199},
        15: {"thing": "diamond",       "count":  1, "thresh": 200}
    }
    slot_mach_prize_dict = {
        "sand":               64,
        "bone":              158,
        "square":           1000,
        "green":            2370,
        "red":              4630,
        "water":            6011,
        "grass":            8000,
        "fish":            10974,
        "flower":          15625,
        "racoon":          23324,
        "microphone":      37037,
        "clown":           64000,
        "elephant":       125000,
        "dinosaur":       296296,
        "space station": 1000000,
        "diamond":       8000000
    }
    slot_choice = 1  # initialize
    while slot_choice != 0 and current_balance > 0:
        clear()
        hp_bank_header()
        print("________________________________________________")
        print("")
        print("                     SLOTS                      ")
        print("")
        print("                    diamond")
        print("                    diamond")
        print("                    diamond")
        print("")
        print("           Up to 160,000,000 cR prize!!         ")
        print("")
        print("1 | Play (20 cR)")
        print("")
        print("0 | Leave")
        print("")
        try:
            slot_choice = int(input())
        except ValueError:
            print(drunk_filter("Please choose one of the options..."))  # leave drug filter off
            time.sleep(error_delay)
            continue
        if slot_choice == 1:
            slot_game_won = False  # initialize
            print("play slot machine")  # for testing
            time.sleep(1)  # for testing
            # Charge player game entry fee
            clear()
            balance_chng_animation(down=20)
            # Create randomly ordered list of possible slot outcomes
            slot_answer_main_list = []
            for index in slot_mach_dict.keys():
                if random.random() >= 0.5:
                    slot_answer_main_list.append(slot_mach_dict[index]["thing"])
                else:
                    slot_answer_main_list.insert(0, slot_mach_dict[index]["thing"])
            print(slot_answer_main_list)  # for testing

            # Generate outcome indexes for 3 "reels"
            slot1_num = random.randint(1, 200)
            slot2_num = random.randint(1, 200)
            slot3_num = random.randint(1, 200)
            print(slot1_num)  # for testing
            print(slot2_num)  # for testing
            print(slot3_num)  # for testing

            # Generate 3 answers
            # Get slot 1 answer, ensuring at least "sand" is the outcome
            slot1_answer = "sand"
            for slot1_index in slot_mach_dict.keys():
                thresh_num = slot_mach_dict[slot1_index]["thresh"]
                if slot1_num >= thresh_num:
                    slot1_answer = slot_mach_dict[slot1_index]["thing"]
            print(slot1_answer)  # for testing
            # Get slot 2 answer, ensuring at least "sand" is the outcome
            slot2_answer = "sand"
            for slot2_index in slot_mach_dict.keys():
                thresh_num = slot_mach_dict[slot2_index]["thresh"]
                if slot2_num >= thresh_num:
                    slot2_answer = slot_mach_dict[slot2_index]["thing"]
            print(slot2_answer)  # for testing
            # Get slot 3 answer, ensuring at least "sand" is the outcome
            slot3_answer = "sand"
            for slot3_index in slot_mach_dict.keys():
                thresh_num = slot_mach_dict[slot3_index]["thresh"]
                if slot3_num >= thresh_num:
                    slot3_answer = slot_mach_dict[slot3_index]["thing"]
            print(slot3_answer)  # for testing

            # Generate how many flips are required before showing answer
            # 3rd reel takes longer if reels 1 and 2 match
            min_flips1 = random.randint(400, 1000)
            min_flips2 = random.randint(200, 1000)
            if slot1_num == slot2_num:
                min_flips3 = random.randint(700, 1200)
            else:
                min_flips3 = random.randint(100, 400)

            # Create 3 lists to flip through
            # Create 1st list, landing on slot 1 answer
            # Make sure list to flip through is of good length
            slot1_list = []  # initialize
            while len(slot1_list) < min_flips1:
                slot1_list += slot_answer_main_list
            # Make sure list ends on the correct answer
            while slot1_list[-1] != slot1_answer:
                slot1_list.pop(-1)
            # Create 2nd list, landing on slot 2 answer
            # Make sure list to flip through is of good length
            slot2_list = []  # initialize
            while len(slot2_list) < min_flips2:
                slot2_list += slot_answer_main_list
            # Make sure list ends on the correct answer
            while slot2_list[-1] != slot2_answer:
                slot2_list.pop(-1)
            # Create 3rd list, landing on slot 3 answer
            # Make sure list to flip through is of good length
            slot3_list = []  # initialize
            while len(slot3_list) < min_flips3:
                slot3_list += slot_answer_main_list
            # Make sure list ends on the correct answer
            while slot3_list[-1] != slot3_answer:
                slot3_list.pop(-1)

            # Print reels
            # Print reel 1
            reel1_print_index = 0
            reel1_final_index = len(slot1_list) - 1
            while reel1_print_index <= reel1_final_index:
                clear()
                hp_bank_header()
                print("________________________________________________")
                print("")
                print("                     SLOTS                      ")
                print("")
                print_middle(slot1_list[reel1_print_index])
                if 0 <= (reel1_final_index - reel1_print_index) < 10:
                    reel1_print_index += 1
                    time.sleep(0.0000001)
                elif 10 <= (reel1_final_index - reel1_print_index) < 25:
                    reel1_print_index += 1
                    time.sleep(0.0000001)
                elif 25 <= (reel1_final_index - reel1_print_index) < 50:
                    reel1_print_index += 2
                    time.sleep(0.0000001)
                elif 50 <= (reel1_final_index - reel1_print_index) < 100:
                    reel1_print_index += 2
                    time.sleep(0.0000001)
                else:
                    reel1_print_index += 3
                    time.sleep(0.0000001)
            time.sleep(med_delay)
            # Print reel 2
            reel2_print_index = 0
            reel2_final_index = len(slot2_list) - 1
            while reel2_print_index <= reel2_final_index:
                clear()
                hp_bank_header()
                print("________________________________________________")
                print("")
                print("                     SLOTS                      ")
                print("")
                print_middle(slot1_answer)
                print_middle(slot2_list[reel2_print_index])
                if 0 <= (reel2_final_index - reel2_print_index) < 10:
                    reel2_print_index += 1
                    time.sleep(0.0000001)
                elif 10 <= (reel2_final_index - reel2_print_index) < 25:
                    reel2_print_index += 1
                    time.sleep(0.0000001)
                elif 25 <= (reel2_final_index - reel2_print_index) < 50:
                    reel2_print_index += 2
                    time.sleep(0.0000001)
                elif 50 <= (reel2_final_index - reel2_print_index) < 100:
                    reel2_print_index += 2
                    time.sleep(0.0000001)
                else:
                    reel2_print_index += 3
                    time.sleep(0.0000001)
            time.sleep(med_delay)
            # Print reel 3
            reel3_print_index = 0
            reel3_final_index = len(slot3_list) - 1
            while reel3_print_index <= reel3_final_index:
                clear()
                hp_bank_header()
                print("________________________________________________")
                print("")
                print("                     SLOTS                      ")
                print("")
                print_middle(slot1_answer)
                print_middle(slot2_answer)
                print_middle(slot3_list[reel3_print_index])
                if 0 <= (reel3_final_index - reel3_print_index) < 10:
                    reel3_print_index += 1
                    time.sleep(0.0000001)
                elif 10 <= (reel3_final_index - reel3_print_index) < 25:
                    reel3_print_index += 1
                    time.sleep(0.0000001)
                elif 25 <= (reel3_final_index - reel3_print_index) < 50:
                    reel3_print_index += 2
                    time.sleep(0.0000001)
                elif 50 <= (reel3_final_index - reel3_print_index) < 100:
                    reel3_print_index += 2
                    time.sleep(0.0000001)
                else:
                    reel3_print_index += 3
                    time.sleep(0.0000001)
            time.sleep(med_delay)
            time.sleep(med_delay)

            # Display win/loose message
            clear()
            win_amount = 0  # initialize
            if slot1_answer == slot2_answer and slot2_answer == slot3_answer:
                win_amount = slot_mach_prize_dict[slot1_answer] * 20
                banner_text("WINNER!")
                time.sleep(med_delay)
                time.sleep(med_delay)
                banner_text("You won " + str(win_amount) + " cR!!")
                clear()
                balance_chng_animation(up=win_amount)
            else:
                banner_text("YOU LOSE")
                time.sleep(med_delay)
                time.sleep(med_delay)
                clear()
                banner_text("BETTER LUCK NEXT TIME ;)")
            time.sleep(med_delay)
            time.sleep(med_delay)
        elif slot_choice == 0:
            time.sleep(med_delay)
            continue
        else:
            print(drunk_filter("Please choose one of the options..."))  # leave drug filter off
            time.sleep(error_delay)
            continue

    # If no money, don't let player play
    if current_balance <= 0:
        clear()
        banner_text("Come back when you got some credits...")
        time.sleep(med_delay)
        time.sleep(med_delay)
        clear()


# slot_machine()  # for testing

# --------------------------------------------------- Combat -----------------------------------------------------------

# ----------------------------------------- Overworld Random events ----------------------------------------------------

# -------------------- go random event! --------------------
# Aim:
# > Need this to run at the start of every turn in the overworld
# > Need to check current tile and get related chance of each kind of event
# > Mix of good and bad events, e.g. mugging and gang fights etc

def ow_go_random_event():
    print("check random event and go")  # for testing
    # time.sleep(0.2)  # for testing

# ---------------------------------------- Procedural Quest Functions --------------------------------------------------

# ----------------------------------------- Scripted Quest Functions ---------------------------------------------------
# NOTE:
# > Every scripted quest will need its own function.


# ------------------------------ Functions for accessing specific fixed buildings --------------------------------------
# NOTE: Should come after quest functions, in case quest is run from inside a building. Tbh a lot will be.
# > Lets have 5 other apartment blocks in addition to players.
# > These apartments could have procedurarly generated content.

# ----- Access player apartment building ----- IN PROGRESS

def access_player_appt_buil():
    print("accessing player apartment")  # for testing
    time.sleep(2)  # for testing


# ------------------------------------------- Overworld Functions ------------------------------------------------------

#       ##### ------------------------------ Get current tile info ------------------------------ ######

# ---------- Get or generate current tile "shop" list ---------- GFN
# When player is on a tile, check if they have been there before.
# If not, generate "shops" based on probability and type of tile.
# > Save result in dict and as current tile place list.
# If yes, lookup shops from dictionary and updated cur_shop_list to the result.
# "Shops" are not just food shops etc, they can also be clinics etc. Any place the player can go that is procedural.
# "Buildings" are all fixed to certain tiles e.g. hacker base and player appt. But a restaurant is a "shop".

def get_or_gen_cur_shop_list():
    global sol_overworld_biome_dict
    global cur_shop_list
    cur_shop_list.clear()  # start with empty list
    temp_tile_dict = {}
    temp_col_dict = {}
    cur_biome_tile = sol_overworld_biome_list[cur_loc_row][cur_loc_col]
    # Check if there is an entry for row, col, and shop list in the sol overworld biome dict
    # If we have all 3, lookup shop list for current tile. If not, generate one with tile type and probabilities.
    if cur_loc_row in sol_overworld_biome_dict.keys():
        if cur_loc_col in sol_overworld_biome_dict[cur_loc_row].keys():
            if str("shop_list") in sol_overworld_biome_dict[cur_loc_row][cur_loc_col].keys():
                # print("yes")  # for testing
                # time.sleep(5)  # for testing
                cur_shop_list = sol_overworld_biome_dict[cur_loc_row][cur_loc_col]["shop_list"][:]
                print(sol_overworld_biome_dict[cur_loc_row][cur_loc_col]["shop_list"])
                print("current shop list is")  # for testing
                # print(cur_shop_list)  # for testing
                # time.sleep(5)  # for testing
            else:
                for shop in sol_ow_shop_probs[cur_biome_tile]:
                    if random.random() < sol_ow_shop_probs[cur_biome_tile][shop]:
                        cur_shop_list.append(shop)
                sol_overworld_biome_dict[cur_loc_row][cur_loc_col]["shop_list"] = cur_shop_list[:]
                # print("no")  # for testing
                # time.sleep(5)  # for testing
        else:
            for shop in sol_ow_shop_probs[cur_biome_tile]:
                if random.random() < sol_ow_shop_probs[cur_biome_tile][shop]:
                    cur_shop_list.append(shop)
            temp_tile_dict["shop_list"] = cur_shop_list[:]
            sol_overworld_biome_dict[cur_loc_row][cur_loc_col] = temp_tile_dict
    else:
        for shop in sol_ow_shop_probs[cur_biome_tile]:
            if random.random() < sol_ow_shop_probs[cur_biome_tile][shop]:
                cur_shop_list.append(shop)
        temp_tile_dict["shop_list"] = cur_shop_list[:]
        temp_col_dict[cur_loc_col] = temp_tile_dict
        sol_overworld_biome_dict[cur_loc_row] = temp_col_dict

# I think this is that thing about lists getting cleared, i need a new copy of the list, but it's treating the list
# inside the dictionary as the same list!!!!!!
# might be fixed with slice but not sure


# ---------- Get current avail scripted quest list (for overworld tile quests only) ---------- GFN
# > Need to check current tile for list of possible quests, then check requirements and only show possible quests.
# > Don't show any quests already marked as "comp" (completed).
# > Then produce a list of quest names.
# > NOTE: would be easier to handle procedural quests later as a separate function.
# > Also, this is only for quests accessible in the overworld. Quests inside buildings should be handled by specific
#   building functions.
# > NOTE: only call requirement flag functions if requirements are specified

# ----- Check char met requirement for specific quest against dict ----- GFN

def ow_char_met_req(spec_quest):
    char_met_flag = 0  # intialize
    for char in quest_req[spec_quest]["char_met"].keys():
        if quest_req[spec_quest]["char_met"][char] != char_met[char]:
            char_met_flag += 1
    if char_met_flag > 0:
        flag = "failed"
    else:
        flag = "passed"
    return flag


# ----- Check char dead requirement for specific quest against dict ----- GFN
# put all the keys for the quest char dead dict in a list
# then do a for loop where you check them one at a time against the main char_dead dict
# if any don't match, flag it and return fail

def ow_char_dead_req(spec_quest):
    char_dead_flag = 0  # intialize
    for char in quest_req[spec_quest]["char_dead"].keys():
        if quest_req[spec_quest]["char_dead"][char] != char_dead[char]:
            char_dead_flag += 1
    if char_dead_flag > 0:
        flag = "failed"
    else:
        flag = "passed"
    return flag


# ----- Check char romance requirement for specific quest against dict ----- GFN

def ow_char_rom_req(spec_quest):
    char_rom_flag = 0  # intialize
    for char in quest_req[spec_quest]["char_rom"].keys():
        if quest_req[spec_quest]["char_rom"][char] < rom_scores[char]:
            char_rom_flag += 1
    if char_rom_flag > 0:
        flag = "failed"
    else:
        flag = "passed"
    return flag


# ----- Check char friend requirement for specific quest against dict ----- GFN

def ow_char_fren_req(spec_quest):
    char_fren_flag = 0  # intialize
    for char in quest_req[spec_quest]["char_fren"].keys():
        if quest_req[spec_quest]["char_fren"][char] < fren_scores[char]:
            char_fren_flag += 1
    if char_fren_flag > 0:
        flag = "failed"
    else:
        flag = "passed"
    return flag


# ----- Check char allegiance requirement for specific quest against dict ----- GFN

def ow_alleg_req(spec_quest):
    alleg_flag = 0  # intialize
    for char in quest_req[spec_quest]["alleg"].keys():
        if quest_req[spec_quest]["alleg"][char] < alleg_dict[char]:
            alleg_flag += 1
    if alleg_flag > 0:
        flag = "failed"
    else:
        flag = "passed"
    return flag


# ----- Check char skills requirement for specific quest against dict ----- GFN

def ow_skills_req(spec_quest):
    skills_flag = 0  # intialize
    for char in quest_req[spec_quest]["skills"].keys():
        if quest_req[spec_quest]["skills"][char] < skills[char]:
            skills_flag += 1
    if skills_flag > 0:
        flag = "failed"
    else:
        flag = "passed"
    return flag


# ----- Check quest prog requirement for specific quest against dict ----- GFN

def ow_quest_prog_req(spec_quest):
    quest_prog_flag = 0  # intialize
    for char in quest_req[spec_quest]["quest_prog"].keys():
        if quest_req[spec_quest]["quest_prog"][char] != quest_prog[char]["prog"]:
            quest_prog_flag += 1
    if quest_prog_flag > 0:
        flag = "failed"
    else:
        flag = "passed"
    return flag


# ----- Get all possible quests for current tile, then remove any that don't match requirements ----- GFN

def get_cur_ow_quest():
    global cur_ow_quest_list
    cur_ow_quest_list.clear()  # start with clear list
    # Get any and all quests for the current overworld tile
    try:
        cur_ow_quest_list = ow_quest_loc[cur_loc_row][cur_loc_col][:]
    except KeyError:
        cur_ow_quest_list.clear()

    # Check requirements for each quest on tile and remove any that the player shouldn't have access to.
    # Le epic for loop!
    # Reset requirement flags to zero each iteration. If any requirements not met, set flag to 1.
    # At end of loop, sum all flags and if > 0 then not all requirements and quest should be removed from avail list.
    for quest_name in cur_ow_quest_list:
        char_met_rflag = 0
        char_dead_rflag = 0
        char_rom_rflag = 0
        char_fren_rflag = 0
        alleg_rflag = 0
        skills_rflag = 0
        quest_prog_rflag = 0
        # These are SUPPOSED to be separate "ifs". We need ALL of them to be checked sequentially.
        if quest_req[quest_name]["char_met"]:
            if ow_char_met_req(quest_name) == "failed":
                char_met_rflag = 1
        if quest_req[quest_name]["char_dead"]:
            if ow_char_dead_req(quest_name) == "failed":
                char_dead_rflag = 1
        if quest_req[quest_name]["char_rom"]:
            if ow_char_rom_req(quest_name) == "failed":
                char_rom_rflag = 1
        if quest_req[quest_name]["char_fren"]:
            if ow_char_fren_req(quest_name) == "failed":
                char_fren_rflag = 1
        if quest_req[quest_name]["alleg"]:
            if ow_alleg_req(quest_name) == "failed":
                alleg_rflag = 1
        if quest_req[quest_name]["skills"]:
            if ow_skills_req(quest_name) == "failed":
                skills_rflag = 1
        if quest_req[quest_name]["quest_prog"]:
            if ow_quest_prog_req(quest_name) == "failed":
                quest_prog_rflag = 1
        # Total up requirement flags
        req_flag_total = (char_met_rflag + char_dead_rflag + char_rom_rflag + char_fren_rflag + alleg_rflag +
                          skills_rflag + quest_prog_rflag)
        # If requirements not met for quest, remove from available list for current tile
        # print(char_met_rflag)
        # print(char_dead_rflag)
        # print(char_rom_rflag)
        # print(char_fren_rflag)
        # print(alleg_rflag)
        # print(skills_rflag)
        # print(quest_prog_rflag)
        if req_flag_total > 0:
            cur_ow_quest_list.remove(quest_name)


# ---------- Get current building ---------- GFN
# Lookup current building for tile, max 1 building per tile
# All buildings are fixed, so if there is no reference for current col or row, there cannot be a building.
# Buildings are different to "shops", as they are all fixed. "Shops" are procedurally generated, e.g. cafés.

def get_cur_building():
    global cur_building
    if cur_loc_row in sol_overworld_biome_dict.keys():
        if cur_loc_col in sol_overworld_biome_dict[cur_loc_row].keys():
            if "building" in sol_overworld_biome_dict[cur_loc_row][cur_loc_col].keys():
                cur_building = sol_overworld_biome_dict[cur_loc_row][cur_loc_col]["building"][:]
            else:
                cur_building = "none"
        else:
            cur_building = "none"
    else:
        cur_building = "none"


# ---------- Get current move info ---------- GFN
# Store as dict, so we can remember which info relates to which direction
# Heirachy for info is "edge of dome" > "border" > "gate" > "building info" > "shops"
# cur_move_dict = {
#    "w": {"disp": up (info), "command": "north"},
#    "s": {"disp": down (info), "command": "south"},
#    "a": {"disp": left (info), "command": "west" <- if next to gate, set command to "gate"},
#    "d": {"disp": right (info), "command": "east" <- if blocked by border or n, set command to "blocked"}
# }

def get_move_info():
    global cur_move_dict
    global cur_tile
    # Check adjacent tiles
    try:
        cur_tile = sol_overworld_biome_list[cur_loc_row][cur_loc_col]
    except KeyError:
        cur_tile = "none"
    try:
        up_tile = sol_overworld_biome_list[cur_loc_row - 1][cur_loc_col]
    except KeyError:
        up_tile = "none"
    try:
        down_tile = sol_overworld_biome_list[cur_loc_row + 1][cur_loc_col]
    except KeyError:
        down_tile = "none"
    try:
        left_tile = sol_overworld_biome_list[cur_loc_row][cur_loc_col - 1]
    except KeyError:
        left_tile = "none"
    try:
        right_tile = sol_overworld_biome_list[cur_loc_row][cur_loc_col + 1]
    except KeyError:
        right_tile = "none"

    # Get option info for adjacent tiles
    up_disp = "W | Up (" + move_opt_info[up_tile] + ")"
    down_disp = "S | Down (" + move_opt_info[down_tile] + ")"
    left_disp = "A | Left (" + move_opt_info[left_tile] + ")"
    right_disp = "D | Right (" + move_opt_info[right_tile] + ")"

    # Get commands for adjacent tiles
    # > If next to gate, then command will be "gate". If next to border or edge of dome, command will be "blocked".

    # Up command
    if up_tile == "none" or up_tile == "border" or up_tile == "nope":
        up_command = "blocked"
    elif up_tile == "gate":
        up_command = "gate"
    else:
        up_command = "north"

    # Down command
    if down_tile == "none" or down_tile == "border" or down_tile == "nope":
        down_command = "blocked"
    elif down_tile == "gate":
        down_command = "gate"
    else:
        down_command = "south"

    # Left command
    if left_tile == "none" or left_tile == "border" or left_tile == "nope":
        left_command = "blocked"
    elif left_tile == "gate":
        left_command = "gate"
    else:
        left_command = "west"

    # Right command
    if right_tile == "none" or right_tile == "border" or right_tile == "nope":
        right_command = "blocked"
    elif right_tile == "gate":
        right_command = "gate"
    else:
        right_command = "east"

    # Update cur move dict
    cur_move_dict["w"]["disp"] = up_disp
    cur_move_dict["w"]["command"] = up_command
    cur_move_dict["s"]["disp"] = down_disp
    cur_move_dict["s"]["command"] = down_command
    cur_move_dict["a"]["disp"] = left_disp
    cur_move_dict["a"]["command"] = left_command
    cur_move_dict["d"]["disp"] = right_disp
    cur_move_dict["d"]["command"] = right_command


# -------------------- get sol current overworld display text list -------------------- IN PROGRESS
# Aim:
# > Create a list for relevant display text for overworld tile.
# > Check if any fixed disp text first, if not check tile type and look in generic source. Get random text for tile.
# > Then use RNG to see if disp text should be printed. 1 in 5 chance of showing generic text to keep it fresh.
# > If not going to print, empty the list. Result should be fixed before loop that controls for bad inputs.
# NOTE: Could have it so fixed display text is deleted form the ow biome dict when moving off the square, so it isn't
#       repeated.


def get_ow_disp_text():
    global cur_tile
    global cur_ow_disp_text
    cur_ow_disp_text.clear()  # clear list if needed
    cur_tile = sol_overworld_biome_list[cur_loc_row][cur_loc_col]  # get current tile
    use_gen_disp = False  # initialize, will use generic display text if none specificed
    min_disp_num = 1  # initialize
    max_disp_num = 1  # initialize
    show_disp_dice_roll = random.randint(1,5)
    # Check if there is fixed display text for current tile
    try:
        cur_ow_disp_text = sol_overworld_biome_dict[cur_loc_row][cur_loc_col]["ow_disp"][:]
    # If there isn't, check for generic text to select from. If it can't find any, empty the display text list.
    except KeyError:
        use_gen_disp = True
        try:
            min_disp_num = min(ow_gen_disp_dict[cur_tile].keys())
        except ValueError:
            use_gen_disp = False
            cur_ow_disp_text.clear()
        try:
            max_disp_num = max(ow_gen_disp_dict[cur_tile].keys())
        except ValueError:
            use_gen_disp = False
            cur_ow_disp_text.clear()
    # if we've found generic display text for the current tile, there's a 1 in 5 chance of displaying it
    disp_random = random.randint(min_disp_num, max_disp_num)
    if use_gen_disp:
        cur_ow_disp_text = ow_gen_disp_dict[cur_tile][disp_random][:]
    if use_gen_disp and show_disp_dice_roll != 3:
        cur_ow_disp_text.clear()


# -------------------- sol overworld option dict builder -------------------- IN PROGRESS
# Aim:
# > To generate options for player in the overworld
# > Need to take into account conditional availability of options etc
# > ONLY ALLOW POSSIBLE options. No blocked or unavailable missions etc.
# >> Check current and adjacent tiles for directional options, and retain info to advise player
# > Build a dictionary for purposes of displaying options and accepting input from player
# >> In the form of something like
# cur_ow_option_dict = {
#    1: {"disp_opt": blah,         opt_type: "quest",        rel: "quest_name"    }
#    2: {"disp_opt": blah,         opt_type: "building",     rel: "building_name" }
#    3: {"disp_opt": blah,         opt_type: "shop",         rel: "shop_name"     }
#    6: {"disp_opt": ARC menu,     opt_type: "personal",     rel: "arc_menu"      }
#    w: {"disp_opt": up (info),    opt_type: "move",         rel: "north"         }
#    s: {"disp_opt": down,         opt_type: "move",         rel: "south"         }
#    d: {"disp_opt": right,        opt_type: "move",         rel: "east" <- swap out for blocked if border or n}
#    a: {"disp_opt": left,         opt_type: "move",         rel: "west" <- could also be gate}
#    b: {"disp_opt": black market, opt_type: "black_market", rel: "black_market"  }
# }
# Info:
# > so we have the keys which will be player inputs
# > disp_opt is the way the option will be displayed to the player
# > opt type is the type of option, e.g. a quest, fixed building, shop, movement option
# > rel is the related info, e.g. the name of the quest to run, the name of the building to enter, the direction
#   command.
#   >> If direction leads to gate, need to set rel to "gate" and deal with as a special case.
#   >> If rel: is "blocked" then when executing in next step, display message don't allow player to move.
# > NOTE: May need to also use a list to order options by type, e.g. prioritise quest, etc, then use that list order
#   to build the dictionary and option order will then make sense.
# IMPORTANT: this function actually calls the above functions to get the different parts and then assembles into one
#            dict.


def ow_option_builder():
    # call all necessary functions
    get_or_gen_cur_shop_list()
    get_cur_ow_quest()
    get_cur_building()
    get_move_info()
    get_ow_disp_text()
    # start building dictionary
    global cur_ow_option_dict
    cur_ow_option_dict.clear()  # start with empty dictionary
    next_key = 1  # initialize, only increment on numbered options
    # if we have overworld quests, add them
    if len(cur_ow_quest_list) > 0:
        for quest in cur_ow_quest_list:
            cur_ow_option_dict[next_key] = {"disp_opt": str(next_key) + " | " + quest_opt_text[quest],
                                            "opt_type": "quest",
                                            "rel": quest}
            next_key += 1
    # if we have a building, add it - should just be max 1 per tile
    if cur_building != "none":
        building_disp = str(next_key) + " | Enter " + building_fullnames[cur_building]
        cur_ow_option_dict[next_key] = {"disp_opt": building_disp,
                                        "opt_type": "building",
                                        "rel": cur_building}
        next_key += 1
    # if we have shops, add them
    if len(cur_shop_list) > 0:
        for shop in cur_shop_list:
            cur_ow_option_dict[next_key] = {"disp_opt": str(next_key) + " | " + shop_fullnames[shop],
                                            "opt_type": "shop",
                                            "rel": shop}
            next_key += 1
    # if ARC menu available, add it
    if ARC_menu_avail:
        cur_ow_option_dict["u"] = {"disp_opt": "U | ARC Menu",
                                   "opt_type": "personal",
                                   "rel": "arc_menu"}
    # if player inventory available, add it - no need for appt or hackerbase storage as these in buildings only
    if player_invent_avail:
        cur_ow_option_dict["i"] = {"disp_opt": "I | Inventory",
                                   "opt_type": "personal",
                                   "rel": "inventory"}
    # add small map
    cur_ow_option_dict["m"] = {"disp_opt": "M | Map",
                               "opt_type": "personal",
                               "rel": "map"}
    # if black market available, add it
    if bmarket_avail:
        cur_ow_option_dict["b"] = {"disp_opt": "B | Blackmarket",
                                   "opt_type": "blackmarket",
                                   "rel": "blackmarket"}
    # add movement options
    cur_ow_option_dict["w"] = {"disp_opt": cur_move_dict["w"]["disp"],
                               "opt_type": "move",
                               "rel": cur_move_dict["w"]["command"]}
    cur_ow_option_dict["s"] = {"disp_opt": cur_move_dict["s"]["disp"],
                               "opt_type": "move",
                               "rel": cur_move_dict["s"]["command"]}
    cur_ow_option_dict["a"] = {"disp_opt": cur_move_dict["a"]["disp"],
                               "opt_type": "move",
                               "rel": cur_move_dict["a"]["command"]}
    cur_ow_option_dict["d"] = {"disp_opt": cur_move_dict["d"]["disp"],
                               "opt_type": "move",
                               "rel": cur_move_dict["d"]["command"]}


# ow_option_builder()  # for testing
#
# print(cur_ow_quest_list)  # for testing
# print(cur_ow_option_dict)  # for testing
# time.sleep(60)  # for testing


#        ##### ------------------------------ Actions for current tile info ------------------------------ ######

# ---------- Enter building ---------- IN PROGRESS
# Prompt and choice should be controlled elsewhere

def enter_building(building):
    print("enter " + building)  # for testing
    time.sleep(2)  # for testing
    if building == "player_appt_buil":
        access_player_appt_buil()


# ---------- Run quest ---------- IN PROGRESS
# Prompt and choice should be controlled elsewhere

def run_quest(quest):
    print("run " + quest)  # for testing
    time.sleep(2)  # for testing
    # if quest == "name_of_quest":
    #      access_quest1() etc


# ---------- Enter shop ---------- IN PROGRESS
# Prompt and choice should be controlled elsewhere

def enter_shop(shop):
    print("enter " + shop)  # for testing
    time.sleep(2)  # for testing
    # if shop == "name_of_shop":
    #     access_shop1() etc


# -------------------- Move player -------------------- IN PROGRESS
# > Pass direction for player to move in from ow option print execute
# > If move is not possible, e.g. border, display message
# > If it's to a gate, will need to handle separately, for now block same as border.
# > If move is successful, update

def move_player(direction):
    global cur_loc_row
    global cur_loc_col
    # print("move player " + direction)  # for testing
    # time.sleep(2)  # for testing
    if direction == "north":
        cur_loc_row -= 1
    elif direction == "south":
        cur_loc_row += 1
    elif direction == "east":
        cur_loc_col += 1
    elif direction == "west":
        cur_loc_col -= 1


# -------------------- sol overworld option printer and executor --------------------
# Easier to keep this as one function in case of re-printing
# First:
# > Compile and print what the player actually sees in the overworld
# > This includes relevant display text for tile and list of options as determined by cur ow option dict
# Second:
# > process player's choice using cur_ow_option_dict
# > If player input is invalid, will need to clear and loop back to first step (but with "page already read") to skip
#   any printing delays.
# > Based on what the player has chosen, need to do the following...
# >> For quests, call run_quest, using run_quest(quest_name)  -- this will work a lot like enter building
# >> For buildings, call enter_building, using enter_building(building_name)
# >> For shops, call enter_shop, using enter_shop(shop_name)  -- this will work a lot like enter building
# >>> Regarding shops, I think I should rename "places" to shops, and call all such things shops
# >>> Again, the buildings should be any fixed buildings, but shops are proceduraly generated.
# >>> This will include clinics, maybe debt offices etc.
# NEED LOOP WITHIN FUNCTION TO HANDLE BAD INPUTS


def ow_print_exec():
    ow_choice_made = False  # initialize
    ow_disp_read = False  # initialize
    ow_choice = 1  # initialize
    ow_type = ""  # initialize
    ow_command = ""  # initialize
    # get disp name
    ow_disp_location = move_opt_info[cur_tile]
    if ow_disp_location == "Your Apartment":
        ow_disp_location = "Outside Your Apartment"
    # loop to ensure choice
    while not ow_choice_made:
        clear()
        hp_bank_header()
        sol_map_banner()
        print("")
        print_middle("(" + ow_disp_location + ")")
        print("")
        # ow disp text
        for ow_disp in cur_ow_disp_text:
            if ow_disp == '!PAUSE!':
                time.sleep(text_delay)
            elif ow_disp == '!SHORTPAUSE!':
                time.sleep(med_delay)
                time.sleep(med_delay)
            else:
                print(ow_disp)
        print("")
        for ow_key in cur_ow_option_dict.keys():
            print(" " + cur_ow_option_dict[ow_key]["disp_opt"])
        print("")
        read_speed(4)
        # input works so only a key is accepted, only numberic or str, for str accepts upper and lower
        ow_choice = input()
        if ow_choice.isnumeric():
            # print("string is numeric")  # for testing
            ow_choice = int(ow_choice)
            # time.sleep(3)  # for testing
        elif ow_choice.isalpha():
            # print("string is alpha")  # for testing
            ow_choice = ow_choice.lower()
            # time.sleep(3)  # for testing
        else:
            print("Please choose one of the options...")  # no drug/drunk filters
            time.sleep(error_delay)
            clear()
            continue
        if ow_choice not in cur_ow_option_dict.keys():
            print("Please choose one of the options...")  # no drug/drunk filters
            time.sleep(error_delay)
            clear()
            continue
        try:
            ow_type = cur_ow_option_dict[ow_choice]["opt_type"]
            ow_command = cur_ow_option_dict[ow_choice]["rel"]
        except KeyError:
            print("Please choose one of the options...")  # no drug/drunk filters
            time.sleep(error_delay)
            clear()
            continue
        # on each succesful choice, confirm choice has been made so loop will not trigger and reset read speed
        # print(ow_type)  # for testing
        # print(ow_command)  # for testing
        # play quest
        if ow_type == "quest":
            ow_choice_made = True
            read_speed(read_speed_choice)
            run_quest(ow_command)
        # enter building
        elif ow_type == "buidling":
            ow_choice_made = True
            read_speed(read_speed_choice)
            enter_building(ow_command)
            continue
        # enter shop
        elif ow_type == "shop":
            ow_choice_made = True
            read_speed(read_speed_choice)
            enter_shop(ow_command)
        # personal e.g. inventory or arc menu
        elif ow_type == "personal":
            ow_choice_made = True
            read_speed(read_speed_choice)
            # print("do personal, put different options")  # for testing
            # time.sleep(2)  # for testing
            if ow_command == "arc_menu":
                access_arc_menu()
            elif ow_command == "inventory":
                access_personal_inventory()
            elif ow_command == "map":
                quick_big_sol_map()
        # move player
        elif ow_type == "move":
            if ow_command == "blocked":  # if you can't move, want to clear and reset without chaning read delays yet
                print("You can't go that way...")
                time.sleep(error_delay)
                continue
            elif ow_command == "gate":
                print("That's a gate...")  # need to figure out gates later
                time.sleep(error_delay)
                continue
            else:
                ow_choice_made = True
                read_speed(read_speed_choice)
                move_player(ow_command)
        # enter blackmarket
        elif ow_type == "blackmarket":
            ow_choice_made = True
            read_speed(read_speed_choice)
            # print("access blackmarket")  # for testing
            # time.sleep(2)  # for testing
            access_black_market()
        # print("loop still in function?")  # for testing
        # time.sleep(5)  # for testing
        # time.sleep(30)  # for testing


# ------------------------------------------ New Game/Load functions ---------------------------------------------------

# -------------------- Sandcastle start screen --------------------
# > Display cool graphic, probably top one ^^^
# > Check if player has any valid saves that can be loaded (if player killed then save will be wiped)
# > Display option for new game or load (if no save files, display to player that load is unavailable etc, or hide)

# -------------------- Start new game --------------------
# > Let player either start a new game without saving (in case of 3 saves already taken) or just feel like it.
# > Or prompt player to overwrite a save if no spare saves (max of 3 slots).

# -------------------- New game dict and variable reset --------------------
# > Calling function will reset all diaries and variables to new game states
# > Run this before welcome banner
# > Always run before welcome banner, on any new game or new game following game over
# > This may seem redundant, as many variables defined at top, but should be easier as if I give global permission to
#   the function, it will say they aren't defined in main body etc. And it needs to run on any reset.

# -------------------- Load game --------------------
# > Display available saves to player (I think max of 3 is good)
# > Saving/loading will probably be done with pickle to a notepad file (maybe one for each save).
# > So deliverable to player will be a folder with exe and save notepads (maybe saving can write these?)
# > Player then chooses a save file to load, and they are locked into this file unless they quit and go back to start
#   screen. Don't want players saving across multiple slots to get around roguelike design.

# ----------------------------------------------- Save functions -------------------------------------------------------

# > Players will need to save manually, to avoid chance of quiting during save.
# > Probably put save in the ARC settings menu.
# > Player needs to be locked into a save slot, either when new game is chosen or save loaded.
#   i.e. don't let player save their current game onto multiple saves to cheat the game over.
# > Use pickle or something to write current position, quest progress and dictionary/variable info to notepad file etc.
# > Not sure yet how player will exit the game. Can hopefully just close the app. Program is only writing to save file
#   during save process. So most of the time should be fine to exit.

# --------------------------------------------- Game over functions ----------------------------------------------------

# -------------------- Generate and print game over screen --------------------
# Aim:
# > Need a cool game over screen, displayed related message
# > Handle player choice to reset or not from within PLAY GAME section itself, after game over has been printed

# -------------------- wipe current save --------------------
# > In case of game over, current save needs to be wiped

# -------------------- retry and send back to new game/load screen --------------------

# > If player retries on a game over, send them back to the start screen, with option to load any remaining games
#   or start a new game.
#   >> In case of loading, don't want to reset any variables, obviously.
#   >> In case of new game, should run new game reset as part of new game.

# ----------------------------------------------- Welcome screen -------------------------------------------------------

# ----- welcome banner ----- GFN

def welcome_banner():
    print("________________________________________________")
    print("                                                ")
    print("     oOOOoo   oOoo         |           oOoo     ")
    print("   oOOo                   -O-      oOOo   oOo   ")
    print("                           |                    ")
    print("                                                ")
    print("                xxxX        Xxxx                ")
    print("-------------xxXx              xXxx-------------")
    print("----------xxXx                    xXxx----------")
    print("-------xxXx        SANDCASTLE:       xXxx-------")
    print("-----xXx  A GAME ABOUT THE NEAR FUTURE  xXx-----")
    print("---xXx                                    xXx---")
    print("-xXx                                        xXx-")
    print("xXx..|.||.|...||.||.||..|..|.||...|.||...||..xXx")
    print("")
    print("________________________________________________")


# ----- welcome screen ----- GFN

def welcome_screen():
    global read_speed_choice
    global current_page
    global current_chapter
    global already_read_page
    global skills
    global alleg_dict
    player_choice = 0
    while player_choice != 1 and player_choice != 2 and player_choice != 3:
        clear()
        welcome_banner()
        print("")
        print("First, a few questions...")
        print("")
        print("Q1. What is your preferred reading speed?")
        print(" >  Text is currently unskippable")
        print(" >  This setting can be changed later")
        print("")
        print("1 | Normal.")
        print("2 | Fast.")
        print("3 | Super Fast.")
        print("")
        try:
            player_choice = int(input())
        except ValueError:
            print("Please choose one of the options...")
            time.sleep(error_delay)
            continue
        if player_choice == 1:
            read_speed_choice = 1
            read_speed(read_speed_choice)
        elif player_choice == 2:
            read_speed_choice = 2
            read_speed(read_speed_choice)
        elif player_choice == 3:
            read_speed_choice = 3
            read_speed(read_speed_choice)
        else:
            print("Please choose one of the options...")
            time.sleep(error_delay)

    player_choice = 0
    while player_choice != 1 and player_choice != 2 and player_choice != 3:
        clear()
        welcome_banner()
        print("")
        print("Q2. If you find yourself in a confrontation, ")
        print("    what are you more likely to do?")
        print("")
        print("1 | Talk your way out of it.")
        print("2 | Exit while no one is looking.")
        print("3 | Stand up for yourself and fight back.")
        print("")
        try:
            player_choice = int(input())
        except ValueError:
            print("Please choose one of the options...")
            time.sleep(error_delay)
            continue
        if player_choice == 1:
            skills["speech_sc"] += 10
            print("Your speech skill has increased...")
            time.sleep(text_delay)
        elif player_choice == 2:
            skills["stealth_sc"] += 10
            print("Your stealth skill has increased...")
            time.sleep(text_delay)
        elif player_choice == 3:
            skills["combat_sc"] += 10
            print("Your combat skill has increased...")
            time.sleep(text_delay)
        else:
            print("Please choose one of the options...")
            time.sleep(error_delay)

    player_choice = 0
    while player_choice != 1 and player_choice != 2 and player_choice != 3:
        clear()
        welcome_banner()
        print("")
        print("Q3. What does CPU stand for?")
        print("")
        print("1 | Computer Processor Unit.")
        print("2 | Central Processing Unit.")
        print("3 | Central Power Unit.")
        print("")
        try:
            player_choice = int(input())
        except ValueError:
            print("Please choose one of the options...")
            time.sleep(error_delay)
            continue
        if player_choice == 1:
            print("Nope, sorry...")
            time.sleep(text_delay)
        elif player_choice == 2:
            skills["hacking_sc"] += 10
            print("Nice one!")
            print("Your hacking skill has increased!")
            time.sleep(text_delay)
        elif player_choice == 3:
            print("Nope, sorry...")
            time.sleep(text_delay)
        else:
            print("Please choose one of the options...")
            time.sleep(error_delay)

    player_choice = 0
    while player_choice != 1 and player_choice != 2:
        clear()
        welcome_banner()
        print("")
        print("Q4. How's your hand-eye co-ordination?")
        print("")
        print("1 | Pretty great!")
        print("2 | Not so good.")
        print("")
        try:
            player_choice = int(input())
        except ValueError:
            print("Please choose one of the options...")
            time.sleep(error_delay)
            continue
        if player_choice == 1:
            skills["aim_sc"] += 10
            print("Nice!")
            print("Your aim skill has increased!")
            time.sleep(text_delay)
        elif player_choice == 2:
            print("That's too bad.")
            print("Sorry, no free points for you.")
            time.sleep(text_delay)
        else:
            print("Please choose one of the options...")
            time.sleep(error_delay)

    player_choice = 0
    while player_choice != 1 and player_choice != 2 and player_choice != 3:
        clear()
        welcome_banner()
        print("")
        print("And last one...")
        print("")
        #      aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
        print("Q5. If a friend or family member said something ")
        print("    bad about the government, what would you do?")
        print("")
        print("1 | Report them. They should know better.")
        print("2 | Have an open conversation about it. You're ")
        print("    on the fence yourself.")
        print("3 | Probably agree with them.")
        print("")
        try:
            player_choice = int(input())
        except ValueError:
            print("Please choose one of the options...")
            time.sleep(error_delay)
            continue
        if player_choice == 1:
            alleg_dict["reb_sc"] = random.randint(1, 3)
            alleg_dict["gov_sc"] = random.randint(7, 9)
            print("Good for you, thinking for yourself.")
            time.sleep(text_delay)
        elif player_choice == 2:
            alleg_dict["reb_sc"] = random.randint(4, 5)
            alleg_dict["gov_sc"] = random.randint(4, 5)
            print("You might need to pick a side soon.")
            time.sleep(text_delay)
        elif player_choice == 3:
            alleg_dict["reb_sc"] = random.randint(7, 9)
            alleg_dict["gov_sc"] = random.randint(1, 3)
            print("Find the rebels. Take back control.")
            time.sleep(text_delay)
        else:
            print("Please choose one of the options...")
            time.sleep(error_delay)

    clear()
    time.sleep(med_delay)
    time.sleep(short_delay)
    time.sleep(short_delay)
    time.sleep(short_delay)
    time.sleep(short_delay)
    time.sleep(short_delay)
    #      aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    banner_text("That's all the questions for now...")
    time.sleep(text_delay)
    clear()
    empty_banner()
    time.sleep(med_delay)
    time.sleep(short_delay)
    time.sleep(short_delay)
    time.sleep(short_delay)
    time.sleep(short_delay)
    time.sleep(short_delay)
    clear()
    #      aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    banner_text("Welcome...               ")
    time.sleep(med_delay)
    time.sleep(med_delay)
    clear()
    banner_text("Welcome... to Sol City...")
    time.sleep(med_delay)
    time.sleep(med_delay)
    time.sleep(text_delay)

    current_chapter = "intro_appt"  # ought to replace these with a refresh function
    current_page = 0
    already_read_page = False

    clear()


# -------------------------------------------------- Prologue ----------------------------------------------------------

def prologue():
    # prologue variables
    global current_page_game_over_msg
    read_prol_page = False
    prol_med_delay = med_delay
    prol_text_delay = text_delay

    # dictionary just for prologue, simplified from quest dict format
    prologue_dict = {
                            # aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
        0: {"Disp_text":    ["!SHORTPAUSE!",
                             "> The piercing cry of your alarm tears you from \nyour sleep.",
                             "!PAUSE!",
                             "> You check the time.",
                             "!PAUSE!",
                             "> It's 10:53 -- 2 minutes before dawn.",
                             "!PAUSE!"],
            "Disp_choices": ["1 | Get up",
                             "2 | Stay in bed"],
            "Dest": {1: 1, 2: 2},
            "Is_game_over": "N",
            "Game_over_msg": [""]},
                            # aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
        1: {"Disp_text":    ["!SHORTPAUSE!",
                             "> You rise, walk to the window, and step out ",
                             "  onto the short balcony.",
                             "!PAUSE!",
                             "> Far above you, the metal dome over the city",
                             "  groans as the waves crash against it.",
                             "!PAUSE!",
                             "> At the top of the dome is a small opening --",
                             "  getting smaller each day.",
                             "!PAUSE!",
                             "> The waves are always rising, and construction",
                             "  is always ongoing.",
                             "!PAUSE!",
                             "> Some days the waves are high enough to spill ",
                             "  over the edge and onto the streets far below.",
                             "!ENDPAGE!",
                             "!SHORTPAUSE!",
                             "> Some poor bastard will be walking through the ",
                             "  streets, minding their own business...",
                             "!PAUSE!",
                             "> ...and a swimming pool's worth of water will ",
                             "  come crashing down down on them.",
                             "!PAUSE!",
                             "> Sometimes there's fish too.",
                             "!PAUSE!",
                             "> Once there was even a shark.",
                             "!PAUSE!",
                             "> The Mayor was on stage, giving her acceptance ",
                             "  speech for her 10th consecutive re-election..., ",
                             "!PAUSE!",
                             "> ...and luckily, from the perspective of almost ",
                             "  everyone involved,",
                             "!PAUSE!",
                             "> ...the shark completely missed her",
                             "!PAUSE!",
                             "> ...and landed on one of her assistants instead.",
                             "!PAUSE!",
                             "> Anyway, we're getting side tracked.",
                             "!ENDPAGE!",
                             "!SHORTPAUSE!",
                             "> You stare up at the narrow opening...",
                             "!PAUSE!",
                             "> ...and you wait",
                             "!PAUSE!",
                             "> ...and wait.",
                             "!PAUSE!",
                             "> All around you, on other balconies, on other ",
                             "  high rises, people are waiting...",
                             "!PAUSE!",
                             "> All of you waiting for the morning SUN...",
                             "!PAUSE!",
                             "> ...and finally",
                             "!PAUSE!",
                             "> ...there it is.",
                             "!ENDPAGE!",
                             "!SHORTPAUSE!",
                            # aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
                             "> A sliver of light appears far above you.",
                             "!PAUSE!",
                             "> You shield your eyes and feel the warmth on",
                             "  your hand.",
                             "!PAUSE!",
                             "> You check the time again.",
                             "!PAUSE!",
                             "> It's late...",
                             "!PAUSE!",
                             "> The *dawn* is late.",
                             "!PAUSE!",
                             "> Perhaps this it the new time?",
                             "!PAUSE!",
                             "> Yes.",
                             "!ENDPAGE!",
                             "!SHORTPAUSE!",
                             "> The opening must have shrunk since you last ",
                             "  set your alarm.",
                             "!PAUSE!",
                             "> And as the opening closes up... the sun must ",
                             "  climb higher in the the sky to appear through ",
                             "  it.",
                             "!PAUSE!",
                             "> And one day soon...",
                             "!PAUSE!",
                             "> ...not just yet, but it won't be too long now",
                             "!PAUSE!",
                             "> ...the waves will have risen up so high",
                             "!PAUSE!",
                             "> ...that the dome will have to be closed off",
                             "  completely",
                             "!PAUSE!",
                             "> ...like all the other domed-cities before it",
                             "!PAUSE!",
                             "> ...and you will never see the sun again.",
                             "!PAUSE!"],
            "Disp_choices": ["1 | Go back inside",
                             "2 | Wait a little longer"],
            "Dest": {1: 7, 2: 3},
            "Is_game_over": "N",
            "Game_over_msg": [""]},
        2: {"Disp_text":    ["!SHORTPAUSE!",
                             "> You snooze your alarm and fall back to sleep \nfor 10 minutes.",
                             "!PAUSE!",
                             "> When you wake again, the dawn light has moved \n on to another part of the city.",
                             "!PAUSE!",
                             "> You've missed out on the best part of your \nday.",
                             "!PAUSE!",
                             "> You'd better get up and get ready for work.",
                             "!PAUSE!"],
            "Disp_choices": ["1 | Get up, you lazy fuck",
                             "2 | Continue to stay in bed"],
            "Dest": {1: 7, 2: 4},
            "Is_game_over": "N",
            "Game_over_msg": [""]},
                            # aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
        3: {"Disp_text":    ["!SHORTPAUSE!",
                             "> As you stand there with sun warmin your face, \n  you hear a grunting sound.",
                             "!PAUSE!",
                             "> You look up...",
                             "!PAUSE!",
                             "> It's your neighbour from the floor above you.",
                             "!PAUSE!",
                             "> They're stretched over their balcony. You can \n  just see the ends of their fingers.",
                             "!PAUSE!",
                             "> They're desparately trying to reach the golden \n  sun but they're just short.",
                             "!PAUSE!",
                             "> It must be the latest lot of construction.",
                             "!PAUSE!",
                             "> The hole's gotten smaller, and your neighbour \n  has been cut off.",
                             "!PAUSE!",
                             "> Bummer.",
                             "!ENDPAGE!",
                             "!SHORTPAUSE!",
                             "> But they keep on reaching...",
                             "!PAUSE!",
                             "> ...rocking back and forwards",
                             "!PAUSE!",
                             "> ...desparately trying to reach, if just with \n  a finger.",
                             "!PAUSE!",
                             "> There's a squeal as your neighbour lunges \n  forward and finally touches the light...",
                             "!PAUSE!",
                             "> ...which is followed by a sharp gasp as they \n  tip over the edge",
                             "!PAUSE!",
                             "> ...and plummet down to the street, 112 floors \n  below.",
                             "!PAUSE!",
                             "> A few people on the opposite building look \n  over.",
                             "!PAUSE!",
                             "> But most dont.",
                             "!ENDPAGE!",
                             "!SHORTPAUSE!",
                             "> It's not the first time it's happened.",
                             "!PAUSE!",
                             "> People just can't stand the dark.",
                             "!PAUSE!",
                             "> The floors above you are nearly all vacant, \n  having been in shadow for a while.",
                             "!PAUSE!",
                             "> For some reason, you cannot remember your \n  neighbour's name.",
                             "!PAUSE!",
                             "> Oh, well. It's not worth worrying about now.",
                             "!PAUSE!",
                             "> Just be sure to avoid the mess on the way \n  out.",
                             "!PAUSE!"],
            "Disp_choices": ["1 | Go back inside"],
            "Dest": {1: 7},
            "Is_game_over": "N",
            "Game_over_msg": [""]},
                            # aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
        4: {"Disp_text":    ["!SHORTPAUSE!",
                             "> You know you really *should* get up.",
                             "!PAUSE!",
                             "> You've got things to do. Places to be.",
                             "!PAUSE!",
                             "> Go out and explore the world!",
                             "!PAUSE!",
                             "> Also, your bank balance is fucked.",
                             "!PAUSE!",
                             "> So some of that exploring should involve \n  going to work.",
                             "!PAUSE!",
                             "> But you don't have to listen to me.",
                             "!PAUSE!",
                             "> You can do anything you want.",
                             "!PAUSE!",
                             "> Almost anything, at least...",
                             "!PAUSE!",
                             "> Anything I've thought of...",
                             "!ENDPAGE!",
                             "!SHORTPAUSE!",
                             "> You don't even have to play this game if you \n  don't want to.",
                             "!PAUSE!",
                             "> You can close it down now and go eat a bagel \n  for all I care.",
                             "!PAUSE!",
                             "> ...",
                             "!PAUSE!",
                             "> ...",
                             "!PAUSE!",
                             "> Well?",
                             "!PAUSE!",
                             "> You *are* staying then?",
                             "!PAUSE!",
                             "> Okay, in that case, I'm going to slim this \n down to 2 options.",
                             "!PAUSE!",
                             "> You can either: get your arse up. Get out of \n  this comfy, comfy bed.",
                             "!PAUSE!",
                             "> Embrace life! Go buy a toaster and so on!",
                             "!ENDPAGE!",
                             "!SHORTPAUSE!",
                             "> Or: you can fully commit to your new life as \n  bed-dwelling insectoid.",
                             "!PAUSE!",
                             "> Become one with the duvet.",
                             "!PAUSE!",
                             "> ...wither away as all sustenance leaves your \n  broken body",
                             "!PAUSE!",
                             "> ...and you become figuratively",
                             "!PAUSE!",
                             "> ...and literally",
                             "!PAUSE!",
                             "> ...a potato.",
                             "!PAUSE!",
                             "> What's it gonna be?",
                             "!PAUSE!"],
            #                 aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
            "Disp_choices": ["1 | Okay, fine. I want the toaster and shit.",
                             "2 | I am Spuds-MacKenzie! FREEEEEDDDDOOOOMMMM!!!"],
            "Dest": {1: 7, 2: 5},
            "Is_game_over": "N",
            "Game_over_msg": [""]},
        5: {"Disp_text":    [],
            "Disp_choices": [],
            "Dest": {},
            "Is_game_over": "Y",
            "Game_over_msg": ["You were a brave potato indeed but that is all.",
                              "Hopefully, somone can make something useful out\n  of you now.",
                              "How about some tasty Soilent Green?"]}
    }

    # Play prologue
    skip_choice_made = False  # initialize
    skip_prologue = False  # initialize
    while not skip_choice_made:
        clear()
        banner_text("Skip prologue? Y/N")
        print("")
        skip_choice = "n"  # initialize
        skip_yes = ["y", "yes", "yup", "yeah", "Y", "Yes", "Yup", "Yeah", "YES", "YUP", "YEAH"]
        skip_no = ["n", "no", "nope", "N", "No", "Nope", "N", "NO", "NOPE"]
        try:
            skip_choice = str(input())
        except ValueError:
            print("Please choose one of the options...")  # no drug/drunk filters
            time.sleep(error_delay)
            clear()
        if skip_choice in skip_yes:
            skip_prologue = True
            skip_choice_made = True
        elif skip_choice in skip_no:
            skip_prologue = False
            skip_choice_made = True
        else:
            print("Please choose one of the options...")  # no drug/drunk filters
            time.sleep(error_delay)
            clear()
    if not skip_prologue:
        prol_pos = 0                                                       # initialize
        prol_cur_disp_text = prologue_dict[prol_pos]["Disp_text"]          # initialize
        prol_cur_disp_choice = prologue_dict[prol_pos]["Disp_choices"]     # initialize
        prol_cur_dest_dict = prologue_dict[prol_pos]["Dest"]               # initialize
        prol_cur_is_game_over = prologue_dict[prol_pos]["Is_game_over"]    # initialize
        prol_cur_game_over_msg = prologue_dict[prol_pos]["Game_over_msg"]  # initialize
        while not perks_and_bools["game_over"]:
            checked_input = False
            while not checked_input:
                # game over code, I think just the one potato game over for the prologue
                if prol_cur_is_game_over == "Y":
                    perks_and_bools["game_over"] = True
                    print("its game over")  # for testing
                    time.sleep(5)  # for testing
                    break
                # Print display text
                clear()
                print("")
                print("________________________________________________")
                print("")
                if read_prol_page:
                    prol_med_delay = 0
                    prol_text_delay = 0
                for disp_text in prol_cur_disp_text:
                    if disp_text == "!PAUSE!":
                        time.sleep(prol_text_delay)
                    elif disp_text == "!SHORTPAUSE!":
                        time.sleep(prol_med_delay)
                    elif disp_text == "!ENDPAGE!":
                        time.sleep(prol_text_delay)
                        time.sleep(prol_med_delay)
                        clear()
                        print("")
                        print("________________________________________________")
                        print("")
                    else:
                        print(disp_text)
                print("")
                prol_med_delay = med_delay
                prol_text_delay = text_delay
                read_prol_page = True
                # Print display options
                for disp_choice in prol_cur_disp_choice:
                    print(disp_choice)
                print("")
                try:
                    prol_choice = int(input())
                except ValueError:
                    print("Please choose one of the options...")  # no drug/drunk filters
                    time.sleep(error_delay)
                    clear()
                    continue
                if prol_choice in prol_cur_dest_dict.keys():
                    prol_pos = prol_cur_dest_dict[prol_choice]
                    checked_input = True
                else:
                    print("Please choose one of the options...")  # no drug/drunk filters
                    time.sleep(error_delay)
                    clear()
            # After selecting accepted option, loop back and setup for next turn
            prol_cur_disp_text = prologue_dict[prol_pos]["Disp_text"]          # initialize
            prol_cur_disp_choice = prologue_dict[prol_pos]["Disp_choices"]     # initialize
            prol_cur_dest_dict = prologue_dict[prol_pos]["Dest"]               # initialize
            prol_cur_is_game_over = prologue_dict[prol_pos]["Is_game_over"]    # initialize
            prol_cur_game_over_msg = prologue_dict[prol_pos]["Game_over_msg"]  # initialize
            read_prol_page = False

        current_page_game_over_msg = prol_cur_game_over_msg


# ------------------------------------------------- Play music ---------------------------------------------------------
# controller = webbrowser.get()
# controller.open("https://youtu.be/J1xAEWXT7_M?t=1")

# ----------------------------------------------- Test minigames -------------------------------------------------------
# uncomment to test minigames
# roulette()
# slot_machine()

# ------------------------------------------------- Play game ----------------------------------------------------------
# NOTE: when implementing save/load, may need an extra loop or what IDK, because prologue can game over

# set shops for testing
ARC_menu_avail = True
player_invent_avail = True
bmarket_avail = True

while not perks_and_bools["game_over"]:
    welcome_screen()
    prologue()

    while not perks_and_bools["game_over"]:
        clear()
        ow_go_random_event()  # need a counter or something for min turns between events
        ow_option_builder()
        ow_print_exec()  # should contain its own loop to catch bad inputs
        # print("loop in play game?")  # for testing
        # time.sleep(5)  # for testing
        # update counters (will also need this buried in quest functions where relevant, so counters still update)

    # Game over screen
    clear()
    game_over_choice = 0  # initialize
    print("GAME OVER:")  # game over message needs to be msg not string! as long messages!
    time.sleep(med_delay)
    for msg in current_page_game_over_msg:
        print(msg)
    time.sleep(text_delay)
    print("")
    print("1 | Play again?")
    try:
        game_over_choice = int(input())
    except ValueError:
        clear()
        print("Thank you for playing. Good bye :)")
    if game_over_choice == 1:
        perks_and_bools["game_over"] = False
    else:
        clear()
        print("Thank you for playing. Good bye :)")

# ------------------------------------------------ To do list ----------------------------------------------------------

# Implement saves - think I want to go for a rogue-like setup.
# > You will start on screen just before welcome with option pick a new game or load game.
# > Attempt to load games in slots 1, 2, and 3 first to determine if save is allowed.
# > Save/load will be managed with pickle module and need to stick to a specific save file.
# > If game_over occures then lose the save/overwrite with initial values and save.
# > Pickle save loads works with a variable, so will probably need to store entire save as dictionary and then write
# > When starting new game, allow new game without saving or new game but locked into a save file.
# > Whether you start new game or load, need to lock player into a save slot and the start with a separate variable
# > This is to stop them cheating and saving on multiple slots, incase they then die.

# Implement minigame logic to allow for following minigames
# Random combat
# Scripted combat (?)
# Hacking
# Generally need to make use of skills
# Have training to be able to increase skills
# > Increase aim at shooting range (pay money for turn)
# > Increase hacking with ash quest
# > Increase combat with martial arts training
# > Secret way to max out combat by hacking some difficult thing - "I know kung fu"
# >> Is this different to predator module?

# Implement merchants

# Add notification system for quest prompts. More like a "pager". You can't text back.

# Check seeds for random ints, seem to get a lot of repeated answers. May need random seed each time?

# When implementing predator module, and activating through quest etc, have cool animation and then choice to say
# "I know kung fu" or let the moment pass

# Need a better game over screen
# game over needs to reset all variables to initial values