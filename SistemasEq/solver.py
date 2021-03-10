# Import PuLP modeler functions
from pulp import *
from typing import Type

class Solver():
    def __init__(self, type_problem: str):
        # Create the 'prob' variable to contain the problem data
        self.vars = {}
        # Only: LpMinimize, LpMaximize
        if type_problem == "maximize":
            self.prob = LpProblem("The_Shop_aggregator_Problem", LpMaximize)
        elif type_problem == "minimize":
            self.prob = LpProblem("The_Shop_aggregator_Problem", LpMinimize)
        else:
            print("Not supported type of  problem. Aborting.")
            return
    
    def addVariables(self, 
                     variable_name: str, 
                     variable_min: int = 0, 
                     variable_max: int = 1):
        # The variables are created with a lower limit of zero and a maximal number of 1
        self.vars[variable_name] = LpVariable(variable_name,
                                              variable_min,
                                              variable_max,
                                              LpInteger)
        # for selection in self.costs:
        #     for elem in selection:
        #         #print("var:",i,j)
        #         var_name = "var_"+str(i)+str(j)
        #         self.vars[var_name] = LpVariable(var_name,0,1,LpInteger)
        #         j+=1
        #     var_name = "ship_"+str(i)
        #     self.vars[var_name] = LpVariable(var_name,0,1,LpInteger)
        #     i+=1
        #     j=0
        # self.setObjectiveFunction()
        # self.addRestrictions()

    def setObjectiveFunction(self, costs: list):
        #We create then the objective function:
        objective_funct = None
        constants = []
        vars = []
        for elem in costs:
            for name,damage in elem.items():
                # print(f"All: {elem}, damage: {int(damage)}")
                vars.append(self.vars[name])
                constants.append(int(damage))
        print(vars)
        print(constants)
        model = pulp.lpDot(vars, constants)
        #Add objective to the problem
        self.prob += model
        print(f"Objective function:{model}")
        print("Subject to:")

    def addRestrictions(self, restriction: list, operator: str, total: int):
        r1 = None
        for elem in restriction:
            # print(elem)
            for name,value in elem.items():
                r1 += self.vars[name]*int(value)

        #Add objective to the problem
        if operator == "leq":
            self.prob += r1 <= total
        elif operator == 'geq':
            self.prob += r1 >= total
        elif operator == 'eq':
            self.prob += r1 == total
        else:
            print("Operation not considered. Exiting.")
            return -1
        print(f"Restriction: {r1} {operator} {total}")

        # #First restriction, only one element of each material required
        # for j in range(self.num_elems):
        #     r1=None
        #     for i in range(self.num_shops):
        #         if self.costs[i][j]>0:
        #             var_name = "var_"+str(i)+str(j)
        #             r1 += self.vars[var_name]
        #     print(f"{r1} >= 1")
        #     self.prob += r1 >= 1

        # #Last restriction, a shipment for at least one element
        # for i in range(self.num_shops):    
        #     ship_name = "ship_"+str(i)
        #     for j in range(self.num_elems):
        #         r3 = None
        #         var_name = "var_"+str(i)+str(j)
        #         r3 += self.vars[var_name]
        #         self.prob += self.vars[ship_name] >= r3
        #         print(f"{self.vars[ship_name]} >= {r3}")

    def solve(self):
        #We (the solver, of course) solve the problem
        troops = {}
        GLPK().solve(self.prob)
        for v in self.prob.variables():
            if v.varValue > 0:
                print(v.name, "=", v.varValue)
            troops[v.name] = v.varValue
        print("Objective =", value(self.prob.objective) )
        return troops