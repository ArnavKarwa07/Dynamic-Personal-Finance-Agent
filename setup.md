## Start backend server without virtual environment
cd backend
pip install -r requirements.txt
copy sample.env .env  # Then configure your API keys
uvicorn main:app --reload --port 8000

## Start backend server with virtual environment
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy sample.env .env  # Then configure your API keys
uvicorn main:app --reload --port 8000

## Start frontend
cd frontend
npm install
echo "VITE_API_URL=http://localhost:8000" > .env.local
npm run dev