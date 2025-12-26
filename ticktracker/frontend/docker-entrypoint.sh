#!/bin/sh
echo "🚀 Starting Next.js standalone server..."
echo "re: PORT environment variable: '$PORT'"

# Fallback to 3000 if PORT is not set (e.g. local testing)
export PORT=${PORT:-3000}
export HOSTNAME="0.0.0.0"

echo "✅ Binding to HOST: $HOSTNAME"
echo "✅ Binding to PORT: $PORT"

# Execute the server
exec node server.js
