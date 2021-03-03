/**
 * @file demonizar.h
 * @author Nazariy Gunko
 * @author Leah Hadeed
 * @brief Library that allows to daemonize a process.
 *
 */

#ifndef __DEMONIZAR_H__
#define __DEMONIZAR_H__

#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <syslog.h>
#include <unistd.h>
#include <signal.h>
#include <sys/wait.h>

/**
 * @brief Function that daemonizes the process that calls it.
 *
 * @param cadena string that identifies the service.
 */
void demonizar(char* cadena);

#endif /* __DEMONIZAR_H__ */
