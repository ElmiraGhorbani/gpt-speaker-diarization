#!/bin/bash
[[ -z "${NUM_WORKERS}" ]] && NUM_WORKERS=1 || NUM_WORKERS="${NUM_WORKERS}"
uvicorn --workers ${NUM_WORKERS} --host 0.0.0.0 scripts.app:app