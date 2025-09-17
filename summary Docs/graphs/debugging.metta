; !(println! Hello)
; !(println! (chitkara univ))


(is Gentlemen A)
(is Lady B)
(is Lady C)

!(match &self (is Gentlemen $x) ($x))
!(println! (match &self (is Lady $x) (Lady $x)))


(= (is Gentlemen $x) (trace! (Input: $x) (Output: (match &self (is Gentlemen $x) True))))

!(is Gentlemen A)