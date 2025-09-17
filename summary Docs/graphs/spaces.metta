; (Parent drey zory)

; !(match &self (Parent drey $x) ($x))


; create a new space
; bind!, new-space


!(bind! &smith-family (new-space))

; !(match &smith-family $x $y)


; add new atom

!(add-atom &smith-family (Parent zoe joe))
!(add-atom &smith-family (Parent zoe moe))
!(add-atom &self (Parent zoe koe))

!(match &smith-family (Parent zoe $x) ($x))
!(match &self (Parent zoe $x) ($x))


; remove-atom

!(remove-atom &self (Parent zoe koe))

!(match &self (Parent zoe $x) ($x))

; update atom  we do not have any such in std so we can use remove and then add atom fxn

; !(let $x (+ 1 2) (* $x 4))

; !(let* 
; (
;     ($x (+ 1 2) )
;     ($y (* $x 4) )
;     ($z (+ $x $y) )
; )
; (
;     + 10 $z
; )


; )

(= (update-atom $space $old-atom $new-atom)
    
        (let $x (remove-atom $space $old-atom)   (add-atom $space $new-atom) )

    
   
  
)
