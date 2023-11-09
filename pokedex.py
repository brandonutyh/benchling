#!/usr/bin/python3
import requests
import json
import sys
from pprint import pprint


def find_known_associates(target, allNames):
    """Given target pokemon name, find relaed pokemon, in same "species"

    Args:
        target (string): pokemon to be examined
        allNames (_type_): all the existing pokemon names

    Returns:
        list: all related pokemon to the target
    """
    base_name = target.split('-')[0]
    return [name for name in allNames if ((base_name in name.split('-')) and (target != name))]


def find_items(target):
    """Find the items that the target pokemon could be holding, also returns and saves the height.

    Args:
        target (string): pokemon to be examined

    Returns:
        string: items the target has as well as it's height
    """
    url = f'https://pokeapi.co/api/v2/pokemon/{target}'
    result = requests.get(url).json()
    pokeItems =  [d.get('item', {}).get('name', None) for d in result['held_items']]
    height = result.get("height")
    return pokeItems, height
 
def get_data(url):
    """gets data in json format from API request

    Args:
        url (string): url to API

    Returns:
        the data from the API call, or exception if there is error
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None


def final_result(abilities):
    """Final method outputting the results given the ability input

    Args:
        abilities (list): list of the abilities to be examined
    """
    url = f'https://pokeapi.co/api/v2/pokemon/?limit=2000'
    pokedex = get_data(url)
    #pokedex = requests.get(url).json()
    
    allNames = set([d.get('name') for d in pokedex['results']])
    finalResult = {}
    for ability in abilities:
        ability_url = f'https://pokeapi.co/api/v2/ability/{ability}'
        result = get_data(ability_url)
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
    final_result(arg)
