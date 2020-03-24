(define
    (domain toggle)
    (:requirements :strips)
    (:types default_object - None)
    (:constants
      
    )

    (:predicates 
        (p)
        (q)
        (g)
        (newpred)
    )
    (:action toggle1
        :parameters ()
        :precondition
            (and
                (p)
            )
        :effect
            (and
                (not
                    (p)
                )
                (q)
            )
    )
    (:action toggle2
        :parameters ()
        :precondition
            (and
                (q)
            )
        :effect
            (and
                (not
                    (q)
                )
                (p)
            )
    )
    (:action win
        :parameters ()
        :precondition
            (and
                (p)
                (q)
            )
        :effect
            (and
                (newpred)
            )
    )
)