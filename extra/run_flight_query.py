















from hyperon import MeTTa, ExpressionAtom
import os
import sys

# Initialize MeTTa
metta = MeTTa()
metta.run("!(bind! &space (new-space))")

print("\n✅ Testing manual atom injection...")
metta.run("!(add-atom &space (flight 2013 1 1 LGA IAD 150))")

test_result = metta.run("!(match &space (flight 2013 1 1 LGA IAD ?cost))")
print("\n✅ TEST QUERY RESULT (should show one match):", test_result)


# --- Load Flights Data (Clean and Inject) ---
original_file = "flights.metta"
if not os.path.exists(original_file):
    print("Flights data file not found!")
    sys.exit(1)

fact_count = 0
with open(original_file, "r") as infile:
    for line in infile:
        line = line.strip()
        if line.startswith("!"):
            line = line[1:].strip()
        if line.startswith("(flight"):
            metta.run(f'!(add-atom &space {line})')
            fact_count += 1


print(f"\nDEBUG: Loaded {fact_count} flight facts.")

# Load rules
rules_file = "find_flights.metta"
if os.path.exists(rules_file):
    metta.run(f'!(load-ascii &space "{rules_file}")')
else:
    print(f"File not found: {rules_file}")
    sys.exit(1)

print("\nDEBUG: Dumping first 10 atoms:")
dump_results = metta.run("!(dump &space)")

if dump_results and isinstance(dump_results[0], list):
    printed = 0
    for group in dump_results:
        for atom in group:
            print(atom)
            printed += 1
            if printed >= 10:
                break
        if printed >= 10:
            break
else:
    print("Failed to dump actual atoms.")


# --- Take user input ---
try:
    year = int(input("Enter year (e.g., 2013): "))
    month = int(input("Enter month (1-12): "))
    day = int(input("Enter day (1-31): "))
    source = input("Enter source airport code (e.g., JFK): ").strip().upper()
    dest = input("Enter destination airport code (e.g., MIA): ").strip().upper()
except Exception as e:
    print(f"Input error: {e}")
    sys.exit(1)

# --- Queries ---
direct_query = f"!(match &space (flight {year} {month} {day} {source} {dest} ?cost))"
path_query = f"!(match &space (path {year} {month} {day} {source} {dest} ?route))"
print("DEBUG Final Direct Query:", direct_query)

# Execute queries
direct_results = metta.run(direct_query)
path_results = metta.run(path_query)

print("\nDEBUG Direct Query Raw:", direct_results)
print("DEBUG Path Query Raw:", path_results)

# --- Parse direct flights ---
direct_flights = []
for match_group in direct_results:
    for res in match_group:
        if isinstance(res, ExpressionAtom):
            children = res.get_children()
            if len(children) == 6:
                direct_flights.append({
                    'from': str(children[4]),
                    'to': str(children[5]),
                    'cost': int(str(children[-1])) if str(children[-1]).isdigit() else 0
                })

# --- Parse paths and compute cost ---
paths = []
for match_group in path_results:
    for res in match_group:
        if isinstance(res, ExpressionAtom):
            children = res.get_children()
            if len(children) == 6:
                route_atom = children[5]
                route_list = [str(atom) for atom in route_atom.get_children()]
                total_cost = 0
                for i in range(len(route_list) - 1):
                    src = route_list[i]
                    dst = route_list[i + 1]
                    cost_query = f"!(match &space (flight {year} {month} {day} {src} {dst} ?c))"
                    cost_result = metta.run(cost_query)
                    if cost_result and cost_result[0]:
                        for cr in cost_result[0]:
                            if isinstance(cr, ExpressionAtom):
                                cost_children = cr.get_children()
                                if len(cost_children) == 6:
                                    total_cost += int(str(cost_children[-1]))
                paths.append({'route': route_list, 'cost': total_cost})

# Sort paths by cost
paths.sort(key=lambda x: x['cost'])

# --- Display results ---
print("\n================= RESULTS =================")
if direct_flights:
    print(f"\nDirect flights from {source} to {dest} on {year}-{month}-{day}:")
    for f in direct_flights:
        print(f"From: {f['from']} To: {f['to']} Cost: {f['cost']}")
else:
    print("\nNo direct flights found for the given input.")

if paths:
    print(f"\nAvailable flight paths from {source} to {dest} on {year}-{month}-{day} (sorted by cost):")
    for p in paths:
        print(f"Route: {' -> '.join(p['route'])}, Cost: {p['cost']}")
else:
    print("\nNo available paths found for the given input.")
