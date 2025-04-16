(define (problem standard-game-alt)
  (:domain basketball-stamina)

  ;; Scenario: Standard full game with an alternate starting lineup.
  ;; Player stamina, fatigue rates, and max stamina are reassigned to show flexibility in initialization.
  ;; Goal is the same — finish the game while managing stamina and maximizing momentum.

  (:objects
    curry lillard irving lebron durant kawhi embiid - player
    G F C - slot
    b1 b2 b3 - slot
  )

  (:init
    ;; Court players (alternate lineup)
    (has-player G lillard)
    (has-player F durant)
    (has-player C kawhi)

    ;; Bench players
    (has-player b1 curry)
    (has-player b2 lebron)
    (has-player b3 embiid)
    (has-player b3 embiid)

    ;; Slot Roles
    (court-slot G)
    (court-slot F)
    (court-slot C)
    (bench-slot b1)
    (bench-slot b2)
    (bench-slot b3)

    ;; Stamina values
    (= (stamina lillard) 3)
    (= (stamina durant) 2)
    (= (stamina kawhi) 4)
    (= (stamina curry) 3)
    (= (stamina lebron) 4)
    (= (stamina embiid) 2)

    ;; Max Stamina
    (= (max-stamina lillard) 5)
    (= (max-stamina durant) 6)
    (= (max-stamina kawhi) 6)
    (= (max-stamina curry) 5)
    (= (max-stamina lebron) 7)
    (= (max-stamina embiid) 5)

    ;; Fatigue Rate (adjusted)
    (= (fatigue-rate lillard) 1)
    (= (fatigue-rate durant) 2)
    (= (fatigue-rate kawhi) 1)
    (= (fatigue-rate curry) 2)
    (= (fatigue-rate lebron) 1)
    (= (fatigue-rate embiid) 2)

    ;; Game State
    (= (time-left) 20)
    (= (momentum) 5)
  )

  (:goal
    (<= (time-left) 0)
  )

  (:metric maximize (momentum))
)
