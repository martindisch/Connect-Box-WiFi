#!/bin/bash
export FLASK_APP=connectboxcontrol
export FLASK_DEBUG=0
. venv/bin/activate
flask run --host=0.0.0.0 --port=80
