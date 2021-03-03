/**
 * @file demonizar.c
 * @author Nazariy Gunko
 * @author Leah Hadeed
 * @brief File that contains the implementation of the demonizar() function.
 */
#define _POSIX_C_SOURCE 199506L

#include "demonizar.h"
#include "servidor_thread.h"

/**
 * @brief Function that daemonizes a process.
 * @param cadena String string that identifies the service.
 */
void demonizar(char* cadena) {
  pid_t pid, sid;
  int file = 0;
  FILE* fp;
  char cwd[PATH_MAX];
  
  /* Save current working directory */
  if (getcwd(cwd, sizeof(cwd)) == NULL) {
    perror("getcwd() error");
    return;
  }

  /* Child creation */
  pid = fork();

  /* If fork fails, exit with error code */
  if (pid < 0) {
    exit(EXIT_FAILURE);
  }

  /* If parent, process is exited to create orphan */
  if (pid > 0) {
    
    /* Save the process PID to a file for later process exit  */
    fp = fopen("daemonPid.txt", "w+");
    if (fp == NULL){
      perror("File creation error.");
      exit(EXIT_FAILURE);
    }
    /* Write PID to file */
    fprintf(fp, "%d", pid);
    /* Close file */
    fclose(fp);
    /* Exit program successfully */
    return;
  }

  /* Set permissions */
  umask(0);

  /* Change the session ID of current process */
  sid = setsid();

  /* If creation of a new session fails, exit with error code */
  if (sid < 0) {
    exit(EXIT_FAILURE);
  }

  /* Catch all signals that alert the parent that it's child has terminated */
  signal(SIGCHLD, SIG_IGN);
  signal(SIGHUP, SIG_IGN);

  /* Change working directory to root directory */
  if ((chdir("/")) < 0) {
    exit(EXIT_FAILURE);
  }

  /* Test for the runtime configuration information */
  for (file = getdtablesize(); file >= 0; file--) {
    close(file);
  }

  /* Open log to write */
  openlog(cadena, LOG_PID, LOG_DAEMON);

  syslog(LOG_NOTICE, "----->Starting web server...");

  servidor_thread(cwd);

}

/* Main code for daemon process */
int main()
{
  /* Start daemon process */
  demonizar("DAEMON WEB SERVER");
  syslog (LOG_NOTICE, "----->Daemon started.");
  return EXIT_SUCCESS;
}
