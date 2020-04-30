import json
import re

from PIL import Image

import modules.basics as basics
from modules import utility, ccc
import os

def getclothing():
    with open('json/ch_clothing.json') as f:
        return json.load(f)

def getdepths():
    with open('json/ch_depths.json') as f:
        return json.load(f)

def getdefaults():
    with open('json/ch_defaults.json') as f:
        return json.load(f)

def getmappings():
    with open('json/ch_mappings.json') as f:
        return json.load(f)

def determineclothing(bot, uid, s):
    errorreport = ""
    clothingapplied = []
    clothingdb = getclothing()
    layers = []
    slots = {}

    for k,i in clothingdb.items():
        layers.append(
            {
                "ret": k,
                "equals":
                    [
                        [k], [i["name"]]
                    ]
            }
        )

    for x in s.split("\n"):
        match = re.search(r"^(\w+)(\W+?\w+\W+?\w+)*\s*$", x)
        if match is None:
            errorreport += f"Invalid syntax in {basics.spitback(x)}. You want `CLOTHING` or `CLOTHING SECTION TEXTURE SECTION TEXTURE`.\n"
            continue

        currentclothing = utility.layeredsearch(layers, match.group(1))
        if currentclothing is None:
            errorreport += f"I wasn't able to figure out what clothing you meant by {basics.spitback(match.group(1))}.\n"
        else:
            clothingapplied.append(currentclothing)
            for slot in clothingdb[currentclothing]["slots"]:
                slots.setdefault(slot, [])
                slots[slot].append(currentclothing)

    for k,i in slots.items():
        if len(i)>1:
            l = []
            for x in i:
                l.append(clothingdb[x]['name'])
            errorreport+=f"You have {len(i)} items in the {k} slot: {ccc.andstr(l)}. You can only have one.\n"

    if errorreport:
        raise Exception('InvalidClothingError', errorreport)

    return clothingapplied, slots

def editclothingperhippo(clothingapplied, slotsused, hippos=[]):
    clothing = getclothing()
    print(slotsused)
    #Defaults
    for x in getdefaults():
        print(x)
        print(clothing[x]["slots"][0])
        if clothing[x]["slots"][0] not in slotsused:
            slotsused[clothing[x]["slots"][0]] = [x]
            clothingapplied.append(x)
    print(clothingapplied)
    #Special
    ret={}
    mappings = getmappings()
    for hippo in hippos:
        l = list(clothingapplied)
        if hippo in mappings:
            for c in mappings[hippo]:
                for slot in clothing[c]["slots"]:
                    if slot in slotsused:
                        for y in slotsused[slot]:
                            try:
                                l.remove(y)
                            except ValueError:
                                pass
                l.append(c)
        ret[hippo] = l
    return ret

def determinelayers(clothingperhippo):
    layers = []
    depths = getdepths()
    needed = set() # What combinations are needed

    allclothing = set()
    for k,i in clothingperhippo.items():
        allclothing |= set(i)

    for frame in range(1):
        for depth in depths:
            for cloth in allclothing:
                d = os.listdir(f"images/ch/masks/{cloth}/{frame}")
                for base in ["out"]+[f"layer{x}" for x in range(len(d))]:
                    if f"{base}{depth}.png" in d:
                        # Actual placement
                        hippos = set()
                        for k,i in clothingperhippo.items():
                            if cloth in i:
                                hippos.add(k)
                                appliesto = {
                                "frames": {frame},
                                "hippos": hippos
                            }
                        if len(layers)==0 or appliesto != layers[-1]["appliesto"]:
                            layers.append({
                                "img": [],
                                "appliesto": appliesto
                            })
                        layers[-1]["img"].append( f"images/ch/masks/{cloth}/{frame}/{base}{depth}.png")
                        # Get needed
                        for h in hippos:
                            needed.add((h, frame))
    return layers, needed

def imagesfromlayers(layers):
    for layer in layers:
        img = Image.new("RGBA", (980,980), (0,0,0,0))
        for i in layer["img"]:
            img = Image.alpha_composite(img, Image.open(i).convert("RGBA"))
        layer["img"] = img
    return layers

def combineimages(layers, needed):
    ret = {}
    for x in needed:
        ret[x] = Image.new("RGBA", (980,980), (0,0,0,0))
        for layer in layers:
            if x[0] in layer["appliesto"]["hippos"] and x[1] in layer["appliesto"]["frames"]:
                ret[x] = Image.alpha_composite(ret[x], layer["img"])
    return ret