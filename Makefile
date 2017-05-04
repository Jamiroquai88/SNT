CP=g++
CPFLAGS=-std=c++11 -pthread -pedantic -Wall
CPP_FILES := $(wildcard *.cpp)
OBJ_FILES := $(CPP_FILES:.cpp=.o)

all: CPFLAGS += -O3
all: checksln

checksln: checksln.o
	$(CP) $(CPFLAGS) $^ -o $@ -lm

%.o:%.cpp
	$(CP) $(CPFLAGS) -c $< -o $@ -I/usr/local/include -L/usr/local/lib64 -lm

clean:
	$(RM) checksln $(OBJ_FILES) *.h.gch

zip:
	zip xprofa00.zip *.cpp *.h Makefile xprofa00.pdf
