NAME = a_maze_ing

PYTHON = python3

MAIN = a_maze_ing.py

VENV = venv

PIP = pip

all: run

# -------------------------
# INSTALL DEPENDENCIES
# -------------------------
install:
	$(PIP) install -r requirements.txt

# -------------------------
# RUN PROGRAM
# -------------------------
run:
	$(PYTHON) $(MAIN) config.txt

# -------------------------
# DEBUG MODE (pdb)
# -------------------------
debug:
	$(PYTHON) -m pdb $(MAIN) config.txt

# -------------------------
# CLEAN CACHE FILES
# -------------------------
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +

# -------------------------
# LINT (STRICT 42 VERSION)
# -------------------------
lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores \
	--ignore-missing-imports --disallow-untyped-defs \
	--check-untyped-defs

# -------------------------
# LINT STRICT (OPTIONAL)
# -------------------------
lint-strict:
	flake8 .
	mypy . --strict

# -------------------------
# HELP (OPTIONAL NICE ADD)
# -------------------------
help:
	@echo "Available commands:"
	@echo "  make install     Install dependencies"
	@echo "  make run         Run project"
	@echo "  make debug       Run with pdb"
	@echo "  make clean       Remove cache files"
	@echo "  make lint        Run flake8 + mypy (42 rules)"
	@echo "  make lint-strict Run strict mypy"