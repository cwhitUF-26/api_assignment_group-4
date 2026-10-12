import json
from typing import Any

import requests

SERVICE_URL = 'https://emojihub.yurace.pro/api'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
TIMEOUT_SECONDS = 15

def fetch_emoji_data(session: requests.Session, emoji_type: str) -> list[dict[str, Any]] | None:
    url = f"{SERVICE_URL}/all/category/{emoji_type}"
    print('Retrieving', url)

    try:
        response = session.get(url, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
        print('Retrieved', len(response.text), 'characters')
        return response.json()
    except requests.exceptions.RequestException as err:
        print('Request error:', err)
        return None
    except ValueError:
        print('Response did not contain valid JSON.')
        return None
    
def print_emojis(emojis: list[dict[str, Any]]) -> None:
    print(json.dumps(emojis, indent=4))

    for emoji in emojis:
        print('Emoji name:', emoji.get('name', 'N/A'))
        category = emoji.get('category') or 'N/A'
        group = emoji.get('group') or 'N/A'
        htmlCode = emoji.get('htmlCode') or 'N/A'
        unicode = emoji.get('unicode') or 'N/A'
        print(f'Category: {category}, Group: {group}, HTML Code: {htmlCode}, Unicode: {unicode}')

def main() -> None:
    session = requests.Session()
    session.headers.update(HEADERS)

    while True:
        emoji_type = input('Enter an emoji category to search for emojis (blank to quit): ').strip()
        if not emoji_type:
            break

        emojis = fetch_emoji_data(session, emoji_type)
        if not emojis:
            print('No emoji data returned.')
            continue

        print_emojis(emojis)

if __name__ == '__main__':
    main()