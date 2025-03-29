(define (problem raptors-game)
    (:domain basketball-lineup)
    (:objects 
        quickley - player
        barrett - player
        barnes - player
        dick - player
        poeltl - player
        shead - player
        agbaji - player
        boucher - player
        mogbo - player
        battle - player

        pg sg sf pf c - position
        
        t1 - time-unit
    )

    (:init
        ;; Initialize game state
        (= (time-elapsed) 0)
        (= (team-score) 0)
        (= (opponent-score) 0)
        (= (total-lineup-cost) 0)

        ;;quickley's attributes
        (= (height quickley) 75)
        (= (stamina quickley) 28)
        (= (shooting quickley) 82)
        (= (defense quickley) 58)
        (= (playmaking quickley) 81)
        (= (offense quickley) 76)
        (= (composite-score quickley) 215)

        ;;barrett's attributes
        (= (height barrett) 78)
        (= (stamina barrett) 33)
        (= (shooting barrett) 79)
        (= (defense barrett) 65)
        (= (playmaking barrett) 80)
        (= (offense barrett) 76)
        (= (composite-score barrett) 221)

        ;;barnes' attributes
        (= (height barnes) 76)
        (= (stamina barnes) 34)
        (= (shooting barnes) 69)
        (= (defense barnes) 76)
        (= (playmaking barnes) 77)
        (= (offense barnes) 80)
        (= (composite-score barnes) 233)

        ;;dick's attributes
        (= (height dick) 78)
        (= (stamina dick) 29)
        (= (shooting dick) 78)
        (= (defense dick) 58)
        (= (playmaking dick) 66)
        (= (offense dick) 70)
        (= (composite-score dick) 194)

        ;;poeltl's attributes
        (= (height poeltl) 84)
        (= (stamina poeltl) 30)
        (= (shooting poeltl) 45)
        (= (defense poeltl) 69)
        (= (playmaking poeltl) 50)
        (= (offense poeltl) 76)
        (= (composite-score poeltl) 195)

        ;;shead's attributes
        (= (height shead) 72)
        (= (stamina shead) 19)
        (= (shooting shead) 78)
        (= (defense shead) 55)
        (= (playmaking shead) 84)
        (= (offense shead) 60)
        (= (composite-score shead) 199)

        ;;abgaji's attributes
        (= (height agbaji) 77)
        (= (stamina agbaji) 27)
        (= (shooting agbaji) 83)
        (= (defense agbaji) 66)
        (= (playmaking agbaji) 61)
        (= (offense agbaji) 69)
        (= (composite-score agbaji) 196)

        ;;boucher's attributes
        (= (height boucher) 79)
        (= (stamina boucher) 17)
        (= (shooting boucher) 80)
        (= (defense boucher) 59)
        (= (playmaking boucher) 38)
        (= (offense boucher) 78)
        (= (composite-score boucher) 175)

        ;;mogbo's attributes
        (= (height mogbo) 79)
        (= (stamina mogbo) 18)
        (= (shooting mogbo) 74)
        (= (defense mogbo) 65)
        (= (playmaking mogbo) 64)
        (= (offense mogbo) 63)
        (= (composite-score mogbo) 192)

        ;;battle's attributes
        (= (height battle) 76)
        (= (stamina battle) 16)
        (= (shooting battle) 84)
        (= (defense battle) 49)
        (= (playmaking battle) 52)
        (= (offense battle) 69)
        (= (composite-score battle) 170)

        ;;Mark everyone as available and assign positions
        (available barnes)
        (available quickley)
        (available dick)
        (available barrett)
        (available boucher)
        (available poeltl)
        (available mogbo)
        (available battle)
        (available agbaji)
        (available shead)

        (can-play quickley pg)
        (can-play quickley sg)

        (can-play barnes pf)
        (can-play barnes sf)

        (can-play barrett sf)
        (can-play barrett pf)

        (can-play dick sg)
        (can-play dick sf)

        (can-play poeltl c)

        (can-play shead pg)

        (can-play agbaji sf)
        (can-play agbaji pf)

        (can-play boucher c)
        (can-play boucher pf)

        (can-play mogbo pf)
        (can-play mogbo c)

        (can-play battle sf)
        (can-play battle sg)
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
    (:metric maximize (total-lineup-cost))
)