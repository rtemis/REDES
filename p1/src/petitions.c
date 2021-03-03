/**
 * @file petitions.c
 * @author Nazariy Gunko
 * @author Leah Hadeed
 * @brief Implementation of the server response code
 */

#include "petitions.h"

/************************************************************************
 * Function responsible for printing to systems log.                    *
 ************************************************************************/
void system_print(char * buffer){
	/* Print to systems log */
	syslog(LOG_NOTICE, "\n\n%s\n\n", buffer);
}

/************************************************************************
 * Function responsible for sending the response to requests that 		*
 * invoke code from the terminal. Creates pipes to communicate with the *
 * main terminal. The response is passed to the server through the 		*
 * socket as per usual.
 ************************************************************************/
void response_cgi(int sockfd, char * path, char * variables, int flag) {
	int fd_cgi_request[2];
	int fd_cgi_response[2];
	int readFlag;
	char buffer[MAXBUF] = {'0'};
	char response[MAXBUF];

	/* Test path passed */
	if (path == NULL) {
		perror("path--passing-null");
		return;
	}

	/* Creation of pipe to send data to python interpreter */
	if (pipe(fd_cgi_request) || pipe(fd_cgi_response)) {
		perror("pipe--failure");
		return;
	}

	/* Creation of script execution process */
	switch (fork()) {
		/* Scenario fork failure */
		case -1: 
			perror("fork--failure");
			return;
		/* Scenario child process */
		case 0:
			/* Closes output side of request pipe */
			close(fd_cgi_request[1]);
			/* Closes input side of response pipe */
			close(fd_cgi_response[0]);

			/* Changes standard input & output file descriptors to pipe file descriptors */
			dup2(fd_cgi_request[0], STDIN_FILENO);
			close(fd_cgi_request[0]);
			
			dup2(fd_cgi_response[1], STDOUT_FILENO);
			close(fd_cgi_response[1]);

			/* Switch case controls the type of code to be executed: Python3 or PHP */
			switch (flag) {
				/* In the case of Python script */
				case PYC: 
					if (variables == NULL)
						execlp("python3", "python3", path, (char *)NULL);
					else 
						execlp("python3", "python3", path, variables, (char *)NULL);
					break;
				/* In the case of PHP script */
				case PHP:
					if (variables == NULL)
						execlp("php", "php", path, (char *)NULL);
					else 
						execlp("php", "php", path, variables, (char *)NULL);
					break;
				default:
					break;
			}
			exit(0);
			break;

		/* Scenario parent process */
		default:
			/* Closes input side of request pipe */
			close(fd_cgi_request[0]);
			/* Closes output side of response pipe */
			close(fd_cgi_response[1]);

			readFlag = read(fd_cgi_response[0], buffer, sizeof(buffer) - 1);

			if (readFlag < 0) {
				response_server_error(sockfd);
			}
			else {
				/* Begin the file confirmation and transfer */
				sprintf(response,
				 	"%s 200 OK\r\n"
				 	"Date: %s \r\n"
				 	"Server: %s\r\n"
					"Content-Type: %s\r\n"
					"Content-Length: %d\r\n"
					"\r\n"
				, http_version, date, cfg_getstr(cfg, "server_signature"), content_type, (int)strlen(buffer));

				/* Send part 1 of the server response: headers */
				send(sockfd, response, strlen(response), 0);
				send(sockfd, buffer, strlen(buffer), 0);

				system_print(response);
			}

			/* Close pipes */
			close(fd_cgi_request[1]);
			close(fd_cgi_response[0]);

			break;
	}
	/* Wait for child process */
	wait(NULL);
}

/************************************************************************
 * Function responsible for sending the response to the OPTIONS method 	*
 * petition. Creates the response variable and fills it with the		*
 * pre-determined response text. 										*
 ************************************************************************/
void response_options(int sockfd) {
	char response[MAXBUF];

	/* Initialization of response petition */
	sprintf(response,
		"%s 200 OK\r\n"
		"Date: %s \r\n"
		"Server: %s\r\n"
		"Allow: GET,POST,OPTIONS\r\n"
		"Content-Type: %s\r\n"
		"\r\n"
	, http_version, date, cfg_getstr(cfg, "server_signature"), content_type);
	/* Send response through socket */
 	send(sockfd, response, strlen(response), 0);

}

/************************************************************************
 * Function responsible for sending the header portion of the server 	*
 * response for file transfers. 										*
 ************************************************************************/
void response_file_headers(int sockfd, const char *filename) {
	char response[MAXBUF];
	FILE * resource = NULL;
	int fileLen = 0;

	if (content_type == NULL) {
		response_server_error(sockfd);
	}
	else {
		/* Open the required file */
		resource = fopen(filename, "rb");
		/* Testing for missing files */
	 	if (resource == NULL) {
	 		/* Report a file not found error */
	 		response_file_not_found(sockfd);
		}
		else {
			/* Position the file pointer at the end of the file */
			if (fseek(resource, 0, SEEK_END)) {
				perror("error fseek");
				response_server_error(sockfd);
			}
			/* Discover content length */
		  	fileLen=ftell(resource);

			/* Begin the file confirmation and transfer */
			sprintf(response,
			 	"%s 200 OK\r\n"
			 	"Date: %s \r\n"
			 	"Server: %s\r\n"
				"Content-Type: %s\r\n"
				"Content-Length: %d\r\n"
				"\r\n"
			, http_version, date, cfg_getstr(cfg, "server_signature"), content_type, fileLen);

			/* Send part 1 of the server response: headers */
			send(sockfd, response, strlen(response), 0);
			system_print(response);
			/* Call function for file transfer */
			response_file_concatenate(sockfd, resource);
			/* Closing file resource */
			fclose(resource);
		}		
	}

}

/************************************************************************
 * Function responsible for sending the file portion of the server 		*
 * response for file transfers. 										*
 ************************************************************************/
void response_file_concatenate(int sockfd, FILE *resource) {
	char response[MAXBUF] = {0};
	int fileFlag = 0;

	/* Non-Null variable check */
	if (resource == NULL) {
		perror("concatenate--file-error");
		exit(EXIT_FAILURE);
	}

	/* Positions the file cursor at the beginning */
	fseek(resource, 0, SEEK_SET);

	/* Loop for sending portions of the file, in case it is too big. */
    while (!feof(resource)) {

		fileFlag = fread(response, 1, MAXBUF - 1, resource);

		if (fileFlag > 0) {
			send(sockfd, response, fileFlag, 0);
		}
 	}
}

/************************************************************************
 * Function responsible for sending the server error response to the 	*
 * client when the server receives a bad request. 						*
 ************************************************************************/
void response_bad_request(int sockfd) {
	char response[MAXBUF];

	/* Initializes the response buffer with pre-determined error text */
 	sprintf(response,
 		"%s 400 Bad Request\r\n"
 		"Date: %s \r\n"
 		"Content-Type: %s\r\n"
 		"\r\n"
 		"<P>Oops! Something went wrong.\r\n"
 	, http_version, date, content_type);

 	/* Sends the response through the socket */
 	send(sockfd, response, strlen(response), 0);
}

/************************************************************************
 * Function responsible for sending the file portion of the server 		*
 * response for file transfers. 										*
 ************************************************************************/
void response_file_not_found(int sockfd) {
	char response[MAXBUF];
	FILE * file = NULL;

	file = fopen("htmlfiles/www/error404.html", "rb");

	/* Initializes the response buffer with pre-determined error text */
	sprintf(response,
		"%s 404 NOT FOUND\r\n"
		"Date: %s \r\n"
		"Server: %s\r\n"
		"Content-Type: text/html\r\n"
		"\r\n"
	, http_version, date, cfg_getstr(cfg, "server_signature"));

	/* Sends the response through the socket */
	send(sockfd, response, strlen(response), 0);
	system_print(response);
	/* Call function for file transfer */
	response_file_concatenate(sockfd, file);
	fclose(file);
}

/************************************************************************
 * Function responsible for sending the server error response to the 	*
 * client when something goes wrong.									*
 ************************************************************************/
void response_server_error(int sockfd) {
	char response[MAXBUF];
	FILE * file = NULL;

	file = fopen("htmlfiles/www/error500.html", "rb");

	/* Initializes the response buffer with pre-determined error text */
 	sprintf(response,
 		"%s 500 Internal Server Error\r\n"
 		"Date: %s \r\n"
 		"Content-Type: text/html\r\n"
 		"\r\n"
 		"<P>Oops! Something went wrong.\r\n"
 	, http_version, date);

 	/* Sends the response through the socket */
 	send(sockfd, response, strlen(response), 0);
 	/* Sends the response through the socket */
	send(sockfd, response, strlen(response), 0);
	system_print(response);
	/* Call function for file transfer */
	response_file_concatenate(sockfd, file);
	fclose(file);
}

/************************************************************************
 * Function responsible for sending the server response to a petition 	*
 * with and unimplemented method header.								*
 ************************************************************************/
void response_unimplemented(int sockfd) {
	char response[MAXBUF];

	/* Initializes the response buffer with pre-determined error text */
	sprintf(response,
		"%s 501 Method Not Implemented\r\n"
		"Date: %s \r\n"
		"Server: %s\r\n"
		"Content-Type: %s\r\n"
		"\r\n"
		"<HTML><HEAD><TITLE>Method Not Implemented\r\n"
		"</TITLE></HEAD>\r\n"
		"<BODY><P>HTTP request method not supported.\r\n"
		"</BODY></HTML>\r\n"
	, http_version, date, cfg_getstr(cfg, "server_signature"), content_type);

	/* Sends the response through the socket */
 	send(sockfd, response, strlen(response), 0);
}



/* Main code for server thread execution */
void server_main(int sockfd){
	/* Variables for socket communication */
	char buffer[MAXBUF];

  	/* Variables for picoHTTPparser */
	const char *method;						/* Method pointer defines the option allowed [GET,POST,OPTIONS, etc] */
  	size_t method_len;						/* Length of method [size of word] */
  	const char *path;						/* Path of solicited resource */
  	size_t path_len;						/* Length of path */
  	int minor_version;						/* HTTP version 1.0/1.1 */
  	struct phr_header headers[32];			/* Typical headers, i.e. Date, Content-Length, etc. */
  	size_t num_headers;						/* Number of headers in HTTP petition */
  	int ret;								/* Return value of phr_parse_request (For error control purposes) */

	/* Local specified parsed HTTP variables */
 	char met[20];
  	char pa[BUFSIZE];
  	char final_path[BUFSIZE];
  	char new_path[BUFSIZE];
  	char path_args[BUFSIZE];
  	int flag;

	/* Testing recv */
	if (recv(sockfd, buffer, MAXBUF, 0) < 0){
		/* Error macro 'Empty Again' */
		perror("Error receiving.");
		exit(EXIT_FAILURE);
	}

	/* Header parse from the received petition */
	num_headers = sizeof(headers) / sizeof(headers[0]);
    ret = phr_parse_request((const char *)buffer, sizeof(buffer) - 1, &method, &method_len, &path, &path_len, &minor_version, headers, &num_headers, 0);
	/* Error control, if function return error */
	if (ret == -1) {
		perror("Parsing Error: Headers");
		response_server_error(sockfd);
	}
	/* If the petition is sent incorrectly */
	if (ret == -2) {
		/* Sends server petition error */
		response_bad_request(sockfd);
	}

	/* Variable initialization */
	sprintf(met, "%.*s", (int)method_len, method);
  	sprintf(pa, "%.*s", (int)path_len, path);

  	/* Setting up global variables */
	init_date(date);
	init_version(minor_version, http_version);

	signal(SIGPIPE, SIG_IGN);

	if (strncmp(method, "GET", method_len) == 0) {
    	/* Open and read the file to send */
    	path_stripped(pa, new_path);
    	
    	if (new_path == NULL) {
    		response_server_error(sockfd);
    	}
    	else {
			sprintf(final_path, "%s%s", cfg_getstr(cfg, "server_root"), new_path);

	    	/* Case: final path is index path */
	    	if (strcmp(final_path, "htmlfiles/www/") == 0) {
	    		sprintf(new_path, "%s/index.html", cfg_getstr(cfg, "server_root"));
	    		/* Set content-type header */
				init_content_type(new_path, content_type, &flag);
				/* Call HTTP response function */
	    		response_file_headers(sockfd, new_path);
	    	}
	    	/* Case: final path not index path */
	    	else {
	    		/* Set content-type header */
				init_content_type(new_path, content_type, &flag);
				/* Test content-type */
				if (content_type == NULL) {
					response_server_error(sockfd);
				}
				/* test flag type for code type */
				else if (flag == PYC || flag == PHP) {
					path_params(pa, path_args);
					response_cgi(sockfd, final_path, path_args, flag);
				}
		      	else 
		      		response_file_headers(sockfd, final_path);
	      	
    		}
    	}
	}
	else if (strncmp(method, "POST", method_len) == 0) {
    	path_stripped(pa, new_path);
    	sprintf(final_path, "%s%s", cfg_getstr(cfg, "server_root"), new_path);		
		init_content_type(pa, content_type, &flag);

		if (content_type == NULL){
			response_server_error(sockfd);
		}

		else if (flag == PYC || flag == PHP) {
			path_post_params(buffer, path_args);
			response_cgi(sockfd, final_path, path_args, flag);
		}
		else 
		    response_file_headers(sockfd, final_path);
	}
	else if (strncmp(method, "OPTIONS", method_len) == 0) {
		response_options(sockfd);
	}
	else {
		response_unimplemented(sockfd);
	}

}
