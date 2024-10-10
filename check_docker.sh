#!/bin/bash

# Function to check if Docker is installed
check_docker() {
    if command -v docker >/dev/null 2>&1; then
        echo "Docker is installed."
    else
        echo "Docker is not installed. Installing Docker..."
        install_docker
    fi
}

# Function to install Docker
install_docker() {
    # Update the package index
    sudo apt-get update
    # Install necessary packages
    sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
    # Add Docker's official GPG key
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    # Add the Docker repository
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    # Update the package index again
    sudo apt-get update
    # Install Docker
    sudo apt-get install -y docker-ce
    echo "Docker has been installed."
}

# Run the check
check_docker
