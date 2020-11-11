# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 22:34:37 2020

@author: tadeo
"""
class Portafolio():
    def __init__(self, tipo):
        self.tipo = tipo
    
    def __str__(self):
        return "del portafolio de tipo {}".format(self.tipo)

class Accion(Portafolio):
    def __init__(self, tipo, nombre, preciocompra, cantidad):
        super().__init__(tipo)
        self.nombre = nombre
        self.preciocompra = preciocompra
        self.cantidad = cantidad
    def __str__(self):
        return super().__str__() + ", compramos {}, por la cantidad de {}, a un precio de {}$.".format(self.nombre, self.cantidad, self.preciocompra)
class Opcion(Accion):
    def __init__(self, tipo, nombre, preciocompra, cantidad, nombreOp, precioOp, valIntrinseco):
        super().__init__(tipo, nombre, preciocompra, cantidad)
        self.nombreOp = nombreOp
        self.precioOp = precioOp
        self.valIntrinseco = valIntrinseco
    def __str__(self):
        return super().__str__() + ", compramos opcion {}, a un precio {}$, teniendo valor intrinseco {}$.".format(self.nombreOp, self.precioOp, self.valIntrinseco)

activos = [
    Accion("moderado", "GGAL", 109, 1000),
    Accion("moderado", "PAMP", 52, 3200),
    Accion("moderado", "AAPL", 120, 500),
    Accion("moderado", "MELI", 1200, 100),
    Opcion("moderado", "GGAL", 109, 1000, "GFGC105.DI", 4, 5)
    ]
    
def describir(lista):
    for a in lista:
        print("{} {}".format( type(a).__name__, a))
describir(activos)