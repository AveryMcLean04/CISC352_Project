(define (domain basketball-lineup)
    (:requirements :typing :negative-preconditions :fluents)
    (:types
        player position time-unit - object
    )
    (:predicates
        (assigned ?p - player ?pos - position)
        (can-play ?p - player ?pos - position)
        (position-filled ?pos - position)
        (available ?p - player)
    )
    (:functions
        (height ?p - player)
        (stamina ?p - player)
        (shooting ?p - player)
        (defense ?p - player)
        (playmaking ?p - player)
        (offense ?p - player)
        (composite-score ?p - player)
        
        (time-elapsed)
        (team-score)
        (opponent-score)
        (total-lineup-cost)
    )
    (:action assign-player
        :parameters (?p - player ?pos - position)
        :precondition (and
            (available ?p)
            (can-play ?p ?pos)
            (not (position-filled ?pos))
            (forall (?other - player)
                (or
                    (not (available ?other))
                    (not (can-play ?other ?pos))
                    (<= (composite-score ?other) (composite-score ?p))
                )
            )
        )
        :effect (and
            (not (available ?p))
            (assigned ?p ?pos)
            (position-filled ?pos)
        )
    )
    (:action substitute-player
        :parameters (?p1 - player ?p2 - player ?pos - position)
        :precondition (and
            (available ?p1)
            (can-play ?p1 ?pos)
            (assigned ?p2 ?pos)
            (>= (stamina ?p1) 50)
        )
        :effect (and
            (not (available ?p1))
            (not (assigned ?p2 ?pos))
            (assigned ?p1 ?pos)
            (available ?p2)
        )
    )


)