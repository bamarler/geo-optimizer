#!/bin/bash
set -e

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║         🚀 GEO PLATFORM DEPLOYMENT SCRIPT                     ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Configuration
SERVER_IP="54.221.56.44"
SERVER_USER="ec2-user"
SSH_KEY="$HOME/Downloads/my.pem"
DOMAIN="test.citable.xyz"
APP_DIR="/home/ec2-user/geo-platform"

echo "📋 Deployment Configuration:"
echo "   Server: $SERVER_USER@$SERVER_IP"
echo "   Domain: $DOMAIN"
echo "   App Directory: $APP_DIR"
echo ""

# Step 1: Install dependencies on server
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 Step 1: Installing dependencies on server..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

ssh -i "$SSH_KEY" "$SERVER_USER@$SERVER_IP" << 'ENDSSH'
set -e

echo "Updating system packages..."
sudo dnf update -y

echo "Installing Python 3.11..."
sudo dnf install -y python3.11 python3.11-pip python3.11-devel

echo "Installing Node.js 20..."
sudo dnf install -y nodejs20 npm

echo "Installing git..."
sudo dnf install -y git

echo "Installing nginx..."
sudo dnf install -y nginx

echo "✅ Dependencies installed!"
echo "Note: Playwright will install its own Chromium browser"
ENDSSH

# Step 2: Create application directory and copy files
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📂 Step 2: Creating app directory and copying files..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

ssh -i "$SSH_KEY" "$SERVER_USER@$SERVER_IP" "mkdir -p $APP_DIR"

echo "Copying project files (this may take a minute)..."
rsync -avz --progress \
  --exclude 'node_modules' \
  --exclude 'venv' \
  --exclude '__pycache__' \
  --exclude '.git' \
  --exclude '*.pyc' \
  --exclude '.env' \
  --exclude '*.log' \
  -e "ssh -i $SSH_KEY" \
  /Users/mariagorskikh/sundai_GEO/ \
  "$SERVER_USER@$SERVER_IP:$APP_DIR/"

echo "✅ Files copied!"

# Step 3: Setup backend
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🐍 Step 3: Setting up Python backend..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

ssh -i "$SSH_KEY" "$SERVER_USER@$SERVER_IP" << ENDSSH
set -e
cd $APP_DIR/geo-frontend/server

echo "Creating Python virtual environment..."
python3.11 -m venv venv
source venv/bin/activate

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Backend setup complete!"
ENDSSH

# Step 4: Setup testing environment
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🧪 Step 4: Setting up testing environment..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

ssh -i "$SSH_KEY" "$SERVER_USER@$SERVER_IP" << ENDSSH
set -e
cd $APP_DIR/geo-testing

echo "Creating Python virtual environment for testing..."
python3.11 -m venv venv
source venv/bin/activate

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Installing Playwright browsers..."
playwright install chromium
playwright install-deps chromium

echo "✅ Testing environment setup complete!"
ENDSSH

# Step 5: Setup frontend
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "⚛️  Step 5: Setting up React frontend..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

ssh -i "$SSH_KEY" "$SERVER_USER@$SERVER_IP" << ENDSSH
set -e
cd $APP_DIR/geo-frontend/client

echo "Installing npm dependencies..."
npm install

echo "Building production frontend..."
npm run build

echo "✅ Frontend built!"
ENDSSH

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Application deployed to EC2!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "⚠️  Next steps:"
echo "   1. Create .env files on server with your API keys"
echo "   2. Configure Nginx for domain: $DOMAIN"
echo "   3. Set up SSL certificate with Let's Encrypt"
echo "   4. Create systemd services to run backend"
echo ""
echo "Run: ./deploy-services.sh to complete setup"

