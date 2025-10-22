"""
Pide numero de empleados 
cada empleado solicita nombre y salario
determina quien tiene el mayor salario  y muestralo"""

empleados = int(input("Número de empleados: "))
mayor_salario = 0
nombre_mayor = ""

for i in range(empleados):
    nombre = input(f"nombre empleado {i+1}: ")
    salario = float(input(f"salario empleado {i+1}: "))
    if salario > mayor_salario:
        mayor_salario = salario
        nombre_mayor = nombre
print(f"Empleado con mayor salario: {nombre_mayor}, Salario: {mayor_salario}")


   


