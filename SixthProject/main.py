import os
import cv2
import numpy as np
from matplotlib import pyplot as plt

# Obtém a lista de arquivos na pasta local
arquivos_png = [arquivo for arquivo in os.listdir() if arquivo.endswith('.png')]
print("\nArquivos PNG na pasta local:")
for arquivo in arquivos_png:
    print(f"\t{arquivo}")

nome_do_arquivo = input("\nDigite o nome do arquivo PNG que você deseja carregar: ")

# Carregar a imagem
imagem = cv2.imread(nome_do_arquivo)

# Converter para escala de cinza
imagem_gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

# Aplicar filtro passa-baixa (suavização)
imagem_suavizada = cv2.GaussianBlur(imagem_gray, (5, 5), 0)

# Aplicar filtro passa-alta (realce de bordas)
imagem_realce_bordas = cv2.Laplacian(imagem_gray, cv2.CV_64F)
imagem_realce_bordas = np.uint8(np.absolute(imagem_realce_bordas))

# Exibir as imagens original, suavizada e com realce de bordas
plt.subplot(1, 3, 1), plt.imshow(imagem_gray, cmap='gray')
plt.title('Original'), plt.xticks([]), plt.yticks([])

plt.subplot(1, 3, 2), plt.imshow(imagem_suavizada, cmap='gray')
plt.title('Suavizada'), plt.xticks([]), plt.yticks([])

plt.subplot(1, 3, 3), plt.imshow(imagem_realce_bordas, cmap='gray')
plt.title('Realce de Bordas'), plt.xticks([]), plt.yticks([])

# Set the window title
manager = plt.get_current_fig_manager()
manager.set_window_title('Filtragem espacial: filtros passa-alta e passa-baixa')

plt.show()
