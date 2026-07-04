PYTHON ?= python
PIP ?= pip

.PHONY: setup generate-data train api dashboard report test lint docker-up docker-down

setup:
	$(PYTHON) -m venv .venv
	. .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

generate-data:
	$(PYTHON) scripts/generate_sensor_data.py

train:
	$(PYTHON) -m src.models.train

api:
	uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload

dashboard:
	streamlit run app/streamlit_app.py --server.address 0.0.0.0 --server.port 8501

report:
	$(PYTHON) scripts/generate_report.py

test:
	pytest -q

lint:
	ruff check .

docker-up:
	docker compose up --build

docker-down:
	docker compose down
