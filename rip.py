import sys
import requests
import json
import time

f = open(sys.argv[1], "r")
logOnly = False

try:
    logOnly = sys.argv[2] == "logOnly"
except:
    pass

for x in f:
    line = x.replace("\n", "")
    print(line)

    try:
        response = None
        num = line.split("/")[0]
        printTotal = line.split("/")[1]
        if len(line.split("/")) > 2:
            response = requests.get("https://api.pokemontcg.io/v2/cards?q=number:{num}%20set.printedTotal:{printTotal}%20name:{name}".format(num=num, printTotal=printTotal, name=line.split("/")[2]))
        else:
            response = requests.get("https://api.pokemontcg.io/v2/cards?q=number:{num}%20set.printedTotal:{printTotal}".format(num=num, printTotal=printTotal))

        raw = json.loads(response.text)["data"]
        if len(raw) > 1:
            print("-----------multiple!-----------")
            continue
        obj = raw[0]

        normalPrice = 0
        holoFoilPrice = 0
        reverseHoloFoilPrice = 0

        if obj["tcgplayer"]["prices"].get("normal") is not None:
          normalPrice = obj["tcgplayer"]["prices"]["normal"]["market"]

        if obj["tcgplayer"]["prices"].get("reverseHolofoil") is not None:
          reverseHoloFoilPrice = obj["tcgplayer"]["prices"]["reverseHolofoil"]["market"]

        if obj["tcgplayer"]["prices"].get("holofoil") is not None:
          holoFoilPrice = obj["tcgplayer"]["prices"]["holofoil"]["market"]

        csvVal = "{num},{printTotal},{natNumber},{name},{type},{setName},{normalPrice},{reverseHoloFoilPrice},{holoFoilPrice},{priceUpdated}\n".format(num=line.split("/")[0], printTotal=line.split("/")[1], natNumber=obj["nationalPokedexNumbers"][0], name=obj["name"], type=obj["types"][0], setName=obj["set"]["name"], normalPrice=normalPrice, reverseHoloFoilPrice=reverseHoloFoilPrice, holoFoilPrice=holoFoilPrice, priceUpdated=obj["tcgplayer"]["updatedAt"])

        if logOnly:
            print(csvVal)
        else:
            file1 = open("pokemon.csv", "a")  # append mode
            file1.write(csvVal)
            file1.close()
    except:
        print("-----------Failed!-----------")
        csvVal = "{num},{printTotal},???,???,???,???,???,???,???\n".format(num=line.split("/")[0], printTotal=line.split("/")[1])

        if logOnly:
            print("")
        else:
            file1 = open("pokemon.csv", "a")  # append mode
            file1.write(csvVal)
            file1.close()

    time.sleep(2)
