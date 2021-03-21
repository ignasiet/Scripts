from .solver import Solver
import yaml

class Problem1():
   def __init__(self, filename: str, problem: str):
      # instantiate
      with open(filename, 'r') as stream:
         codex = yaml.safe_load(stream)
      # return ConfigFile(config).problem
      roles = codex['roles']
      self.troops = {role:[] for role in roles}
      for troop in codex['unit']:
         self.troops[troop['role']].append(troop)
      self.detachments = {detachment['type']:detachment for detachment in codex['detachments']}
      if problem not in self.detachments:
         print("Not supported type of problem. Aborting.")
      self.create_problem("patrol")


   def create_problem(self, problem: str):
         # costs = ([1,0,6,10,4],[0,3,10,8,0],[2,4,6,11,3],[0,0,5,8,4],[1,4,6,8,3])
         self.solver = Solver("maximize")
         self.type_problem = problem
         mandatory = self.detachments[self.type_problem]['mandatory'][0]
         optional = self.detachments[self.type_problem]['optional'][0]
         mandatory.update(optional)
         # troops = [self.troops[role] for role in mandatory]
         print(mandatory)
         # i = 0
         # j = 0
         obj_function = []
         pointsRestriction = []
         original_damage = {}
         self.readMinMax(mandatory.keys())
         for role in mandatory:
            units_role = []
            num = mandatory[role].split(',')
            print(num)
            if len(num) == 1:
               num_min = int(num[0])
               num_max = int(num[0])
            else:
               num_min = int(num[0])
               num_max = int(num[1])
            for troop in self.troops[role]:
               # print(troop)
               var_name = role + "_" + troop['name']
               # print(var_name)
               units_troop = str(troop['number']).split(',')
               self.solver.addVariables(var_name, 0, min(num_max, int(units_troop[0])))
               print(f'0 <= {var_name} <= {min(num_max, int(units_troop[0]))}')
               obj_function.append({var_name: self.scaleValues(float(troop['damage']))})
               original_damage[var_name] = float(troop['damage'])
               pointsRestriction.append({var_name: round(float(troop['costs']))})
               units_role.append({var_name: 1})
            self.solver.addRestrictions(units_role, operator='leq', total=num_max)
            self.solver.addRestrictions(units_role, operator='geq', total=num_min)

               # if len(units_troop) == 1:
               #    self.solver.addVariables(var_name, 0, min(num_max, int(units_troop[0])))
               #    print(f'0 <= {var_name} <= {min(num_max, int(units_troop[0]))}')
               #    obj_function.append({var_name: self.scaleValues(float(troop['damage']))})
               #    pointsRestriction.append({var_name: round(float(troop['costs']))})
               # else:
               #    for i in range(num_max):
               #       sub_name = var_name + "_" + str(i)
               #       self.solver.addVariables(sub_name,0, int(units_troop[1]))
               #       print(f'0 <= {sub_name} <= {int(units_troop[1])}')
               #       obj_function.append({sub_name: self.scaleValues(float(troop['damage']))})
               #       pointsRestriction.append({sub_name: round(float(troop['costs']))})

         # print(obj_function)
         
         self.solver.setObjectiveFunction(obj_function)
         self.solver.addRestrictions(pointsRestriction, operator='leq', total=1000)
         selected_troops = self.solver.solve()
         points = {k:v for elem in pointsRestriction for k,v in elem.items()}
         cost = 0
         dmg = 0.0
         for k,v in selected_troops.items():
            if v > 0:
               cost += v*points[k]
               dmg += v*original_damage[k]
         print(f'Total cost: {cost}')
         print(f'Total (original) damage: {dmg}')


   def readMinMax(self, roles: list):
      min_val=10000
      max_val=0
      for role in roles:
         for troop in self.troops[role]:
            if troop['damage'] >= max_val:
               max_val = troop['damage']
               print(f'Higher damage found: {max_val} by {troop["name"]}')
            if troop['damage'] <= min_val:
               min_val = troop['damage']
               print(f'Lower damage found: {min_val} by {troop["name"]}')
      self.old_max = max_val
      self.old_min = min_val

   def scaleValues(self, value: int):
      new_value = ( (value - self.old_min) / (self.old_max - self.old_min) ) * 100 + 1
      return int(new_value)


if __name__ == "__main__":
   Problem1("SistemasEq/config.yaml", "patrol")