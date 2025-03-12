#! /usr/bin/env bash

set -e
set -x

source .venv/bin/activate
alembic upgrade head
python main.py