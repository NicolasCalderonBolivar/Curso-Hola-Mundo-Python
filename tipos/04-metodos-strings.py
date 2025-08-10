# con alt + shift y flecha abajo duplicamos linea de codigo
# metodo es una funcion que se encuentra dentro de un objeto

animal = " chanchito feliz"

print(animal.upper())  # comvierte todo el string en mayusculas
print(animal.lower())  # comvierte todo el string en minuscula
print(animal.strip().capitalize())  # toma la primera letra en mayus
print(animal.title())  # iniciales en mayuscula
print(animal.strip())  # quita los espacios
print(animal.rstrip())  # quita los espacios a la der
print(animal.lstrip())  # quita los espacios a la izq
print(animal.find("hi"))  # nos devuelve el indice del caracter
print(animal.replace("nchi", "Feo"))  # remplazamos caracteres
print("nchi" in animal)  # te devuelve un boolean si se encuentra o no
print("nchi" not in animal)  # te devuelve un boolean si se encuentra o no
