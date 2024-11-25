#   Projeto de Sistemas Operacionais I 2024
#       Prof. Caetano Mazzoni Ranieri
#
#   Integrantes:
#       Arnaldo Martins de Godoy
#       Caio Henrique Sidô dos Santos
#


import threading
import random
import time
from queue import Queue
import sys
import os
import shutil

# Diretorio que sera salvo
track_dir = "tracking"
# Controle de total de pacotes no sistema
pending_packages_lock = threading.Lock()
pending_packages_count = None


class DistPoint:
    def __init__(self, id):
        self.id = id
        self.queue = Queue()  # Fila de encomendas do CD
        self.lock = threading.Lock()

    def __str__(self):
        # DEbug ponto
        return f"Ponto {self.id} (Encomendas: {self.queue.qsize()})"


class Truck(threading.Thread):
    def __init__(self, id, points, capacity):
        super().__init__()
        self.id = id
        self.points = points  # Todos os CD's que ele conhece
        self.capacity = capacity  # Capacidade Maxima de carga do caminhão
        self.current_point = random.choice(points)  # Ponto Atual
        self.cargo = []
        self.visited = set()  # Para logica da lista não repetida
        self.running = True

    def run(self):
        global pending_packages_lock, pending_packages_count
        while self.running:
            with self.current_point.lock:  # ! Garante que só um veiculo é atendido por vez
                # Carregar ou descarregar encomendas
                if self.current_point.queue.empty() and not self.cargo:
                    print(
                        f"Caminhão {self.id}: Sem encomendas no {self.current_point.id}, Indo para outro ponto")
                else:
                    # Criar lista de encomendas para entregar
                    to_unload = []
                    for p in self.cargo:
                        if p.unload_if_reached(self.id, self.current_point):
                            to_unload.append(p)

                    # Entregar as necessarias
                    for p in to_unload:
                        time.sleep(random.uniform(5, 10))
                        self.cargo.remove(p)
                        p.log_event(
                            f"{time.strftime('%H:%M:%S')} - Encomenda {p.id}: Entregue pelo caminhao {self.id} no ponto {self.current_point.id}")
                        with pending_packages_lock:  # Reduzir o numero total de encomendas no sistema com lock
                            pending_packages_count -= 1
                    # Carregar oq for necessario
                    while not self.current_point.queue.empty() and len(self.cargo) < self.capacity:
                        package = self.current_point.queue.get()
                        package.log_event(
                            f"{time.strftime('%H:%M:%S')} - Encomenda {package.id}: Iniciando carregamento pelo caminhao {self.id} no ponto {self.current_point.id}")
                        time.sleep(random.uniform(5, 10))
                        self.cargo.append(package)
                        package.log_event(
                            f"{time.strftime('%H:%M:%S')} - Encomenda {package.id}: Carregado pelo caminhao {self.id} no ponto {self.current_point.id}")
            # Log das encomendas carregadas
            for p in self.cargo:
                p.log_event(
                    f"{time.strftime('%H:%M:%S')} - Encomenda {p.id}: Caminhao {
                        self.id} passou no ponto {self.current_point.id}"
                )

            # Ve se tem algo para entregar no sistema geral, se não, se desliga
            with pending_packages_lock:  # Lock para evitar um caso de o caminhão fazer uma viagem a mais
                if pending_packages_count == 0:
                    self.running = False
                    print(
                        f"Caminhão {self.id}: Todas as encomendas foram entregues. Encerrando...")

            # Basicamente uma lista que não se repete até voltar ao ponto inicial
            if self.running:
                next_points = [p for p in self.points if p !=
                               self.current_point and p not in self.visited]
                if not next_points:
                    self.visited.clear()
                    next_points = [
                        p for p in self.points if p != self.current_point]
                self.current_point = random.choice(next_points)
                self.visited.add(self.current_point)
                print(
                    f"Caminhão {self.id}: Viajando para {self.current_point.id}")
                time.sleep(random.uniform(5, 20))  # Tempo de viagem


class Package(threading.Thread):
    def __init__(self, id, origin, destination):
        super().__init__()
        self.id = id
        self.origin = origin
        self.destination = destination
        self.log = []
        self.file_name = f"{track_dir}/package_{self.id}.ptt"
        open(self.file_name, "w")  # Crua os arquivos

    def log_event(self, message):  # Vai salvando no arquivo conforme é atualizado
        print(message)
        self.log.append(message)
        with open(self.file_name, "a") as f:
            f.write(message + "\n")

    # Verificação simples se vai descarregar nesse ponto ou não
    def unload_if_reached(self, vehicle_id, current_point):
        if current_point == self.destination:
            self.log_event(
                f"{time.strftime('%H:%M:%S')} - Encomenda {self.id}: Vai ser descarregada pelo caminhao {
                    vehicle_id} no ponto {current_point.id}"
            )
            return True
        return False

    def run(self):
        with self.origin.lock:  # Se coloca na fila quando iniciado
            self.origin.queue.put(self)
            self.log_event(
                f"{time.strftime('%H:%M:%S')} - Encomenda {self.id}: Criada no ponto {self.origin.id} para o ponto {self.destination.id}")


# Inicialização
def packageSystem(S, C, P, A):
    # Criar pontos de redistribuição
    points = [DistPoint(i) for i in range(S)]
    print("CD's criados")

    # Criar encomendas
    packages = []
    if os.path.exists(track_dir):
        shutil.rmtree(track_dir)
    os.mkdir(track_dir)

    # Controle de total de pacotes no sistema
    global pending_packages_count
    pending_packages_count = P

    for i in range(P):
        origin, destination = random.sample(points, 2)
        package = Package(i, origin, destination)
        packages.append(package)

    print("Encomendas criadas")

    # Criar caminhao vrum vrum
    trucks = [
        Truck(i, points, A)
        for i in range(C)
    ]
    print("Caminhões criados")

    # Iniciar pacotes
    for p in packages:
        p.start()

    time.sleep(1)  # pra nn ficar feio o terminal
    print()

    # Iniciar veiculos
    for t in trucks:
        t.start()

    # Esperar encomendas
    for p in packages:
        p.join()

    # Esperar caminhões pararem depois das encomendas acabarem
    for t in trucks:
        t.join()

    print("Todas as encomendas foram entregues!!!")


if __name__ == "__main__":
    # Quantidade de Pontos
    S = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    # Quantidade de caminhões
    C = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    # Quantidade pacotes
    P = int(sys.argv[3]) if len(sys.argv) > 3 else 25
    # Quantidade de pacotes por caminhão
    A = int(sys.argv[4]) if len(sys.argv) > 4 else 5

    if not (P > A > C):
        print("Falha na definição de P > A > C")
        exit()

    packageSystem(S, C, P, A)
