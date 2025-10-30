## SafeNest — Copilot instructions for code changes

Quick context
- This is a Django 5.1 project named SafeNest (root package `safenest`). It is an ASGI app using Channels, Celery and integrates with an external AI provider (OpenRouter / Claude fallback).
- Key apps: `ai_assistant`, `dashboard`, `devices`, `security`, `energy`, `automation`, plus user management apps `accounts` and `profile`.

What an agent should know (big picture)
- HTTP and realtime: normal HTTP routes are handled by Django; websockets are routed via Channels (see `safenest/asgi.py` and `dashboard/consumers.py`). The project expects a Redis-backed channel layer.
- Background tasks: Celery is configured to use Redis (broker/result backend). Worker tasks live in each app's `tasks.py` (if present); run workers locally when testing async flows.
- AI integration: AI settings and model choices live in `safenest/settings.py` under `AI_ASSISTANT_SETTINGS`. The OpenRouter API key is read from environment as `OPENROUTER_API_KEY`. Debug helpers exist (`debug_openrouter.py`, `debug_api.py`) for quick testing.

Developer workflows & commands (PowerShell examples)
- Run local dev server (Django dev server, works for most HTTP dev):
  python manage.py runserver
- Run ASGI production-like server (for Channels / Daphne):
  daphne -b 0.0.0.0 -p 8000 safenest.asgi:application
- Start Redis locally (required for channels & celery). On Windows use WSL or Docker; otherwise install and run Redis on 127.0.0.1:6379.
- Start Celery worker (in project root):
  celery -A safenest worker -l info
- Run tests:
  python manage.py test
- Quick OpenRouter debug: inspect `debug_openrouter.py` to see usage patterns for requests and expected env var `OPENROUTER_API_KEY`.

Important files & patterns (examples)
- `safenest/settings.py` — central config: Channels/CHANNEL_LAYERS, Celery broker URLs, AI assistant defaults (DEFAULT_MODEL, FALLBACK_MODEL). Use it to discover model names and timeout defaults.
- `safenest/asgi.py` — ASGI entry: HTTP + websocket ProtocolTypeRouter. Websocket patterns are added via `URLRouter` (check `dashboard/consumers.py` and `dashboard/urls.py`).
- `ai_assistant/views.py` — shows how API routes call the AI stack and how conversation history / settings are used.
- `templates/ai_assistant.html` and `static/js/main.js` — front-end example of how the assistant is called from the client and how results are displayed.
- `requirements.txt` — lists core runtime dependencies (Django, channels, channels-redis, celery, redis, requests). Match versions when adding new deps.

Project-specific conventions
- App structure: each Django app follows the standard layout (models.py, views.py, urls.py, admin.py). Add new endpoints in the app's `urls.py` and wire to project `safenest/urls.py` only when global routing is required.
- Settings: environment secrets are loaded via `python-decouple` (look for `config(...)` in `safenest/settings.py`). Do not hardcode keys — use env vars or a `.env` local file.
- AI configuration: prefer using `AI_ASSISTANT_SETTINGS` keys rather than hardcoding model strings. Use the fallback pattern present in settings when network/timeouts occur.
- Static files: static assets are in `static/` while templates are in `templates/`. Whitenoise is enabled; static collection will output to `staticfiles/`.

Integration points and gotchas
- Redis is required for both Channels and Celery. Tests or local runs that touch websocket or background processing will fail without Redis running.
- Although `db.sqlite3` is present by default, `requirements.txt` includes `psycopg2-binary` — the codebase may be deployed with Postgres. Avoid schema-changing migrations assuming Postgres-specific features.
- ASGI routing: `safenest/asgi.py` uses an AllowHosts validator and AuthMiddlewareStack. If adding websocket endpoints, ensure they are added to the URLRouter and test origin/security settings.
- External AI calls: network calls to OpenRouter are centralized; look for `ai_assistant` and `debug_openrouter.py` for examples. TIMEOUT and MAX_TOKENS are configurable in settings.

When changing or adding AI-related code
- Use `AI_ASSISTANT_SETTINGS` values for defaults and fallbacks. Example: when adding a new model name, add it to settings and reference `settings.AI_ASSISTANT_SETTINGS['DEFAULT_MODEL']`.
- Keep network calls idempotent and wrapped with timeouts and retries; the project expects a fallback model when the default is unavailable.
- Add a small unit/integration test for any new assistant endpoint. Tests can call `debug_openrouter.py` style helpers (or mock requests using `responses`/`requests-mock`).

Quick contract for changes an agent may make
- Inputs: HTTP/JSON requests from `api/` or form submissions from templates; websocket messages via `dashboard/consumers.py`.
- Outputs: HTML templates, JSON responses (DRF), websocket messages. Errors should return HTTP 4xx/5xx with helpful JSON error messages for API routes.
- Error modes: missing env vars (OPENROUTER_API_KEY), Redis not reachable, or AI timeout. Use clear logging and graceful fallbacks.

If you edit files, validate:
- Run `python manage.py check` and `python manage.py test` (or targeted tests).
- Confirm local Redis and Celery workers if your change touches channels or tasks.

Where to look for examples
- `debug_openrouter.py` — quick usage of the OpenRouter API.
- `dashboard/consumers.py` — websocket consumer patterns.
- `ai_assistant/views.py` and `templates/ai_assistant.html` — request/response flow for the assistant.

Need more detail?
- Tell me which area you want more examples for (websocket flows, Celery tasks, AI request wiring) and I will expand this file with concrete code snippets and tests.
