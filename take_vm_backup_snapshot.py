#!/usr/bin/env python

"""
Take backup snapshot of a VM managed by a VMware vCenter
"""

from pyVim import connect
from pyVmomi import vim
import argparse
import logging
import time
import ssl

# Set logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%m/%d/%y %H:%M')

def create_vcenter_connection(vcenter_host, vcenter_user, vcenter_pwd):
    """Get VM object by its DNS name or if not found by its VM name"""
    try:
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        context.verify_mode = ssl.CERT_NONE
        si = connect.SmartConnect(host=vcenter_host,
                                  user=vcenter_user,
                                  pwd=vcenter_pwd,
                                  sslContext=context)
        logging.info("Connection successful with vCenter %s" % vcenter_host)
        return si
    except:
        raise SystemExit("ABORT: Unable to connect to vCenter %s with the provided credentials" % vcenter_host)


def get_vm_object(vcenter_host, vcenter_user, vcenter_pwd, vm_name):
    """Get VM object by its DNS name or if not found by its VM name"""
    # Create connection with vCenter and get vC serviceInstance
    vCenter_si = create_vcenter_connection(vcenter_host, vcenter_user, vcenter_pwd)

    # Get VM by DNS name
    # The DNS name for a virtual machine is the one returned from VMware tools, hostName
    vm = vCenter_si.content.searchIndex.FindByDnsName(dnsName=vm_name, vmSearch=True)

    if not vm:
        # Get VM by VM name
        container = vCenter_si.content.viewManager.CreateContainerView(
                    container=vCenter_si.content.rootFolder,
                    type=[vim.VirtualMachine],
                    recursive=True)
        for c in container.view:
            if c.name == vm_name:
                return c
    return vm


def take_backup_snapshot_on_vm(vm, vm_name):
    """Take backup snapshot of the VM"""
    timestamp = time.strftime("%m%d%y-%H%M", time.gmtime())
    snapshot_task = vm.CreateSnapshot_Task(
                            name="backup_%s" % timestamp,
                            description="Backup snapshot of VM '%s' triggered at GMT time %s" % (vm_name, timestamp),
                            memory=True,
                            quiesce=True)

    logging.info("Taking backup snaphost for VM '%s'" % vm_name)
    while snapshot_task.info.state == vim.TaskInfo.State.running:
        time.sleep(1)
    if snapshot_task.info.state != vim.TaskInfo.State.success:
        raise SystemExit("ABORT: Taking VM backup snaphost for VM '%s' failed" % vm_name)

    logging.info("Backup snaphost for VM '%s' succesfully taken!" % vm_name)


def main(vcenter_host, vcenter_user, vcenter_pwd, vm_name):
    # Get VM object by its DNS name or its VM name
    vm = get_vm_object(vcenter_host, vcenter_user, vcenter_pwd, vm_name)

    # Take a backup snapshot of the target VM
    take_backup_snapshot_on_vm(vm, vm_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Take a backup snapshot of a VM')
    parser.add_argument('--vcenter-host', help='vCenter Host/IP', required=True)
    parser.add_argument('--vcenter-user', help='vCenter username', required=True)
    parser.add_argument('--vcenter-pwd', help='vCenter password', required=True)
    parser.add_argument('--vm-name', help='Target VM name or DNS name', required=True)
    args = vars(parser.parse_args())

    main(args['vcenter_host'], args['vcenter_user'], args['vcenter_pwd'], args['vm_name'])
