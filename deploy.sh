#!/bin/bash

# TickTracker Deployment Script
# This script helps automate deployment to a VPS

set -e

echo "🚀 TickTracker Deployment Helper"
echo "================================"
echo ""

# Check if running on server or local
if [ "$1" == "server" ]; then
    echo "📦 Setting up on server..."
    
    # Update system
    echo "Updating system packages..."
    sudo apt update && sudo apt upgrade -y
    
    # Install dependencies
    echo "Installing Python, Node.js, Nginx..."
    sudo apt install -y python3 python3-pip python3-venv nodejs npm nginx certbot python3-certbot-nginx
    
    # Setup backend
    echo "Setting up backend..."
    cd ticktracker/backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    
    # Setup frontend
    echo "Setting up frontend..."
    cd ../frontend
    npm install
    npm run build
    
    echo "✅ Setup complete!"
    echo ""
    echo "Next steps:"
    echo "1. Create .env file in ticktracker/backend with your API keys"
    echo "2. Run: sudo ./deploy.sh systemd"
    echo "3. Run: sudo ./deploy.sh nginx yourdomain.com"
    echo "4. Run: sudo certbot --nginx -d yourdomain.com"
    
elif [ "$1" == "systemd" ]; then
    echo "Creating systemd services..."
    
    BACKEND_PATH=$(pwd)/ticktracker/backend
    FRONTEND_PATH=$(pwd)/ticktracker/frontend
    
    # Backend service
    cat > /etc/systemd/system/ticktracker-backend.service << EOF
[Unit]
Description=TickTracker FastAPI Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=$BACKEND_PATH
Environment="PATH=$BACKEND_PATH/venv/bin"
ExecStart=$BACKEND_PATH/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

    # Frontend service
    cat > /etc/systemd/system/ticktracker-frontend.service << EOF
[Unit]
Description=TickTracker Next.js Frontend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=$FRONTEND_PATH
Environment="NODE_ENV=production"
Environment="PORT=3000"
ExecStart=/usr/bin/npm start
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

    systemctl daemon-reload
    systemctl enable ticktracker-backend ticktracker-frontend
    systemctl start ticktracker-backend ticktracker-frontend
    
    echo "✅ Services created and started!"
    echo "Check status with: sudo systemctl status ticktracker-backend"
    
elif [ "$1" == "nginx" ]; then
    if [ -z "$2" ]; then
        echo "❌ Please provide domain name: ./deploy.sh nginx yourdomain.com"
        exit 1
    fi
    
    DOMAIN=$2
    
    echo "Configuring Nginx for $DOMAIN..."
    
    cat > /etc/nginx/sites-available/ticktracker << EOF
server {
    listen 80;
    server_name api.$DOMAIN;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}

server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

    ln -sf /etc/nginx/sites-available/ticktracker /etc/nginx/sites-enabled/
    nginx -t && systemctl restart nginx
    
    echo "✅ Nginx configured!"
    echo "Next: Run SSL setup with: sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN -d api.$DOMAIN"
    
elif [ "$1" == "update" ]; then
    echo "Updating application..."
    
    git pull
    
    # Update backend
    cd ticktracker/backend
    source venv/bin/activate
    pip install -r requirements.txt
    sudo systemctl restart ticktracker-backend
    
    # Update frontend
    cd ../frontend
    npm install
    npm run build
    sudo systemctl restart ticktracker-frontend
    
    echo "✅ Application updated!"
    
else
    echo "Usage:"
    echo "  ./deploy.sh server          - Initial server setup"
    echo "  ./deploy.sh systemd         - Create systemd services"
    echo "  ./deploy.sh nginx DOMAIN    - Configure Nginx"
    echo "  ./deploy.sh update          - Update application"
    echo ""
    echo "Example workflow:"
    echo "  1. ./deploy.sh server"
    echo "  2. sudo ./deploy.sh systemd"
    echo "  3. sudo ./deploy.sh nginx yourdomain.com"
    echo "  4. sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com -d api.yourdomain.com"
fi
