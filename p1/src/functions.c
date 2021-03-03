/**
 * @file functions.c
 * @author Nazariy Gunko
 * @author Leah Hadeed
 * @brief Implementation of useful initialization functions
 */
#include "functions.h"


/************************************************************************
 * Function initializes the HTTP date header                          	*
 ************************************************************************/
void init_date(char * date) {
  	/* Variables for http date */
  	struct tm * tm;
	time_t now;

	/* Time initialization */
  	time(&now);
	tm = localtime(&now);
	strftime(date, 1000, "%A, %d %B %Y %H:%M:%S %Z", tm);
}

/************************************************************************
 * Function initializes the HTTP version header                         *
 ************************************************************************/
void init_version(int version, char * http_version) {
	/* String initialization */
	sprintf(http_version, "HTTP/1.%d", version);
}

/************************************************************************
 * Function initializes the HTTP content type header                    *
 ************************************************************************/
void init_content_type(char * path, char * content_type, int *flag) {
    const char s[2] = ".";
    char buffer[80];
    char * token;
    char new_path[80];

    content_type[0] = '\0';
    /* Non-Null variable check */
    if (path == NULL) {
    	perror("path--error");
    	return;
    }
    strcpy(new_path, path);
    /* get the first token */
    token = strtok(new_path, s);
    if (token == NULL){
        return;
    }
    /* get the first token */
    token = strtok(NULL, "\0");
    
    if (token == NULL){
        return;
    }

	/* Testing content type options */
	if (strcmp(token, "txt") == 0) {
		sprintf(buffer, "text/plain");
		*flag = TXT;
	}
	else if (strcmp(token, "htm") == 0 || strcmp(token, "html") == 0 ) {
		sprintf(buffer, "text/html");
		*flag = TXT;
	}
	else if (strcmp(token, "php") == 0){
		sprintf(buffer, "text/html");
		*flag = PHP;
	}
	else if (strcmp(token, "py") == 0) {
		sprintf(buffer, "text/html");
		*flag = PYC;
	}
	else if (strcmp(token, "xml") == 0) {
		sprintf(buffer, "text/xml");
		*flag = OTH;
	}
	else if (strcmp(token, "gif") == 0) {
		sprintf(buffer, "image/gif");
		*flag = IMG;
	}
	else if (strcmp(token, "png") == 0) {
		sprintf(buffer, "image/png");
		*flag = IMG;
	}
	else if (strcmp(token, "jpeg") == 0 || strcmp(token, "jpg") == 0) {
		sprintf(buffer, "image/jpeg");
		*flag = IMG;
	}
	else if (strcmp(token, "mpeg") == 0 || strcmp(token, "mpg") == 0) {
		sprintf(buffer, "video/mpeg");
		*flag = MOV;		
	}
	else if (strcmp(token, "pdf") == 0) {
		sprintf(buffer, "application/pdf");
		*flag = PDF;
	}
	else if (strcmp(token, "doc") == 0 || strcmp(token, "docx")) {
		sprintf(buffer, "application/msword");
		*flag = DOC;
	}
    else if (strcmp(token, "js") == 0) {
        sprintf(buffer, "application/javascript");
        *flag = TXT;
    }
    else if (strcmp(token, "css") == 0) {
        sprintf(buffer, "text/css");
        *flag = TXT;
    }
	else {
		return;
	}

	strcpy(content_type, buffer);
}

/************************************************************************
 * Function parses the parameters from the HTTP requested path        	*
 ************************************************************************/
void path_params(char * path, char * mod_path) {
	const char s[2] = "?";
    char buffer[80];
    char * token;

    /* Non-Null variable check */
    if (path == NULL) {
    	perror("path--error");
      return;
    }

    /* get the first token */
    token = strtok(path, s);
/*    sscanf(s,"%*[^.%s",buffer);
*/
    /* walk through other tokens */
    while (token != NULL) {
    	memset(buffer, 0, sizeof(buffer));
    	strcpy(buffer, token);
      	token = strtok(NULL, s);
	}

	if (buffer == NULL) {
		mod_path = NULL;
	}

	strcpy(mod_path, buffer);
}

/************************************************************************
 * Function strips the HTTP requested path of its headers             	*
 ************************************************************************/
void path_stripped(char * path, char * mod_path) {
	const char s[2] = "?";
    char * token;

    /* Non-Null variable check */
    if (path == NULL) {
    	perror("path--error");
    	return;
    }

    /* get the first token */
    token = strtok(path, s);
    if (token == NULL) {
    	perror("path--error");
    }

    strcpy(mod_path, token);
}


void path_post_params(char * request, char * params) {
	const char s[] = "\r\n\r\n";
	char * token;
	char buffer[80];

	if (request == NULL) {
		perror("path--error");
		return;
	}

	token = strtok(request, s);

	while (token != NULL) {
		memset(buffer, 0, sizeof(buffer));
		strcpy(buffer, token);

		token = strtok(NULL, s);
	}

	strcpy(params, buffer);
}
