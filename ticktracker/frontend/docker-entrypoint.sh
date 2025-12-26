#!/bin/sh
echo "🚀 Starting Next.js debug wrapper..."
export PORT=${PORT:-3000}
export HOSTNAME="0.0.0.0"

echo "✅ Environment: PORT=$PORT, HOSTNAME=$HOSTNAME"

# Start the application in the background
node server.js &
PID=$!

echo "⏳ Waiting for server to start (PID: $PID)..."
sleep 5

echo "🔎 Testing connectivity from INSIDE the container..."
if curl -v "http://127.0.0.1:$PORT"; then
  echo "✅ SUCCESS: App is reachable internally at 127.0.0.1:$PORT"
else
  echo "❌ FAIL: App is NOT reachable internally at 127.0.0.1:$PORT"
fi

if curl -v "http://localhost:$PORT"; then
  echo "✅ SUCCESS: App is reachable internally at localhost:$PORT"
else
  echo "❌ FAIL: App is NOT reachable internally at localhost:$PORT"
fi

echo "🔄 Keeping process alive..."
wait $PID
