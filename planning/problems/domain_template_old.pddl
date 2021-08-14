(define (domain Warhammer40k)

(:requirements :strips :negative-preconditions :adl)


(:types troop objective location )


(:predicates ;todo: define predicates here
    (troop_at ?troop - troop ?pos - location)
    (objective_at ?obj - objective ?pos - location)
    (connected ?pos1 ?pos2 - location)
    (conquer ?troop - troop ?obj - objective)
    (holded ?obj - objective)
    (wounded ?troop - troop)
    (killed ?troop - troop)
    (in_range ?tr1 ?tr2 - troop)
    (psyker ?troop - troop)
    (smited ?troop - troop)
    (attacked ?troop - troop)
    (shooted ?troop - troop)
    (ranged_weapon ?troop - troop)
    (melee_weapon ?troop - troop)
    (healthy ?troop - troop)    
)


(:action move
    :parameters (?who ?from ?to)
    :precondition (and (troop_at ?who ?from) (connected ?from ?to))
    :effect (and (not (troop_at ?who ?from)) (troop_at ?who ?to))
)


(:action hold
    :parameters (?who ?obj ?pos)
    :precondition (and (troop_at ?who ?pos) (objective_at ?obj ?pos) (not (holded ?obj)))
    :effect (and (holded ?obj) (conquer ?who ?obj))
)

(:action smite
    :parameters (?who ?target)
    :precondition (and (psyker ?who) (in_range ?who ?target) (not (smited ?who)))
    :effect (and 
                (smited ?who)
                (when (and (healthy ?target)) (and (wounded ?target) (not (healthy ?target))) )
                (when (wounded ?target) (killed ?target) )
            )  
)

(:action shot
    :parameters (?who ?target)
    :precondition (and (ranged_weapon ?who) (in_range ?who ?target) (not (shooted ?who)) )
    :effect (and 
                (shooted ?who)
                (when (and (healthy ?target)) (and (wounded ?target) (not (healthy ?target))) )
                (when (wounded ?target) (killed ?target) )
            )
)

(:action kill
    :parameters (?who ?target)
    :precondition (and (melee_weapon ?who) (in_range ?who ?target) (not (attacked ?who)) )
    :effect (and 
                (attacked ?who)
                (when (and (healthy ?target)) (and (wounded ?target) (not (healthy ?target))) )
                (when (wounded ?target) (killed ?target) )
            )
)

)