PYTHON ?= python3
VENV ?= .venv
PACKAGE ?= financial-advisor-agent
IMAGE ?= ghcr.io/lemduc/financial-advisor-agent:latest

.PHONY: install dev test lint typecheck docker-build docker-run kube-apply kube-delete clean

install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt

dev:
	uvicorn app.main:app --reload

test:
	pytest

lint:
	ruff check .

typecheck:
	mypy app

docker-build:
	docker build -t $(PACKAGE):dev .

docker-run:
	docker run --rm -p 8000:8000 $(PACKAGE):dev

kube-apply:
	kubectl apply -f k8s/deployment.yaml

kube-delete:
	kubectl delete -f k8s/deployment.yaml

clean:
	rm -rf $(VENV) .ruff_cache .mypy_cache .pytest_cache
