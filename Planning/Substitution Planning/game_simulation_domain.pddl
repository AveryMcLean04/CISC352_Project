(define (domain basketball-stamina)
  ;; Domain for simulating stamina-based basketball player rotation and game flow.
  ;; Players sub in/out based on stamina; momentum increases with continuity and decreases with disruption.

  (:requirements :typing :fluents :equality)

  ;; Define the basic types of objects in the domain
  (:types player slot)

  ;; Predicates to describe current player-slot assignments and slot types
  (:predicates
    (has-player ?s - slot ?p - player)   ;; Player ?p is currently occupying slot ?s
    (court-slot ?s - slot)               ;; Slot ?s is part of the current on-court lineup
    (bench-slot ?s - slot)               ;; Slot ?s is part of the bench
  )

  ;; Numeric fluents used to track game state
  (:functions
    (stamina ?p - player)                ;; Current stamina of player ?p
    (max-stamina ?p - player)            ;; Maximum stamina player ?p can be reset to
    (fatigue-rate ?p - player)           ;; How quickly player ?p loses stamina while playing
    (time-left)                          ;; Remaining game time (in turns)
    (momentum)                           ;; Represents team rhythm/energy; high = good flow
  )

  ;; Core game action: playing a unit of time with 3 players on the court
  (:action play-time
    :parameters (?c1 - slot ?p1 - player
                 ?c2 - slot ?p2 - player
                 ?c3 - slot ?p3 - player)
    :precondition (and
      ;; Ensure all 3 slots are court slots and filled by distinct players with stamina
      (court-slot ?c1) (court-slot ?c2) (court-slot ?c3)
      (has-player ?c1 ?p1) (has-player ?c2 ?p2) (has-player ?c3 ?p3)
      (>= (stamina ?p1) 1)
      (>= (stamina ?p2) 1)
      (>= (stamina ?p3) 1)
      (not (= ?p1 ?p2))
      (not (= ?p1 ?p3))
      (not (= ?p2 ?p3))
    )
    :effect (and
      ;; Time decreases by 1 unit
      ;; Each player's stamina decreases based on their fatigue rate
      ;; Momentum increases (team rhythm improves with stable lineups)
      (decrease (time-left) 1)
      (decrease (stamina ?p1) (fatigue-rate ?p1))
      (decrease (stamina ?p2) (fatigue-rate ?p2))
      (decrease (stamina ?p3) (fatigue-rate ?p3))
      (increase (momentum) 2)
    )
  )

  ;; Substitution action: swap a tired player from court with a fresh player from bench
  (:action substitute
    :parameters (?c - slot ?b - slot ?pc - player ?pb - player)
    :precondition (and
      ;; Only allow a sub when the court player has no stamina and the bench player has stamina
      (court-slot ?c) (bench-slot ?b)
      (has-player ?c ?pc)
      (has-player ?b ?pb)
      (<= (stamina ?pc) 0)
      (>= (stamina ?pb) 1)
    )
    :effect (and
      ;; Swap players between slots
      ;; Restore outgoing player's stamina to full
      ;; Momentum decreases slightly since subs break continuity
      (not (has-player ?c ?pc))
      (not (has-player ?b ?pb))
      (has-player ?c ?pb)
      (has-player ?b ?pc)
      (assign (stamina ?pc) (max-stamina ?pc))
      (decrease (momentum) 2)
    )
  )
)
