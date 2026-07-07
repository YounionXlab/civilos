import json
from pathlib import Path
from .events import random_event

ROOT = Path(__file__).resolve().parents[2]
WORLD = ROOT / 'data' / 'world.json'


def load_world():
    with open(WORLD,'r',encoding='utf-8') as f:
        return json.load(f)


def save_world(world):
    with open(WORLD,'w',encoding='utf-8') as f:
        json.dump(world,f,ensure_ascii=False,indent=2)


def tick(world):
    world['day'] += 1
    world['energy']=max(0,world['energy']-2)
    world['water']=max(0,world['water']-1)
    world['food']=max(0,world['food']-1)
    world.setdefault('history',[]).append({'day':world['day'],'title':random_event()})
    return world

if __name__=='__main__':
    w=load_world(); save_world(tick(w)); print(f"Day {w['day']} complete")