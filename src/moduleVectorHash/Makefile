PROG = moduleVectorHash
HDRS = vector.h hashset.h support.h
SRCS = vector.c hashset.c support.c
OBJS = vector.o hashset.o support.o

compile:
	cc -fPIC -c $(SRCS)
	cc -shared -o $(PROG).so $(OBJS)
	@echo "Make complete."

clean:
	rm -f core $(PROG).so $(OBJS)
	@echo "$(obj) files are removed."