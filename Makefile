CC = gcc -std=c99
CFLAGS = -Wall -Wextra
LDFLAGS = -ladvapi32

SRC = ft_fastexpo.c ft_findinverse.c ft_gcd.c ft_genprime.c ft_isprime.c ft_longrandom.c ft_pown.c main.c
OBJ = $(SRC:.c=.o)
TARGET = program

all: $(TARGET)

$(TARGET): $(OBJ)
	$(CC) $(OBJ) -o $@ $(LDFLAGS)

%.o: %.c crypto.h
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	del /Q *.o *.exe

restart:
	make clean && make all

.PHONY: all clean restart
