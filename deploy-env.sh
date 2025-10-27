#!/bin/bash
set -e

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║         🔐 GEO PLATFORM ENVIRONMENT SETUP                     ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Configuration
SERVER_IP="54.221.56.44"
SERVER_USER="ec2-user"
SSH_KEY="$HOME/Downloads/my.pem"
APP_DIR="/home/ec2-user/geo-platform"

echo "This script will copy your local .env files to the server."
echo "Make sure you have:"
echo "  1. /Users/mariagorskikh/sundai_GEO/geo-frontend/server/.env"
echo "  2. /Users/mariagorskikh/sundai_GEO/geo-testing/.env"
echo ""

# Check if .env files exist locally
if [ ! -f "/Users/mariagorskikh/sundai_GEO/geo-frontend/server/.env" ]; then
    echo "❌ Backend .env file not found!"
    echo "   Create it at: /Users/mariagorskikh/sundai_GEO/geo-frontend/server/.env"
    exit 1
fi

if [ ! -f "/Users/mariagorskikh/sundai_GEO/geo-testing/.env" ]; then
    echo "❌ Testing .env file not found!"
    echo "   Create it at: /Users/mariagorskikh/sundai_GEO/geo-testing/.env"
    exit 1
fi

echo "📤 Copying backend .env..."
scp -i "$SSH_KEY" \
    /Users/mariagorskikh/sundai_GEO/geo-frontend/server/.env \
    "$SERVER_USER@$SERVER_IP:$APP_DIR/geo-frontend/server/.env"

echo "📤 Copying testing .env..."
scp -i "$SSH_KEY" \
    /Users/mariagorskikh/sundai_GEO/geo-testing/.env \
    "$SERVER_USER@$SERVER_IP:$APP_DIR/geo-testing/.env"

echo "✅ Environment files copied!"
echo ""
echo "🔄 Restarting backend service..."
ssh -i "$SSH_KEY" "$SERVER_USER@$SERVER_IP" "sudo systemctl restart geo-backend"

echo ""
echo "✅ Done! Backend restarted with new environment variables."

