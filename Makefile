CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra
TARGET = myvcs
SOURCES = main.cpp repository.cpp utils.cpp

all: $(TARGET)

$(TARGET): $(SOURCES)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(SOURCES)

clean:
	rm -f $(TARGET)

install: $(TARGET)
	cp $(TARGET) /usr/local/bin/

.PHONY: all clean install
