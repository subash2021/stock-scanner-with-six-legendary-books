#!/bin/bash

# ============================================
# 10X Stock Scanner - One Command Startup
# ============================================
# Usage: ./start.sh          - Start all services
#        ./start.sh stop     - Stop all services
#        ./start.sh restart  - Restart all services

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/backend"
FRONTEND_DIR="$SCRIPT_DIR/frontend"
LOG_DIR="$SCRIPT_DIR/logs"
PID_DIR="$SCRIPT_DIR/pids"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

mkdir -p "$LOG_DIR" "$PID_DIR"

check_port() {
    if command -v lsof &>/dev/null; then
        lsof -Pi ":$1" -sTCP:LISTEN -t >/dev/null 2>&1
    elif command -v ss &>/dev/null; then
        ss -tlnp | grep -q ":$1 "
    elif command -v netstat &>/dev/null; then
        netstat -tlnp 2>/dev/null | grep -q ":$1 "
    else
        curl -s "http://localhost:$1" >/dev/null 2>&1
    fi
}

kill_port() {
    if command -v lsof &>/dev/null; then
        local pid=$(lsof -ti :"$1" 2>/dev/null)
    else
        local pid=$(ss -tlnp | grep ":$1 " | grep -oP 'pid=\K[0-9]+' 2>/dev/null | head -1)
    fi
    if [ -n "$pid" ]; then
        echo -e "${YELLOW}Killing process on port $1 (PID: $pid)${NC}"
        kill "$pid" 2>/dev/null
        sleep 1
    fi
}

stop_all() {
    echo -e "${YELLOW}Stopping all services...${NC}"
    kill_port 8001
    kill_port 3000
    rm -f "$PID_DIR"/*.pid
    echo -e "${GREEN}All services stopped.${NC}"
}

if [ "$1" = "stop" ]; then
    stop_all
    exit 0
fi

if [ "$1" = "restart" ]; then
    stop_all
    sleep 2
fi

echo -e "${BLUE}==========================================${NC}"
echo -e "${BLUE}   10X Stock Scanner${NC}"
echo -e "${BLUE}==========================================${NC}"
echo ""

# Auto-setup if venv missing
if [ ! -d "$BACKEND_DIR/venv" ]; then
    echo -e "${YELLOW}First run - setting up Python backend...${NC}"
    cd "$BACKEND_DIR"
    python3 -m venv venv
    source venv/bin/activate
    pip install -q -r requirements.txt
    echo -e "${GREEN}Backend setup complete.${NC}"
fi

# Auto-setup if node_modules missing
if [ ! -d "$FRONTEND_DIR/node_modules" ]; then
    echo -e "${YELLOW}First run - setting up frontend...${NC}"
    cd "$FRONTEND_DIR"
    npm install --silent
    echo -e "${GREEN}Frontend setup complete.${NC}"
fi

# Start backend
if check_port 8001; then
    echo -e "${GREEN}Backend already running on port 8001${NC}"
else
    echo -e "${BLUE}Starting backend on port 8001...${NC}"
    cd "$BACKEND_DIR"
    source venv/bin/activate
    setsid python -m uvicorn main:app --host 0.0.0.0 --port 8001 > "$LOG_DIR/backend.log" 2>&1 &
    echo $! > "$PID_DIR/backend.pid"
    
    for i in {1..30}; do
        if check_port 8001; then
            echo -e "${GREEN}Backend started successfully${NC}"
            break
        fi
        if [ $i -eq 30 ]; then
            echo -e "${RED}Backend failed to start. Check: $LOG_DIR/backend.log${NC}"
            exit 1
        fi
        sleep 1
    done
fi

# Start frontend
if check_port 3000; then
    echo -e "${GREEN}Frontend already running on port 3000${NC}"
else
    echo -e "${BLUE}Starting frontend on port 3000...${NC}"
    cd "$FRONTEND_DIR"
    setsid npm run dev > "$LOG_DIR/frontend.log" 2>&1 &
    echo $! > "$PID_DIR/frontend.pid"
    
    for i in {1..30}; do
        if check_port 3000; then
            echo -e "${GREEN}Frontend started successfully${NC}"
            break
        fi
        if [ $i -eq 30 ]; then
            echo -e "${RED}Frontend failed to start. Check: $LOG_DIR/frontend.log${NC}"
            exit 1
        fi
        sleep 1
    done
fi

echo ""
echo -e "${GREEN}==========================================${NC}"
echo -e "${GREEN}   All services running!${NC}"
echo -e "${GREEN}==========================================${NC}"
echo ""
echo -e "  ${BLUE}Frontend:${NC} http://localhost:3000"
echo -e "  ${BLUE}Backend:${NC}  http://localhost:8001"
echo -e "  ${BLUE}API Docs:${NC} http://localhost:8001/docs"
echo ""
echo -e "  ${YELLOW}Logs:${NC}"
echo -e "    Backend:  $LOG_DIR/backend.log"
echo -e "    Frontend: $LOG_DIR/frontend.log"
echo ""
echo -e "  ${YELLOW}Commands:${NC}"
echo -e "    ./start.sh          Start services"
echo -e "    ./start.sh stop     Stop services"
echo -e "    ./start.sh restart  Restart services"
echo ""
