""" Sistema que pida por hora y horas trabajadas. 
Las primeras 40h son normales, las extras se pagan el 15%
calcula y muestra el total a pagar"""

hora = float(input("Pago por hora: "))
horas = int(input("Horas trabajadas: "))

if horas <= 40:
    total = hora * horas
else:
    total = hora * 40 + (hora * 1.15 * (horas - 40))

print("Total a pagar:", total) 