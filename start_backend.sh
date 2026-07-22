#!/bin/bash
cd /home/sshahi12/app_ideas/stock_pattern_scanner/backend
source venv/bin/activate
exec uvicorn main:app --host 0.0.0.0 --port 8001
