create table if not exists public.civilos_state (
  name text primary key,
  payload jsonb not null,
  updated_at timestamptz not null default now()
);

alter table public.civilos_state enable row level security;
