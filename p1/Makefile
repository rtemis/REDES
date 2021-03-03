###############################################################################
#                                  MAKEFILE                                   #
#-----------------------------------------------------------------------------#
# Authors: Leah Hadeed													      #
# 		   Nazariy Gunko													  #
#-----------------------------------------------------------------------------#
# Grupo: 2311																  #
# Subject: REDES II 														  #
# Assignment: Pactica 1 													  #
###############################################################################

###############################################################################
#                                 DEFINITIONS                                 #
###############################################################################

# Compiler
CC = gcc
# Compile flags
CFLAGS = -Wall -ansi
# Valgrind flags
VFLAGS = --leak-check=full
# Shared static library flags
STDLFLAGS = -lpthread -lconfuse
# PicoHTTTPParser static library flags
PCOFLAG = -Llib -lpicohttpparser
# Requests static library flags
REQFLAG = -Llib -lrequests

# Header file flags
HEADERS = -I include

# Directories
SRC_DIR = src/
INC_DIR = include/
OBJ_DIR = obj/
LIB_DIR = lib/

# Executable programs
EXE = webserver exit 

###############################################################################
#                                 DEFINITIONS                                 #
###############################################################################

# Make all command
all: clean static objects $(EXE) clear

# Make without recompiling static libraries
no-static: clear objects $(EXE) clear

# Clean command removes executables, objects, libraries, and dependencies
clean:
	rm -f $(EXE) $(DEXE) $(OBJ_DIR)*.o $(INC_DIR)*.h.gch daemonPid.txt $(LIB_DIR)*

# Clear command removes the objects and dependencies
clear:
	rm -f $(OBJ_DIR)*.o $(INC_DIR)*.h.gch

# Creation of static libraries
static: $(LIB_DIR)libpicohttpparser.a $(LIB_DIR)librequests.a

# Creation of object files
objects: $(OBJ_DIR)server.o $(OBJ_DIR)threads.o $(OBJ_DIR)servidor_thread.o

# Creation of folders in the case that they don't previously exist
folders:
		@mkdir obj
		@mkdir lib

# Removal of phony commands
.PHONY: clean

###############################################################################
#                       DEFINITIONS - STATIC LIBRARIES                        #
###############################################################################

# Creation of static libraries
$(LIB_DIR)libpicohttpparser.a: $(OBJ_DIR)picohttpparser.o
	ar -r $@ $^

$(LIB_DIR)librequests.a: $(OBJ_DIR)picohttpparser.o $(OBJ_DIR)petitions.o $(OBJ_DIR)functions.o
	ar -r $@ $^


###############################################################################
#                                 EXECUTABLES                                 #
###############################################################################

# Creation of main executable
servidor_thread: $(SRC_DIR)servidor_thread.c $(SRC_DIR)server.c $(SRC_DIR)threads.c
	$(CC) $(CFLAGS) $^ $(HEADERS) $(STDLFLAGS) $(PCOFLAG) $(REQFLAG) -o $@

# Creation of daemon executable
webserver: $(SRC_DIR)demonizar.c $(SRC_DIR)servidor_thread.c $(SRC_DIR)server.c $(SRC_DIR)threads.c
	$(CC) $(CFLAGS) $^ $(HEADERS) $(STDLFLAGS) $(PCOFLAG) $(REQFLAG) -o $@

# Creation of exit executable 
exit: $(SRC_DIR)exit.c 
	$(CC) $(CFLAGS) $^ $(HEADERS) -o $@
###############################################################################
#                                   OBJECTS                                   #
###############################################################################

# Creation of objects
$(OBJ_DIR)functions.o : $(SRC_DIR)functions.c
	@echo "#---------------------------"
	@echo "# Generating: $@"
	@echo "# Dependencies: $^"
	@echo "# Modified: $<"
	$(CC) $(CFLAGS) -c $^ $(HEADERS) -o $@
	@echo "#---------------------------"

$(OBJ_DIR)petitions.o : $(SRC_DIR)petitions.c
	@echo "#---------------------------"
	@echo "# Generating: $@"
	@echo "# Dependencies: $^"
	@echo "# Modified: $<"
	$(CC) $(CFLAGS) -c $^ $(HEADERS) -o $@
	@echo "#---------------------------"

$(OBJ_DIR)server.o : $(SRC_DIR)server.c
	@echo "#---------------------------"
	@echo "# Generating: $@"
	@echo "# Dependencies: $^"
	@echo "# Modified: $<"
	$(CC) $(CFLAGS) -c $^ $(HEADERS) $(STDLFLAGS) $(PCOFLAG) -o $@
	@echo "#---------------------------"

$(OBJ_DIR)threads.o : $(SRC_DIR)threads.c
	@echo "#---------------------------"
	@echo "# Generating: $@"
	@echo "# Dependencies: $^"
	@echo "# Modified: $<"
	$(CC) $(CFLAGS) -c $^ $(HEADERS) $(STDLFLAGS) -o $@
	@echo "#---------------------------"

$(OBJ_DIR)picohttpparser.o : $(SRC_DIR)picohttpparser.c
	@echo "#---------------------------"
	@echo "# Generating: $@"
	@echo "# Dependencies: $^"
	@echo "# Modified: $<"
	$(CC) $(CFLAGS) -c $^ $(HEADERS) -o $@
	@echo "#---------------------------"

$(OBJ_DIR)servidor_thread.o : $(SRC_DIR)servidor_thread.c
	@echo "#---------------------------"
	@echo "# Generating: $@"
	@echo "# Dependencies: $^"
	@echo "# Modified: $<"
	$(CC) $(CFLAGS) -c $^ $(HEADERS) -o $@
	@echo "#---------------------------"

###############################################################################
#                           TARGET EXECUTION CODES                            #
###############################################################################

# Run server normally with terminal feedback
run:
	@echo "#---------------------------"
	@echo "# Starting server..."
	@echo "#---------------------------"
	@./webserver 
	
# Run server in valgrind
runv:
	@echo "#---------------------------"
	@echo "# Starting server with memory check..."
	@echo "#---------------------------"
	@valgrind $(VFLAGS) ./webserver 

# Exit server 
rune:
	@echo "#---------------------------"
	@echo "# Exiting server..."
	@echo "#---------------------------"
	@./exit 