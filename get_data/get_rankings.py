import brawlstats
import os
import sys
import io
import json
import pandas as pd
from dotenv import load_dotenv

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

output_dir = os.path.join(os.path.dirname(__file__), 'output')
os.makedirs(output_dir, exist_ok=True)
file_path = os.path.join(output_dir, 'rankings.json')

f = open(file_path, 'r', encoding='utf-8')
data = json.load(f)

tags = []
for player in data['items']:
    tags.append(player['tag'])

print(len(tags))
print(tags)