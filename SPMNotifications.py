from download_api import *
import time
import requests

base_url = 'https://www.speedrun.com/api/v1/'
endpoint = f'runs?game=nd2eqrd0&status=new'

endpoint1 = f'runs?game=nd2eqrd0&status=new'
endpoint2 = f'runs?game=m1mxlv46&status=new'

notified_runs = set()

notified_runs_file = 'notified_runs.txt'

string_game_name = None
string_category_name = None

file_path = 'C:\webhook.txt'
with open(file_path, 'r') as file:
    file_content = file.read()

def id_to_name():
    global string_game_name, string_category_name
    if game_name == "Game ID: nd2eqrd0":
        string_game_name = "Super Paper Mario"
    elif game_name == "Game ID: m1mxlv46":
        string_game_name = "Super Paper Mario CE"
    if category_name == "Category ID: z276lzd0":
        string_category_name = "Any%"
    elif category_name == "Category ID: jdrpr702":
        string_category_name = "100%"
    elif category_name == "Category ID: z27ln80d":
        string_category_name = "All Pixls"
    elif category_name == "Category ID: xk9nqrg2":
        string_category_name = "New Game"
    elif category_name == "Category ID: n2yjl0z2":
        string_category_name = "Flipside Pit of 100 Trials"
    elif category_name == "Category ID: jdz7003k":
        string_category_name = "Defeat Shadoo"
    elif category_name == "Category ID: z27r9p4d":
        string_category_name = "999 Coins"
    elif category_name == "Category ID: jdrv0xn2":
        string_category_name = "All Maps"
    elif category_name == "Category ID: q25gv0gd":
        string_category_name = "Glitchless"
    elif category_name == "Category ID: wk687xr2":
        string_category_name = "Game Over"
    elif category_name == "Category ID: 82408znd":
        string_category_name = "All Items"
    elif category_name == "Category ID: xd11z38d":
        string_category_name = "Multiplayer Any%"
    elif category_name == "Category ID: wk6635ek":
        string_category_name = "Any% NG+"
    elif category_name == "Category ID: 9d8yj73k":
        string_category_name = "Red & Green Bridge Skip"
    elif category_name == "Category ID: wdmory4k":
        string_category_name = "Flipside Pit: Boomerless"
    elif category_name == "Category ID: vdogy9o2":
        string_category_name = "Feed the Meatball"

def save_notified_runs():
    with open(notified_runs_file, 'w') as file:
        file.write('\n'.join(notified_runs))

def load_notified_runs():
    try:
        with open(notified_runs_file, 'r') as file:
            return set(file.read().splitlines())
    except FileNotFoundError:
        return set()

notified_runs = load_notified_runs()

def send_discord_webhook(run_id):
    webhook_url = f"{file_content}"
    message = f'<@&480158412064292864> New run for {string_game_name} - {string_category_name} is avalible for verification!' # <@&480158412064292864>
    payload = {'content': message}
    response = requests.post(webhook_url, json=payload)

    if response.status_code == 200 or response.status_code == 204:
        print(f"Discord webhook sent successfully for run ID: {run_id}")
        notified_runs.add(run_id)
    else:
        print(f"Error sending Discord webhook. Status Code: {response.status_code}")

while True:
    url = f'{base_url}{endpoint}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        for run in data['data']:
            print(f"Run Data: {run}")
            run_id = run.get('id', 'Unknown Run ID')

            if run_id in notified_runs:
                continue

            if 'game' in run:
                if isinstance(run['game'], dict):
                    game_data = run['game'].get('data', {})
                else:
                    downloaded_data = download_api(run['game'])
                    game_data = downloaded_data.get('data', {}) if downloaded_data else {}
            else:
                game_data = {}

            game_name = game_data.get('names', {}).get('international')

            if not game_name:
                game_name = f'Game ID: {run.get("game", "Unknown Game ID")}'

            if 'category' in run:
                if isinstance(run['category'], dict):
                    category_data = run['category'].get('data', {})
                else:
                    downloaded_data = download_api(run['category'])
                    category_data = downloaded_data.get('data', {}) if downloaded_data else {}
            else:
                category_data = {}

            category_name = category_data.get('name')

            if not category_name:
                category_name = f'Category ID: {run.get("category", "Unknown Category ID")}'

            id_to_name()

            print(f"Run for {string_game_name} - {string_category_name}, Run ID: {run_id}, Status: {run.get('status', {}).get('status', 'Unknown Status')}")

            print(f"New run submitted for {string_game_name} - {string_category_name}")

            with open('notified_runs.txt', 'r') as file:
                notified_runs = set(file.read().splitlines())

            if run_id not in notified_runs:
                send_discord_webhook(run_id)
            else:
                print(f"Run ID: {run_id} has already been notified.")
            save_notified_runs()
            
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
    if endpoint == endpoint1:
        endpoint = endpoint2
    elif endpoint == endpoint2:
        endpoint = endpoint1
        
    if endpoint == endpoint2:
        time.sleep(60)