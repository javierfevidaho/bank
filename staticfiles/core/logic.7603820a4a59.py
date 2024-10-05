import random
from datetime import datetime
from core.models import Ticket, WinningNumbers, Jackpot

def realizar_sorteo():
    # Generar números ganadores aleatorios
    numeros_ganadores = [random.randint(1, 50) for _ in range(6)]
    
    # Crear un nuevo objeto WinningNumbers
    ganadores = WinningNumbers.objects.create(
        numeros=numeros_ganadores,
        draw_date=datetime.now()
    )
    
    # Obtener todos los tickets y verificar si hay ganadores
    tickets = Ticket.objects.all()
    ganadores_list = []
    for ticket in tickets:
        if ticket.numeros == numeros_ganadores:
            ganadores_list.append(ticket.usuario)
            # Guardar en la base de datos el ganador
            Jackpot.objects.create(ticket=ticket, ganadores=ganadores)
    
    return ganadores_list
