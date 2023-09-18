import cv2

# Carregar a imagem com o OpenCV
image_path = input("Add the path to the image: ")  # Substitua pelo caminho da sua imagem
original_image = cv2.imread(image_path)


# Função para diminuir a resolução espacial
def downsample_image(image, interval):
    ds_image = image[::interval, ::interval]
    return ds_image


interval_list = [2, 4, 8, 16]
# Processar e salvar as imagens resultantes
for i in interval_list:
    downsampled_image = downsample_image(original_image, i)
    output_path = f'downsampled_image_{i}.jpg'
    cv2.imwrite(output_path, downsampled_image)