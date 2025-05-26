#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Starting AIsk App...${NC}"

# Function to handle cleanup on exit
cleanup() {
    echo -e "\n${YELLOW}Shutting down services...${NC}"
    kill 0
}
trap cleanup EXIT

# Start backend
echo -e "${GREEN}📡 Starting backend server...${NC}"
cd aisk-backend

# Check if virtual environment exists
if [ -d "aisk/Scripts" ]; then
    echo -e "${BLUE}Activating existing virtual environment...${NC}"
    source aisk/Scripts/activate
else
    echo -e "${YELLOW}Virtual environment not found. Creating one...${NC}"
    python -m venv aisk
    source aisk/Scripts/activate
fi

# Install/update requirements if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo -e "${BLUE}Installing/updating Python dependencies...${NC}"
    pip install -r requirements.txt
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Python dependencies installed successfully${NC}"
    else
        echo -e "${RED}❌ Failed to install Python dependencies${NC}"
        exit 1
    fi
else
    echo -e "${YELLOW}⚠️  No requirements.txt found, skipping dependency installation${NC}"
fi

# Start the backend server
echo -e "${BLUE}Starting Python API server...${NC}"
python api.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start frontend
echo -e "${GREEN}🎨 Starting frontend server...${NC}"
cd ../aisk-frontend

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}Installing frontend dependencies...${NC}"
    npm install
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Frontend dependencies installed successfully${NC}"
    else
        echo -e "${RED}❌ Failed to install frontend dependencies${NC}"
        kill $BACKEND_PID
        exit 1
    fi
else
    echo -e "${BLUE}Frontend dependencies already installed${NC}"
fi

# Start the frontend server
npm start &
FRONTEND_PID=$!

echo -e "${GREEN}✅ Both servers started successfully!${NC}"
echo -e "${YELLOW}Backend: http://localhost:5000${NC}"
echo -e "${YELLOW}Frontend: http://localhost:3000${NC}"
echo -e "${BLUE}Press Ctrl+C to stop both servers${NC}"

# Wait for both processes
wait