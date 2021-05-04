
class Plan():
    def __init__(self):
        self.phases = ['Movement',
                       'Psychic',
                       'Shooting Phase',
                       'Combat Phase']
        self.allowed_orders = {}
        # 0 phase - move
        self.allowed_orders[0] = ['move', 'hold']
        # 1 phase - psyker
        self.allowed_orders[1] = ['smite']
        # 2 phase - shoot
        self.allowed_orders[2] = ['shot']
        # 3 phase - combat
        self.allowed_orders[3] = ['kill']
        self.actions = {phase: [] for phase in self.phases}
        with open('sas_plan', 'r') as f:
            for line in f:
                x = line.replace('(', '')
                x = x.replace(')', '')
                x = x.replace('\n', '')
                order = x.split(' ')
                for i in range(0, 4):
                    if order[0] in self.allowed_orders[i]:
                        self.actions[self.phases[i]].append(order)

    def readPlan(self, current_phase, counter):
        return self.actions[self.phases[current_phase]][counter]
