



from hyperon import *

def parse_flight_file(filepath):
    metta = MeTTa()
    result = []

   
    with open(filepath, 'r') as f:
        data = f.read()

   
    parsed = metta.parse_all(data)

    for expr in parsed:
        if isinstance(expr, ExpressionAtom):
            parts = expr.get_children()  
            
            edge = str(metta.parse_single(f"{parts[0]}"))      
            year = str(metta.parse_single(f"{parts[1]}"))
            month = str(metta.parse_single(f"{parts[2]}"))
            day = str(metta.parse_single(f"{parts[3]}"))
            source = str(metta.parse_single(f"{parts[4]}"))
            target = str(metta.parse_single(f"{parts[5]}"))
            cost = str(metta.parse_single(f"{parts[6]}"))

            result.append({
                'edge': edge,
                'date': f"{year} {month} {day}",
                'source': source,
                'target': target,
                'cost': cost
            })

    return result



flights = parse_flight_file("Data/flights.metta")
print(f"Total flights parsed: {len(flights)}")
print(flights[:5]) 
