terraform {
  backend "s3" {
    bucket = "iac-backup-statefile"
    key    = "terraform.tfstate"
    region = "us-east-1"
  }
}