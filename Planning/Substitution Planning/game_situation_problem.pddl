(define (problem standard-game-long)
  (:domain basketball-stamina)

  ;; Scenario: Full-length, balanced game with all players available.
  ;; Designed to test endurance and lineup rotation over a longer game (20 time units).
  ;; Momentum should build with consistent lineups and fall with excessive substitutions.

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

    ;; Stamina values
    (= (stamina curry) 4)
    (= (stamina lebron) 4)
    (= (stamina embiid) 3)
    (= (stamina lillard) 3)
    (= (stamina irving) 3)
    (= (stamina durant) 3)

    ;; Max Stamina
    (= (max-stamina curry) 6)
    (= (max-stamina lebron) 7)
    (= (max-stamina embiid) 5)
    (= (max-stamina lillard) 5)
    (= (max-stamina irving) 5)
    (= (max-stamina durant) 6)

    ;; Fatigue Rate
    (= (fatigue-rate curry) 1)
    (= (fatigue-rate lebron) 1)
    (= (fatigue-rate embiid) 2)
    (= (fatigue-rate lillard) 1)
    (= (fatigue-rate irving) 1)
    (= (fatigue-rate durant) 2)

    ;; Game State
    (= (time-left) 20)
    (= (momentum) 5)
  )

  (:goal
    (<= (time-left) 0)
  )

  (:metric maximize (momentum))
)
