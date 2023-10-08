import cv2

# Cargar la imagen
imagen = cv2.imread('logo.png')

# Verificar si la imagen se cargó correctamente
if imagen is None:
    print("No se pudo cargar la imagen.")
else:
    # Invertir los colores
    imagen_negativa = cv2.bitwise_not(imagen)

    # Mostrar la imagen original y la imagen negativa
    cv2.imshow('Imagen Original', imagen)
    cv2.imshow('Imagen Negativa', imagen_negativa)

    # Guardar la imagen negativa en un archivo
    cv2.imwrite('imagen_negativa.jpg', imagen_negativa)

    # Esperar hasta que se presione una tecla y luego cerrar las ventanas
    cv2.waitKey(0)
    cv2.destroyAllWindows()
