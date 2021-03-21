from __future__ import annotations
from typing import TypeVar, Tuple, Type
from copy import deepcopy
import random
import yaml
from .rollsimulator import compute_damage, plot, plot_dict
from .genetic_algorithm import GeneticAlgorithm
import pandas as pd

T = TypeVar('T', bound='Armylist')

list_troops = {}
detachment = {}
weapons = {}
max_points = 0

class Problem1():
    def __init__(self, filename: str, filename2: str):
        # instantiate
        with open(filename, 'r') as stream:
            self.codex = yaml.safe_load(stream)
        with open(filename2, 'r') as stream:
            self.list_weapons = yaml.safe_load(stream)
        
    
    def list_troops(self, problem: str) -> dict:
        # return ConfigFile(config).problem
        roles = self.codex['roles']
        list_troops = {role:[] for role in roles}
        weapons = {k: v for k,v in self.list_weapons['weapons'].items()}
        for troop in self.codex['unit']:
            list_troops[troop['role']].append(troop)
        self.detachments = {detachment['type']:detachment for detachment in self.codex['detachments']}
        if problem not in self.detachments:
            print("Not supported type of problem. Aborting.")
        self.create_problem("patrol")
        return list_troops, weapons
    
    def create_problem(self, problem: str):
        self.type_problem = problem
        self.mandatory = self.detachments[self.type_problem]['mandatory'][0]
        optional = self.detachments[self.type_problem]['optional'][0]
        self.mandatory.update(optional)
        # troops = [self.troops[role] for role in mandatory]

class Armylist():
    # troops are stored as dicts in different positions of the array:
    # hq pos 0
    # troops pos 1
    # elites pos 2
    # heavy pos 3
    # fast pos 4
    def __init__(self):
        self.troops = []
        self.abilities = []
        self.random_instance()
        self.value = self.compute_value()
        # print(self.value)

    def isValid(self, troops: list, must: dict) -> bool:
        # verify hqs
        # print(troops)
        # print('HQ:')
        # print(troops[0])
        # print(must['hq'])
        if not self.checkTroopSize(len(troops[0]), must['hq']):
            return False
        # verify troops
        # print('troops:')
        # print(troops[1])
        # print(must['troops'])
        if not self.checkTroopSize(len(troops[1]), must['troops']):
            return False
        # verify elites
        # print('elites:')
        # print(troops[2])
        # print(must['elites'])
        if not self.checkTroopSize(len(troops[2]), must['elites']):
            return False
        # verify heavy
        # print('heavy:')
        # print(troops[3])
        # print(must['heavysupport'])
        if not self.checkTroopSize(len(troops[3]), must['heavysupport']):
            return False
        # verify fastattack
        # print('fastattack:')
        # print(troops[4])
        # print(must['fastattack'])
        if not self.checkTroopSize(len(troops[4]), must['fastattack']):
            return False
        return True
    
    def checkTroopSize(self, unit: int, mandatory: str)-> bool:
        lower_limit = int(mandatory.split(',')[0])
        higher_limit = int(mandatory.split(',')[1])
        # print(f"lower_limit: {lower_limit} < {unit}")
        # print(f"higher_limit: {higher_limit} > {unit}")
        if unit < lower_limit or unit > higher_limit:
            return False
        return True
    
    def fitness(self) -> float:
        return self.value

    def compute_value(self) -> float:
        if not self.isValid(self.troops, detachment):
            return 0.0
        total_damage = 0.0
        total_cost = 0
        # print(self.troops)
        reroll_hits = False
        reroll_wounds = False
        # verify abilities
        for units in self.troops:
            for troop in units: 
                if 'plague' in troop:
                    reroll_wounds = True
                if 'abilities' in troop:
                    if 'reroll_1_hit' in troop['abilities']:
                        reroll_hits = True
        for role in self.troops:
            # total_damage += self.troops[troop]
            _damage = []
            for troop in role:
                number_units = int(str(troop['number']).split(',')[0])
                for i in range(100):
                    _damage.append(compute_damage(troop,
                                                  reroll_hits,
                                                  reroll_wounds))
                df = pd.DataFrame(_damage, columns=['Values'])
                total_damage += df['Values'].mean()
                total_cost += troop['costs'] * number_units
        # print(f"Total cost: {total_cost}")
        # print(f"Total damage: {total_damage}")
        if total_cost >= max_points:
            return 0.0
        return total_damage

    def random_instance(self) -> float:
        # choosing HQ:
        self.appendTroops('hq', detachment['hq'], index=0)
        # choosing troops:
        self.appendTroops('troops', detachment['troops'], index=1)
        # choosing elites:
        self.appendTroops('elites', detachment['elites'], index=2)
        # choosing heavy:
        self.appendTroops('heavysupport', detachment['heavysupport'], index=3)
        # choosing fast:
        self.appendTroops('fastattack', detachment['fastattack'], index=4)

    def appendTroops(self, role: str, detachments: dict, index: int):
        lower_limit = int(detachments.split(',')[0])
        higher_limit = int(detachments.split(',')[1])
        troop = []
        for i in range(lower_limit, higher_limit):
            _selected = random.randint(0,len(list_troops[role]))
            if _selected < len(list_troops[role]):
                _unit = deepcopy(list_troops[role][_selected])
                if 'weapons' in _unit:
                    _weapon = weapons[_unit['weapons'][random.randint(0,len(_unit['weapons'])-1)]]
                    for k,v in _weapon.items():
                        _unit[k] = v
                troop.append(_unit)
        self.troops.insert(index, troop)

    def crossover(self: T, other: T) -> Tuple[T,T]:
        child1: Armylist = deepcopy(self)
        child2: Armylist = deepcopy(other)
        selected_genes_1 = random.randint(0,4)
        selected_genes_2 = random.randint(0,4)
        child1.troops[selected_genes_1] = other.troops[selected_genes_1]
        child2.troops[selected_genes_2] = self.troops[selected_genes_2]
        return child1, child2
        
    def mutate(self) -> None:
        roles = ['hq', 'troops', 'elites', 'fastattack', 'heavysupport']
        _i = random.randint(0, len(roles)-1)
        _delete = random.randint(0,1)
        if _delete:
            self.troops.pop(_i)
        self.appendTroops(roles[_i], detachment[roles[_i]], index=_i)

    def __str__(self) -> str:
        str_converted = f"""HQ: {self.troops[0]}
        troops: {self.troops[1]}
        elites: {self.troops[2]}
        heavy: {self.troops[3]}
        fast: {self.troops[4]}
        Fitness: {self.fitness()}"""
        return str_converted


if __name__ == "__main__":
    p1 = Problem1("SistemasEq/config.yaml", "SistemasEq/weapons.yaml")
    list_troops, weapons = p1.list_troops("patrol")
    detachment = p1.mandatory
    max_points = 1000
    # print(weapons)
    avg_result = []
    average_window = {}
    for i in range(10):
        max_generations = 20
        initial_population: List[Armylist] = [Armylist() for _ in range(100)]
        ga: GeneticAlgorithm[Armylist] = GeneticAlgorithm(initial_population=initial_population,
                                                        threshold=40.0,
                                                        max_generations = max_generations,
                                                        mutation_chance = 0.25,
                                                        crossover_chance = 0.8)
        result, avg_increase = ga.run()
        avg_result.append(result.fitness())
        print(result.fitness())
        if len(avg_increase) < max_generations:
            print(len(avg_increase))
            _last = avg_increase[-1]
            for i in range(len(avg_increase), max_generations):
                avg_increase.append(_last)
        average_window[f"Count_{i}"] = avg_increase
    plot(avg_result, ['Total'])
    plot_dict(average_window)
    print(result)