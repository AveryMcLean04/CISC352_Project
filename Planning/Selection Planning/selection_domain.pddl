(define (domain basketball-lineup-multi-objective)
  ;; OPTIC-compatible domain for selecting a basketball lineup.
  ;; Each player can play certain positions. The goal is to fill all 5 positions (PG, SG, SF, PF, C)
  ;; while maximizing one specific attribute (shooting, defense, playmaking, offense, or composite).
  ;; Each action is isolated to one attribute. Negative preconditions are replaced with explicit flags.

  (:requirements :typing :fluents :equality)

  (:types player position)

  (:predicates
    (available ?p - player)                ;; Player is eligible for selection
    (can-play ?p - player ?pos - position) ;; Player can play the given position
    (position-available ?pos - position)   ;; Position not yet filled
    (not-in-lineup ?p - player)            ;; Player has not yet been assigned
    (in-lineup ?p - player)                ;; Player has been assigned
    (position-filled ?pos - position)      ;; Position is filled
  )

  (:functions
    (total-lineup-cost)
    (total-shooting)
    (total-defense)
    (total-playmaking)
    (total-offense)

    (height ?p - player)
    (stamina ?p - player)
    (shooting ?p - player)
    (defense ?p - player)
    (playmaking ?p - player)
    (offense ?p - player)
    (composite-score ?p - player)
  )

  ;; Composite score
  (:action assign-for-composite
    :parameters (?p - player ?pos - position)
    :precondition (and
      (available ?p)
      (can-play ?p ?pos)
      (position-available ?pos)
      (not-in-lineup ?p)
    )
    :effect (and
      (in-lineup ?p)
      (position-filled ?pos)
      (increase (total-lineup-cost) (composite-score ?p))
      ;; flip flags
      (not (not-in-lineup ?p))
      (not (position-available ?pos))
    )
  )

  ;; Shooting
  (:action assign-for-shooting
    :parameters (?p - player ?pos - position)
    :precondition (and
      (available ?p)
      (can-play ?p ?pos)
      (position-available ?pos)
      (not-in-lineup ?p)
    )
    :effect (and
      (in-lineup ?p)
      (position-filled ?pos)
      (increase (total-shooting) (shooting ?p))
      (not (not-in-lineup ?p))
      (not (position-available ?pos))
    )
  )

  ;; Defense
  (:action assign-for-defense
    :parameters (?p - player ?pos - position)
    :precondition (and
      (available ?p)
      (can-play ?p ?pos)
      (position-available ?pos)
      (not-in-lineup ?p)
    )
    :effect (and
      (in-lineup ?p)
      (position-filled ?pos)
      (increase (total-defense) (defense ?p))
      (not (not-in-lineup ?p))
      (not (position-available ?pos))
    )
  )

  ;; Playmaking
  (:action assign-for-playmaking
    :parameters (?p - player ?pos - position)
    :precondition (and
      (available ?p)
      (can-play ?p ?pos)
      (position-available ?pos)
      (not-in-lineup ?p)
    )
    :effect (and
      (in-lineup ?p)
      (position-filled ?pos)
      (increase (total-playmaking) (playmaking ?p))
      (not (not-in-lineup ?p))
      (not (position-available ?pos))
    )
  )

  ;; Offense
  (:action assign-for-offense
    :parameters (?p - player ?pos - position)
    :precondition (and
      (available ?p)
      (can-play ?p ?pos)
      (position-available ?pos)
      (not-in-lineup ?p)
    )
    :effect (and
      (in-lineup ?p)
      (position-filled ?pos)
      (increase (total-offense) (offense ?p))
      (not (not-in-lineup ?p))
      (not (position-available ?pos))
    )
  )
)
