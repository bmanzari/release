#!/usr/bin/env python

import os

def log(msg):
  print(msg)

try:
    from pylint.lint import Run
    file_path = os.path.realpath(__file__)
    Run([file_path], exit=False)
except ImportError:
    log("linter not available, run outside of CI")

shared_dir = os.environ.get("SHARED_DIR")
namespace = os.environ["NAMESPACE"]
cluster_name=f"{namespace}"

platform_spec = f"""platform:
  vsphere:
    vcenters:
      - server: {cluster_name}-vcenter-1
        datacenters:
        - cidatacenter-nested-0
        - cidatacenter-nested-1
    failureDomains:
      - server: {cluster_name}-1
        name: "zone-1"
        zone: "zone-1"
        region: "region-1"
        topology:
          resourcePool: /cidatacenter-nested-0/host/cicluster-nested-0/Resources/ipi-ci-clusters
          computeCluster: /cidatacenter-nested-0/host/cicluster-nested-0
          datacenter: cidatacenter-nested-0
          datastore: /cidatacenter-nested-0/datastore/dsnested
          networks:
            - "VM Network"
      - server: {cluster_name}-vcenter-1
        name: "zone-2"
        zone: "zone-2"
        region: "region-2"
        topology:
          resourcePool: /cidatacenter-nested-1/host/cicluster-nested-1/Resources/ipi-ci-clusters
          computeCluster: /cidatacenter-nested-1/host/cicluster-nested-1
          datacenter: cidatacenter-nested-1
          datastore: /cidatacenter-nested-1/datastore/dsnested
          networks:
            - "VM Network"
"""

with open(os.path.join(shared_dir, "nested-ansible-platform.yaml"), "w") as nested_ansible_platform_file:
    nested_ansible_platform_file.write(platform_spec)