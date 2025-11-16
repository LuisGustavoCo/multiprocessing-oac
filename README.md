# Trabalho Final — Organização e Arquitetura de Computadores: Multiprocessamento

Resumo
------
Este repositório contém o código do trabalho final da disciplina sobre multiprocessamento. O objetivo é comparar três versões de uma carga de trabalho (base sequencial, otimizada com Numba e paralela com multiprocessing) e apresentar métricas de desempenho (speedup e eficiência).

Arquivos importantes
-------------------
- `main.py`: implementação principal e funções do experimento.
  - Funções centrais: `tarefa_pesada`, `tarefa_pesada_jit`, `versao_base_sequencial`, `versao_otimizada_sequencial`, `versao_paralela`, `rodar_experimento`, `analisar_resultados`
- Resultados (tempos de execução) gerados pelo script:
  - `tempos_versao_base_sequencial.txt`
  - `tempos_versao_otimizada_sequencial.txt`
  - `tempos_versao_paralela.txt`

Como funciona (resumo)
----------------------
- `tarefa_pesada`: função que realiza a soma de logaritmos em um intervalo; usada como trabalho unitário.
- `tarefa_pesada_jit`: mesma lógica, compilada com Numba (`@jit(nopython=True)`) para acelerar a execução.
- `versao_base_sequencial`: executa `n_tarefas` sequencialmente chamando `tarefa_pesada`.
- `versao_otimizada_sequencial`: executa sequencialmente chamando `tarefa_pesada_jit` (inclui aquecimento do JIT).
- `versao_paralela`: cria uma lista de argumentos e usa `multiprocessing.Pool.starmap` para executar `tarefa_pesada` em paralelo.
- `rodar_experimento`: executa uma função várias vezes, mede tempos com `time.perf_counter()` e salva em `tempos_<funcao>.txt`.
- `analisar_resultados`: carrega os tempos, calcula média e desvio padrão e imprime.

Execução
--------
Instale dependências (ex.: Python 3.8+, numpy, numba):
```sh
pip install numpy numba
```

Execute:
```sh
python main.py
```

Os tempos serão salvos em arquivos `tempos_*.txt` (um arquivo por função testada).

Métricas e interpretações
------------------------
Calculam-se as métricas clássicas:

- Speedup entre base e otimizada:
  S_otim = T_base / T_otim

- Speedup entre base e paralela:
  S_par = T_base / T_par

- Eficiência da versão paralela (com p processos):
  E = S_par / p

Valores de exemplo podem ser obtidos a partir dos arquivos `tempos_versao_base_sequencial.txt`, `tempos_versao_otimizada_sequencial.txt` e `tempos_versao_paralela.txt` carregando as médias e aplicando as fórmulas acima.

Observações
----------
- A aceleração com Numba depende do aquecimento do compilador JIT (por isso há uma chamada preliminar em `versao_otimizada_sequencial`).
- A versão paralela usa a função Python pura (`tarefa_pesada`) para compatibilidade com multiprocessing; para usar funções Numba em paralelo é necessário cuidado adicional (compilação e serialização).
- Ajuste `n_tarefas`, `tamanho_tarefa` e `n_processos` em `main.py` conforme o ambiente de execução para obter medições representativas.

Licença
-------
Material criado para fins acadêmicos (disciplina de Organização e Arquitetura de Computadores).