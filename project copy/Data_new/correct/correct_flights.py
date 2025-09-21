import re
from datetime import datetime, timedelta
from collections import defaultdict

# Input/output files
input_file = "flights.metta"
output_file = "flights_updated.metta"

# Date range
start_date = datetime(2025, 9, 27)
end_date = datetime(2025, 10, 15)
date_range = (end_date - start_date).days + 1

# Dictionary to group flights by route (SRC-DEST)
routes = defaultdict(list)

# Step 1: Read and group flights by route
with open(input_file, "r") as f:
    for line in f:
        match = re.match(r"\(flight 2025 \d{2} \d{2} (\w+) (\w+) (.+)\)", line.strip())
        if match:
            src, dest = match.group(1), match.group(2)
            routes[(src, dest)].append(line.strip())

# Step 2: Assign new dates evenly across the range
updated_lines = []
for (src, dest), flights in routes.items():
    num_flights = len(flights)
    for i, flight in enumerate(flights):
        # Distribute evenly within date range
        offset = (i * date_range) // num_flights
        new_date = start_date + timedelta(days=offset)

        # Replace old date with new one
        updated_line = re.sub(
            r"\(flight 2025 \d{2} \d{2}",
            f"(flight 2025 {new_date.strftime('%m %d')}",
            flight
        )
        updated_lines.append(updated_line)

# Step 3: Write output
with open(output_file, "w") as f:
    f.write("\n".join(updated_lines))

print("✅ Flights updated and written to", output_file)
