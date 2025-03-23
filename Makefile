CC = gcc
CFLAGS = -Wall -Wextra
LDFLAGS = -ladvapi32
SRC = ft_fastexpo.c ft_findinverse.c ft_gcd.c ft_genprime.c ft_isprime.c ft_longrandom.c ft_pown.c
OBJ = $(SRC:.c=.o)
DEPS = crypto.h

all: $(SRC)

$(TARGET): $(OBJ)
	$(CC) $(OBJ) -o $@ $(LDFLAGS)

%.o: %.c $(DEPS)
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	del /Q *.o *.exe

.PHONY: all clean
