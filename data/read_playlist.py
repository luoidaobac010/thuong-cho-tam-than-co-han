import json
with open('playlist.json', 'r', encoding='utf-16') as f, open('playlist_summary.txt', 'w', encoding='utf-8') as out:
    for i, line in enumerate(f):
        data = json.loads(line)
        out.write(f"{i+1}. {data.get('title')} - {data.get('url')}\n")
