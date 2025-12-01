#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
  int *valores;
  int tamanho;
  int capacidade;
} valores;

static void vetor_inic(valores *v) {
  v->tamanho = 0;
  v->capacidade = 16;
  v->valores = (int *)malloc(sizeof(int) * v->capacidade);
}

static void vetor_add(valores *v, int x) {
  if (v->tamanho == v->capacidade) {
    v->capacidade *= 2;
    v->valores = (int *)realloc(v->valores, sizeof(int) * v->capacidade);
  }
  v->valores[v->tamanho++] = x;
}

static void vetor_liberar(valores *v) {
  free(v->valores);
  v->valores = NULL;
  v->tamanho = v->capacidade = 0;
}

static int *gaps_shell(int n, int *count) {
  int cap = 32, tam = 0;
  int *gaps = (int *)malloc(sizeof(int) * cap);
  for (int g = n / 2; g > 0; g /= 2) {
    if (tam == cap) {
      cap *= 2;
      gaps = (int *)realloc(gaps, sizeof(int) * cap);
    }
    gaps[tam++] = g;
  }
  *count = tam;
  return gaps;
}

static int *gaps_knuth(int n, int *count) {
  int cap = 32, tam = 0;
  int *temp = (int *)malloc(sizeof(int) * cap);
  int h = 1;
  while (h < n) {
    if (tam == cap) {
      cap *= 2;
      temp = (int *)realloc(temp, sizeof(int) * cap);
    }
    temp[tam++] = h;
    h = 3 * h + 1;
  }

  int *gaps = (int *)malloc(sizeof(int) * tam);
  for (int i = 0; i < tam; i++)
    gaps[i] = temp[tam - 1 - i];
  free(temp);
  *count = tam;
  return gaps;
}

static int *gaps_sedgewick(int n, int *count) {
  int cap = 64, tam = 0;
  int *temp = (int *)malloc(sizeof(int) * cap);
  int k = 0;
  while (1) {
    long g1 = (k > 0) ? ((1L << (2 * k)) + 3 * (1L << (k - 1)) + 1)
                      : 1;                             
    long g2 = 9 * (1L << (2 * k)) - 9 * (1L << k) + 1; 
    int adicionado = 0;
    if (g1 < n) {
      if (tam == cap) {
        cap *= 2;
        temp = (int *)realloc(temp, sizeof(int) * cap);
      }
      temp[tam++] = (int)g1;
      adicionado = 1;
    }
    if (g2 < n) {
      if (tam == cap) {
        cap *= 2;
        temp = (int *)realloc(temp, sizeof(int) * cap);
      }
      temp[tam++] = (int)g2;
      adicionado = 1;
    }
    if (!adicionado)
      break;
    k++;
  }
  for (int i = 0; i < tam; i++)
    for (int j = i + 1; j < tam; j++)
      if (temp[j] > temp[i]) {
        int t = temp[i];
        temp[i] = temp[j];
        temp[j] = t;
      }
  int *gaps = (int *)malloc(sizeof(int) * tam);
  for (int i = 0; i < tam; i++)
    gaps[i] = temp[i];
  free(temp);
  *count = tam;
  return gaps;
}

static void shell_sort(int *a, int n, const char *sequencia) {
  int count = 0;
  int *gaps = NULL;
  if (strcmp(sequencia, "shell") == 0)
    gaps = gaps_shell(n, &count);
  else if (strcmp(sequencia, "knuth") == 0)
    gaps = gaps_knuth(n, &count);
  else if (strcmp(sequencia, "sedgewick") == 0)
    gaps = gaps_sedgewick(n, &count);
  else
    gaps = gaps_shell(n, &count);

  for (int i_gap = 0; i_gap < count; i_gap++) {
    int gap = gaps[i_gap];
    for (int i = gap; i < n; i++) {
      int temp = a[i];
      int j = i;
      while (j >= gap && a[j - gap] > temp) {
        a[j] = a[j - gap];
        j -= gap;
      }
      a[j] = temp;
    }
  }
  free(gaps);
}

static void demo() {
  int arr[] = {23, 12, 1, 8, 34, 54, 2, 3};
  int n = sizeof(arr) / sizeof(arr[0]);
  printf("Antes:");
  for (int i = 0; i < n; i++)
    printf(" %d", arr[i]);
  printf("\n");
  shell_sort(arr, n, "shell");
  printf("Depois: ");
  for (int i = 0; i < n; i++)
    printf(" %d", arr[i]);
  printf("\n");
}

int main(int argc, char **argv) {
  const char *seq = "shell";
  int modo_demo = 0;
  for (int i = 1; i < argc; i++) {
    if (strcmp(argv[i], "--sequence") == 0 && i + 1 < argc) {
      seq = argv[++i];
    } else if (strcmp(argv[i], "--demo") == 0) {
      modo_demo = 1;
    }
  }
  if (modo_demo) {
    demo();
    return 0;
  }
  
  valores v;
  vetor_inic(&v);
  int x;
  while (scanf("%d", &x) == 1) {
    vetor_add(&v, x);
  }
  shell_sort(v.valores, v.tamanho, seq);
  for (int i = 0; i < v.tamanho; i++) {
    if (i)
      printf(" ");
    printf("%d", v.valores[i]);
  }
  printf("\n");
  vetor_liberar(&v);
  return 0;
}