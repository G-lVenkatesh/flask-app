# flask-app
## Live URL
http://public-ip

## Tech Stack
- **App**: Python + Flask + Gunicorn
- **Server:** AWS EC2 (Ubuntu 22.04, t2.micro)
- **Reverse Proxy:** Nginx

## Architecture
Internet → EC2 Public IP → Nginx (port 80) → Gunicorn → Flask (port 5000)

## Setup Steps
1. Launch EC2 (Ubuntu 22.04, t2.micro)
2. Install Python, Nginx
3. Clone repo & setup virtualenv
4. Run app via Gunicorn as a systemd service
5. Configure Nginx as reverse proxy
