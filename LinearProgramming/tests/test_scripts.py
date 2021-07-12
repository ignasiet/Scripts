from .solver import Solver

def test_main_load():
    costs = ([1,0,6,10,4],[0,3,10,8,0],[2,4,6,11,3],[0,0,5,8,4],[1,4,6,8,3])
    s = Solver("minimize")
    i=0
    j=0
    for selection in costs:
    for elem in selection:
        var_name = "var_"+str(i)+str(j)
        s.addVariables(var_name,0,1)
        j+=1
    var_name = "ship_"+str(i)
    s.addVariables(var_name,0,1)
    i+=1
    j=0

    assert len(s.variables) == 25