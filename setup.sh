PORT="$1"

kill -9 $(lsof -ti ":$PORT") 2>/dev/null
git pull
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
gunicorn -b ":$PORT" --access-logfile /path/to/access.log --error-logfile /path/to/error.log api.main:app

