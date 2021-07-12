(define (domain Warhammer40k)

(:requirements :strips :negative-preconditions :adl :equality :derived-predicates :equality
:universal-preconditions)


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
    (in_cc_range ?tr1 ?tr2 - troop)
    (psyker ?troop - troop)
    (smited ?troop - troop)
    (attacked ?troop - troop)
    (shooted ?troop - troop)
    (ranged_weapon ?troop - troop)
    (melee_weapon ?troop - troop)
    (healthy ?troop - troop)
    (psikering ?troop - troop)
    (shooting ?troop - troop)
    (combat ?troop - troop)
    (stopped ?troop - troop)
    (can_move ?who)
)


(:action move
    :parameters (?who ?from ?to)
    :precondition (and (troop_at ?who ?from) (connected ?from ?to) (can_move ?who))
    :effect (and (not (troop_at ?who ?from)) (troop_at ?who ?to) )
)


(:action hold
    :parameters (?who ?obj ?pos)
    :precondition (and (troop_at ?who ?pos) (objective_at ?obj ?pos) (not (holded ?obj)))
    :effect (and (holded ?obj) (conquer ?who ?obj) (stopped ?who) (not (can_move ?who)))
)

(:action smite
    :parameters (?who ?target)
    :precondition (and (psyker ?who) (in_range ?who ?target) (not (smited ?who)) (psikering ?who))
    :effect (and 
                (smited ?who)
                (when (and (healthy ?target)) (and (wounded ?target) (not (healthy ?target))) )
                (when (wounded ?target) (killed ?target) )
            )  
)

(:action shot
    :parameters (?who ?target)
    :precondition (and (ranged_weapon ?who) (in_range ?who ?target) (not (shooted ?who)) (shooting ?who))
    :effect (and 
                (shooted ?who)
                (when (and (healthy ?target)) (and (wounded ?target) (not (healthy ?target))) )
                (when (wounded ?target) (killed ?target) )
            )
)

(:action charge
    :parameters (?who ?from ?to)
    :precondition (and (combat ?who) (melee_weapon ?who) (not (attacked ?who)) (troop_at ?who ?from) (connected ?from ?to))
    :effect (and (not (troop_at ?who ?from)) (troop_at ?who ?to) )
)

(:action kill
    :parameters (?who ?target ?pos)
    :precondition (and (melee_weapon ?who) (troop_at ?who ?pos) (troop_at ?target ?pos) (not (attacked ?who)) (combat ?who))
    :effect (and 
                (attacked ?who)
                (when (and (healthy ?target)) (and (wounded ?target) (not (healthy ?target))) )
                (when (wounded ?target) (killed ?target) )
            )
)

(:derived (combat ?who)
    (or 
        (and 
            (melee_weapon ?who)
            (shooted ?who)
        )
        (and 
            (not (ranged_weapon ?who))
            (smited ?who)
        )
    )
)

(:derived (psikering ?who)
    (and 
        (psyker ?who)
        (stopped ?who)
    )
)

(:derived (shooting ?who)
    (and 
        (ranged_weapon ?who)
        (stopped ?who)
    )
)

)