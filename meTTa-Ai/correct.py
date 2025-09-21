import re
from datetime import datetime, timedelta
from collections import defaultdict

# Input/output
input_file = "flightsas.metta"
output_file = "flights.metta"

# Date range
start_date = datetime(2025, 9, 27)
end_date = datetime(2025, 10, 15)
date_range = (end_date - start_date).days + 1

# Group by route (SRC-DEST)
routes = defaultdict(list)

pattern = re.compile(
    r"\(flight 2025 \d{2} \d{2} (\w+) (\w+) (\d+) (\d{4}) (\d{4}) ([A-Za-z_]+)\)"
)

# Step 1: Read and group flights
with open(input_file, "r") as f:
    for line in f:
        line = line.strip()
        match = pattern.match(line)
        if match:
            src, dest = match.group(1), match.group(2)
            routes[(src, dest)].append(line)

# Step 2: Assign new dates
updated_lines = []
for (src, dest), flights in routes.items():
    num_flights = len(flights)
    for i, flight in enumerate(flights):
        # Spread dates evenly
        offset = (i * date_range) // num_flights
        new_date = start_date + timedelta(days=offset)

        # Replace only year-month-day
        updated_line = re.sub(
            r"\(flight 2025 \d{2} \d{2}",
            f"(flight 2025 {new_date.strftime('%m %d')}",
            flight
        )
        updated_lines.append(updated_line)

# Step 3: Write output
with open(output_file, "w") as f:
    f.write("\n".join(updated_lines))

print("✅ Flights updated with new dates (airlines preserved).")
