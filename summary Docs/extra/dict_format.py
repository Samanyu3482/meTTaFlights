from hyperon import *

metta = MeTTa()

transcript = "[[(, (transcribed_to (gene ENSG00000166913) (transcript ENST00000372839))), (, (transcribed_to (gene ENSG00000166913) (transcript ENST00000353703)))]]"

parsed = metta.parse_all(transcript)
result = []

for p in parsed:
    if (type(p) == ExpressionAtom):
        x = p.get_children()[1].get_children()
        temp1 = x[1].get_children()
        source = f"{metta.parse_single(f"{temp1[0]}")} {metta.parse_single(f"{temp1[1]}")}"
        temp2 = x[2].get_children()
        target = f"{metta.parse_single(f"{temp2[0]}")} {metta.parse_single(f"{temp2[1]}")}"
        
        dict = {'edge': x[0],
                'source': source,
                'target': target,
                }
        result.append(dict)
print(result)