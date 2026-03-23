#!/bin/bash
# EC2 User Data script to install Docker and prepare for CommandX deployment

# Wait to ensure OS package manager locks are released during boot
sleep 15

# Detect OS
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    OS="unknown"
fi

if [ "$OS" == "amzn" ]; then
    yum update -y
    amazon-linux-extras install docker -y || yum install docker -y
    yum install git -y
    systemctl start docker
    systemctl enable docker
    usermod -aG docker ec2-user
elif [ "$OS" == "ubuntu" ]; then
    apt-get update -y
    apt-get install -y docker.io git curl
    systemctl start docker
    systemctl enable docker
    usermod -aG docker ubuntu
fi

# Note: Once the instance is running and you have SSH access,
# execute the following commands to start the pipeline:
#
# git clone https://github.com/yourusername/CommandX.git
# cd CommandX
# docker build -t commandx:latest .
# docker run -d -p 80:8501 --name commandx --restart unless-stopped commandx:latest
