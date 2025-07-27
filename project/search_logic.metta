;; Flight Search Logic in MeTTa

;; Search flights by source airport only
(= (search-by-source $source)
   (match &space (flight $year $month $day $source $dest $cost)
          (flight $year $month $day $source $dest $cost)))

;; Search flights by destination airport only  
(= (search-by-destination $dest)
   (match &space (flight $year $month $day $src $dest $cost)
          (flight $year $month $day $src $dest $cost)))

;; Search flights by date only (year, month, day)
(= (search-by-date $year $month $day)
   (match &space (flight $year $month $day $src $dest $cost)
          (flight $year $month $day $src $dest $cost)))

;; Search flights by route (source and destination)
(= (search-by-route $source $dest)
   (match &space (flight $year $month $day $source $dest $cost)
          (flight $year $month $day $source $dest $cost)))

;; Search flights by source and date
(= (search-by-source-date $source $year $month $day)
   (match &space (flight $year $month $day $source $dest $cost)
          (flight $year $month $day $source $dest $cost)))

;; Search flights by destination and date
(= (search-by-dest-date $dest $year $month $day)
   (match &space (flight $year $month $day $src $dest $cost)
          (flight $year $month $day $src $dest $cost)))

;; Search flights by route and date (all parameters)
(= (search-comprehensive $source $dest $year $month $day)
   (match &space (flight $year $month $day $source $dest $cost)
          (flight $year $month $day $source $dest $cost)))

;; Get all flights
(= (search-all-flights)
   (match &space (flight $year $month $day $src $dest $cost)
          (flight $year $month $day $src $dest $cost)))