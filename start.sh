#!/bin/bash

# ============================================
# Stock Pattern Scanner - One Command Startup
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
    lsof -Pi ":$1" -sTCP:LISTEN -t >/dev/null 2>&1
}

kill_port() {
    local pid=$(lsof -ti :"$1" 2>/dev/null)
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

echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}   Stock Pattern Scanner - CVNA Edition${NC}"
echo -e "${BLUE}============================================${NC}"
echo ""

# Start backend
if check_port 8001; then
    echo -e "${GREEN}Backend already running on port 8001${NC}"
else
    echo -e "${BLUE}Starting backend on port 8001...${NC}"
    cd "$BACKEND_DIR"
    source venv/bin/activate
    setsid python -m uvicorn main:app --host 0.0.0.0 --port 8001 > "$LOG_DIR/backend.log" 2>&1 &
    echo $! > "$PID_DIR/backend.pid"
    
    # Wait for backend
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
    
    # Wait for frontend
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
echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}   All services running!${NC}"
echo -e "${GREEN}============================================${NC}"
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
