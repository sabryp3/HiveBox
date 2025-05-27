module "eks" {
  source  = "terraform-aws-modules/eks/aws"

  cluster_name    = var.cluster_name
  cluster_version = var.cluster_version

  vpc_id     = var.vpc_id
  subnet_ids = var.private_subnet_ids //Cluster is deployed in private subnet

  cluster_endpoint_private_access = true
  cluster_endpoint_public_access  = true
  //cluster_endpoint_public_access_cidrs can be added to restrict the cidrs for public access. https://github.com/terraform-aws-modules/terraform-aws-eks/issues/1867

  eks_managed_node_group_defaults = { //Map of EKS managed node group default configurations
    instance_types         = var.instance_types
  }
  eks_managed_node_groups = { //Map of EKS managed node group definitions to create
    nodegroup1 = {
      labels = {
        NodeGroup = "nodegroup1"
      }
      min_size     = var.min_capacity
      max_size     = var.max_capacity
      desired_size = var.desired_capacity

      instance_types = var.instance_types
      capacity_type  = "SPOT"
    }
  }
  cluster_addons = {
    coredns = {
      most_recent = true
    }
    kube-proxy = {
      most_recent = true
    }
    vpc-cni = {
      most_recent = true
    }
  }

}
