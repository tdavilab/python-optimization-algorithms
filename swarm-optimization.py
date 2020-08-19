'''
SWARM OPTIMIZATION - ENJAMBRE
Hecho por Thomas Daniel Avila Blenkey - 20151020012
Para la clase de cibernética cualitativa III
Universidad Distrital - Facultad de Ingeniería
'''

import random

# Problema
funcion_objetivo = "(x1-3)**2+(x2-5)**2"
op = "min"

iteraciones = 10000

# 1. TAMANO DEL ENJAMBRE
tam_enjambre = 4

# 2. POBLACIÓN INICIAL
# Rango de la población inicial
x_min = 0
x_max = 7

# Población inicial
x1 = [random.uniform(x_min, x_max) for i in range(tam_enjambre)]
x2 = [random.uniform(x_min, x_max) for i in range(tam_enjambre)]

# 4. VELOCIDADES INICIALES
p_best = []
g_best = []
velocidades_x1 = [0 for i in range(len(x1))]
velocidades_x2 = [0 for i in range(len(x2))]


# 3. EVALUAR FUNCIÓN OBJETIVO
def reemplazar_valores(z, x1, x2):
    exec('x1=' + str(x1))
    exec('x2=' + str(x2))
    return eval(z)

for itr in range(0, iteraciones):

    #print("X1: " + str(x1))
    #print("X2: " + str(x2))
    #print("INFO: VX1: "+str(velocidades_x1)+" VX2: "+str(velocidades_x2)+", PBEST: "+str(p_best)+" GBEST: "+str(g_best))

    # Lista en donde cada elemento es una lista con el valor de x1, x2 y el valor de la función objetivo evaluada
    # 16 valores
    z = [[x1[i], x2[j], reemplazar_valores(funcion_objetivo, x1[i], x2[j])] for i in range(len(x1)) for j in
         range(len(x2))]


    # 5. SELECCIONAR PBEST Y GBEST
    # Selección PBest (16 valores)

    if itr == 0:
        p_best = [z[i][2] for i in range(len(z))]
    else:
        p_best = [z[i][2] if z[i][2] < p_best[i] else p_best[i] for i in range(len(z))]

    # Selección GBest
    g_best = min(p_best)

    # 6. VELOCIDADES DE LAS PARTICULAS
    c1 = 1
    c2 = 1
    r1 = random.uniform(0,1)
    r2 = random.uniform(0,1)
    o_min = 0.4
    o_max = 0.9
    o = o_max - ((o_max - o_min) / 20)

    # Para la ecuación de las velocidades, se comparan listas para obtener el mejor p_best para cada x1 y x2
    # 4 valores
    p_best_x1 = [min([p_best[i + 4 * j] for i in range(0, 4)]) for j in range(0, 4)]
    p_best_x2 = [min([p_best[i] for i in range(len(p_best)) if i % 4 == j]) for j in range(0, 4)]

    # Calcula las velocidades para cada valor de x1 y x2
    velocidades_x1 = [o * velocidades_x1[i] + c1 * r1 * (p_best_x1[i] - x1[i]) + c2 * r2 * (g_best - x1[i]) for i in
                      range(len(x1))]
    velocidades_x2 = [o * velocidades_x2[i] + c1 * r1 * (p_best_x2[i] - x2[i]) + c2 * r2 * (g_best - x2[i]) for i in
                      range(len(x2))]

    # 7. CALCULAR NUEVOS VALORES
    x1 = [x1[i] + velocidades_x1[i] for i in range(len(x1))]
    x2 = [x2[i] + velocidades_x2[i] for i in range(len(x2))]


# FINALMENTE SE IMPRIME LA SOLUCIÓN EN CADA ITERACIÓN POR CONSOLA
z = [[x1[i], x2[j], reemplazar_valores(funcion_objetivo, x1[i], x2[j])] for i in range(len(x1)) for j in
         range(len(x2))]

zmin = min(el[2] for el in z)
x1min = 0
x2min = 0
for el in z:
    if el[2] == zmin:
        x1min = el[0]
        x2min = el[1]

print("ITERACION = "+str(itr)+", X1 = "+str(x1min)+", X2 = "+str(x2min)+", Z = "+str(zmin))





