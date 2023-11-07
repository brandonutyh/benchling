import argparse
import requests
import json

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('abilities', nargs='+', help='List of abilities to search for')
    return parser.parse_args()

args = parse_arguments()



def get_pokemon_data(ability):
    url = f'https://pokeapi.co/api/v2/ability/{ability}/'
    response = requests.get(url)

    #check code was successful
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed to fetch data for ability: {ability}")
        return None

#get name of pokemon
def extract_pokemon_info(ability_data):
    pokemon_info = []

    for pokemon in ability_data['pokemon']:
        # Extract the Pokémon name
        name = pokemon['pokemon']['name']

        # Extract items associated with the Pokémon
        items = []
        for item in pokemon['pokemon']['held_items']:
            items.append(item['item']['name'])

        # Extract known associates (if any)
        associates = []
        for associate in pokemon['pokemon']['known_associates']:
            associates.append(associate['name'])

        # Create a dictionary to store the extracted information
        pokemon_dict = {
            'name': name,
            'items': items,
            'known_associates': associates
        }

        # Append the Pokémon dictionary to the list
        pokemon_info.append(pokemon_dict)

    return pokemon_info

#formate into JSON format

# Fetch data for a specific ability
ability_data = get_pokemon_data('stench')

# Extract information for the ability
pokemon_info = extract_pokemon_info(ability_data)

# Format the output for this ability 
output = {
    'stench': pokemon_info
}

# Print or return the output as a JSON object
print(json.dumps(output, indent=2))  # Use 'json.dumps' to format the output
