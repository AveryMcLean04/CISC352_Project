(define (problem late-game-pressure)
  (:domain basketball-stamina)

  ;; Scenario: Late-game pressure situation.
  ;; Only 5 units of time remain. Several players have low stamina and cannot recover if subbed out.
  ;; Simulates end-of-game fatigue, foul trouble, and strategic lineup juggling under pressure.

  (:objects
    curry lillard lebron embiid durant irving kawhi - player
    G F C - slot
    b1 b2 b3 b4 - slot
  )

  (:init
    ;; Court players
    (has-player G curry)
    (has-player F lebron)
    (has-player C embiid)

    ;; Bench players (some usable, some gassed out)
    (has-player b1 lillard)
    (has-player b2 durant)
    (has-player b3 irving)
    (has-player b4 kawhi)

    ;; Slot Roles
    (court-slot G)
    (court-slot F)
    (court-slot C)
    (bench-slot b1)
    (bench-slot b2)
    (bench-slot b3)
    (bench-slot b4)

    ;; Stamina (very low across the board)
    (= (stamina curry) 2)
    (= (stamina lebron) 1)
    (= (stamina embiid) 2)
    (= (stamina lillard) 2)
    (= (stamina durant) 1)
    (= (stamina irving) 1)
    (= (stamina kawhi) 1)

    ;; Max Stamina
    (= (max-stamina curry) 3)
    (= (max-stamina lebron) 4)
    (= (max-stamina embiid) 3)
    (= (max-stamina lillard) 0)  ;; Can't recover after playing
    (= (max-stamina durant) 0)   ;; Already gassed
    (= (max-stamina irving) 2)
    (= (max-stamina kawhi) 0)    ;; Also unavailable for recovery

    ;; Fatigue Rate
    (= (fatigue-rate curry) 2)
    (= (fatigue-rate lebron) 1)
    (= (fatigue-rate embiid) 2)
    (= (fatigue-rate lillard) 2)
    (= (fatigue-rate durant) 2)
    (= (fatigue-rate irving) 1)
    (= (fatigue-rate kawhi) 2)

    ;; Game State
    (= (time-left) 5)
    (= (momentum) 5)
  )

  (:goal
    (<= (time-left) 0)
  )

  (:metric maximize (momentum))
)
