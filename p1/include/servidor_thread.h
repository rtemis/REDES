/**
 * @file servidor_thread.h
 * @author Nazariy Gunko
 * @author Leah Hadeed
 * @brief Library that controls webserver 
 *
 */

#ifndef __SERVIDOR_THREAD_H__
#define __SERVIDOR_THREAD_H__

#include "server.h"
#include "threads.h"



/**
 * @brief Function that controls kill signal
 * @param Signal being used
 */
void handler(int sig);

/**
 * @brief Function that daemonizes the process that calls it.
 *
 * @return 0 if everything went ok and -1 if ERROR.
 */
int servidor_thread(char * current_dir);

#endif /* _SERVICOR_THREAD_H__ */
