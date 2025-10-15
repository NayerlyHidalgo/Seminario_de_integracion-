

salario = float(input("Ingrese su salario mensual: "))

if salario < 1000:
    print("Junior")
elif 1000 <= salario < 2000:
    print("Semi-Senior")
elif salario >= 2000:
    print("Senior")
else:
    print("Salario no válido")