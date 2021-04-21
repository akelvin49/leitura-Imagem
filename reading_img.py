import os
import cv2
import numpy as np
import pytesseract as ocr
import sys
from PIL import Image
 
cropping = False
 
x_start, y_start, x_end, y_end = 0, 0, 0, 0
 
image = cv2.imread('saoluis.jpg')
#image = cv2.imread('t1.jpg')

oriImage = image.copy()
 
 
def mouse_crop(event, x, y, flags, param):
    # pegar referências para as variáveis globais
    global x_start, y_start, x_end, y_end, cropping
 
    # se o botão esquerdo do mouse estiver PARA BAIXO, comece a RECORTAR
    # (x, y) coordena e indica onde está sendo o corte
    if event == cv2.EVENT_LBUTTONDOWN:
        x_start, y_start, x_end, y_end = x, y, x, y
        cropping = True
 
    # Movimento do mouse
    elif event == cv2.EVENT_MOUSEMOVE:
        if cropping == True:
            x_end, y_end = x, y
 
    # if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # gravar as coordenadas finais (x, y)
        x_end, y_end = x, y
        cropping = False # cropping foi finalizado
 
        refPoint = [(x_start, y_start), (x_end, y_end)]
 
        if len(refPoint) == 2: #quando dois pontos foram encontrados
            roi = oriImage[refPoint[0][1]:refPoint[1][1], refPoint[0][0]:refPoint[1][0]]
            cv2.imshow("Cropped", roi)
            cv2.imwrite('grey.png', roi)           
            # tipando a leitura para os canais de ordem RGB
            imagem = Image.open('grey.png').convert('RGB')

            # convertendo em um array editável de numpy[x, y, CANALS]
            npimagem = np.asarray(imagem).astype(np.uint8)  

            # diminuição dos ruidos antes da binarização
            npimagem[:, :, 0] = 0 # zerando o canal R (RED)
            npimagem[:, :, 2] = 0 # zerando o canal B (BLUE)

            # atribuição em escala de cinza
            im = cv2.cvtColor(npimagem, cv2.COLOR_RGB2GRAY) 

            # aplicação da truncagem binária para a intensidade
            # pixels de intensidade de cor abaixo de 127 serão convertidos para 0 (PRETO)
            # pixels de intensidade de cor acima de 127 serão convertidos para 255 (BRANCO)
            # A atrubição do THRESH_OTSU incrementa uma análise inteligente dos nivels de truncagem
            ret, thresh = cv2.threshold(im, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU) 

            # reconvertendo o retorno do threshold em um objeto do tipo PIL.Image
            binimagem = Image.fromarray(thresh)

            # chamada ao tesseract OCR por meio de seu wrapper
            phrase = ocr.image_to_string(binimagem, lang='por')

            # impressão do resultado
            print(phrase)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            os.remove('grey.png')
            sys.exit()
            
            
            
            
 
cv2.namedWindow("image")
cv2.setMouseCallback("image", mouse_crop)

 
while True:
 
    i = image.copy()
 
    if not cropping:
        cv2.imshow("image", image)
 
    elif cropping:
        cv2.rectangle(i, (x_start, y_start), (x_end, y_end), (255, 0, 0), 2)
        cv2.imshow("image", i)
 
    cv2.waitKey(1)
 
#fecha todas as janelas abertas
cv2.destroyAPlayerPrefsPlayerPrefsllWindows()
