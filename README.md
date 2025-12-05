# Setup Instructions

## Backend Setup
1. Create database:
```bash 
psql -U postgres -h localhost -c "CREATE DATABASE local_hero;"
tourch backend/.env
echo "DATABASE_URL=postgresql://postgres:password@localhost:5432/local_hero" > backend/.env
```
2. Install dependencies
```bash
# it is recommended to use a virtual environment
cd backend
pip install -r requirements.txt
```
3. Run migrations
```bash
alembic upgrade head
```
4. Start the backend server
```bash
uvicorn main:app --reload
```
or if using PyCharm, run the configuration for `main.py`.


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
