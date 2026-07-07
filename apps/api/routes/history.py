from fastapi import APIRouter
import json
from pathlib import Path

router = APIRouter()
ROOT = Path(__file__).resolve().parents[3]
WORLD = ROOT / 'data' / 'world.json'

@router.get('/history')
def get_history(limit: int = 30):
    with open(WORLD,'r',encoding='utf-8') as f:
        world = json.load(f)
    history = world.get('history', [])
    return {'items': history[-limit:], 'count': len(history)}
