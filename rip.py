import sys
import requests
import json

print(sys.argv)
response = requests.get("https://api.pokemontcg.io/v2/cards?q=number:{num}%20set.printedTotal:{printTotal}".format(num=sys.argv[1], printTotal=sys.argv[2]))
obj = json.loads(response.text)["data"][0]
print(obj["name"])
print(obj["types"][0])
print(obj["nationalPokedexNumbers"][0])

csvVal = "{num}/{printTotal},{natNumber},{name},{type}".format(num=sys.argv[1], printTotal=sys.argv[2], natNumber=obj["nationalPokedexNumbers"][0], name=obj["name"], type=obj["types"][0])

print(csvVal)

file1 = open("pokemon.csv", "a")  # append mode
file1.write(csvVal)
file1.close()
