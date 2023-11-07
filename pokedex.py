import argparse
import requests

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('abilities', nargs='+', help='List of abilities to search for')
    return parser.parse_args()

args = parse_arguments()



def get_pokemon_data(ability):
    url = f'https://pokeapi.co/api/v2/ability/{ability}/'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed to fetch data for ability: {ability}")
        return None

print(get_pokemon_data(["stench"]))