__author__ = 'napperley'

# -*- coding: utf-8 -*-
#
# Establishes an OpenVPN connection using an OVPN file. Based on a Hacking Lab Python script
# (http://media.hacking-lab.com/largefiles/livecd/z_openvpn_config/backtrack/vpn-with-python.py). Requires Python 3
# and the pexpect library (module).
#
# Copyright 2015 Nick Apperley

import pexpect

# Set the timeout in seconds.
timeout = 15


def open_vpn_connection(username, password, conf_dir, ovpn_file):
    process = pexpect.spawn('openvpn %s' % ovpn_file, cwd=conf_dir, timeout=timeout)

    process.expect('Enter Auth Username:')
    process.sendline(username)
    process.expect('Enter Auth Password:')
    process.sendline(password)

    print('Connecting...')
    process.expect('Initialization Sequence Completed')
    print('Connected')
    return process


def close_vpn_connection(process):
    if process is not None:
        process.kill(0)
