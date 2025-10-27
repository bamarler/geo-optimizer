#!/bin/bash
set -e

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║         ⚙️  GEO PLATFORM SERVICES SETUP                       ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Configuration
SERVER_IP="54.221.56.44"
SERVER_USER="ec2-user"
SSH_KEY="$HOME/Downloads/my.pem"
DOMAIN="test.citable.xyz"
APP_DIR="/home/ec2-user/geo-platform"

# Step 1: Create systemd service for backend
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔧 Step 1: Creating systemd service for backend..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

ssh -i "$SSH_KEY" "$SERVER_USER@$SERVER_IP" << 'ENDSSH'
sudo tee /etc/systemd/system/geo-backend.service > /dev/null <<EOF
[Unit]
Description=GEO Platform Backend API
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/home/ec2-user/geo-platform/geo-frontend/server
Environment="PATH=/home/ec2-user/geo-platform/geo-frontend/server/venv/bin"
ExecStart=/home/ec2-user/geo-platform/geo-frontend/server/venv/bin/python app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

echo "✅ Backend service created!"
ENDSSH

# Step 2: Configure Nginx
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🌐 Step 2: Configuring Nginx..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

ssh -i "$SSH_KEY" "$SERVER_USER@$SERVER_IP" << ENDSSH
sudo tee /etc/nginx/conf.d/geo-platform.conf > /dev/null <<EOF
# Backend API
server {
    listen 80;
    server_name api.$DOMAIN;

    client_max_body_size 50M;

    location / {
        proxy_pass http://localhost:5001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \\\$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \\\$host;
        proxy_cache_bypass \\\$http_upgrade;
        proxy_set_header X-Real-IP \\\$remote_addr;
        proxy_set_header X-Forwarded-For \\\$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \\\$scheme;
        
        # Increase timeouts for long-running tests
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
    }
}

# Frontend
server {
    listen 80;
    server_name $DOMAIN;

    root /home/ec2-user/geo-platform/geo-frontend/client/dist;
    index index.html;

    location / {
        try_files \\\$uri \\\$uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:5001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \\\$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \\\$host;
        proxy_cache_bypass \\\$http_upgrade;
        
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
    }

    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF

echo "Testing Nginx configuration..."
sudo nginx -t

echo "✅ Nginx configured!"
ENDSSH

# Step 3: Install and configure SSL with Certbot
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔒 Step 3: Setting up SSL with Let's Encrypt..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

ssh -i "$SSH_KEY" "$SERVER_USER@$SERVER_IP" << ENDSSH
# Install certbot
sudo dnf install -y certbot python3-certbot-nginx

echo "⚠️  Before running certbot, ensure DNS is pointing to this server:"
echo "   $DOMAIN -> $SERVER_IP"
echo "   api.$DOMAIN -> $SERVER_IP"
echo ""
echo "Run this command manually when DNS is ready:"
echo "sudo certbot --nginx -d $DOMAIN -d api.$DOMAIN --non-interactive --agree-tos --email maria@citable.xyz"
echo ""
echo "For now, starting services without SSL..."
ENDSSH

# Step 4: Start services
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 Step 4: Starting services..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

ssh -i "$SSH_KEY" "$SERVER_USER@$SERVER_IP" << 'ENDSSH'
echo "Reloading systemd..."
sudo systemctl daemon-reload

echo "Enabling and starting backend service..."
sudo systemctl enable geo-backend
sudo systemctl start geo-backend

echo "Enabling and starting Nginx..."
sudo systemctl enable nginx
sudo systemctl start nginx

echo "Checking service status..."
sudo systemctl status geo-backend --no-pager -l || true
sudo systemctl status nginx --no-pager -l || true

echo "✅ Services started!"
ENDSSH

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Services configured and started!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 Summary:"
echo "   ✅ Backend service: geo-backend.service"
echo "   ✅ Nginx configured for: $DOMAIN"
echo "   ✅ API endpoint: api.$DOMAIN"
echo ""
echo "⚠️  Important next steps:"
echo "   1. Configure DNS:"
echo "      $DOMAIN A record -> $SERVER_IP"
echo "      api.$DOMAIN A record -> $SERVER_IP"
echo ""
echo "   2. Create environment files on server:"
echo "      ssh -i ~/Downloads/my.pem ec2-user@$SERVER_IP"
echo "      nano $APP_DIR/geo-frontend/server/.env"
echo "      nano $APP_DIR/geo-testing/.env"
echo ""
echo "   3. After DNS propagates, run SSL setup:"
echo "      ssh -i ~/Downloads/my.pem ec2-user@$SERVER_IP"
echo "      sudo certbot --nginx -d $DOMAIN -d api.$DOMAIN"
echo ""
echo "   4. Restart backend after adding .env:"
echo "      sudo systemctl restart geo-backend"

