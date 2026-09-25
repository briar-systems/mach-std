/* test fixture only: C code that owns threads and thread-local state, so the
   probe can check that std leaves a C runtime's thread pointer alone and that
   a thread C created can call back into mach. std itself never links this. */
#include <pthread.h>
#include <stdlib.h>
#include <sys/syscall.h>
#include <unistd.h>

static __thread long tls_counter;

/* the main thread's C identity, taken by the loader before the program's entry */
static long *main_tls;

__attribute__((constructor)) static void probe_record_main(void) {
    main_tls = &tls_counter;
}

/* malloc and a __thread variable both read the calling thread's control block.
   on the main thread, a thread pointer moved since the loader set it shows as a
   different address for the same variable, even where nothing faults. the
   main thread is told by its kernel thread id, which no thread pointer moves */
long probe_c_tls(void) {
    if (syscall(SYS_gettid) == getpid() && &tls_counter != main_tls) return -2;
    void *p = malloc(64);
    if (!p) return -1;
    tls_counter = tls_counter + 1;
    free(p);
    return tls_counter;
}

typedef void (*probe_callback)(void *);

struct probe_start {
    probe_callback cb;
    void *arg;
    long result;
};

static void *probe_run(void *x) {
    struct probe_start *s = x;
    s->cb(s->arg);
    /* the C runtime still works on this thread after mach ran on it */
    s->result = probe_c_tls();
    return 0;
}

/* run cb(args[i]) on n threads pthread_create made, all live at once */
int probe_c_threads(probe_callback cb, void **args, int n) {
    pthread_t threads[8];
    struct probe_start starts[8];
    if (n < 1 || n > 8) return 1;
    for (int i = 0; i < n; i++) {
        starts[i].cb = cb;
        starts[i].arg = args[i];
        starts[i].result = 0;
        if (pthread_create(&threads[i], 0, probe_run, &starts[i]) != 0) return 2;
    }
    for (int i = 0; i < n; i++) {
        if (pthread_join(threads[i], 0) != 0) return 3;
    }
    for (int i = 0; i < n; i++) {
        if (starts[i].result != 1) return 4;
    }
    return 0;
}
