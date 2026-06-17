**Simulador de Escalonamento de Processos**

Trabalho de Sistemas Operacionais: um simulador de escalonamento de processos
feito em Python, usando Round Robin com feedback e múltiplas filas.

**O que é preciso:**

Este projeto usa apenas a biblioteca padrão do Python, então não é necessário instalar
nada. Dá para rodar de duas formas: com o Python na máquina (usamos a versão 3.11) ou
pelo Docker.

**Como rodar:**

Com o Python, estando na pasta do projeto:

```
python src/escalonador.py
```

Em alguns sistemas o comando é `python3`.

Pelo Docker:

```
docker compose up --build
```

Esse comando monta a imagem e roda o simulador.

**Mudando os parâmetros**

Os valores principais ficam no começo do `escalonador.py`, em constantes:

```
QUANTUM = 3
QUANTIDADE_PROCESSOS = 5
SEMENTE_ALEATORIA = 4867654453
```

Para alterar os dados é só alterar o valor e rodar de novo. No caso da semente, manter o mesmo
número gera sempre os mesmos processos, e trocá-lo gera processos diferentes.

**O que aparece na tela:**

Aparecem a criação dos processos, a execução na CPU, as preempções, os pedidos de I/O
e as finalizações. No fim, um resumo com quantos processos terminaram e o tempo total
da simulação.
