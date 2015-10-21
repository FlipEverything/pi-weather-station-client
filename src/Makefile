BIN=../bin/
SRC=./

TARGET = read_sensor_temp
LIBS = -lwiringPi
CC = gcc
CFLAGS = -g -Wall

.PHONY: default all clean

default: $(TARGET)
all: default

OBJECTS = $(patsubst $(SRC)%.c, $(SRC)%.o, $(wildcard $(SRC)*.c))
HEADERS = $(wildcard $(SRC)*.h)

$(SRC)%.o: $(SRC)%.c $(HEADERS)
	$(CC) $(CFLAGS) -c $< -o $@

.PRECIOUS: $(TARGET) $(OBJECTS)

$(TARGET): $(OBJECTS)
	$(CC) $(OBJECTS) -Wall $(LIBS) -o $(BIN)$@

clean:
	-rm -f $(SRC)*.o
	-rm -f $(BIN)$(TARGET)
