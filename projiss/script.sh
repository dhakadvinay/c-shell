#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Starting automated environment setup..."

# 1. System Dependencies (C++ Build Tools)
echo "Installing C++ build tools and system dependencies..."
sudo dnf update -y
sudo dnf install -y cmake gcc gcc-c++ make python3-devel

# 2. Install and Start MySQL
echo "Installing MySQL Server..."
sudo dnf install -y community-mysql-server
sudo systemctl enable --now mysqld

# 3. Configure and Install MongoDB
echo "Setting up MongoDB repository..."
cat <<EOF | sudo tee /etc/yum.repos.d/mongodb-org.repo
[mongodb-org-7.0]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/redhat/9/mongodb-org/7.0/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-7.0.asc
EOF

echo "Installing MongoDB..."
sudo dnf install -y mongodb-org
sudo systemctl enable --now mongod

# 4. Install the 'uv' Package Manager
echo "Checking for 'uv' package manager..."
if ! command -v uv &> /dev/null
then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # Source the environment to use uv immediately in the script
    source $HOME/.local/bin/env || source $HOME/.cargo/env
else
    echo "uv is already installed."
fi

# 5. Initialize Project and Install Python Dependencies
echo "Setting up Python project and dependencies..."
# Initialize uv project (fails silently if already initialized)
uv init 2>/dev/null || true 

# Install Phase 1, 2, and 3 dependencies
uv add face-recognition numpy Pillow fastapi "uvicorn[standard]" pymongo mysql-connector-python requests websockets

echo "===================================================="
echo "✅ Setup Complete!"
echo "===================================================="
echo "ACTION REQUIRED:"
echo "1. Check your MySQL temporary root password:"
echo "   sudo grep 'temporary password' /var/log/mysqld.log"
echo "2. Log into MySQL and set your password to 'MySQLpassword42':"
echo "   mysql -u root -p"
echo "   ALTER USER 'root'@'localhost' IDENTIFIED BY 'MySQLpassword42';"
echo "3. Create your database:"
echo "   CREATE DATABASE project;"