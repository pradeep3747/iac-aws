output "instance_id" {
	description = "ID of the EC2 instance"
	value       = aws_instance.web.id
}

output "instance_public_ip" {
	description = "Public IP address of the EC2 instance"
	value       = aws_instance.web.public_ip
}

output "instance_public_dns" {
	description = "Public DNS name of the EC2 instance"
	value       = aws_instance.web.public_dns
}

output "instance_private_ip" {
	description = "Private IP address of the EC2 instance"
	value       = aws_instance.web.private_ip
}

output "instance_az" {
	description = "Availability zone of the EC2 instance"
	value       = aws_instance.web.availability_zone
}

output "instance_type" {
	description = "Instance type of the EC2 instance"
	value       = aws_instance.web.instance_type
}

output "instance_subnet_id" {
	description = "Subnet ID where the EC2 instance is launched"
	value       = aws_instance.web.subnet_id
}

output "instance_security_groups" {
	description = "Security groups attached to the EC2 instance"
	value       = aws_instance.web.security_groups
}

output "instance_ami" {
	description = "AMI used to launch the EC2 instance"
	value       = aws_instance.web.ami
}
