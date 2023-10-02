# • Implementar um algoritmo que realize a convoluçã o em uma dada
# imagem a partir de uma determinada máscara. Com o algoritmo de
# convoluçã o implementado, utilize-o para desenvolver os 4iltros da
# média, da média com limiar, e da mediana.

import cv2
import os
import numpy as np

# 1. Carregar a imagem com o OpenCV
image_path = "gaussianruid.jpg"
image_path_two = "saltandpepperruid.jpg"
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)


def convolucao(imagem, mascara):
    altura, largura = imagem.shape
    m_altura, m_largura = mascara.shape
    resultado = np.zeros((altura, largura))

    for i in range(altura):
        for j in range(largura):
            for m in range(m_altura):
                for n in range(m_largura):
                    if i+m >= m_altura//2 and i+m < altura - m_altura//2 and j+n >= m_largura//2 and j+n < largura - m_largura//2:
                        resultado[i, j] += imagem[i+m-m_altura//2, j+n-m_largura//2] * mascara[m, n]

    return resultado

# FILTRO DA MEDIA
mascara_media = np.array([[1, 1, 1],
                         [1, 1, 1],
                         [1, 1, 1]]) / 9

# FILTRO DA MEDIA COM LIMIAR
mascara_media_limiar = np.array([[1, 1, 1],
                                [1, 1, 1],
                                [1, 1, 1]]) / 9
limiar = 100  # Defina o limiar desejado

def filtro_media_limiar(imagem, mascara, limiar):
    resultado = convolucao(imagem, mascara)
    resultado[resultado < limiar] = 0
    return resultado


# FILTRO DA MEDIANA
def filtro_mediana(imagem):
    altura, largura = imagem.shape
    resultado = np.zeros((altura, largura))

    for i in range(altura):
        for j in range(largura):
            vizinhos = []
            for m in range(-1, 2):
                for n in range(-1, 2):
                    if i+m >= 0 and i+m < altura and j+n >= 0 and j+n < largura:
                        vizinhos.append(imagem[i+m, j+n])
            resultado[i, j] = np.median(vizinhos)

    return resultado

imagem_filtrada_media = convolucao(image, mascara_media)
cv2.imwrite('imagem_filtrada_media.jpg', imagem_filtrada_media)
imagem_filtrada_media_limiar = filtro_media_limiar(image, mascara_media_limiar, limiar)
cv2.imwrite('imagem_filtrada_media_limiar.jpg', imagem_filtrada_media_limiar)
imagem_filtrada_mediana = filtro_mediana(image)
cv2.imwrite('imagem_filtrada_mediana.jpg', imagem_filtrada_mediana)

