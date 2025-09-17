from hyperon import MeTTa

metta=MeTTa()



# a=metta.run('!(+ 1 2)')
# print(a)

# print(metta.run('(john isParentOf mary)'))
# print(metta.run('(elisa isParentOf mary)'))
# print(metta.run('!(match &self ($x isParentOf mary) $x)'))

with open("family.metta") as file:
    metta.run(file.read())

    output=metta.run('!(isSibling adam monica)')

    print(output)

    