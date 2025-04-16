provider "aws" {
  region = var.aws_region
}

resource "aws_security_group" "flask_sg" {
  name        = "${var.project_name}-sg"
  description = "Allow HTTP/Flask inbound traffic"

  ingress {
    from_port   = var.flask_port
    to_port     = var.flask_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-sg"
  }
}

resource "aws_instance" "flask_instance" {
  ami                         = var.ami_id
  instance_type               = var.instance_type
  key_name                    = var.key_pair_name
  vpc_security_group_ids      = [aws_security_group.flask_sg.id]
  associate_public_ip_address = true

  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              yum install -y python3 git
              pip3 install --upgrade pip
              cd /home/ec2-user
              git clone ${var.app_repo_url} flask-app
              cd flask-app
              pip3 install -r requirements.txt
              nohup python3 run.py > output.log 2>&1 &
              EOF

  tags = {
    Name = "${var.project_name}-instance"
  }
}
