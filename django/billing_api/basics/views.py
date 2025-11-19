from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def area_triangulo(request):
    try:
        base = float(request.data.get('base', 0))
        altura = float(request.data.get('altura', 0))
    except (TypeError, ValueError):
        return Response({"error": "Parametros Invalidos"}, status=status.HTTP_400_BAD_REQUEST)
    area = (base * altura) / 2
    return Response({
        "base": base,
        "altura": altura,
        "area": area
    })

@api_view(['GET'])
def tabla_multiplicar(request):
    try:
        n = int(request.query_params.get('numero', 0))
    except (TypeError, ValueError):
        return Response({"error": "Numero Invalido"}, status=status.HTTP_400_BAD_REQUEST)
    tabla = [f"{n}x{i}={n*(i)}" for i in range(1,11)]
    return Response({
        "numero": n,
        "tabla": tabla
    })

@api_view(['GET'])
def contar_mayores(request):
    try:
        numeros = request.data.get('numeros', [])
        limite = request.data.get('limite',0)
    except (TypeError, ValueError):
        return Response({"error": "Parametros Invalidos"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        limite=float(limite)
        lista_numeros=[float(n) for n in numeros]
    except (TypeError, ValueError):
        return Response({"error": "Valores numericos Invalidos"}, status=status.HTTP_400_BAD_REQUEST)
    contador = 0
    for n in lista_numeros:
        if n > limite:
            contador += 1
    return Response({
        "numeros": lista_numeros,
        "limite": limite,
        "contador": contador
    })


@api_view(['POST'])
def sumar_incrementos(request):
    try:
        if 'numero' not in request.data:
            return Response({"error": "Parametro 'numero' requerido"}, status=status.HTTP_400_BAD_REQUEST)
        numero = float(request.data.get('numero'))
    except (TypeError, ValueError):
        return Response({"error": "Numero invalido"}, status=status.HTTP_400_BAD_REQUEST)
    if 'incrementos' in request.data:
        incrementos = request.data.get('incrementos')
        try:
            lista_incrementos = [float(x) for x in incrementos]
        except (TypeError, ValueError):
            return Response({"error": "Incrementos invalidos"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        if 'hasta' not in request.data:
            return Response({"error": "Parametro 'hasta' reuerido Invalido"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            hasta = int(request.data.get('hasta'))
        except (TypeError, ValueError):
            return Response({"error": "Parametro 'hasta' debe ser entero"}, status=status.HTTP_400_BAD_REQUEST)
        if hasta < 1:
            return Response({"error": "Parametro 'hasta' debe ser >= 1"}, status=status.HTTP_400_BAD_REQUEST)
        lista_incrementos = [float(i) for i in range(1, hasta + 1)]

    resultado = numero + sum(lista_incrementos)
    return Response({
        "numero": numero,
        "incrementos": lista_incrementos,
        "resultado": resultado
    })