import csv

input_file = "flights.csv"
output_file = "flights_bang.metta"

with open(input_file, newline='') as csvfile, open(output_file, 'w') as mettafile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        year = row['year']
        month = row['month']
        day = row['day']
        origin = row['origin']
        dest = row['dest']
        cost = row['flight_cost']
        # Skip rows with missing data
        if not (year and month and day and origin and dest and cost):
            continue
        mettafile.write(f"! (flight {year} {month} {day} {origin} {dest} {cost})\n")

print(f"Metta facts written to {output_file} with ! at the start of each line.") 