from collections import deque
import random

QUANTUM = 3
QUANTIDADE_PROCESSOS = 5
SEMENTE_ALEATORIA = 4867654453

random.seed(SEMENTE_ALEATORIA)

tempo_atual = 0
quant_processos_finalizados = 0

fila_alta_prioridade = deque()
fila_baixa_prioridade = deque()
fila_io = []

def criar_processo(pid):

    tempo_total_cpu = random.randint(8, 20)

    return {
        "pid": pid,
        "ppid": 0,
        "status": "NOVO",
        "prioridade": "ALTA",
        "tempo_cpu_restante": tempo_total_cpu,
        "tipo_io": random.choice(["DISCO", "FITA", "IMPRESSORA"]),
        "tempo_total_io": random.randint(2, 5),
        "tempo_io_restante": 0,
        "realizou_io": False,
        "momento_io": random.randint(max(1, tempo_total_cpu // 3), max(2, tempo_total_cpu - 2))
    }

def inicializar_processos():
    lista_processos = []
    for pid in range(1, QUANTIDADE_PROCESSOS + 1):
        processo = criar_processo(pid)
        lista_processos.append(processo)
        processo["status"] = "PRONTO"
        fila_alta_prioridade.append(processo)

        print(f"[t=0] P{processo['pid']} criado -> fila ALTA")

    return lista_processos

def atualizar_fila_io():

    global tempo_atual
    processos_io_concluidos = []
    for processo in fila_io:
        processo["tempo_io_restante"] -= 1

        if processo["tempo_io_restante"] <= 0:
            processos_io_concluidos.append(processo)

    for processo in processos_io_concluidos:

        fila_io.remove(processo)
        processo["status"] = "PRONTO"

        if processo["tipo_io"] == "DISCO":
            fila_baixa_prioridade.append(processo)
            print(f"[t={tempo_atual}] P{processo['pid']} retornou do DISCO -> fila BAIXA")

        else:
            fila_alta_prioridade.append(processo)
            print(f"[t={tempo_atual}] P{processo['pid']} retornou de {processo['tipo_io']} -> fila ALTA")


def selecionar_proximo_processo():

    if fila_alta_prioridade:
        return fila_alta_prioridade.popleft()

    if fila_baixa_prioridade:
        return fila_baixa_prioridade.popleft()

    return None


def executar_processo_por_um_quantum(processo):
    global tempo_atual

    processo["status"] = "EXECUTANDO"

    tempo_ate_fim = processo["tempo_cpu_restante"]

    if not processo["realizou_io"]:
        tempo_ate_io = processo["tempo_cpu_restante"] - processo["momento_io"]
    else:
        tempo_ate_io = float('inf')

    tempo_executado = min(QUANTUM, tempo_ate_fim, tempo_ate_io)

    print(f"[t={tempo_atual}] CPU executa P{processo['pid']} por {tempo_executado} unidades")

    for _ in range(tempo_executado):
        tempo_atual += 1
        atualizar_fila_io() 

    processo["tempo_cpu_restante"] -= tempo_executado


def processo_deve_solicitar_io(processo):

    if processo["realizou_io"]:
        return False

    return (processo["momento_io"] >= processo["tempo_cpu_restante"])


def finalizar_processo(processo):
    global quant_processos_finalizados

    processo["status"] = "FINALIZADO"
    quant_processos_finalizados += 1

    print(f"[t={tempo_atual}] P{processo['pid']} finalizado")


def mover_para_io(processo):

    processo["status"] = "BLOQUEADO"
    processo["realizou_io"] = True
    
    processo["tempo_io_restante"] = (processo["tempo_total_io"])

    fila_io.append(processo)

    print(f"[t={tempo_atual}] P{processo['pid']} solicitou I/O {processo['tipo_io']} por {processo['tempo_total_io']} unidades")


def mover_fila_baixa_prioridade(processo):
    processo["status"] = "PRONTO"
    fila_baixa_prioridade.append(processo)

    print(f"[t={tempo_atual}] P{processo['pid']} sofreu preempção -> fila BAIXA")

def registrar_cpu_ociosa():

    global tempo_atual
    print(f"[t={tempo_atual}] CPU OCIOSA")
    tempo_atual += 1


def imprimir_resumo_final():
    print("")
    print(f"[fim] Processos finalizados: {quant_processos_finalizados}/{QUANTIDADE_PROCESSOS} | tempo total: {tempo_atual}")


print(f"[config] quantum={QUANTUM} | processos={QUANTIDADE_PROCESSOS} | seed={SEMENTE_ALEATORIA}")

lista_processos = inicializar_processos()

while quant_processos_finalizados < QUANTIDADE_PROCESSOS:

    atualizar_fila_io()

    processo_em_execucao = selecionar_proximo_processo()

    if processo_em_execucao is None:
        registrar_cpu_ociosa()
        continue

    executar_processo_por_um_quantum(
        processo_em_execucao
    )

    if processo_em_execucao["tempo_cpu_restante"] <= 0:
        finalizar_processo(processo_em_execucao)

    elif processo_deve_solicitar_io(processo_em_execucao):
        mover_para_io(processo_em_execucao)

    else:
        mover_fila_baixa_prioridade(processo_em_execucao)

imprimir_resumo_final()