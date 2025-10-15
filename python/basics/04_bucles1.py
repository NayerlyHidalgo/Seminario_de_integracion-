"""Pide cuantos dias registraras
para cada dia T(tarde) O(ok) P(permisos)
Cuenta y muestra tardanzas totales"""

dias = int(input("¿Cuántos días registraras? "))
tardes = 0 
for i in range(dias):
    marca = input(f"Dia {i+1} (T=tarde, O=ok, P=permiso)").strip().upper()
    if marca == "T":
        tardes += 1
print(f"Tardanzas totales: {tardes}")