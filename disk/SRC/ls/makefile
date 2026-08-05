# makefile -- build ls for OS-9/68k
# Usage (inside os9exec):  make
# Then:                     copy ls /dd/CMDS/SHARE/ls

CC = gcc
CFLAGS = -O

ls: ls.c
	$(CC) $(CFLAGS) -o ls ls.c

clean:
	del ls
