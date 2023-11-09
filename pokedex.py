import requests
import json
import sys
from pprint import pprint


def find_known_associates(target, allNames):
    base_name = target.split('-')[0]
    return [name for name in allNames if ((base_name in name.split('-')) and (target != name))]


def find_items(target):
    url = f'https://pokeapi.co/api/v2/pokemon/{target}'
    result = requests.get(url).json()
    pokeItems =  [d.get('item', {}).get('name', None) for d in result['held_items']]
    height = result.get("height")
    return pokeItems, height\




def finalResult(abilities):
    url = f'https://pokeapi.co/api/v2/pokemon/?limit=2000'
    pokedex = requests.get(url).json()
    
    allNames = set([d.get('name') for d in pokedex['results']])
    finalResult = {}
    for ability in abilities:
        url = f'https://pokeapi.co/api/v2/ability/{ability}'
        result = requests.get(url).json()
        pokemonWithAbility = [d.get('pokemon', {}).get('name', None) for d in result.get("pokemon")]
        abilityResult = []
        heightDict = {}
        minHeight = 999999999999999999999
        maxHeight = -9999999999999999999
        for pokemon in pokemonWithAbility:
            items, height = find_items(pokemon)
            heightDict[pokemon] = height
            pokemonResult = {"name" : pokemon, "known_associates" : find_known_associates(pokemon, allNames), "items" : items}
            abilityResult.append(pokemonResult)
        biggestHeights = []
        smallestHeights = []
        for pokemon, height in heightDict.items():
            if height > maxHeight:
                biggestHeights = [pokemon]
                maxHeight = height
            if height == maxHeight:
                biggestHeights.append(pokemon)
            if height < minHeight:
                smallestHeights = [pokemon]
                minHeight = height
            if height == minHeight:
                smallestHeights.append(pokemon)
        for pokemonResult in abilityResult:
            if pokemonResult["name"] in biggestHeights:
                pokemonResult["tallest"] = True
            if pokemonResult["name"] in smallestHeights:
                pokemonResult["shortest"] = True
        finalResult[ability] = abilityResult
    pprint(finalResult)
        
if __name__ == "__main__":
    #test
    arg = sys.argv[1:]
    finalResult(arg)
