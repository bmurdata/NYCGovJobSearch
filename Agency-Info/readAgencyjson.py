import json

jsonfile="Agency_json.json"

json_outpu="second.json"

# Combine agency lists with same names but trailing spaces

with open(jsonfile,"r") as ifile:

    data=json.load(ifile)

    #Make a Dictionary to combine into new JSON
    agency_dict=dict()
    for item in data:
        stripped=item['address'].strip()
        if stripped in agency_dict:
            print(stripped + " already in dictionary")
            
        else:
            print(stripped+" is not in dictionary")
            agency_dict[stripped]=item['dpt']
    print(len(agency_dict))
    print(len(data))
    with open(json_outpu,"w") as ofile:
        json.dump(agency_dict,ofile)
