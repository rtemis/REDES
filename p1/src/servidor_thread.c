/**
 * @file servidor_thread.c
 * @author Nazariy Gunko
 * @author Leah Hadeed
 * @brief Implementation of server setup.
 */

/* To be able to use the function pthread_kill */
#define _POSIX_C_SOURCE 199506L

/* Included libraries */
#include "server.h"
#include "threads.h"

void handler(int sig) {
	int i;

	/* Frees used memory before exit */
	for (i = 0; i < nthreads; i++) {
		pthread_kill(tptr[i].thread_id, SIGKILL);
		pthread_join(tptr[i].thread_id, NULL);
		free(cliaddr[i]);
	}

	/* Liberates memory held by thread pool pointer */
	free(tptr);
	/* Liberates memory held by client address pointer */
	free(cliaddr);
	/* Liberates memory held by connections */
	free(connection);
	/* Liberates memory used in libconfuse pointer */
	cfg_free(cfg);
	/* Closes socket */
	close_socket(socketfd);
	/* Exit program successfully */
	exit(0);
}

/* Main server code */
int servidor_thread(char * current_dir) {
	int i;
 	struct sockaddr_in new_server;

 	/* Change working directory to root directory */
	if ((chdir(current_dir)) < 0) {
		exit(EXIT_FAILURE);
	}
	/* Creation of parameter list to parse from server.conf */
	cfg_opt_t opts[] =
	{
		CFG_STR("server_root", "htmlfiles/", CFGF_NONE),
		CFG_INT("listen_port", 9999, CFGF_NONE),
		CFG_INT("max_clients", 10, CFGF_NONE),
		CFG_STR("server_signature", 0, CFGF_NONE),
		CFG_END()
	};

	/* Here is where libconfuse is used to parse from server.conf */
	cfg = cfg_init(opts, CFGF_NONE);
	/* Testing output of parsing */
	switch (cfg_parse(cfg, "server.conf")) {
		case CFG_FILE_ERROR:
			perror("Configuration file could not be read.");
			exit(EXIT_FAILURE);
		case CFG_PARSE_ERROR:
			perror("Parsing error.");
			exit(EXIT_FAILURE);
		default:
			break;
	}

	/* Socket creation */
	socketfd = socket_create();
	/* Initialization of socket with parsed listen_port */
	new_server = socket_init(cfg_getint(cfg, "listen_port"));
	/* Bind socket to port */
	socket_bind(socketfd, new_server);
	/* Begin listening process with the parsed number of clients */
	socket_listen(socketfd, cfg_getint(cfg, "max_clients"));

	/* Initialization of thread pool */
	nthreads = cfg_getint(cfg, "max_clients");

	/* Memory allocation for thread pool pointer */
	tptr = (Thread *)calloc(nthreads, sizeof(Thread));
	/* Error checking */
	if (tptr == NULL) {
		perror("Thread memory allocation error.");
		exit(EXIT_FAILURE);
	}

	/* Allocation of double-pointer client address structure for threads */
	cliaddr = (struct sockaddr **)malloc(sizeof(struct sockaddr *) * nthreads);
	/* Error checking */
	if (cliaddr == NULL) {
		perror("Cliaddr memory allocation error.");
		exit(EXIT_FAILURE);
	}

	connection = (int *)malloc(sizeof(int) * nthreads);
	if (connection == NULL) {
		perror("connection memory allocation error.");
		exit(EXIT_FAILURE);
	}

	/* Creation of thread pool */
	for (i = 0; i < nthreads; i++) {
		/* Allocation of memory to client */
		cliaddr[i] = (struct sockaddr*)malloc(addrlen);

		/* Control of memory allocation */
		if (cliaddr[i] == NULL) {
			perror("Error reserving memory.");
			exit(EXIT_FAILURE);
		}

		/* Command for thread creation*/
		thread_make(i);
	}

	/* Pre-cleaning of arguments */
	cfg_free_value(opts);

	/* Set signal handler for exiting server */
	if (signal(SIGINT, handler) == SIG_ERR) {
		perror("Signal error.");
	}

	/* Parent process remains waiting while threads control server functioning */
	while(1) {
		pause();
	}

	/* Close socket */
 	close_socket(socketfd);

 	return 0;
 }
