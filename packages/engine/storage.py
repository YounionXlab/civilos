from pathlib import Path
import json

DATA_DIR = Path(__file__).resolve().parents[2] / 'data'
DATA_DIR.mkdir(exist_ok=True)

class Storage:
    @staticmethod
    def load(name:str, default=None):
        path = DATA_DIR / f'{name}.json'
        if not path.exists():
            return default
        with open(path,'r',encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def save(name:str, data):
        path = DATA_DIR / f'{name}.json'
        with open(path,'w',encoding='utf-8') as f:
            json.dump(data,f,ensure_ascii=False,indent=2)
