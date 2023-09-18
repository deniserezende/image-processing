import logging
import cv2
import numpy as np
import time
import random


def numerar_pixels(image):
    """"Retorna numbered image com os valores equivalentes ao preto numerados
    e os valores equivalentes ao branco igual a zero"""
    # Crie uma matriz para armazenar os números dos pixels ativos
    numbered_image = np.zeros_like(image, dtype=np.uint16)

    # Inicialize o número do pixel ativo
    current_number = 1

    # Itere sobre a imagem para numerar os pixels ativos
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            if image[y, x] == 0:  # 0 é o preto e 255 é o branco
                numbered_image[y, x] = current_number
                current_number += 1
            else:
                numbered_image[y, x] = 0

    return numbered_image


def colorir_imagem(valores):
    amount = np.max(valores)  # Encontra o valor máximo na imagem

    # Cria um mapa de cores para os valores diferentes de 0
    colors = np.random.randint(0, 256, size=(amount + 1, 3), dtype=np.uint8)

    # Cria uma imagem em branco do mesmo tamanho que a imagem original
    altura, largura = valores.shape
    imagem_colorida = np.zeros((altura, largura, 3), dtype=np.uint8)

    # Atribui cores aos valores diferentes de 0
    for valor in range(1, amount + 1):
        mask = valores == valor
        imagem_colorida[mask] = colors[valor]

    # Define a cor branca para os valores 0
    imagem_colorida[valores == 0] = (255, 255, 255)

    return imagem_colorida


def union_find(image):
    def find(label):
        if label_parents[label] != label:
            label_parents[label] = find(label_parents[label])
        return label_parents[label]

    def union(label1, label2):
        root1 = find(label1)
        root2 = find(label2)
        if root1 != root2:
            label_parents[root1] = root2

    height, width = image.shape
    labeled_image = np.zeros_like(image, dtype=np.uint16)
    label_parents = {}
    num_components = 0  # Initialize the component counter

    current_label = 1

    for y in range(height):
        for x in range(width):
            if image[y, x] != 0:
                neighbors = []

                if y > 0 and labeled_image[y - 1, x] != 0:
                    neighbors.append(labeled_image[y - 1, x])
                if x > 0 and labeled_image[y, x - 1] != 0:
                    neighbors.append(labeled_image[y, x - 1])

                if not neighbors:
                    labeled_image[y, x] = current_label
                    label_parents[current_label] = current_label
                    current_label += 1
                    num_components += 1  # New component found
                else:
                    min_neighbor = min(neighbors)
                    labeled_image[y, x] = min_neighbor
                    for neighbor in neighbors:
                        if neighbor != min_neighbor:
                            union(min_neighbor, neighbor)

    for y in range(height):
        for x in range(width):
            if labeled_image[y, x] != 0:
                labeled_image[y, x] = find(labeled_image[y, x])

    return labeled_image, num_components

def analisar_vizinhanca(numbered_image):

    def get_neighbors(numbered_image, y, x):
        # Verificar se os vizinhos estão dentro dos limites da imagem
        neighbors = [
            numbered_image[y - 1, x] if (numbered_image[y - 1, x] > 0) else float('inf'),
            # Verifica a vizinhança acima
            numbered_image[y + 1, x] if (numbered_image[y + 1, x] > 0) else float('inf'),
            # Verifica a vizinhança abaixo
            numbered_image[y, x - 1] if (numbered_image[y, x - 1] > 0) else float('inf'),
            # Verifica a vizinhança à esquerda
            numbered_image[y, x + 1] if (numbered_image[y, x + 1] > 0) else float('inf'),
            # Verifica a vizinhança à direita
        ]
        return neighbors

    def change_value(numbered_image, y, x, minimum):
        changed = False
        if minimum < numbered_image[y, x]:
            numbered_image[y, x] = minimum
            changed = True
        return numbered_image, changed, min(numbered_image[y, x], minimum)

    def check_neighbors(numbered_image, y, x, minimum):
        if numbered_image[y - 1, x] > 0:
            numbered_image[y - 1, x] = minimum
        if numbered_image[y + 1, x] > 0:
            numbered_image[y + 1, x] = minimum
        if numbered_image[y, x - 1] > 0:
            numbered_image[y, x - 1] = minimum
        if numbered_image[y, x + 1] > 0:
            numbered_image[y, x + 1] = minimum
        return numbered_image

    changed = True
    height, width = numbered_image.shape
    print(f"height={height}")
    print(f"width={width}")
    # active_pixels = numbered_image > 0
    valores_distintos = np.unique(numbered_image)
    amount = len(valores_distintos)
    logging.info(f"Components: {amount - 1}")

    range_variaty = [
        # (start, end, step, start, end, step)
        (1, height-1, 1, 1, width-1, 1),
     #   (height - 1, 1, -1, 1, width - 1, 1),
     #   (1, height-1, 1, width-1, 1, -1),
     #   (height-1, 1, -1, width-1, 1, -1),
    ]

    while changed:
        changed = False
        for start_y, end_y, step_y, start_x, end_x, step_x in range_variaty:
            for y in range(start_y, end_y, step_y):
                for x in range(start_x, end_x, step_x):
                    if numbered_image[y, x] > 0:
                        neighbors = get_neighbors(numbered_image, y, x)
                        numbered_image, temp, minimum = change_value(numbered_image, y, x, min(neighbors))

                        if not changed and temp:
                            changed = temp

                        numbered_image = check_neighbors(numbered_image, y, x, minimum)
            valores_distintos = np.unique(numbered_image)
            amount = len(valores_distintos)
            logging.info(f"Components: {amount - 1}")
            if not changed:
                break
    return numbered_image

def rotular_componentes_conexos(image):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    start_time = time.time()
    # 1) Numerar todos os pixels “ativos” começando no canto superior esquerdo até o canto inferior direito.
    numbered_image = numerar_pixels(image)
    end_time = time.time()
    logging.info(f"Execution time: {end_time-start_time} seconds")

    # # 2) Analisar a vizinhança dos pixels numerados:
    # # • se existe um pixel “ativo” com valor menor que o valor do pixel central,
    # # o pixel central adota esse menor valor.
    # # 3) Repetir o passo 2 até não ocorrer mais mudanças
    start_time = time.time()
    # processed_image = analisar_vizinhanca(numbered_image)
    processed_image, amount = union_find(numbered_image)
    end_time = time.time()
    logging.info(f"Execution time: {end_time-start_time} seconds")

    # 4) Rotular os grupos resultantes com base no histograma.
    # • Calcular o Histograma*
    # • Numerar apenas as posições do histograma que possuem valores acima de zero.
    # • Aplicar esta nova tabela para mudar os números na imagem
    # Obtém os valores únicos na imagem
    valores_distintos = np.unique(processed_image)
    amount = len(valores_distintos)
    logging.info(f"Components: {amount-1}")

    # Colorir
    imagem_colorida = colorir_imagem(processed_image)
    return imagem_colorida
