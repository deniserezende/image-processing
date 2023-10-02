
import cv2
import os
import numpy as np
import matplotlib.pyplot as plt


def count_occurrences(array, valor_maximo):
    return np.bincount(array, minlength=valor_maximo + 1)


# 1. Carregar a imagem com o OpenCV
# image_path = input("Add the path to the image: ")
image_path = "lenna.png"
gray_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
cv2.imwrite('gray_image.png', gray_image)

tom_maximo = np.max(gray_image)
tom_minimo = np.min(gray_image)
array_aplanado = gray_image.ravel()

# 2. Montar o histograma
histograma = count_occurrences(array_aplanado, 255)

# Plot do Histograma
plt.bar(range(256), histograma, color='b', alpha=0.7)
plt.xlim(-10, 260)  # Define os limites para o eixo x
plt.xlabel('Valor do Pixel')
plt.ylabel('Frequência')
plt.title('Histograma Original')
plt.savefig('histograma_original.png')
plt.clf()


# 3. Função sk
def transformation_function_sk(rk, L, probabilidade):
    sk = int((L - 1) * np.sum(probabilidade[:rk+1]))
    return sk


# Obtém as dimensões da imagem (altura x largura) para calcular total de pixels
altura, largura = gray_image.shape[:2]
total_de_pixels = altura * largura
# Calcula a função sk
sk_array = []
for i in range(tom_minimo, tom_maximo):
    sk_array.append(transformation_function_sk(i, 255, histograma/total_de_pixels))

# Plot da função de transformação
plt.plot(range(tom_minimo, tom_maximo), sk_array, label='Função de Transformação')
plt.xlim(-10, 260)  # Define os limites para o eixo x
plt.xlabel('r_k')
plt.ylabel('s_k')
plt.title('Função de Transformação')
plt.savefig('funcao_transformacao.png')
plt.clf()

# 4. Calcular a Função de Transformação para Equalização
def transformation_function_eq(rk, L, probabilidade):
    sk = int((L - 1) * np.sum(probabilidade[:rk+1]))
    return sk

transformation_eq_array = []
for i in range(tom_minimo, tom_maximo):
    transformation_eq_array.append(transformation_function_eq(i, 255, histograma/total_de_pixels))

# 5. Calcular o Histograma Equalizado
equalized_histogram = count_occurrences(transformation_eq_array, 255)

# Plot do Histograma Equalizado
plt.bar(range(256), equalized_histogram, color='g', alpha=0.7)
plt.xlim(-10, 260)  # Define os limites para o eixo x
plt.xlabel('Valor do Pixel')
plt.ylabel('Frequência')
plt.title('Histograma Equalizado')
plt.savefig('histograma_equalizado.png')
plt.clf()

# 6. Aplicar a Transformação na Imagem Original
imagem_equalizada = np.zeros_like(gray_image)
for i in range(tom_minimo, tom_maximo):
    imagem_equalizada[gray_image == i] = transformation_eq_array[i-tom_minimo]

# Salvar a imagem equalizada
cv2.imwrite('imagem_equalizada.png', imagem_equalizada)



# os.remove("gray_image.png")
