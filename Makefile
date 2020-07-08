### help - help docs for this Makefile
.PHONY: help
help :
	@sed -n '/^###/p' Makefile

### install - install requirements in venv
.PHONY: install
install: install-backend install-frontend

### install-backend - install backend requirements in venv
.PHONY: install-backend
install-backend:
	#	 backend installation
	python3 -m venv backend/.venv; \
	. backend/.venv/bin/activate; \
	pip3 install -r backend/requirements.txt

### install-frontend - install frontend requirements
.PHONY: install-frontend
install-frontend:
	#	 frontend installation
	npm install --prefix frontend

### start - start both backend and frontend together
.PHONY: start
start:
	make -j 2 frontend backend

### backend - start flask backend
.PHONY: backend
backend:
	. backend/.venv/bin/activate; python3 backend/app.py

### frontend - start react frontend
.PHONY: frontend
frontend:
	npm run serve --prefix frontend

### lint - lint all code
.PHONY: lint
lint: lint-backend lint-frontend

### lint-frontend - lint frontend
.PHONY: lint-frontend
lint-frontend:
	npm run lint --prefix frontend

### lint-backend - lint backend
.PHONY: lint-backend
lint-backend:
	isort --multi-line=3 --trailing-comma --force-grid-wrap=0 --use-parentheses --line-width=88 backend/
	black backend

