"""
Pide el numero de empleados y luego el sueldo de cada uno.
suma y muestra  la nomina total
"""

empleados = int(input("Número de empleados: "))
nomina = 0
for i in range(empleados):
    sueldo = float(input(f"Sueldo empleado {i+1}: "))
    nomina += sueldo
print(f"Nomina total: {nomina}")