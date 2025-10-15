""" Escriba un programa que pida edad, años de experiencia y su tiene titulo universitario.
Un candidato es elegible si tiene >=21 años y experiencia >=2 años o titulo.
Muestra Elegible o No elegible """

edad = int(input("Edad del candidato: "))
exp= int(input("Años de experiencia: "))
titulo = input("Tiene titulo universitario? (s/n): ").lower() == "s"

if(edad<=21 and (exp>=2 or titulo == "s")):
    print("Elegible")
else:
    print("No elegible")