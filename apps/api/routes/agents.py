from fastapi import APIRouter
import json
from pathlib import Path

router = APIRouter()
ROOT = Path(__file__).resolve().parents[3]
AGENTS = ROOT / 'data' / 'agents.json'

@router.get('/agents')
def get_agents():
    with open(AGENTS,'r',encoding='utf-8') as f:
        agents = json.load(f)
    return {'count': len(agents), 'items': agents}
