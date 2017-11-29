CC = gcc
CFLAGS = -O3 -DMaxSAT
target = wlmc
all : $(target)

$(target) : wlmc-large-weight.c
	$(CC) $(CFLAGS) wlmc-large-weight.c -o $(target) -mcmodel=medium

clean :
	-rm $(target)
