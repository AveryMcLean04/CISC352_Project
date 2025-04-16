(define (problem back-to-back-game)
  (:domain basketball-stamina)

  ;; Scenario: Back-to-back game simulation.
  ;; All players are a bit worn down from a previous game — modeled by reduced max stamina.
  ;; Each player starts at their max stamina (fully rested for today, but overall limited).

  (:objects
    curry lillard irving lebron durant kawhi embiid - player
    G F C - slot
    b1 b2 b3 - slot
  )

  (:init
    ;; Court players
    (has-player G curry)
    (has-player F lebron)
    (has-player C embiid)

    ;; Bench players
    (has-player b1 lillard)
    (has-player b2 irving)
    (has-player b3 durant)

    ;; Slot Roles
    (court-slot G)
    (court-slot F)
    (court-slot C)
    (bench-slot b1)
    (bench-slot b2)
    (bench-slot b3)

    ;; Max Stamina (reduced slightly for all players)
    (= (max-stamina curry) 4)
    (= (max-stamina lebron) 5)
    (= (max-stamina embiid) 4)
    (= (max-stamina lillard) 4)
    (= (max-stamina irving) 4)
    (= (max-stamina durant) 5)

    ;; Stamina values (start fully rested for today, but overall more limited)
    (= (stamina curry) 4)
    (= (stamina lebron) 5)
    (= (stamina embiid) 4)
    (= (stamina lillard) 4)
    (= (stamina irving) 4)
    (= (stamina durant) 5)

    ;; Fatigue Rate (standard)
    (= (fatigue-rate curry) 1)
    (= (fatigue-rate lebron) 1)
    (= (fatigue-rate embiid) 2)
    (= (fatigue-rate lillard) 1)
    (= (fatigue-rate irving) 1)
    (= (fatigue-rate durant) 2)

    ;; Game State
    (= (time-left) 12)
    (= (momentum) 5)
  )

  (:goal
    (<= (time-left) 0)
  )

  (:metric maximize (momentum))
)
