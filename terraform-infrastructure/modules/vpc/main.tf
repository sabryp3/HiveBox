module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = var.vpc_name
  cidr = var.vpc_cidr
  azs = var.availability_zones
  private_subnets = var.private_subnet_cidr_blocks
  public_subnets = var.public_subnet_cidr_blocks
  enable_nat_gateway = true
  enable_vpn_gateway = false
  single_nat_gateway = true
  enable_dns_support = true
  enable_dns_hostnames = true
  public_subnet_tags = {
    // AWS Cloud Controller Manager require subnets to have this tags
    "kubernetes.io/cluster/${var.cluster_name}" = "shared" //AWS Cloud Controller Manager query a cluster's subnets to identify them. The shared value allows more than one cluster to use the subnet.
    "kubernetes.io/role/elb"                    = 1        //Cloud Controller Manager determines if a subnet is public
  }
  private_subnet_tags = {
    "kubernetes.io/cluster/${var.cluster_name}" = "shared" //AWS Cloud Controller Manager query a cluster's subnets to identify them. The shared value allows more than one cluster to use the subnet.
    "kubernetes.io/role/internal-elb"           = 1        //Cloud Controller Manager determines if a subnet is private
  }
  tags = {
    "kubernetes.io/cluster/${var.cluster_name}" = "shared"
    Environment = var.environment
  }
}