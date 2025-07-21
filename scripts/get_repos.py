import yaml
import requests

# COLORS
ERROR = "\033[91m"
PROGRESS = "\033[93m"
SUCCESS = "\033[92m"
NORMAL = "\033[37m"

with open("./data/ctf_ids.yaml", "r") as file:
    CTF_IDS = yaml.safe_load(file).values()
    CTF_DATA = []
    keys = ['title', 'start', 'finish', 'weight']
    for CTF in CTF_IDS:
        try:
            req_url = f"https://ctftime.org/api/v1/events/{CTF['ctftime_id']}/"
            headers = {
             'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0',
             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
             'Accept-Language': 'en-US,en;q=0.5',
             'DNT': '1',
             'Sec-GPC': '1',
             'Connection': 'keep-alive',
             'Upgrade-Insecure-Requests': '1',
             'Sec-Fetch-Dest': 'document',
             'Sec-Fetch-Mode': 'navigate',
             'Sec-Fetch-Site': 'none',
             'Sec-Fetch-User': '?1',
             'Priority': 'u=0, i',
            }
            
            print(PROGRESS, "[~] Fetching Data for ctftime_id ", CTF['ctftime_id'])
            res = requests.get(req_url, headers=headers)

            if res.status_code == 200:
                print(SUCCESS, "[+] Response received from ", req_url, "with status", res.status_code)
                info = {
                    x:res.json()[x] for x in keys
                }
                info['comments'] = CTF['comments']
                info['position'] = CTF['position']
                info['team_name'] = CTF['team_name']
                CTF_DATA.append(info)
            else:
                print(ERROR, "[-] ERROR: ", res.status_code)
        except:
            print(ERROR, "[-] ERROR: an error occurred")
        with open("./data/ctf_data.yaml", "w") as data_file:
            yaml.dump(CTF_DATA, data_file)

            
