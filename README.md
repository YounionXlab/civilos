# civilos
Building living civilizations with AI

CivilOS is an AI-native civilization operating system.

Instead of scripting stories,
we grow worlds.

Instead of NPCs,
we create citizens.

Instead of levels,
we evolve civilizations.

## Alpha 0.1

CivilOS Alpha 0.1 includes:

- FastAPI backend with `GET /world`, `GET /agents`, `GET /history`, and `POST /tick`
- Simulation Engine for advancing the civilization one day at a time
- Next.js dashboard for world state, citizens, and history
- Vercel deployment configuration

## Local development

Run the API:

```bash
pip install -r requirements.txt
uvicorn apps.api.main:app --reload
```

Run the dashboard:

```bash
cd apps/web
npm install
npm run dev
```
