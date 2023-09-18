import cv2
import os
import rotular_componentes_conexos as rcc


# Carregar a imagem com o OpenCV
# image_path = input("Add the path to the image: ")
image_path = "image.jpg"
original_image = cv2.imread(image_path, cv2.IMREAD_COLOR) #IMREAD_COLOR

gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
cv2.imwrite('gray_image.png', gray_image)

threshold_value = 240
_, binary_image = cv2.threshold(gray_image, threshold_value, 255, cv2.THRESH_BINARY)

# Salve a imagem binária
cv2.imwrite('imagem_binaria.png', binary_image)

imagem_colorida = rcc.rotular_componentes_conexos(binary_image)
cv2.imwrite('imagem_final.png', imagem_colorida)

os.remove("gray_image.png")
os.remove("imagem_binaria.png")