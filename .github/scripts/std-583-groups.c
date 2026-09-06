#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
struct record { int error, before, after, pid, sid; };
int main(void) {
    int failures=0;
    for (int mode=0; mode<3; mode++) {
        int child_errors=0, parent_errors=0;
        for (int i=0; i<1200; i++) {
            int gate[2], report[2];
            if (pipe(gate) || pipe(report)) return 2;
            pid_t child=fork();
            if (child<0) return 3;
            if (!child) {
                close(gate[1]); close(report[0]);
                char byte;
                if (mode==1 && read(gate[0],&byte,1)!=1) _exit(4);
                struct record out={0};
                out.before=getpgrp(); out.pid=getpid(); out.sid=getsid(0);
                if (setpgid(0,0)<0) out.error=errno;
                out.after=getpgrp();
                if (write(report[1],&out,sizeof(out))!=sizeof(out)) _exit(5);
                if (mode==2 && read(gate[0],&byte,1)!=1) _exit(6);
                _exit(0);
            }
            close(gate[0]); close(report[1]);
            struct record out;
            if (mode==2 && read(report[0],&out,sizeof(out))!=sizeof(out)) return 7;
            if (setpgid(child,child)<0) parent_errors++;
            if (mode && write(gate[1],"x",1)!=1) return 8;
            if (mode!=2 && read(report[0],&out,sizeof(out))!=sizeof(out)) return 9;
            if (out.error) {
                child_errors++;
                printf("mode=%d child_error=%d before=%d after=%d pid=%d sid=%d\n",mode,out.error,out.before,out.after,out.pid,out.sid);
            }
            close(gate[1]); close(report[0]);
            int status;
            if (waitpid(child,&status,0)!=child || !WIFEXITED(status) || WEXITSTATUS(status)) return 10;
        }
        printf("mode=%d child_errors=%d parent_errors=%d\n",mode,child_errors,parent_errors);
        failures+=child_errors;
    }
    printf("total_child_errors=%d\n",failures);
    return 0;
}
