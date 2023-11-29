import requests
import json
import os

def download_api(api_url, json_name='data.json', file_dirrectory='json_data'):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        json_data = response.json()

        save_path = f'{file_dirrectory}/{json_name}'

        # Create the 'JSON' directory if it doesn't exist
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with open(save_path, 'w', encoding='utf-8') as file:
            json.dump(json_data, file, indent=4)
        return json_data
    
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        return {}

if __name__ == '__main__':
    api_url = 'https://www.speedrun.com/api/v1/games/nd2eqrd0'
    json_name = 'data.json'
    file_dirrectory = 'SRC_data'
    download_api(api_url, json_name, file_dirrectory)