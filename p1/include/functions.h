/**
 * @file functions.h
 * @author Nazariy Gunko
 * @author Leah Hadeed
 * @brief Library that contains thread utility for server use.
 */
#ifndef __FUNCTIONS_H__
#define __FUNCTIONS_H__

/* Predefined Libraries Used */
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <sys/types.h>
#include <fcntl.h>

/* Flags defined for object types */
#define TXT 100
#define IMG 200
#define MOV 300
#define PHP 400
#define PYC 500
#define DOC 600
#define PDF 700
#define OTH 800



/**
* @brief Date function
*
* This subroutine is dedicated to the initialization of the date header.
*
* @return string of date
*/
void init_date(char * date);

/**
* @brief HTTP version function
*
* This subroutine is dedicated to the initialization of the HTTP version header.
*
* @param HTTP version
* @return version
*/
void init_version(int version, char * http_version);

/**
* @brief HTTP Content-Type function
*
* This subroutine is dedicated to the initialization of the HTTP Content-type header.
*
* @param String of content
* @return Content-type
*/
void init_content_type(char * path, char * content_type, int * flag);

/**
* @brief main path function
*
* This subroutine strips the path of its parameters.
*
* @param path to object
* @param path without web extensions
* @return string of path
*/
void path_stripped(char * path, char * mod_path);

/**
* @brief path parameters function
*
* This subroutine parses the parameters from the path.
*
* @param path to object
* @param parameters passed through get
* @return string of parameters
*/
void path_params(char * path, char * mod_path);

/**
* @brief path parameters function
*
* This subroutine parses the parameters from the post body.
*
* @param path to object
* @param parameters from post body
* @return string of parameters
*/
void path_post_params(char * request, char * params);

#endif
