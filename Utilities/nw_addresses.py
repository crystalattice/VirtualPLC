#!/usr/bin/env python3
"""
VirtualPLC nw_addresses.py

Purpose: Utility functions to work with network addresses, such as IP and MAC addresses

Author: Cody Jackson

Date: 11/20/18
#################################
Version 0.1
    Initial build
"""
import netifaces
import socket


def get_ip(interface):
    """Get the IP address of the current device. Must be

    Currently retrieves the IPv4 address, but IPv6 is available by setting netifaces method call to AF_INET6.
    """
    addrs = netifaces.ifaddresses(interface)
    return addrs[netifaces.AF_INET][0]["addr"]


def local_address():
    """Can be used for systems not connected to Internet.

    Found on Stack Overflow (https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib)
    """
    return((([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [
        [(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in
         [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0])


def local_interfaces():
    """Returns the network interfaces on the local machine"""
    return netifaces.interfaces()


def interface_type(interface):
    """Returns the indicated network interfaces on the local machine"""
    interfaces = local_interfaces()
    print(interfaces)
    if interface == "Ethernet":
        conn = "enp"  # Check for Ethernet interfaces
    elif interface == "WiFi":
        conn = "wlp"  # Check for WiFi interfaces
    for item in interfaces:
        if item[:2] in conn:
            return item


if __name__ == "__main__":
    print(interface_type("WiFi"))
