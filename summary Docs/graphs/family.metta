(adam 23 2000 Male) 
(adam 25 3000 Male) 
; will be stored as a graph in our atomspace (it is like a database)
(monica 41 2000 Female)
(john 50 3000 Male)
;((samanyu gautam) 19 40000 Male)
(palm 21 1500 Female)

(john isFatherOf adam) ; we are making a relationship between john and adam
(john isHusbandOf monica)


; now we need to retrieve the data

; !(match &self $x ("Everything is" $x)) 
; what ever we want to run add ! before
; pre-defined function to retrieve data from the atomspace and fxn name comes first and se;f refer to 
; the current atomspace
; $x means try retrieve anything and store it in x


; !(match &self (adam $x $y $g) ("Adam is" $x "years old")) 

; !(match &self (adam 23 $y $g) ("Adam is 23 years old and his salary is" $y)) 

; !(match &self (adam 23 $y $g) ($y $g)) 
; !(match &self (adam 23 $y $g) ($g $y)) 

; !(match &self ($y isFatherOf adam) ("Adam's father is" $y))

; !(match &self ($z isHusbandOf monica) ("Monica's better half is" $z))

; !(match &self (john isFatherOf $d) (match &self ($d $x $y $g) ($d $x $y $g)))

(john isParentOf adam) 
(john isParentOf monica)

(= (isSibling $x $y)
           (match &self ($n isParentOf $x) (match &self ($n isParentOf $y)True))
)


; !(isSibling adam monica)



