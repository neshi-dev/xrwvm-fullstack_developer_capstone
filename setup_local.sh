#!/bin/bash
set -e

PROJECT_DIR="/home/neshi/Documents/fullstack_developer_capstone/server"
DB_DIR="$PROJECT_DIR/database"

echo "=============================="
echo " Step 1: Install MongoDB"
echo "=============================="
if ! command -v mongod &>/dev/null; then
  # Import MongoDB GPG key and add repo for Ubuntu/Mint
  curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor
  echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
  sudo apt-get update -y
  sudo apt-get install -y mongodb-org
  echo "MongoDB installed."
else
  echo "MongoDB already installed."
fi

echo "=============================="
echo " Step 2: Start MongoDB"
echo "=============================="
sudo systemctl start mongod
sudo systemctl enable mongod
sleep 2
echo "MongoDB running."

echo "=============================="
echo " Step 3: Fix app.js connection"
echo "=============================="
# Ensure the connection string uses localhost (now works since mongod is native)
sed -i 's|mongodb://172.18.0.2:27017/|mongodb://127.0.0.1:27017/|g' "$DB_DIR/app.js"
sed -i 's|mongodb://localhost:27017/|mongodb://127.0.0.1:27017/|g' "$DB_DIR/app.js"
echo "app.js connection string fixed."

echo "=============================="
echo " Step 4: Start Node backend"
echo "=============================="
cd "$DB_DIR"
npm install --silent
pkill -f "node app.js" 2>/dev/null || true
sleep 1
nohup node app.js > /tmp/node_app.log 2>&1 &
NODE_PID=$!
echo "Node backend started (PID $NODE_PID). Waiting for it to seed data..."
sleep 5

# Verify it's working
DEALERS=$(curl -s http://localhost:3030/fetchDealers | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d))" 2>/dev/null || echo "0")
echo "Node backend returned $DEALERS dealers."

echo "=============================="
echo " Step 5: Update Django .env"
echo "=============================="
echo "backend_url=http://localhost:3030" > "$PROJECT_DIR/.env"
echo ".env updated."

echo "=============================="
echo " Step 6: Clear Django .env backend URL cache"
echo "=============================="
# Kill any existing Django process
pkill -f "manage.py runserver" 2>/dev/null || true
sleep 1

echo "=============================="
echo " Step 7: Start Django"
echo "=============================="
cd "$PROJECT_DIR"
source djangoenv/bin/activate
python3 manage.py runserver 0.0.0.0:8000 &
DJANGO_PID=$!
sleep 3

echo ""
echo "=============================="
echo " ALL DONE!"
echo "=============================="
echo " Node PID:   $NODE_PID"
echo " Django PID: $DJANGO_PID"
echo ""
echo " Open your browser at: http://localhost:8000/dealers/"
echo " The dealership table should be fully populated!"
echo ""
echo " Logs: /tmp/node_app.log"
