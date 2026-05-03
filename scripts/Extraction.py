import requests

def total_pokemon():
    response_pokemon = requests.get("https://pokeapi.co/api/v2/pokemon").json()
    total_pokemon = response_pokemon["count"]
    return total_pokemon

def evolution_data(total_pokemon : int):
    results = []
    for id in range(1, total_pokemon + 1):
        response = requests.get(f"https://pokeapi.co/api/v2/evolution-chain/{id}/")
        if response.status_code != 200:
            continue
     
        response_evolution = response.json()

        evolution_chain = {
            'id'               : response_evolution['id'],
            'baby_trigger_item': response_evolution['baby_trigger_item'],
            'name'             : response_evolution['chain']['species']['name'],
            'is_baby'          : response_evolution['chain']['is_baby'],

            'evolves_to' : [
                {
                    'name' : evo['species']['name'],

                    'evolution_details' : [
                        {
                            'item'                 : detail['item'],
                            'trigger'              : detail['trigger']['name'],
                            'gender'               : detail['gender'],
                            'held_item'            : detail['held_item'],
                            'known_move'           : detail['known_move'],
                            'known_move_type'      : detail['known_move_type'],
                            'location'             : detail['location'],
                            'min_level'            : detail['min_level'],
                            'min_happiness'        : detail['min_happiness'],
                            'min_beauty'           : detail['min_beauty'],
                            'min_affection'        : detail['min_affection'],
                            'needs_overworld_rain' : detail['needs_overworld_rain'],
                            'party_species'        : detail['party_species'],
                            'party_type'           : detail['party_type'],
                            'relative_physical_stats': detail['relative_physical_stats'],
                            'time_of_day'          : detail['time_of_day'],
                            'trade_species'        : detail['trade_species'],
                            'turn_upside_down'     : detail['turn_upside_down'],
                        }
                        for detail in evo['evolution_details']
                    ]
                }
                for evo in response_evolution['chain']['evolves_to']
            ]
        }

    results.append(evolution_chain)

    return results

def species_data(total_pokemon : int):
    result = []
    for id in range(1, total_pokemon + 1):
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{id}/")
        if response.status_code != 200:
            continue
    response_species = response.json()

    pokemon_species = {
        "id"                     : response_species['id'],
        "name"                   : response_species['name'],
        "is_baby"                : response_species['is_baby'],
        "is_legendary"           : response_species['is_legendary'],
        "is_mythical"            : response_species['is_mythical'],
        "gender_rate"            : response_species['gender_rate'],
        "capture_rate"           : response_species['capture_rate'],
        "base_happiness"         : response_species['base_happiness'],  
        "has_gender_differences" : response_species['has_gender_differences'],
        "forms_switchable"       : response_species['forms_switchable'],
        "growth_rate"            : response_species['growth_rate']['name'],
        "egg_groups"             : ", ".join(x['name'] for x in response_species['egg_groups']),  
        "color"                  : response_species['color']['name'],
        "shape"                  : response_species['shape']['name'],
        "generation"             : response_species['generation']['name'],  
    }
    result.append(pokemon_species)

    return result

def pokemon_location(total_pokemon : int):
    result = []
    for id in range(1, total_pokemon + 1):
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{id}/encounters")
        if response.status_code != 200:
            continue

        response_encounters = response.json()
        encounters = [
        {
            'location_area': encounter['location_area']['name'],
            'version_details': [
                {
                    'version'         : version['version']['name'],
                    'max_chance'      : version['max_chance'],
                    'encounter_details': [
                        {
                            'min_level'  : detail['min_level'],
                            'max_level'  : detail['max_level'],
                            'chance'     : detail['chance'],
                            'method'     : detail['method']['name'],
                            'conditions' : [c['name'] for c in detail['condition_values']],
                        }
                        for detail in version['encounter_details']
                    ]
                }
                for version in encounter['version_details']
            ]
        }
        for encounter in response_encounters
    ]
    result.append(response_encounters)

    return result

def pokemon_form():

    result = []
    for id in range(1, total_pokemon + 1):
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon-form/{id}/")
        if response.status_code != 200:
            continue

        response_form = response.json()

        pokemon_form = {
        'id'            : response_form['id'],
        'name'          : response_form['name'],
        'order'         : response_form['order'],
        'form_order'    : response_form['form_order'],
        'is_default'    : response_form['is_default'],
        'is_battle_only': response_form['is_battle_only'],
        'is_mega'       : response_form['is_mega'],
        'form_name'     : response_form['form_name'],
        'pokemon_name'  : response_form['pokemon']['name'],
        'pokemon_url'   : response_form['pokemon']['url'],
        'types'         : [
            {
                'slot' : t['slot'],
                'type' : t['type']['name'],
            }
            for t in response_form['types']
        ],
        'version_group_details' : [
            vg['name'] for vg in response_form['version_group']['name']
        ],
    }
    result.append(response_form)

    return result

def pokemon_abilities():

    result = []

    response_abilities = requests.get("https://pokeapi.co/api/v2/ability?limit=10000").json()
    total_abilities = response_abilities['count'] 

    for id in range(1, total_abilities + 1):
        response_ability = requests.get(f"https://pokeapi.co/api/v2/ability/{id}/").json()

    ability = {
        'id'            : response_ability['id'],
        'name'          : response_ability['name'],
        'is_main_series': response_ability['is_main_series'],
        'generation'    : response_ability['generation']['name'],
        'names'         : [
            n['name']
            for n in response_ability['names']
            if n['language']['name'] == 'en'
        ],
        'effect_entries': [
            {
                'effect'       : e['effect'],
                'short_effect' : e['short_effect'],
            }
            for e in response_ability['effect_entries']
            if e['language']['name'] == 'en'
        ],
        'effect_changes': [
            {
                'version_group' : ec['version_group']['name'],
                'effect'        : [
                    e['effect']
                    for e in ec['effect_entries']
                    if e['language']['name'] == 'en'
                ]
            }
            for ec in response_ability['effect_changes']
        ],
        'pokemon'       : [
            {
                'is_hidden'    : p['is_hidden'],
                'slot'         : p['slot'],
                'pokemon_name' : p['pokemon']['name'],
                'pokemon_url'  : p['pokemon']['url'],
            }
            for p in response_ability['pokemon']
        ],
    }

    result.append(ability)

    return result