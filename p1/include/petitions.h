/**
 * @file petitions.h
 * @author Nazariy Gunko
 * @author Leah Hadeed
 * @brief Library that contains petition and response utilities for server use.
 */
#ifndef __PETITIONS_H__
#define __PETITIONS_H__

/* Predefined Libraries Used */
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <sys/types.h>
#include <fcntl.h>
#include <limits.h>
#include <sys/wait.h>
#include <signal.h>
#include <syslog.h>


/* Newly designed libraries used */
#include "server.h"
#include "functions.h"

/* Predefined MACROS */
#define BUFSIZE 80
#define MAXBUF 4096

/* Global variables */
char date[50];			/* HTTP Date header 		*/
char http_version[10]; 	/* HTTP Version header 		*/
char content_type[30];	/* HTTP Content-Type header */



/**
* @brief Function that communicates with systems log. 
* 
* This function prints the HTTP Response output to the systems log.
*
* @param buffer with http response
*/
void system_print(char * buffer);

/**
* @brief CGI response function
*
* This subroutine is in charge of sending the server response in the case of 
* script execution, independent of the method [POST, GET].
*
* @param Socket file descriptor
* @param path (command)
* @param variables for command
@ param int flag program type
* @return void
*/
void response_cgi(int sockfd, char * path, char * variables, int flag);

/**
* @brief OPTIONS method response function
*
* This subroutine is in charge of sending the server response in the case of the
* received method being 'OPTIONS'
*
* @param Socket file descriptor
* @return void
*/
void response_options(int sockfd);

/*
* @brief Headers for file transfer
*
* This subroutine is responsible for the partial transfer of files on reception
* of the file transfer petition. This subroutine in particular is responsible
* for sending the headers of the HTTP petition for file transfer.
*
* @param Socket file descriptor
* @param Name of file to be transfered
* @return void
*/
void response_file_headers(int sockfd, const char *filename);

/*
* @brief File for file transfer
*
* This subroutine is responsible for the partial transfer of files on reception
* of the file transfer petition. This subroutine in particular is responsible
* for sending the file portion of the HTTP file transfer petition.
*
* @param Socket file descriptor
* @param File to be transfered
* @return void
*/
void response_file_concatenate(int sockfd, FILE *resource);

/**
* @brief Bad Request function
*
* This subroutine is in charge of sending the server response in the case that
* the server receives a badly formed petition.
*
* @param Socket file descriptor
* @return void
*/
void response_bad_request(int sockfd);

/**
* @brief File not found function
*
* This subroutine is in charge of sending the server response in the case of the
* received method trying to locate a file that is no longer on the server. The
* error code for this is '404' or 'file not found'.
*
* @param Socket file descriptor
* @return void
*/
void response_file_not_found(int sockfd);

/**
* @brief Server error function
*
* This subroutine is in charge of sending the server response in the case of a
* general server error. The error code in this case is '501' or 'Internal Server Error'.
*
* @param Socket file descriptor
* @return void
*/
void response_server_error(int sockfd);

/**
 * @brief unimplemneted options response function
 *
 * This subroutine sends the server response in the case of an unimplemented method option.
 * At the moment, the only available method options are: GET, POST, and OPTIONS
 *
 * @param Socket file descriptor
 * @return void
 */
void response_unimplemented(int sockfd);

/**
 * @brief Server parse function
 *
 * This function provides the main behaviour of the server.
 * It is in charge of parsing the received content from the HTTP petition,
 * and then calls a subroutine for the creation and sending of the appropriate response.
 *
 * @param Socket file descripter
 * @return void
 */
void server_main(int sockfd);

#endif
