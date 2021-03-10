# Import PuLP modeler functions
from pulp import *

#Arrays are shops with prices for material i
#Each position in the array represents the cost of a material 
#across all shops,for ex: costs[i][j] represents the cost of material j in shop i
#a 0 represents a material not found in the shop
costs = ([1,0,6,10,4],[0,3,10,8,0],[2,4,6,11,3],[0,0,5,8,4],[1,4,6,8,3])
num_shops = 5
num_elems = 5


# Create the 'prob' variable to contain the problem data
prob = LpProblem("The_Shop_aggregator_Problem",LpMinimize)

# The variables are created with a lower limit of zero and a maximal number of 1
i=0
j=0
Vars = {}
for shop in costs:
    for elem in shop:
        #print("var:",i,j)
        var_name = "var_"+str(i)+str(j)
        Vars[var_name] = LpVariable(var_name,0,1,LpInteger)
        j+=1
    var_name = "ship_"+str(i)
    Vars[var_name] = LpVariable(var_name,0,1,LpInteger)
    i+=1
    j=0

#We create then the objective function:
i=0
j=0
objective_funct = None
for shop in costs:
    for elem in shop:
        var_name = "var_"+str(i)+str(j)
        objective_funct += Vars[var_name]*costs[i][j]
        j+=1
    var_name = "ship_"+str(i)
    objective_funct += Vars[var_name]
    i+=1
    j=0

#Add objective to the problem
prob += objective_funct
print(f"Minimize objective function:{objective_funct}")
print("Subject to:")

#First restriction, only one element of each material required
for j in range(len(costs[0])):
    r1=None
    for i in range(len(costs)):
        if costs[i][j]>0:
            var_name = "var_"+str(i)+str(j)
            r1 += Vars[var_name]
    print(f"{r1} >= 1")
    prob += r1 >= 1
    

#Last restriction, a shipment for at least one element
for i in range(num_shops):    
    ship_name = "ship_"+str(i)
    for j in range(num_elems):
        r3 = None
        var_name = "var_"+str(i)+str(j)
        r3 += Vars[var_name]
        prob += Vars[ship_name] >= r3

#We (the solver, of course) solve the problem
GLPK().solve(prob)
for v in prob.variables():
    print(v.name, "=", v.varValue)

print("Objective =", value(prob.objective) )