#!/bin/bash
# ════════════════════════════════════════════════════════
# deploy.sh — Full Server Deployment Script
# Tested on Ubuntu 22.04 LTS
#
# Usage: bash deploy.sh
# ════════════════════════════════════════════════════════

set -e  # Exit on any error

APP_DIR="/var/www/rumahalam"
APP_USER="www-data"
LOG_DIR="/var/log/rumahalam"
DOMAIN="rumahalam.my"    # ← Change to your domain

echo ""
echo "🌿 Deploying Rumah Alam Homestay..."
echo "════════════════════════════════"

# 1. System packages
echo "📦 Installing system packages..."
sudo apt-get update -q
sudo apt-get install -y python3 python3-pip python3-venv nginx certbot python3-certbot-nginx

# 2. Create app directory
echo "📁 Setting up app directory..."
sudo mkdir -p $APP_DIR $LOG_DIR
sudo chown -R $USER:$USER $APP_DIR
sudo chown -R $APP_USER:$APP_USER $LOG_DIR

# 3. Copy app files
echo "📋 Copying application files..."
cp -r . $APP_DIR/
cd $APP_DIR

# 4. Python virtual environment
echo "🐍 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt gunicorn -q

# 5. Initialise database
echo "🗄️  Initialising database..."
python manage.py init

# 6. Set permissions
sudo chown -R $APP_USER:$APP_USER $APP_DIR/data $LOG_DIR
sudo chmod 750 $APP_DIR/data

# 7. Copy env file
if [ ! -f "$APP_DIR/.env" ]; then
    cp .env.example .env
    echo "⚙️  Created .env from template — please edit $APP_DIR/.env with your settings"
fi

# 8. Nginx config
echo "🌐 Configuring Nginx..."
sudo cp deploy/nginx.conf /etc/nginx/sites-available/rumahalam
# Update domain in config
sudo sed -i "s/rumahalam.my/$DOMAIN/g" /etc/nginx/sites-available/rumahalam
sudo ln -sf /etc/nginx/sites-available/rumahalam /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# 9. Systemd service
echo "⚙️  Configuring systemd service..."
sudo cp deploy/rumahalam.service /etc/systemd/system/
sudo sed -i "s|/var/www/rumahalam|$APP_DIR|g" /etc/systemd/system/rumahalam.service
sudo systemctl daemon-reload
sudo systemctl enable rumahalam
sudo systemctl start rumahalam

# 10. SSL (optional — requires DNS to point to this server)
read -p "Setup SSL with Let's Encrypt for $DOMAIN? (y/N): " setup_ssl
if [[ "$setup_ssl" == "y" || "$setup_ssl" == "Y" ]]; then
    sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN
fi

echo ""
echo "✅ Deployment complete!"
echo "════════════════════════════════"
echo "  Website  → http://$DOMAIN"
echo "  Admin    → http://$DOMAIN/admin"
echo "  API docs → http://$DOMAIN/api/docs"
echo ""
echo "Useful commands:"
echo "  sudo systemctl status rumahalam    # Check app status"
echo "  sudo journalctl -u rumahalam -f    # Live logs"
echo "  sudo systemctl restart rumahalam   # Restart app"
echo "  python manage.py stats             # DB statistics"
echo "  python manage.py export            # Export bookings to CSV"
echo ""
