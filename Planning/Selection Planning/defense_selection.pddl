(define (problem maximize-defense-lineup)
  (:domain basketball-lineup-multi-objective)

  ;; Problem: Select a 5-player lineup that maximizes total defense

  (:objects 
    quickley barrett barnes dick poeltl shead agbaji boucher mogbo battle - player
    pg sg sf pf c - position
  )

  (:init
    (= (total-defense) 0)

    ;; Attributes
    (= (height quickley) 75) (= (stamina quickley) 28) (= (shooting quickley) 82)
    (= (defense quickley) 58) (= (playmaking quickley) 81) (= (offense quickley) 76)
    (= (composite-score quickley) 215)

    (= (height barrett) 78) (= (stamina barrett) 33) (= (shooting barrett) 79)
    (= (defense barrett) 65) (= (playmaking barrett) 80) (= (offense barrett) 76)
    (= (composite-score barrett) 221)

    (= (height barnes) 76) (= (stamina barnes) 34) (= (shooting barnes) 69)
    (= (defense barnes) 76) (= (playmaking barnes) 77) (= (offense barnes) 80)
    (= (composite-score barnes) 233)

    (= (height dick) 78) (= (stamina dick) 29) (= (shooting dick) 78)
    (= (defense dick) 58) (= (playmaking dick) 66) (= (offense dick) 70)
    (= (composite-score dick) 194)

    (= (height poeltl) 84) (= (stamina poeltl) 30) (= (shooting poeltl) 45)
    (= (defense poeltl) 69) (= (playmaking poeltl) 50) (= (offense poeltl) 76)
    (= (composite-score poeltl) 195)

    (= (height shead) 72) (= (stamina shead) 19) (= (shooting shead) 78)
    (= (defense shead) 55) (= (playmaking shead) 84) (= (offense shead) 60)
    (= (composite-score shead) 199)

    (= (height agbaji) 77) (= (stamina agbaji) 27) (= (shooting agbaji) 83)
    (= (defense agbaji) 66) (= (playmaking agbaji) 61) (= (offense agbaji) 69)
    (= (composite-score agbaji) 196)

    (= (height boucher) 79) (= (stamina boucher) 17) (= (shooting boucher) 80)
    (= (defense boucher) 59) (= (playmaking boucher) 38) (= (offense boucher) 78)
    (= (composite-score boucher) 175)

    (= (height mogbo) 79) (= (stamina mogbo) 18) (= (shooting mogbo) 74)
    (= (defense mogbo) 65) (= (playmaking mogbo) 64) (= (offense mogbo) 63)
    (= (composite-score mogbo) 192)

    (= (height battle) 76) (= (stamina battle) 16) (= (shooting battle) 84)
    (= (defense battle) 49) (= (playmaking battle) 52) (= (offense battle) 69)
    (= (composite-score battle) 170)

    ;; Availability
    (available quickley) (not-in-lineup quickley)
    (available barrett) (not-in-lineup barrett)
    (available barnes) (not-in-lineup barnes)
    (available dick) (not-in-lineup dick)
    (available poeltl) (not-in-lineup poeltl)
    (available shead) (not-in-lineup shead)
    (available agbaji) (not-in-lineup agbaji)
    (available boucher) (not-in-lineup boucher)
    (available mogbo) (not-in-lineup mogbo)
    (available battle) (not-in-lineup battle)

    ;; Positions
    (position-available pg)
    (position-available sg)
    (position-available sf)
    (position-available pf)
    (position-available c)

    ;; Eligibility
    (can-play quickley pg) (can-play quickley sg)
    (can-play barnes pf) (can-play barnes sf)
    (can-play barrett sf) (can-play barrett pf)
    (can-play dick sg) (can-play dick sf)
    (can-play poeltl c)
    (can-play shead pg)
    (can-play agbaji sf) (can-play agbaji pf)
    (can-play boucher c) (can-play boucher pf)
    (can-play mogbo pf) (can-play mogbo c)
    (can-play battle sf) (can-play battle sg)
  )

  (:goal
    (and
      (position-filled pg)
      (position-filled sg)
      (position-filled sf)
      (position-filled pf)
      (position-filled c)
    )
  )

  (:metric maximize (total-defense))
)
