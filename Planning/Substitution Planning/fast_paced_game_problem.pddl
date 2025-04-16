(define (problem fast-paced-game)
  (:domain basketball-stamina)

  ;; Scenario: Fast-paced, high-fatigue game.
  ;; All players have increased fatigue rates to simulate faster stamina drain.
  ;; Time is reduced (10 turns) to prevent an excessive number of substitutions in the output.

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

    ;; Stamina values (moderate to show effect of faster fatigue)
    (= (stamina curry) 3)
    (= (stamina lebron) 3)
    (= (stamina embiid) 3)
    (= (stamina lillard) 3)
    (= (stamina irving) 3)
    (= (stamina durant) 3)

    ;; Max Stamina
    (= (max-stamina curry) 5)
    (= (max-stamina lebron) 6)
    (= (max-stamina embiid) 5)
    (= (max-stamina lillard) 5)
    (= (max-stamina irving) 5)
    (= (max-stamina durant) 6)

    ;; Fatigue Rate (increased for all players to simulate fast pace)
    (= (fatigue-rate curry) 2)
    (= (fatigue-rate lebron) 2)
    (= (fatigue-rate embiid) 3)
    (= (fatigue-rate lillard) 2)
    (= (fatigue-rate irving) 2)
    (= (fatigue-rate durant) 3)

    ;; Game State
    (= (time-left) 10)
    (= (momentum) 5)
  )

  (:goal
    (<= (time-left) 0)
  )

  (:metric maximize (momentum))
)
