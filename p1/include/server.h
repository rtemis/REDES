/**
 * @file server.h
 * @author Nazariy Gunko
 * @author Leah Hadeed
 * @brief Library that contains necessary function descriptions for server use.
 */
#ifndef __SERVER_H__
#define __SERVER_H__

/* Predefined Libraries Used */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <errno.h>
#include <sys/socket.h>
#include <resolv.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <confuse.h>

#include "picohttpparser.h"

/* Predefined Macros */
#define MAXBUF 4096

/* Global Variables */
cfg_t *cfg;

/**
* @brief kill signal handler
*
* This function assures the correct liberation of memory upon server close.
*
* @param int sig
* @return void
*/
void handler(int sig);

/**
* @brief Creation of Socket
*
* This function predefines certain parameters of the socket,
* like the Family (AF_INET), Socket Type (SOCK_STREAM), and Protocol, which
* is 0 in this case because the appropriate protocol will be automatically
* selected.
*
* @param N/a
*
* @return The created socket
*/
int socket_create();

/**
* @brief Initialization of Socket
*
* This function predefines certain parameters of the socket,
* such as the Family (AF_INET), and accepted Listening Address (INADDR_ANY).
* The Server Port is defined through the parsing of the server.conf file,
* and later passed as a parameter.
*
* @param Port to be used by server
* @return The initialized socket
*/
struct sockaddr_in socket_init(int server_port);

/**
* @brief Binds the socket to the port
* @param Socket descriptor
* @param Port structure
* @return void
*/
void socket_bind(int sockfd, struct sockaddr_in sockaddr);

/**
* @brief Begins to listen in the socket
* @param Socket descriptor
* @param num_conn number of connections allowed
* @return void
*/
void socket_listen(int socket, int num_conn);


/**
* @brief Closes the socket descriptor
* @param Socket descriptor
* @return void
*/
void close_socket(int sockfd);

#endif
