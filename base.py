# -*- coding: UTF-8 -*-
from pwn import *
from sys import exit
import argparse

parser = argparse.ArgumentParser()

group = parser.add_mutually_exclusive_group()
group.add_argument("-o", help="path to an elf file.",  metavar="<path to file>")
group.add_argument("-r", help="address of an remote machine.", metavar="<ip:port>")
parser.add_argument("-v", help="debug log level, default level is error.", action="store_true")
parser.add_argument("-g", help="start gdb to debug", action="store_true")
parser.add_argument("-b", help="breakpoints", metavar="main | 0x40115d")
parser.add_argument("--libc", help="specify the libc to preload", metavar="<path to file>")

args = parser.parse_args()

context.terminal = ['tmux', 'splitw', '-h']
elf = ELF(args.o)

verbose_enbale = args.v
gdb_enable = args.g

breakpoint = args.b
remote_addr = args.r
libc = args.libc
env = ''

if not elf and not remote_addr:
    parser.print_usage()
    exit()
if verbose_enbale == True:
    context.log_level = 'debug'
if libc:
    env = {'LD_PRELOAD': libc}
if elf:
    if gdb_enable == True:
        if env:
            p = gdb.debug(elf.path,  'b main\n ' + 'b ' + breakpoint, env=env)
        else:
            p = gdb.debug(elf.path,  'b main\n ' + 'b ' + breakpoint)
    else:
        if env:
            p = process(elf.path, env=env)
        else:
            p = process(elf.path)
else:
    remote_addr = remote_addr.split(':')
    p = remote(remote_addr[0], remote_addr[1])


def sd(delim, data): return p.send(delim, data)
def sa(delim, data): return p.sendafter(delim, data)
def sl(data): return p.sendline(data)
def sla(delim, data): return p.sendlineafter(delim, data)
def rc(num): return p.recv(num)
def rl(): return p.recvline()
def ru(delims): return p.recvuntil(delims)
def uu32(data): return u32(data.ljust(4, b'\x00'))
def uu64(data): return u64(data.ljust(8, b'\x00'))
def info(tag, addr): return log.info(tag + " -> " + hex(addr))
def ia(): return p.interactive()
