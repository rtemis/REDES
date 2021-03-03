/**
 * @file exit.c
 * @author Leah Hadeed
 * @author Nazariy Gunko
 * @brief File that contains the kill code for the web server
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <syslog.h>

/**
* This function is responsible for the termination of the web server. 
*/
int main () {
    FILE * fp;
    char pid[10] = {'\0'};
    char command[20] = "kill -9 ";

    /* Open PID file for daemon process PID */
    fp = fopen("daemonPid.txt", "r"); 
    /* Error control */
    if (fp == NULL) {
        perror("File error - daemonPid");
        exit(EXIT_FAILURE);
    }

    /* Read PID from file */
    if (fgets(pid, 10, fp) == NULL) {
        perror("Error reading from pid file.");
        exit(EXIT_FAILURE);
    }

    /* Setup kill command */
    strcat(command, pid);
    /* Advise of process termination */
    syslog(LOG_NOTICE, "----->Daemon Web Service is shutting down...");
    /* Send kill signal to daemon process */
    system(command);
    /* Close log file */
    closelog();
    /* Close file */
    fclose(fp);
    
    return 0;
}