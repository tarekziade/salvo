HERE = $(shell pwd)
VENV = $(HERE)/venv
BIN = $(VENV)/bin
PYTHON = $(BIN)/python

INSTALL = $(BIN)/pip install --no-deps

.PHONY: all test clean build 

all: build

build:
	python3.9 -m venv $(VENV)
	$(VENV)/bin/pip install tox

clean:
	rm -rf $(VENV)

test: build
	$(BIN)/tox

