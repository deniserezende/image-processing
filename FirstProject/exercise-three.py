import cv2
import numpy as np

# Carregar a imagem com o OpenCV
image_path = input("Add the path to the image: ")
original_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Já carrega em grayscale


# Função para realizar a quantização binária (preto e branco)
# Essa foi a única forma que encontrei para quando for dois níveis só aplicar branco e preto
def binary_quantize(image):
    q_image = image.copy()

    # Aplica a quantização binária
    q_image[q_image < 128] = 0  # Define pixels mais escuros como preto
    q_image[q_image >= 128] = 255  # Define pixels mais claros como branco

    return q_image


# Função para reduzir o número de níveis de intensidade
def quantize_image(image, level):
    if level == 2:
        return binary_quantize(image)
    else:
        factor = 256 // level
        q_image = (image // factor) * factor
        return q_image.astype(np.uint8)


levels_list = [2, 4, 16, 128]
# Processar e salvar as imagens quantizadas
for lev in levels_list:
    quantized_image = quantize_image(original_image, lev)
    output_path = f'quantized_image_{lev}.jpg'
    cv2.imwrite(output_path, quantized_image)
