# civilos
Building living civilizations with AI

CivilOS is an AI-native civilization operating system.

Instead of scripting stories,
we grow worlds.

Instead of NPCs,
we create citizens.

Instead of levels,
we evolve civilizations.

## Alpha 0.2

CivilOS Alpha 0.2 includes:

- FastAPI backend with `GET /world`, `GET /agents`, `GET /history`, and `POST /tick`
- Simulation Engine for advancing the civilization one day at a time
- Next.js dashboard for world state, citizens, and history
- Vercel deployment configuration
- Persistent Supabase Postgres state with serialized ticks

## Supabase persistence

1. Run `supabase/schema.sql` in the Supabase SQL editor.
2. Copy the Supabase Postgres connection string.
3. Set `DATABASE_URL` in Vercel for Production and Preview.
4. Redeploy the project.

Vercel deployments require `DATABASE_URL`; CivilOS will not fall back to ephemeral `/tmp` state.
Local development continues to use JSON files in `data/` when `DATABASE_URL` is unset.

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
