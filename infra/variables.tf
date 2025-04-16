variable "aws_region" {
  description = "AWS region to deploy in"
  default     = "eu-west-1"
}

variable "ami_id" {
  description = "AMI ID for Amazon Linux 2"
  default     = "ami-0c02fb55956c7d316" # EU (Ireland) Amazon Linux 2
}

variable "instance_type" {
  description = "EC2 instance type"
  default     = "t2.micro"
}

variable "flask_port" {
  description = "Port for Flask app"
  default     = 5000
}

variable "key_pair_name" {
  description = "Name of the EC2 Key Pair"
}

variable "project_name" {
  description = "Name of the project/app"
  default     = "flask-app"
}

variable "app_repo_url" {
  description = "GitHub repository with Flask app"
}
