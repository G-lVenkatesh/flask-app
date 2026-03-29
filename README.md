# Flask App — AWS EC2 Deployment

A simple Python Flask application deployed on AWS EC2 using Docker and Nginx as a reverse proxy.

## Live URL

```
http://<YOUR-EC2-PUBLIC-IP>
```

---

## Architecture

```
Internet
   ↓
AWS EC2 (Ubuntu 22.04, t2.micro)
   ↓
Nginx — Reverse Proxy (port 80)
   ↓
Docker Container (port 5000)
   ↓
Gunicorn + Flask App
```

---

## Tech Stack

| Layer | Tool |
|-------|------|
| Cloud | AWS EC2 (Ubuntu 22.04, t2.micro) |
| Reverse Proxy | Nginx |
| Container | Docker |
| App Server | Gunicorn (2 workers) |
| Framework | Python Flask |
| Process Manager | systemd |

---

## Project Structure

```
flask-deployment/
├── app.py               # Flask application
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker image definition
└── README.md            # This file
```

---

## 📄 Application Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | Returns HTML homepage |
| `GET /health` | Returns JSON health status {"status": "ok"} |

---

## Deployment Steps

### 1. Launch EC2 Instance
- AMI: Ubuntu 22.04 LTS
- Instance Type: t2.micro (Free Tier)
- Generated key pair (.pem file)
- Security Group: HTTP (80), HTTPS (443), SSH (22) open

### 2. Install Dependencies on EC2

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv nginx git -y
sudo apt install docker.io -y
sudo usermod -aG docker ubuntu
newgrp docker
```

### 3. Clone Repo & Build Docker Image

```bash
git clone https://github.com/your-username/flask-deployment.git
cd flask-deployment
docker build -t flask-app .
```

### 4. Create systemd Service

```bash
sudo nano /etc/systemd/system/flaskapp.service
```

```ini
[Unit]
Description=Flask App
After=docker.service
Requires=docker.service

[Service]
Restart=always
ExecStartPre=-/usr/bin/docker stop flask-app
ExecStartPre=-/usr/bin/docker rm flask-app
ExecStart=/usr/bin/docker run --name flask-app -p 5000:5000 flask-app
ExecStop=/usr/bin/docker stop flask-app

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable flaskapp
sudo systemctl start flaskapp
```

### 5. Configure Nginx

```bash
sudo nano /etc/nginx/sites-available/flaskapp
```

```nginx
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/flaskapp /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```

---

## Verify Deployment

```bash
# Check container is running
docker ps

# Test app locally on EC2
curl http://127.0.0.1:5000

# Check service status
sudo systemctl status flaskapp
sudo systemctl status nginx
```

---

## Auto-Restart

The app is configured as a systemd service, so it:
- Automatically starts when EC2 reboots
- Restarts if the Docker container crashes
