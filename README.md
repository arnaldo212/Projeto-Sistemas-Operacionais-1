# Projeto-Sistemas-Operacionais-1

Este projeto simula um sistema de logística com pontos de redistribuição (centros de distribuição), caminhões de entrega e pacotes. A implementação utiliza programação com threads para simular a movimentação e entrega das encomendas de maneira paralela.


Funcionalidades
Gerenciamento de pacotes e rastreamento por logs.
Sincronização de recursos compartilhados com threading.Lock.
Caminhões circulam entre CDs, carregando e descarregando pacotes.
Logs de rastreamento salvos em arquivos para cada pacote.

Como executar
Certifique-se de que possui o Python 3.8 ou superior instalado.

Clone este repositório:
git clone <URL_do_repositorio>


Execute o script com os seguintes parâmetros:
python logistics_system.py <S> <C> <P> <A>

Onde:
S: Número de centros de distribuição (CDs).
C: Número de caminhões.
P: Número de pacotes.
A: Capacidade máxima de pacotes por caminhão.

Exemplo:
python logistics_system.py 5 3 50 10

Este comando cria:
5 CDs,
3 caminhões,
50 pacotes,
Capacidade máxima de 10 pacotes por caminhão.

Logs de Rastreamento
Os logs de cada pacote são salvos na pasta tracking/ criada automaticamente na execução. Cada arquivo contém o histórico completo do pacote.
