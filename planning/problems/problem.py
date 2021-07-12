from subprocess import call

class Problem():
    def __init__(self, name, problem, offender, defender, walls):
        self.name = name
        self.problem = problem
        self.attacking = offender
        self.defending = defender
        self.walls = walls

    def print(self, path: str):
        with open(path, 'w') as f:
            f.write(f"(define (problem pb1) (:domain {self.name})\n")
            f.write("(:objects\n")
            self.pos = []
            self.troops = []
            self.objectives = []
            self.printObjects(f)
            f.write(")\n")
            # Start printing initial state
            f.write("(:init \n")
            f.write(self.initialState())
            f.write(")\n\n")
            f.write("(:goal \n")
            f.write(self.printgoal())
            f.write(")\n)")

    def printObjects(self, f):
        for i in range(1, self.problem.max_x):
            for j in range(1, self.problem.max_y):
                self.pos.append(f"{i}-{j}")
                f.write(f"{i}-{j} ")
            f.write("\n")
        f.write("- location\n")
        for t in self.problem.troops:
            self.troops.append(t)
            f.write(f"{t['name']}\n")
        f.write("- troop\n")
        i = 1
        for o in self.problem.objectives:
            n = f"o-{i}"
            self.objectives.append({'name': n, 'position': o})
            f.write(f'{n}\n')
            i += 1
        f.write("- objective\n")


    def connected(self, pos1, pos2):
        pos1_x = int(pos1.split('-')[0])
        pos1_y = int(pos1.split('-')[1])

        pos2_x = int(pos2.split('-')[0])
        pos2_y = int(pos2.split('-')[1])

        if (pos1_x - pos2_x) == 1 and (pos1_y - pos2_y) == 1:
            return True
        elif pos1_x == pos2_x and abs(pos1_y - pos2_y) == 1:
            return True
        elif pos1_y == pos2_y and abs(pos1_x - pos2_x) == 1:
            return True
        else:
            return False

    def initialState(self):
        strInitial = ""
        # troop_at
        for t in self.problem.troops:
            strInitial += f" (troop_at {t['name']} {t['position']})\n"
            if t['army'] == self.attacking:
                strInitial += f" (can_move {t['name']}) \n"
                if t['psyker'] is True:
                    strInitial += f" (psyker {t['name']})\n"
                if t['melee'] is True:
                    strInitial += f" (melee_weapon {t['name']})\n"
                if t['ranged'] is True:
                    strInitial += f" (ranged_weapon {t['name']})\n"
            else:
                strInitial += f" (healthy {t['name']})\n"

        # objective_at
        for o in self.objectives:
            print(o)
            strInitial += f" (objective_at {o['name']} {o['position'].replace(',', '-')})\n"

        # connected
        for position1 in self.pos:
            if position1 in self.walls:
                continue
            for position2 in self.pos:
                if position1 == position2 or position2 in self.walls:
                    continue
                if (self.connected(position1, position2)):
                    strInitial += f" (connected {position1} {position2})"
            strInitial += "\n"

        # in range
        for shooter in self.problem.troops:
            if shooter['army'] == self.attacking:
                for target in self.problem.troops:
                    if target['army'] == self.defending:
                        strInitial += f"(in_range {shooter['name']} {target['name']})\n"

        return strInitial

    def printgoal(self):
        strGoal = "(and\n"
        # or goal of holds
        for t in self.problem.troops:
            if t['army'] == self.attacking:
                strGoal += "\t(or\n"
                for o in self.objectives:
                    strGoal += f"\t\t(conquer {t['name']} {o['name']})\n"
                strGoal += "\t)\n"
        # and kills
        for t in self.problem.troops:
            if t['army'] == self.defending:
                strGoal += f"\t(killed {t['name']})\n"

        return strGoal + ")\n"

    def solve(self, path):
        code = call(["python",
                     path,
                     "--alias",
                     "lama-first",
                     "planning/problems/domain_template.pddl",
                     "planning/problems/problem_1.pddl"])
        print(code)
