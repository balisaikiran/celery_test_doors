#!/bin/bash

# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install Python and Redis
sudo apt-get install -y python3-pip redis-server

# Install project dependencies
pip3 install -r requirements.txt

# Create systemd service for Redis
sudo tee /etc/systemd/system/redis.service << EOF
[Unit]
Description=Redis In-Memory Data Store
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/redis-server
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Create systemd service for Celery Worker
sudo tee /etc/systemd/system/celery-worker.service << EOF
[Unit]
Description=Celery Worker Service
After=network.target redis.service

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/zillow-scraper
Environment=REDIS_URL=redis://localhost:6379
ExecStart=/usr/local/bin/celery -A celery_app worker --loglevel=info
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Create systemd service for Celery Beat
sudo tee /etc/systemd/system/celery-beat.service << EOF
[Unit]
Description=Celery Beat Service
After=network.target redis.service

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/zillow-scraper
Environment=REDIS_URL=redis://localhost:6379
ExecStart=/usr/local/bin/celery -A celery_app beat --loglevel=info
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Start and enable services
sudo systemctl daemon-reload
sudo systemctl start redis
sudo systemctl enable redis
sudo systemctl start celery-worker
sudo systemctl enable celery-worker
sudo systemctl start celery-beat
sudo systemctl enable celery-beat