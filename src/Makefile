PROG = libVectorHash
HDRS = vector.h hashset.h
SRCS = vector.c hashset.c
OBJS = vector.o hashset.o

compile:
	cc -fPIC -c $(SRCS)
	cc -shared -o $(PROG) $(OBJS)
	@echo "make complete."

clean :
	rm -f core $(PROG) $(OBJS)
	@echo "$(obj) files are removed."