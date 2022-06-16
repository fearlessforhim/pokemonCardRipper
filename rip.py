import sys
import requests
import json


f = open("numbers.txt", "r")
for x in f:
  line = x.replace("\n", "")

  response = requests.get("https://api.pokemontcg.io/v2/cards?q=number:{num}%20set.printedTotal:{printTotal}".format(num=line.split("/")[0], printTotal=line.split("/")[1]))
  obj = json.loads(response.text)["data"][0]

  csvVal = "{num}/{printTotal},{natNumber},{name},{type}\n".format(num=line.split("/")[0], printTotal=line.split("/")[1], natNumber=obj["nationalPokedexNumbers"][0], name=obj["name"], type=obj["types"][0])

  file1 = open("pokemon.csv", "a")  # append mode
  file1.write(csvVal)
  file1.close()
  print(".", end="", flush=True)
