terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.1"
    }
  }
}

provider "docker" {}

resource "docker_network" "transit_net" {
  name = "transit-network"
}

resource "docker_container" "transit_app" {
  name  = "transit-terraform-app"
  image = "transit-deals-app:latest"

  ports {
    internal = 8001
    external = 8001
  }

  networks_advanced {
    name = docker_network.transit_net.name
  }

  restart = "always"
}