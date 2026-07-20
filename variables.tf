variable "ami_id" {
  description = "AMI ID for the EC2 instance"
  type        = string
  default = "ami-098e39bafa7e7303d"
  
}
variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t2.micro"
  
}
variable "notification_email" {
  type        = string
  description = "The email address to receive resource count reports"
  default     = "pradeep.reddy91011@gmail.com" # Replace with your email
}

variable "aws_region" {
  type    = string
  default = "us-east-1"
}