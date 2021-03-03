/**
 * @file threads.c
 * @author Nazariy Gunko
 * @author Leah Hadeed
 * @brief Implementation of the thread functionality we will to implement the server.
 */
#include "threads.h"

/* Creation of thread pool */
void thread_make(int i){
	int control;
	/* Thread creation and routine assignation */
	control = pthread_create(&(tptr[i].thread_id), NULL, thread_main, (void *) (intptr_t) i);
	/* Error control */
	if (control != 0) {
		perror("Thread creation");
		free(tptr);
	}
	return;
}

/* Thread routine */
void *thread_main(void* arg){
	socklen_t clilen;

	/* Accept loop for server thread pool */
	for ( ; ; ) {

		/* Set the address size */
		clilen = addrlen;
		/* Error checking */
		if (clilen < 0) {
			perror("Error with memory assignation. ");
			exit(-1);
		}

		/* Accept needs to be controlled by semaphore to assure unique access to shared variables */
		pthread_mutex_lock(&mlock);
		/* Accept controls the amount of petitions that the server can handle */
		connection[(intptr_t) arg] = accept(socketfd, cliaddr[(intptr_t) arg], &clilen);
		/* Unlock semaphore to let the following threads through */
		pthread_mutex_unlock(&mlock);

		/* Increments the thread pool counter */
		tptr[(intptr_t) arg].count++;
		/* Function manages server client communication on per thread basis */
		server_main(connection[(intptr_t) arg]);

		/* Close connection after use */
		close(connection[(intptr_t) arg]);
	}

}
