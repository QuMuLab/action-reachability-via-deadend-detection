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
    )
    (:action toggle1
        :parameters ()
        :precondition
            (and
                (p)
            )
        :effect
            (and
                (newpred)
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
            )
        :effect
            (and
                (g)
            )
    )
)