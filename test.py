import json

with open("Retseptid.json", "r", encoding="utf-8") as fail:
    retseptid = json.load(fail)


def kuva_retsept(retsept):
    print("Retsept:", retsept["nimi"])
    print("Portsjonid:", retsept["portsioonid"])
    
    print("\nKoostisosad:")
    for koostisosa in retsept["koostisosad"]:
        print("-", koostisosa["nimi"] + ":",
              koostisosa["kogus"], koostisosa["ühik"])
    
    print("\nValmistamine:")
    number = 1
    for samm in retsept["valmistamine"]:
        print(str(number) + ".", samm)
        number += 1


for retsept in retseptid:
    print(retsept["id"], "-", retsept["nimi"])
    
kuva_retsept(retseptid[9])