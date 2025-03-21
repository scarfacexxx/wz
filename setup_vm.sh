#!/bin/bash

# Update system and install dependencies
sudo apt-get update
sudo apt-get install -y python3.8 python3.8-venv python3-pip mysql-server git

# Create project directory
sudo mkdir -p /opt/wizards-of-x
sudo chown -R $USER:$USER /opt/wizards-of-x

# Clone repository
cd /opt/wizards-of-x
git clone https://github.com/scarfacexxx/wz .

# Create and activate virtual environment
python3.8 -m venv venv
source venv/bin/activate

# Install project dependencies
pip install -r requirements.txt

# Setup MySQL
sudo mysql_secure_installation

# Create database and user
sudo mysql -e "CREATE DATABASE IF NOT EXISTS wizards_of_x;"
sudo mysql -e "CREATE USER IF NOT EXISTS 'wizard_user'@'localhost' IDENTIFIED BY 'wizard_pass';"
sudo mysql -e "GRANT ALL PRIVILEGES ON wizards_of_x.* TO 'wizard_user'@'localhost';"
sudo mysql -e "FLUSH PRIVILEGES;"

# Create systemd service
sudo tee /etc/systemd/system/wizards-of-x.service << EOF
[Unit]
Description=Wizards of X Game Service
After=network.target

[Service]
User=$USER
Group=$USER
WorkingDirectory=/opt/wizards-of-x
Environment="PATH=/opt/wizards-of-x/venv/bin"
ExecStart=/opt/wizards-of-x/venv/bin/python -m wizards_of_x.main

[Install]
WantedBy=multi-user.target
EOF

# Start and enable service
sudo systemctl daemon-reload
sudo systemctl enable wizards-of-x
sudo systemctl start wizards-of-x

echo "Setup complete!" 