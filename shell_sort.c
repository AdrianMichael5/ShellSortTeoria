/*
 * Shell Sort in C with three gap sequences (Shell, Knuth, Sedgewick).
 * Compile:
 *   gcc -O2 -o shell_sort_c shell_sort.c
 *
 * Usage:
 *   # Sort numbers from stdin, print sorted to stdout (space-separated)
 *   ./shell_sort_c --sequence shell < numbers.txt
 *
 *   # Demo mode
 *   ./shell_sort_c --demo
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int *vals;
    int size;
    int capacity;
} IntVec;

static void vec_init(IntVec *v) {
    v->size = 0;
    v->capacity = 16;
    v->vals = (int*)malloc(sizeof(int)*v->capacity);
}

static void vec_push(IntVec *v, int x) {
    if (v->size == v->capacity) {
        v->capacity *= 2;
        v->vals = (int*)realloc(v->vals, sizeof(int)*v->capacity);
    }
    v->vals[v->size++] = x;
}

static void vec_free(IntVec *v) {
    free(v->vals);
    v->vals = NULL;
    v->size = v->capacity = 0;
}

// Gap sequences
static int* gaps_shell(int n, int *count) {
    int cap = 32, sz = 0;
    int *gaps = (int*)malloc(sizeof(int)*cap);
    for (int g = n/2; g > 0; g /= 2) {
        if (sz == cap) { cap*=2; gaps = (int*)realloc(gaps, sizeof(int)*cap); }
        gaps[sz++] = g;
    }
    *count = sz;
    return gaps;
}

static int* gaps_knuth(int n, int *count) {
    int cap=32, sz=0;
    int *tmp = (int*)malloc(sizeof(int)*cap);
    int h = 1;
    while (h < n) {
        if (sz == cap) { cap*=2; tmp = (int*)realloc(tmp, sizeof(int)*cap); }
        tmp[sz++] = h;
        h = 3*h + 1;
    }
    // Reverse
    int *gaps = (int*)malloc(sizeof(int)*sz);
    for (int i=0;i<sz;i++) gaps[i] = tmp[sz-1-i];
    free(tmp);
    *count = sz;
    return gaps;
}

static int* gaps_sedgewick(int n, int *count) {
    int cap=64, sz=0;
    int *tmp = (int*)malloc(sizeof(int)*cap);
    int k = 0;
    while (1) {
        long g1 = (k>0) ? ( (1L<< (2*k)) + 3*(1L<< (k-1)) + 1 ) : 1; // 4^k + 3*2^(k-1) + 1
        long g2 = 9*(1L<<(2*k)) - 9*(1L<<k) + 1; // 9*4^k - 9*2^k + 1
        int added = 0;
        if (g1 < n) {
            if (sz == cap) { cap*=2; tmp = (int*)realloc(tmp, sizeof(int)*cap); }
            tmp[sz++] = (int)g1; added=1;
        }
        if (g2 < n) {
            if (sz == cap) { cap*=2; tmp = (int*)realloc(tmp, sizeof(int)*cap); }
            tmp[sz++] = (int)g2; added=1;
        }
        if (!added) break;
        k++;
    }
    // sort desc
    for (int i=0;i<sz;i++) for (int j=i+1;j<sz;j++) if (tmp[j]>tmp[i]) { int t=tmp[i]; tmp[i]=tmp[j]; tmp[j]=t; }
    int *gaps = (int*)malloc(sizeof(int)*sz);
    for (int i=0;i<sz;i++) gaps[i] = tmp[i];
    free(tmp);
    *count = sz;
    return gaps;
}

static void shell_sort(int *a, int n, const char *sequence) {
    int count=0;
    int *gaps = NULL;
    if (strcmp(sequence, "shell")==0) gaps = gaps_shell(n, &count);
    else if (strcmp(sequence, "knuth")==0) gaps = gaps_knuth(n, &count);
    else if (strcmp(sequence, "sedgewick")==0) gaps = gaps_sedgewick(n, &count);
    else gaps = gaps_shell(n, &count);

    for (int gi=0; gi<count; gi++) {
        int gap = gaps[gi];
        for (int i=gap; i<n; i++) {
            int temp = a[i];
            int j = i;
            while (j>=gap && a[j-gap] > temp) {
                a[j] = a[j-gap];
                j -= gap;
            }
            a[j] = temp;
        }
    }
    free(gaps);
}

static void demo() {
    int arr[] = {23, 12, 1, 8, 34, 54, 2, 3};
    int n = sizeof(arr)/sizeof(arr[0]);
    printf("Before:");
    for (int i=0;i<n;i++) printf(" %d", arr[i]);
    printf("\n");
    shell_sort(arr, n, "shell");
    printf("After: ");
    for (int i=0;i<n;i++) printf(" %d", arr[i]);
    printf("\n");
}

int main(int argc, char **argv) {
    const char *seq = "shell";
    int demo_mode = 0;
    for (int i=1;i<argc;i++) {
        if (strcmp(argv[i], "--sequence")==0 && i+1<argc) {
            seq = argv[++i];
        } else if (strcmp(argv[i], "--demo")==0) {
            demo_mode = 1;
        }
    }
    if (demo_mode) {
        demo();
        return 0;
    }
    // Read integers from stdin
    IntVec v; vec_init(&v);
    int x;
    while (scanf("%d", &x)==1) {
        vec_push(&v, x);
    }
    shell_sort(v.vals, v.size, seq);
    for (int i=0;i<v.size;i++) {
        if (i) printf(" ");
        printf("%d", v.vals[i]);
    }
    printf("\n");
    vec_free(&v);
    return 0;
}