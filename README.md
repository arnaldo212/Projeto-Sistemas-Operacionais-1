# Projeto-Sistemas-Operacionais-1

Este projeto simula um sistema de logística com pontos de redistribuição (centros de distribuição), caminhões de entrega e pacotes. A implementação utiliza programação com threads para simular a movimentação e entrega das encomendas de maneira paralela.


Funcionalidades
Gerenciamento de pacotes e rastreamento por logs.
Sincronização de recursos compartilhados com threading.Lock.
Caminhões circulam entre Centro de distribuição, carregando e descarregando pacotes.
Logs de rastreamento salvos em arquivos para cada pacote.


Como executar
certifiquese de que possui o Python 3.8 ou superior instalado.

Execute o script com os seguintes parâmetros: python project.py [S] [C] [P] [A]

Onde:  
S: Número de centros de sitribuição.  
C: Número de caminhões.  
P: Número de pacotes.  
A: Capacidade máxima de pacotes por caminhão.  

Exemplo: Python project.py 5 3 50 10  
Este comando cria:  
5 centros de distribuição, 3 caminhões, 50 pacotes, capacidade máxima de 10 pacotes por caminhão.

Logs de Rastreamento
Os log de cada pacote são salvos na pasta tracking criada automaticamento na execução. Cada arquivo contém o histórico completo do pacote.
