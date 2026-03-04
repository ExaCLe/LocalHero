# LocalHero

## Setup Instructions

### Frontend + Convex Setup

1. Install dependencies
```bash
cd frontend
npm install
```

2. Create local env file
```bash
cp .env.local.example .env.local
```

3. Start Convex (backend)
```bash
npm run convex:dev
```

4. Start Next.js frontend
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## Vercel Deployment

### Deploy

1. Import the repository in Vercel.
2. Set the project root to `frontend/` (or configure Vercel to build from that directory).
3. Use the default Next.js framework settings.

### Environment Variables (Vercel)

Set these in Vercel Project Settings -> Environment Variables.

Create the variable for both deployment environments:

- `Preview`
- `Production`

```bash
NEXT_PUBLIC_CONVEX_URL=https://<your-convex-deployment>.convex.cloud
```

If you use separate Convex deployments, set different values per environment:

- `Preview`: `https://<your-preview-deployment>.convex.cloud`
- `Production`: `https://<your-production-deployment>.convex.cloud`

Notes:

- `NEXT_PUBLIC_CONVEX_URL` is required for both client-side and server-side app code in this project.
- This configuration allows both Vercel Preview deployments and Production deployments to run correctly.
- `CONVEX_DEPLOYMENT` and `CONVEX_SELF_HOSTED_URL` are typically for local CLI/dev workflows and are not required for a standard Vercel deployment of this frontend.

## Pre-Commit Hooks

```bash
pre-commit install
pre-commit run --all-files
```

## Development Notes

- Convex backend functions live in `frontend/convex/`.
- `NEXT_PUBLIC_CONVEX_URL` is required for the app to call Convex.
- For self-hosted Convex (Convex OSS), set `CONVEX_SELF_HOSTED_URL` in `frontend/.env.local`.
