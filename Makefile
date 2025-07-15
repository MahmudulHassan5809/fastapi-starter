.PHONY: help run

SHELL := /bin/bash

run:
	@export $$(grep -v '^#' .env | xargs) && \
	export PYTHONPATH=$$(pwd) && \
	source .venv/bin/activate && \
	uvicorn src.main:app --reload

