#!/bin/bash

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Checking CCTV Camera Manager services...${NC}"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
  echo -e "${RED}Docker is not running! Please start Docker first.${NC}"
  exit 1
fi

# Function to check if container is running
check_container() {
  local container_name=$1
  local status=$(docker inspect --format='{{.State.Status}}' $container_name 2>/dev/null)
  
  if [ $? -ne 0 ]; then
    echo -e "${RED}Container $container_name does not exist!${NC}"
    return 1
  fi
  
  if [ "$status" == "running" ]; then
    echo -e "${GREEN}✅ $container_name is running${NC}"
    return 0
  else
    echo -e "${RED}❌ $container_name is not running (status: $status)${NC}"
    return 1
  fi
}

# Check if containers are running
backend_ok=false
frontend_ok=false
rtmp_ok=false

check_container "cctv_backend" && backend_ok=true
check_container "cctv_frontend" && frontend_ok=true
check_container "cctv_rtmp" && rtmp_ok=true

echo ""
echo -e "${YELLOW}Testing service connectivity:${NC}"

# Check if backend API is accessible
if $backend_ok; then
  if curl -s http://localhost:8000/api/cameras/ > /dev/null; then
    echo -e "${GREEN}✅ Backend API is accessible${NC}"
  else
    echo -e "${RED}❌ Backend API is not accessible${NC}"
    backend_ok=false
  fi
fi

# Check if frontend is accessible
if $frontend_ok; then
  if curl -s http://localhost/ > /dev/null; then
    echo -e "${GREEN}✅ Frontend is accessible${NC}"
  else
    echo -e "${RED}❌ Frontend is not accessible${NC}"
    frontend_ok=false
  fi
fi

# Check if RTMP server is accessible
if $rtmp_ok; then
  if curl -s http://localhost:8080/health > /dev/null; then
    echo -e "${GREEN}✅ RTMP server is accessible${NC}"
  else
    echo -e "${RED}❌ RTMP server is not accessible${NC}"
    rtmp_ok=false
  fi
fi

echo ""
if $backend_ok && $frontend_ok && $rtmp_ok; then
  echo -e "${GREEN}All services are up and running!${NC}"
  echo -e "${YELLOW}Frontend: http://localhost/${NC}"
  echo -e "${YELLOW}Backend API: http://localhost:8000/api/${NC}"
  echo -e "${YELLOW}API Documentation: http://localhost/swagger/${NC}"
  echo -e "${YELLOW}RTMP HLS Player: http://localhost:8080/${NC}"
else
  echo -e "${RED}Some services are not running properly.${NC}"
  echo -e "${YELLOW}Try restarting the services with:${NC}"
  echo -e "  docker-compose down"
  echo -e "  docker-compose up -d"
fi 