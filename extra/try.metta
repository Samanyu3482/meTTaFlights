; (= (add 1 2) (3))

; !(add 1 2)


; !(id ("Samanyu"))

; ; storing in atomspace or directly printing
; Hello 
; (Hello World) 
; ! (+ 1 2) 
; ! (Hi there) 


; ; equality =
; ! (respond me)
; (= (respond me) (OK, I will respond))
; ! (respond me)


; ; fxns with parameters

; (= (duplicate $x) ($x $x))
; ! (duplicate A)
; ! (duplicate 1.05)


; (= (swap (Pair $x $y)) (Pair $y $x))
; ! (swap (Pair A B)) ; evaluates to (Pair B A)


; (= (check ($x $y $x)) ($x $y))
; ! (check (B A B)) ; reduced to (B A)
; ! (check (B A A)) ; not 






; (= (bin) 0)
; (= (bin) 1)
; ! (bin) ; both 0 and 1



; (= (f special-value) catched)
; (= (f $x) $x)
; ! (f A) ; A
; ! (f special-value) ; both catched and special-value



;; Dijkstra's shortest path algorithm in OpenClog Metta

;; Define the graph as edges with weights
;; Format: (edge source destination weight)
(edge A B 4)
(edge A C 2)
(edge B C 1)
(edge B D 5)
(edge C D 8)
(edge C E 10)
(edge D E 2)

;; Helper functions for distance management
;; Initialize distances - all nodes start with infinite distance except source
(= (init-distance $node $source)
   (if (== $node $source) 0 inf))

;; Get minimum distance node from unvisited set
(= (min-unvisited $distances $unvisited)
   (let* (($min-node (car $unvisited))
          ($min-dist (get-distance $min-node $distances)))
     (if (== (cdr $unvisited) ())
         $min-node
         (let (($rest-min (min-unvisited $distances (cdr $unvisited))))
           (if (< (get-distance $rest-min $distances) $min-dist)
               $rest-min
               $min-node)))))

;; Update distance if shorter path found
(= (update-distance $current $neighbor $weight $distances)
   (let* (($current-dist (get-distance $current $distances))
          ($neighbor-dist (get-distance $neighbor $distances))
          ($new-dist (+ $current-dist $weight)))
     (if (< $new-dist $neighbor-dist)
         (set-distance $neighbor $new-dist $distances)
         $distances)))

;; Get neighbors of a node
(= (get-neighbors $node)
   (let (($edges (match &self (edge $node $dest $weight) ($dest $weight))))
     $edges))

;; Main Dijkstra algorithm
(= (dijkstra $source $nodes)
   (let* (($distances (map (lambda ($node) (init-distance $node $source)) $nodes))
          ($unvisited $nodes))
     (dijkstra-loop $distances $unvisited)))

;; Recursive loop for Dijkstra
(= (dijkstra-loop $distances $unvisited)
   (if (== $unvisited ())
       $distances
       (let* (($current (min-unvisited $distances $unvisited))
              ($new-unvisited (remove $current $unvisited))
              ($neighbors (get-neighbors $current))
              ($updated-distances 
               (fold-left 
                 (lambda ($acc $neighbor-info)
                   (let (($neighbor (car $neighbor-info))
                         ($weight (cadr $neighbor-info)))
                     (update-distance $current $neighbor $weight $acc)))
                 $distances 
                 $neighbors)))
         (dijkstra-loop $updated-distances $new-unvisited))))

;; Utility functions for distance manipulation
(= (get-distance $node $distances)
   (cdr (assoc $node $distances)))

(= (set-distance $node $dist $distances)
   (cons (cons $node $dist) 
         (remove-assoc $node $distances)))

;; Example usage:
;; Find shortest paths from node A to all other nodes
(= (example-dijkstra)
   (let (($nodes (A B C D E)))
     (dijkstra A $nodes)))

;; To get shortest path between two specific nodes
(= (shortest-path $source $target $nodes)
   (let (($distances (dijkstra $source $nodes)))
     (get-distance $target $distances)))

;; Example query: What's the shortest distance from A to E?
!(shortest-path A E (A B C D E))