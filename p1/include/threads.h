/**
 * @file threads.h
 * @author Nazariy Gunko
 * @author Leah Hadeed
 * @brief Library that contains thread utility for server use.
 */
#ifndef __THREADS_H__
#define __THREADS_H__

/* Predefined Libraries Used */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <errno.h>
#include <unistd.h>
#include <pthread.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <signal.h>

/* Newly designed libraries used */
#include "petitions.h"
/**
* @brief Thread structure
*/
typedef struct {
  pthread_t thread_id;
  long count;
} Thread;

/**
* @brief Definition of global variables
*/
Thread* tptr;
int socketfd, nthreads;
socklen_t addrlen;
pthread_mutex_t mlock;
struct sockaddr ** cliaddr;
int * connection;


/**
* @brief Creation of thread
*
* Fucntion that creates a thread pool for later use.
* The thread pool allows for simultaneous petition processing
* from server side development.
*
* @param thread id
*
* @return void
*/
void thread_make(int i);

/**
* @brief Main thread function
*
* This function controls the instruction execution of the server thread pool.
* Each thread produces its own accept to handle server petitions. This is
* controlled by a semaphore to prevent unwanted memory access and overwrites. 
*
* @param thread id
* @return void
*/
void *thread_main(void* arg);

#endif
