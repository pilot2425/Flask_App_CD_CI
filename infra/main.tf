provider "aws" {
  region = "eu-west-1"
}

resource "aws_s3_bucket" "jenkins_bucket" {
  bucket = var.bucket_name
  acl    = "private"
}
