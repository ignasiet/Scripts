from .main import Problem1, Armylist
from typing import Type
import operator

list_troops = {}
detachment = {}
weapons = {}
max_points = 0

def hillclimbing(seed: Type[Armylist], descendants: int):
    children = [seed.mutate for _ in range(descendants)]
    children.sort(key=operator.attrgetter('fitness'))
    for child in children:
        print(children.fitness)
    return children[0]


if __name__ == "__main__":
    p1 = Problem1("SistemasEq/config.yaml", "SistemasEq/weapons.yaml")
    list_troops, weapons = p1.list_troops("patrol")
    detachment = p1.mandatory
    max_points = 1000
    # print(weapons)
    avg_result = []
    average_window = {}
    initial_seed: Armylist = Armylist()
    hillclimbing(initial_seed)
