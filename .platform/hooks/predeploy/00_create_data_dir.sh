#!/bin/bash
set -e

# Create data directory and set ownership to webapp user
sudo mkdir -p /var/app/data
sudo chown -R webapp:webapp /var/app/data
sudo chmod -R 775 /var/app/data

echo "Data directory setup completed"
