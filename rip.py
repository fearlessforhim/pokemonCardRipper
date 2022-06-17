import sys
import requests
import json
import time

f = open("numbers.txt", "r")
for x in f:
    line = x.replace("\n", "")
    print(line)

    try:
        response = requests.get("https://api.pokemontcg.io/v2/cards?q=number:{num}%20set.printedTotal:{printTotal}".format(num=line.split("/")[0], printTotal=line.split("/")[1]))
        obj = json.loads(response.text)["data"][0]

        normalPrice = 0
        holoFoilPrice = 0
        reverseHoloFoilPrice = 0

        if obj["tcgplayer"]["prices"].get("normal") is not None:
          normalPrice = obj["tcgplayer"]["prices"]["normal"]["market"]

        if obj["tcgplayer"]["prices"].get("reverseHolofoil") is not None:
          reverseHoloFoilPrice = obj["tcgplayer"]["prices"]["reverseHolofoil"]["market"]

        if obj["tcgplayer"]["prices"].get("holofoil") is not None:
          holoFoilPrice = obj["tcgplayer"]["prices"]["holofoil"]["market"]

        csvVal = "{num},{printTotal},{natNumber},{name},{type},{normalPrice},{reverseHoloFoilPrice},{holoFoilPrice},{priceUpdated}\n".format(num=line.split("/")[0], printTotal=line.split("/")[1], natNumber=obj["nationalPokedexNumbers"][0], name=obj["name"], type=obj["types"][0], normalPrice=normalPrice, reverseHoloFoilPrice=reverseHoloFoilPrice, holoFoilPrice=holoFoilPrice, priceUpdated=obj["tcgplayer"]["updatedAt"])

        file1 = open("pokemon.csv", "a")  # append mode
        file1.write(csvVal)
        file1.close()
    except:
        print("Failed!")
        csvVal = "{num},{printTotal},???,???,???,???,???,???,???\n".format(num=line.split("/")[0], printTotal=line.split("/")[1])

        file1 = open("pokemon.csv", "a")  # append mode
        file1.write(csvVal)
        file1.close()

    time.sleep(2)
