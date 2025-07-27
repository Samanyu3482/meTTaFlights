; ============================================
; Rules for finding all available flight paths with cost
; Fact format: (flight YEAR MONTH DAY ORIGIN DEST COST)
; ============================================

; -------------------------------
; Helper: Check if element is in list
; -------------------------------
!(-- (member ?x (?x . ?_)))
!(-- (member ?x (?_ . ?xs)) (member ?x ?xs))

; -------------------------------
; Direct Flight: Path is (?from ?to)
; -------------------------------
!(-- (path ?year ?month ?day ?from ?to (?from ?to) &cost)
    (flight ?year ?month ?day ?from ?to &cost))

; -------------------------------
; Recursive Path: Avoid cycles, accumulate cost
; -------------------------------
!(-- (path ?year ?month ?day ?from ?to (?from . ?rest) &total-cost)
    (flight ?year ?month ?day ?from ?mid &cost1)
    (path ?year ?month ?day ?mid ?to ?rest &cost2)
    (not (member ?from ?rest))
    (= &total-cost (+ &cost1 &cost2)))
