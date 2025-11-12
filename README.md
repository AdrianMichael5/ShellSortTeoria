# 🧩 SHELL SORT — ANÁLISE DE COMPLEXIDADE E BENCHMARK EM PYTHON E C

Este repositório contém implementações completas do algoritmo **Shell Sort** em **Python** e **C**, bem como um estudo experimental detalhado sobre sua complexidade, análise assintótica, desempenho prático, geração de gráficos e relatório acadêmico em PDF.

---

# 📚 CONTEÚDO DO REPOSITÓRIO


---

# 📌 1. SOBRE O PROJETO

Este projeto foi desenvolvido para a disciplina **Teoria da Complexidade e Análise de Tempo de Algoritmos**, tendo como objetivo:

- Implementar o algoritmo **Shell Sort** em linguagens distintas.
- Comparar desempenho entre Python e C.
- Gerar dados experimentais com entradas sintéticas.
- Confirmar empiricamente a complexidade teórica.
- Produzir gráficos, tabelas e relatórios.
- Estudar melhor caso, pior caso e caso médio.
- Compreender o impacto das sequências de gaps.

---

# ⚙️ 2. DESCRIÇÃO DO SHELL SORT

O **Shell Sort** é uma versão otimizada do Insertion Sort.  
Em vez de mover elementos apenas para posições adjacentes, ele compara elementos separados por um **gap** que diminui progressivamente.

Exemplo de sequência de gaps:
- Shell: n/2, n/4, n/8, …, 1  
- Knuth: 1, 4, 13, 40, ...  
- Sedgewick: misto entre potências de 2 e 4  

O objetivo é reduzir movimentos longos no início, tornando o algoritmo mais eficiente que algoritmos quadráticos simples, como Bubble Sort e Insertion Sort.

---

# 📈 3. COMPLEXIDADE ASSINTÓTICA

| CASO | COMPLEXIDADE | DETALHES |
|------|--------------|-----------|
| **Melhor Caso** | O(n log n) | Lista quase ordenada |
| **Caso Médio** | Θ(n^(3/2)) | Com sequência clássica de Shell |
| **Pior Caso** | O(n²) | Muitos deslocamentos |

### SÍNTESE:

- **Big-O:** O(n²)  
- **Big-Ω:** Ω(n log n)  
- **Big-Θ:** Θ(n^(3/2))  

A escolha da sequência de gaps influencia fortemente o desempenho.

---

# 🧮 4. IMPLEMENTAÇÕES

## ✔️ PYTHON — `shell_sort.py`

### Executar demo:

```bash
python shell_sort.py --demo
```

Ordenar números de um arquivo:
```bash
python shell_sort.py --sequence shell < numeros.txt
```

## ⚡ C — shell_sort.c
Implementação otimizada e muito mais rápida que Python.

Compilar:

```bash
gcc -O2 -o shell_sort_c shell_sort.c
```
Executar:
```bash
./shell_sort_c --demo
```
# 🚀 5. BENCHMARKING — benchmark_shell_sort.py

O script gera:
Entradas aleatórias
- 20 execuções por tamanho
- Média + desvio-padrão
- CSV com resultados
- Gráficos PNG
- Comparação entre Python e C
  
### Executar benchmark somente Python:

```base
python benchmark_shell_sort.py
```
### Executar Python + C:

```bash
python benchmark_shell_sort.py --include-c
```
### Alterar sequência de gaps:

```bash
python benchmark_shell_sort.py --sequence knuth
```
### Ajustar tamanhos e repetições:

```bash
python benchmark_shell_sort.py --sizes 2000,5000,10000 --reps 30
```

# 📊 6. GRÁFICOS E RESULTADOS

Os gráficos gerados automaticamente incluem:

- plot_python_mean.png
→ Tempo médio do Shell Sort em Python

- plot_python_vs_theory.png
→ Comparação com curva teórica n^1.5

- plot_python_vs_c.png
→ Comparação direta entre Python e C

O arquivo results_shell_sort.csv contém todas as métricas (média e desvio).


# 🏗️ 7. COMO REPRODUZIR O PROJETO
## 1️⃣ Clonar o repositório:
```
git clone https://github.com/SEU_USUARIO/SEU_REPO.git
cd SEU_REPO
```
## 2️⃣ Rodar benchmarks:
```
python benchmark_shell_sort.py
```
## 3️⃣ Compilar implementação em C:
```
gcc -O2 -o shell_sort_c shell_sort.c
```
## 4️⃣ Gerar gráficos:
```
python benchmark_shell_sort.py --include-c
```





