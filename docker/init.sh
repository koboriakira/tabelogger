source ~/.bashrc
service mysql start
uvicorn tabelogger.main:app --reload --host 0.0.0.0 --port 8000
