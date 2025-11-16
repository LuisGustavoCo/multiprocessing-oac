import time
import math
import numpy as np
import multiprocessing
from numba import jit

#versão base não otimizada
def tarefa_pesada(inicio, fim):
    soma = 0
    for i in range(inicio, fim):
        soma += math.log(i + 1)
    return soma

#versão otimizada com numba
@jit(nopython=True)
def tarefa_pesada_jit(inicio, fim):
    soma = 0
    for i in range(inicio, fim):
        soma += math.log(i + 1)
    return soma

#versão 1: base(python Puro e sequencial)
def versao_base_sequencial(n_tarefas, tamanho_tarefa):
    total = 0
    for i in range(n_tarefas):
        inicio = i * tamanho_tarefa
        fim = (i + 1) * tamanho_tarefa
        total += tarefa_pesada(inicio, fim)
    return total

#versão 2: otimizada (numba e sequencial) 
def versao_otimizada_sequencial(n_tarefas, tamanho_tarefa):
    #aquecimento do JIT 
    tarefa_pesada_jit(0, 1) 
    
    total = 0
    for i in range(n_tarefas):
        inicio = i * tamanho_tarefa
        fim = (i + 1) * tamanho_tarefa
        total += tarefa_pesada_jit(inicio, fim)
    return total

#versão 3: paralela (multiprocessing) 
def versao_paralela(n_tarefas, tamanho_tarefas, n_processos):
    args = []
    for i in range(n_tarefas):
        inicio = i * tamanho_tarefas
        fim = (i + 1) * tamanho_tarefas
        args.append((inicio, fim))

    #cria um pool de processos
    with multiprocessing.Pool(processes=n_processos) as pool:
        #p pool distribui as tarefas entre os processos
        resultados = pool.starmap(tarefa_pesada, args)
    
    return sum(resultados)

#execução e verificação
def rodar_experimento(funcao, n_repeticoes, *args):
    tempos = []
    print(f"Executando {funcao.__name__}...")
    for _ in range(n_repeticoes):
        inicio_time = time.perf_counter()
        funcao(*args)
        fim_time = time.perf_counter()
        tempos.append(fim_time - inicio_time)
    
    #salva os tempos em um arquivo
    np.savetxt(f"tempos_{funcao.__name__}.txt", tempos)
    return tempos

#análise Estatística
def analisar_resultados(nome_arquivo):
    tempos = np.loadtxt(nome_arquivo)
    
    #cálculo da Média e Desvio Padrão 
    media = np.mean(tempos) 
    desvio = np.std(tempos, ddof=1) 
    
    print(f"Arquivo: {nome_arquivo}")
    print(f"  Média (T̄):  {media:.4f} s")
    print(f"  Desvio (σ): {desvio:.4f} s\n")
    return media, desvio

if __name__ == "__main__":
    n_repeticoes = 10 #executar múltiplas repetições 
    n_processos = 8   #número de processos para a versão paralela
    
    #carga de trabalho 
    n_tarefas = 1000
    tamanho_tarefa = 20000

    print(f"Iniciando experimento...")
    print(f"Repetições por versão: {n_repeticoes}")
    print(f"Processos paralelos: {n_processos}")
    print(f"Carga: {n_tarefas} tarefas de tamanho {tamanho_tarefa}\n")

    rodar_experimento(versao_base_sequencial, n_repeticoes, n_tarefas, tamanho_tarefa)
    rodar_experimento(versao_otimizada_sequencial, n_repeticoes, n_tarefas, tamanho_tarefa)
    rodar_experimento(versao_paralela, n_repeticoes, n_tarefas, tamanho_tarefa, n_processos)

    print("--- Análise Estatística ---")
    t_base, _ = analisar_resultados("tempos_versao_base_sequencial.txt")
    t_otim, _ = analisar_resultados("tempos_versao_otimizada_sequencial.txt")
    t_par, _ = analisar_resultados("tempos_versao_paralela.txt")
    
    #calcular speedup (S) e eficiência (E) 
    s_otim = t_base / t_otim
    s_par = t_base / t_par
    
    #eficiência (p = n_processos)
    e_par = s_par / n_processos 

    print("--- Métricas de Desempenho ---")
    print(f"Speedup (Otimizado Numba vs Base): {s_otim:.2f}x")
    print(f"Speedup (Paralelo 8p vs Base):   {s_par:.2f}x")
    print(f"Eficiência (Paralelo 8p):          {e_par:.2f} (ou {e_par*100:.1f}%)")