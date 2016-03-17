# ------------------------
# View object definition
# ------------------------
# {
#     'name': 'Cache file name',
#     'base': 'Base JSON file containing all the resources for a model',
#     'save': 'location to save files',
#     'details': {
#         'defaults': [list of field names here],
#         'conditions': {dict of field names, lambda predicate} MUST HAVE default FIELD
#     }
# }
# ------------------------
# Available Fields
# ------------------------
# Person
#   - hometown
#   - birth_date
#   - games (list of dicts)
#   - country
#   - death_date
#   - deck
#   - name
#   - gender
#   - first_credited_game
#   - id
#   - people (list of dicts)
# Company
#   - name
#   - id
#   - location_address
#   - image
#   - people (list of dicts)
#   - location_city
#   - published_games (list of dicts)
#   - location_country
#   - website
#   - deck
#   - date_founded
#   - developed_games (list of dicts)
#   - location_state
# Game
#   - name
#   - deck
#   - image
#   - people
#   - id
#   - publishers
#   - platforms
#   - similar_games
views = [
    {
        # Include enough info for a 'full' developer profile
        # Made more than 5 games
        'name': 'Robust Developers',
        'base': 'companies.json',
        'save': 'developers/robust/',
        'details': {
            'defaults': [
                'name', 'date_founded', 'deck', 'image',
                'location_city', 'location_country'
            ],
            'conditions': {
                'developed_games': lambda x: len(x) >= 5,
                'people': lambda x: len(x) >= 1,
                'default': lambda x: x is not None
            }
        }
    },
    {
        # Include enough info for a 'minimum' developer profile
        'name': 'Developers w/ min fields',
        'base': 'companies.json',
        'save': 'developers/min/',
        'details': {
            'defaults': [
                    'name', 'date_founded',
                    'location_city', 'location_country'
            ],
            'conditions': {
                'developed_games': lambda x: len(x) >= 1,
                'people': lambda x: len(x) >= 1,
                'default': lambda x: x is not None
            }
        }
    }
] # END VIEWS
