import random
from typing import List
import pandas as pd
import matplotlib.pyplot as plt

def randomDice(dice: int):
    return random.randint(1, dice)

def roll(num_rolls: int) -> List:
    rolls = []
    for i in range(0,num_rolls):
        rolls.append(randomDice(6))
    return rolls

def roll2Hit(bs: int, attacks: int) -> List:
    rolls = roll(attacks)
    return sum(bs <= dice for dice in rolls)

def roll2Wound(hits: int, st: int, t:int):
    rolls = roll(hits)
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
    return sum(required <= dice for dice in rolls)

def roll2Save(wounds: int, ap: int, sv: int):
    rolls = roll(wounds)
    mod = sv - ap
    return sum(mod <= dice for dice in rolls)

def roll2Damage(wounds: int, saved: int, d: str):
    if 'D' in d:
        dice = int(d.split('D')[1])
        num = int(d.split('D')[0])
        damage = num * randomDice(dice)
    else:
        damage = int(d)
    return (wounds - saved) * damage

def stats(turns: list, columns: list):
    df = pd.DataFrame(turns, columns=columns)
    df['Total'] = df.sum(axis=1)
    print(df.shape)
    print(df.head())
    print(df.describe())
    hist = df.hist(bins=5)
    plt.show()


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
        wounds_bolter_1 = roll2Wound(hits_bolter_1, st, t)
        wounds_bolter_2 = roll2Wound(hits_bolter_2, st, t)
        wounds_bolter_3 = roll2Wound(hits_bolter_3, st, t)
        wounds_blightlauncher_1 = roll2Wound(hits_blightlauncher_1, st_blight, t)
        wounds_blightlauncher_2 = roll2Wound(hits_blightlauncher_2, st_blight, t)
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
   