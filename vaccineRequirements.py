# Program to write Vaccine requirement to JSON file

import json

requirements = {
    "bordatella": 6,
    "rabies": 36,
    "dhpp": 36,
    "altered": True,
    "fecal_test": 12
}

with open("vaccineRequirements.JSON", "w") as outfile:
    json.dump(requirements, outfile)

