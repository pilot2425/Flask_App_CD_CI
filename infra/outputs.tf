output "instance_public_ip" {
  description = "Public IP of the Flask EC2 instance"
  value       = aws_instance.flask_instance.public_ip
}

output "access_url" {
  description = "Access URL for the Flask app"
  value       = "http://${aws_instance.flask_instance.public_ip}:${var.flask_port}"
}
