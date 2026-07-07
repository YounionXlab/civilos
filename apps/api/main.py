from fastapi import FastAPI
import json
from pathlib import Path

app = FastAPI(title='CivilOS API')
ROOT = Path(__file__).resolve().parents[2]
WORLD = ROOT / 'data' / 'world.json'

@app.get('/world')
def get_world():
    with open(WORLD,'r',encoding='utf-8') as f:
        return json.load(f)
