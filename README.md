# Zillow Scraper with Celery on EC2

## Setup Instructions

1. Launch an EC2 instance:
   - Use Ubuntu Server 22.04 LTS
   - t2.micro is sufficient for basic usage
   - Configure security group to allow SSH (port 22)

2. Connect to your EC2 instance:
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   ```

3. Clone your project:
   ```bash
   git clone <your-repo> zillow-scraper
   cd zillow-scraper
   ```

4. Make setup script executable and run it:
   ```bash
   chmod +x setup_ec2.sh
   ./setup_ec2.sh
   ```

5. Check service status:
   ```bash
   sudo systemctl status redis
   sudo systemctl status celery-worker
   sudo systemctl status celery-beat
   ```

6. View logs:
   ```bash
   # Redis logs
   sudo journalctl -u redis

   # Celery worker logs
   sudo journalctl -u celery-worker

   # Celery beat logs
   sudo journalctl -u celery-beat
   ```

## Maintenance

- Restart services:
  ```bash
  sudo systemctl restart celery-worker
  sudo systemctl restart celery-beat
  ```

- View real-time logs:
  ```bash
  sudo journalctl -f -u celery-worker
  ```# celery_test_doors
# celery_test_doors
