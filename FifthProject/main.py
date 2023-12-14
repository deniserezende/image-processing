import cv2
import numpy as np

# Load the input image
img_path = 'img.png'
img = cv2.imread(img_path)

# AUXILIARES
size_elemest = (5, 5)
elemest = cv2.getStructuringElement(cv2.MORPH_RECT, size_elemest)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# ABERTURA
abertura = cv2.dilate(cv2.erode(img_gray, elemest, iterations=1), elemest, iterations=1)

# FECHAMENTO
fechamento = cv2.erode(cv2.dilate(img_gray, elemest, iterations=1), elemest, iterations=1)

# GRADIENTE
gradiente = cv2.dilate(img_gray, elemest, iterations=1) - cv2.erode(img_gray, elemest, iterations=1)

# COMPONENTES CONEXOS
_, binarized_img = cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY)
_, rotulos = cv2.connectedComponents(binarized_img)
componentes_visuais = np.zeros_like(img)
for i in range(1, _):
    componentes_visuais[rotulos == i] = i

cv2.imshow("Abertura", abertura)
cv2.imshow("Fechamento", fechamento)
cv2.imshow("Gradiente", gradiente)
cv2.imshow("Componentes Conexos", componentes_visuais)
cv2.waitKey(0)
cv2.destroyAllWindows()
