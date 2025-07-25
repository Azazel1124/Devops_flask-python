resource "aws_instance" "example" {
  ami           = "ami-0c02fb55956c7d316" # Ubuntu 20.04 LTS
  instance_type = "t2.micro"

  tags = {
    Name = "DevopsFlaskPythonInstance"
  }
} 
