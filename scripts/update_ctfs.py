import re
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import yaml


def slugify(text: str) -> str:
    """Converts event name into a clean YAML key (e.g. 'scriptCTF 2026' -> 'scriptCTF-2026')."""
    text = re.sub(r"[^\w\s-]", "", text).strip()
    return re.sub(r"[\s_]+", "-", text)


def fetch_ctftime_events(team_id_or_url: str) -> list[dict]:
    if team_id_or_url.isdigit():
        url = f"https://ctftime.org/team/{team_id_or_url}"
    else:
        url = team_id_or_url

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    events = []

    # Parse all event rows across all rating year tabs
    for row in soup.find_all("tr"):
        place_td = row.find("td", class_="place")
        link_a = row.find("a", href=re.compile(r"^/event/\d+"))

        if place_td and link_a:
            try:
                position = int(place_td.text.strip())
                event_id = int(re.search(r"\d+", link_a["href"]).group())
                event_name = link_a.text.strip()

                events.append({
                    "name": event_name,
                    "ctftime_id": event_id,
                    "position": position,
                })
            except (ValueError, AttributeError):
                continue

    return events


def sync_yaml(yaml_file: str, events: list[dict], default_team_name: str = "libbabel.so"):
    path = Path(yaml_file)
    data = {}

    if path.exists() and path.stat().st_size > 0:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

    # Gather existing ctftime_ids to avoid duplicates while preserving existing data
    existing_ids = {
        item.get("ctftime_id")
        for item in data.values()
        if isinstance(item, dict) and "ctftime_id" in item
    }

    new_entries_count = 0

    for event in events:
        if event["ctftime_id"] in existing_ids:
            continue

        key = slugify(event["name"])

        # Prevent key collision if two different CTFs slugify to the same key
        base_key = key
        counter = 1
        while key in data:
            key = f"{base_key}-{counter}"
            counter += 1

        data[key] = {
            "ctftime_id": event["ctftime_id"],
            "position": event["position"],
            "team_name": default_team_name,
            "comments": "",
        }

        existing_ids.add(event["ctftime_id"])
        new_entries_count += 1

    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)

    print(f"[+] Done. Added {new_entries_count} new CTF(s) to {yaml_file}.")


if __name__ == "__main__":
    team_input = "395398"
    yaml_path = "./data/ctf_ids.yaml"
    team_name = "libbabel.so"

    scraped_events = fetch_ctftime_events(team_input)
    sync_yaml(yaml_path, scraped_events, default_team_name=team_name)
