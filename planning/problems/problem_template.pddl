(define (problem pb1) (:domain warhammer)
(:objects 
A B C D E- location
d1 d2 - troop
o1 - objective
o2 - objective
)

(:init
    (connected A B)
    (connected B A)
    (connected B C)
    (connected C B)
    (connected C D)
    (connected D C)
    (connected C E)
    (connected E C)
    (objective_at o1 D)
    (objective_at o2 E)
    (troop_at d1 A)
    (troop_at d2 B)
    
)

(:goal (or
    (hold d1 o1)
    (hold d2 o2)
    (hold d1 o1)
    (hold d2 o2)
) 
)
)
