import random
from typing import List
import pandas as pd
import matplotlib.pyplot as plt

from typing import TypeVar, Tuple

defender={'t': 4, 'sv': 3}

def randomDice(dice: int):
    return random.randint(1, dice)

def roll(num_rolls: int, reroll: bool=False) -> List:
    rolls = []
    for i in range(0,num_rolls):
        _i = randomDice(6)
        if _i == 1 and reroll:
            _i = randomDice(6)
        rolls.append(_i)
    return rolls

def roll2Hit(bs: int, attacks: int, reroll: bool=False) -> List:
    rolls = roll(attacks, reroll)
    return sum(bs <= dice for dice in rolls)

def roll2Wound(hits: int,
               st: int,
               t:int,
               mortals: int = 7, 
               reroll: bool=False) -> Tuple[int, int]:
    rolls = roll(hits, reroll)
    required = 0
    if st > t*2:
        required = 2
    elif st > t:
        required = 3
    elif st == t:
        required = 4
    elif st < t:
        required = 5
    elif st*2 < t:
        required = 6
    else:
        required = 6
    result = sum(required <= dice for dice in rolls)
    mortal_wounds =  sum(mortals <= dice for dice in rolls)
    return result, mortal_wounds

def roll2Save(wounds: int, ap: int, sv: int):
    rolls = roll(wounds)
    mod = sv - ap
    return sum(mod <= dice for dice in rolls)

def roll2Damage(wounds: int,
                saved: int,
                mortals: int,
                d: str):
    # if 'D' in d:
    #     dice = int(d.split('D')[1])
    #     num = int(d.split('D')[0])
    #     damage = num * randomDice(dice)
    # else:
    #     damage = int(d)
    damage = parseRoll(str(d))
    return (mortals * damage) + (wounds - saved) * damage

def stats(turns: list, columns: list):
    df = pd.DataFrame(turns, columns=columns)
    df['Total'] = df.sum(axis=1)
    print(df.shape)
    print(df.head())
    print(df.describe())
    hist = df.hist(bins=5)
    plt.show()

def plot(bars: list, columns: list=['Total']):
    df = pd.DataFrame(bars, columns=columns)
    df.plot(kind='line')
    plt.show()

def plot_dict(bars: dict):
    df = pd.DataFrame.from_dict(bars)
    df.plot(kind='line')
    plt.show()

def parseRoll(d: str) -> int:
    if 'D' in d:
        dice = int(d.split('D')[1])
        num = int(d.split('D')[0])
        damage = num * randomDice(dice)
    else:
        damage = int(d)
    return damage


def compute_damage(troop: dict, reroll_hits: bool, reroll_wounds: bool):
    num = int(str(troop['number']).split(',')[0])
    damage = 0
    if 'ap' not in troop:
        return troop['damage']
    for i in range(1,num):        
        hits = roll2Hit(troop['bs'], parseRoll(str(troop['attacks'])), reroll_hits)
        wounds, mortals = roll2Wound(hits, 
                                     troop['st'],
                                     defender['t'],
                                     reroll=reroll_wounds)
        savedWounds = roll2Save(wounds,
                                troop['ap'],
                                defender['sv'])
        damage += roll2Damage(wounds, savedWounds, mortals, troop['damage'])
    return damage

if __name__ == "__main__":
    result_bolter_1 = []
    result_bolter_2 = []
    result_bolter_3 = []
    result_blightlauncher_1 = []
    result_blightlauncher_2 = []
    # plague marines with bolter
    bs = 3
    st = 4
    attacks = 2
    ap = 0
    damage_bolter = '1'
    # plague marines with blight launcher
    st_blight = 6
    attacks_blight = 2
    ap_blight = -2
    damage_blight = '1D3'
    # space marines defends
    t = 4
    sv = 3
    # bolter 1
    for i in range(1000):
        hits_bolter_1 = roll2Hit(bs, attacks)
        hits_bolter_2 = roll2Hit(bs, attacks)
        hits_bolter_3 = roll2Hit(bs, attacks)
        hits_blightlauncher_1 = roll2Hit(bs, attacks_blight)
        hits_blightlauncher_2 = roll2Hit(bs, attacks_blight)
        # print(hits)
        wounds_bolter_1, _ = roll2Wound(hits_bolter_1, st, t)
        wounds_bolter_2, _ = roll2Wound(hits_bolter_2, st, t)
        wounds_bolter_3, _ = roll2Wound(hits_bolter_3, st, t)
        wounds_blightlauncher_1, _ = roll2Wound(hits_blightlauncher_1, st_blight, t)
        wounds_blightlauncher_2, _ = roll2Wound(hits_blightlauncher_2, st_blight, t)
        # print(wounds)
        savedWounds_bolter_1 = roll2Save(wounds_bolter_1, ap, sv)
        savedWounds_bolter_2 = roll2Save(wounds_bolter_2, ap, sv)
        savedWounds_bolter_3 = roll2Save(wounds_bolter_3, ap, sv)
        savedWounds_blightlauncher_1 = roll2Save(wounds_blightlauncher_1, ap_blight, sv)
        savedWounds_blightlauncher_2 = roll2Save(wounds_blightlauncher_2, ap_blight, sv)
        # print(savedWounds)
        result_bolter_1.append(roll2Damage(wounds_bolter_1, savedWounds_bolter_1, damage_bolter))
        result_bolter_2.append(roll2Damage(wounds_bolter_2, savedWounds_bolter_2, damage_bolter))
        result_bolter_3.append(roll2Damage(wounds_bolter_3, savedWounds_bolter_3, damage_bolter))
        result_blightlauncher_1.append(roll2Damage(wounds_blightlauncher_1, savedWounds_blightlauncher_1, damage_blight))
        result_blightlauncher_2.append(roll2Damage(wounds_blightlauncher_2, savedWounds_blightlauncher_2, damage_blight))

    result = list(zip(result_bolter_1, result_bolter_2, result_bolter_3, result_blightlauncher_1, result_blightlauncher_2))
    stats(result, columns=['Bolter_1', 'Bolter_2', 'Bolter_3', 'Blightlauncher_1', 'Blightlauncher_2'])
   