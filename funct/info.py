#!/usr/bin/env python3

from socket import gethostname
from platform import system, release, machine
from os import getlogin

def username():
    return getlogin()

def hostname():
    return gethostname()

def uptime():
    with open('/proc/uptime', 'r') as f:
        seconds = float(f.readline().split()[0])

    return seconds

def hardware_model():
    with open('/sys/devices/virtual/dmi/id/sys_vendor', 'r') as f:
        vendor = f.readline().strip()

    with open('/sys/devices/virtual/dmi/id/product_name', 'r') as f:
        product = f.readline().strip()

    return " ".join((str(vendor), str(product)))

def os():
    with open('/etc/os-release', 'r') as f:
        for line in f:
            if "PRETTY_NAME=" in line:
                x = line.rstrip().split("=")[1]
                x = x.strip('"')
                break

    return x

def kernel():
    return " ".join((system(), release()))

def machines():
    return machine()

def cpu_name():
    name = ""
    with open('/proc/cpuinfo', 'r') as f:
        for line in f:
            if line.lower().startswith('model name'):
                name = (line.split(":")[1]).strip()
                break

    return name