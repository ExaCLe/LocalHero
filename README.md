# Setup Instructions

## Backend Setup
1. Create database:
```bash
psql -U postgres -h localhost -c "CREATE DATABASE local_hero;"
touch backend/.env
echo "DATABASE_URL=postgresql://postgres:password@localhost:5432/local_hero" > backend/.env
```
2. Install dependencies
```bash
# it is recommended to use a virtual environment
cd backend
pip install -r requirements.txt
```
3. Create the .env file
```bash
echo "DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/local_hero" > .env
```

4. Generate and set the JWT secret key (see [JWT Key Generation](#jwt-key-generation) below)

5. Run migrations
```bash
alembic upgrade head
```
6. Start the backend server
```bash
uvicorn main:app --reload
```
or if using PyCharm, run the configuration for `Backend`.

### JWT Key Generation

The backend requires a `JWT_SECRET_KEY` environment variable for authentication. Generate a secure key using one of the following methods:

**Linux/macOS:**
```bash
openssl rand -hex 32
```

**Windows (PowerShell):**
```powershell
-join ((1..32) | ForEach-Object { '{0:X2}' -f (Get-Random -Maximum 256) })
```

**Python (cross-platform):**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Add the generated key to your `.env` file:
```bash
JWT_SECRET_KEY=your_generated_key_here
```

**Optional JWT Configuration:**
```bash
JWT_ALGORITHM=HS256           # Default: HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30 # Default: 30
```


## Frontend Setup
1. Install dependencies
```bash
cd frontend
npm install
```

## Pre-Commit Hooks
```bash
pre-commit install
```
You can now run it manually using:
```bash
pre-commit run --all-files
```

# Development

## Backend
### Migrations
You can create a new migration using:
```bash
alembic revision --autogenerate -m "add items table"
```
Then apply the migration using (there also is a run config in PyCharm):
```bash
alembic upgrade head
```
You can undo the last migration using:
```bash
alembic downgrade -1
```
Have Fun!
