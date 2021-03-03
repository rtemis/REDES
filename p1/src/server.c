/**
 * @file server.c
 * @author Nazariy Gunko
 * @author Leah Hadeed
 * @brief Library that contains functions for server use
 */

#include "server.h"

/* TCP Socket Creation */
int socket_create() {
	int sockfd;

	/* Testing the creation of the TCP socket */
	if ((sockfd = socket(AF_INET, SOCK_STREAM, 0)) < 0)  {
		perror("socket--create");
		exit(errno);
	}
	return sockfd;
}

/* Socket Initialization */
struct sockaddr_in socket_init(int server_port) {
	struct sockaddr_in sockaddr;

	/* Test passed variables*/
	if (server_port < 0){
		/* Change error code */
		perror("serverport--passed-variable");
		/* Exit with preset error code */
		exit(errno);
	}

	/* Set all memory in pointer to '\0' */
	bzero(&sockaddr, sizeof(sockaddr));
	/* Set server family to 'Internet' */
	sockaddr.sin_family = AF_INET;
	/* Set server port to selected server port */
	sockaddr.sin_port = htons(server_port);
	/* Set the accepted listening address to any */
	sockaddr.sin_addr.s_addr = INADDR_ANY;
	
	/* Returns the initialized socket connection*/
	return sockaddr;
}

/* Socket binding to given port */
void socket_bind(int sockfd, struct sockaddr_in sockaddr) {
	/* Test passed variables*/
	if (socket < 0) {
		/* Change error code */
		perror("socket--passed-variable");
		/* Exit with preset error code */
		exit(errno);
	}

	/* Function assures the correct binding of a port to a socket */
	if (bind(sockfd, (struct sockaddr*)&sockaddr, sizeof(sockaddr)) != 0 ) {
		/* Change error code */
		perror("socket--bind");
		exit(errno);
	}
}

/* Socket begins listening process */
void socket_listen(int socket, int num_conn) {
	/* Test passed variables*/
	if (socket < 0) {
		/* Change error code */
		perror("socket--passed-variable");
		/* Exit with preset error code */
		exit(errno);
	}

	/* Begins listening process. Allows num_conn connections in queue */
	if (listen(socket, num_conn) != 0) {
		/* Change error code */
		perror("socket--listen");
		/* Exit with preset error code */
		exit(errno);
	}
}

/* Closes file descriptor of socket */
void close_socket(int socket) {
	/* Test passed variables*/
	if (socket < 0) {
		/* Change error code */
		perror("socket--passed-variable");
		/* Exit with preset error code */
		exit(errno);
	}

	/* Test closing of socket */
	if (close(socket) < 0) {
		/* Change error code */
		perror("socket--close");
		/* Exit with preset error code */
		exit(errno);
	}
}
