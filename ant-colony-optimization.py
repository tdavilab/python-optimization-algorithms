'''
ANT COLONY OPTIMIZATION
Hecho por Thomas Daniel Avila Blenkey - 20151020012
Para la clase de cibernética cualitativa III
Universidad Distrital - Facultad de Ingeniería
'''

import random

# Problema
funcion_objetivo = "x**5-5*x**3-20*x+5"
# Factor de decaimiento de feromona
rho = 0.5

# Factor de escala
zeta = 2

sigma = 1

# Número de Hormigas
num_hormigas = 10

# Número de Iteraciones
iteraciones = 10

def reemplazar_valores(z, x):
    exec('x=' + str(x))
    return eval(z)

print("PROBLEMA\n")
print("Función Objetivo : "+str(funcion_objetivo))


# 1. DEFINICIÓN CAPAS Y CAMINOS

# Número de capas es 1, al haber solo una variable
num_capas = 1
min_intervalo = 0
max_intervalo = 3

total_caminos = max_intervalo*2+1

caminos = [x*0.5 for x in range(min_intervalo,total_caminos)]

print("\n1. POSIBLES CAMINOS\n")
[print("X1"+str(i+1)+" = "+str(caminos[i])) for i in range(total_caminos)]
    

# 2. DEFINICIÓN NÚMERO DE HORMIGAS

# Cantidad inicial de feromona a lo largo de cada camino
feromona_inicial = [1 for h in range(total_caminos)]
feromonas = feromona_inicial

# Probabilidad de seleccionar un camino
probabilidades = [feromona_inicial[i]/total_caminos for i in range(total_caminos)]

print("\n2. DEFINICIÓN NÚMERO DE HORMIGAS\n")
print("Número de Hormigas: "+str(num_hormigas))
print("Lista Cantidad Inicial Feromona: "+str(feromona_inicial))
print("Lista Probabilidades"+str(probabilidades))

# 3. AJUSTE PROBABILIDADES ACUMULADAS

rangos_prob_acum = []

for i in range(total_caminos):
    if i==0:
        rangos_prob_acum.append([0, probabilidades[i]])
    else:
        rangos_prob_acum.append([rangos_prob_acum[i-1][1], rangos_prob_acum[i-1][1]+probabilidades[i]])
      
print("\n3. VALORES INICIALES DE LAS HORMIGAS")
print("\nVariable(Xij)\tRangos de Probabilidades Acumuladas")
[print("X1"+str(i+1)+" = "+str(caminos[i])+"\t"+str(rangos_prob_acum[i][0])+" - "+str(rangos_prob_acum[i][1])) for i in range(total_caminos)]


# 4. SELECCIÓN Y EVALUACIÓN DE LAS HORMIGAS INICIALES

# Valores de r aleatorios
vals_r = [random.uniform(0,1) for i in range(num_hormigas)]

horm_sel = []

# Se recorren los valores aleatorios obtenidos y se evalúa el rango en el que
# se encuentran para así agregarlos a la lista de hormigas seleccionadas
for r in vals_r:
    for i in range(total_caminos):
        if r >= rangos_prob_acum[i][0] and r < rangos_prob_acum[i][1]:
            #Realliza append con la variable y el valor"
            horm_sel.append([i, caminos[i]])

# Reemplaza la función objetivo
vals_f_o = [reemplazar_valores(funcion_objetivo, x[1]) for x in horm_sel]

f_best = min(vals_f_o)
h_best = [i for i in range(num_hormigas) if vals_f_o[i] == f_best]
x_best = [horm_sel[i] for i in range(num_hormigas) if vals_f_o[i] == f_best]


f_worst = max(vals_f_o)
h_worst = [i for i in range(num_hormigas) if vals_f_o[i] == f_worst]
x_worst = [horm_sel[i] for i in range(num_hormigas) if vals_f_o[i] == f_worst]



print("\n4. SELECCIÓN Y EVALUACIÓN DE LAS HORMIGAS INICIALES\n")
print("Hormiga\tVar\tValor\tF.O(Xij)")
[print(str(i+1)+"\tX1"+str(horm_sel[i][0]+1)+"\t"+str(horm_sel[i][1])+"\t"+str(vals_f_o[i])) for i in range(num_hormigas)]
print("\nfbest="+str(f_best)+" => hbest="+str([h+1 for h in h_best])+" => xbest=X1"+str(x_best[0][0]+1)+"="+str(x_best[0][1]))


# 5. CÁLCULO DEL INCREMENTO DE FEROMONA PARA LOS MEJORES CAMINOS

# Num de hormigas que tienen el mejor camino
N = 0

for val in vals_f_o:
    if val == f_best:
        N += 1

# Incremento de feromona
incremento = abs(N*((zeta*f_best)/f_worst))

print("\n5. CÁLCULO DEL INCREMENTO DE FEROMONA PARA LOS MEJORES CAMINOS\n")
print("Incremento: "+str(incremento))


# 6. ACTUALIZACIÓN DE LA CANTIDAD DE FEROMONA PARA LOS MEJORES CAMINOS
feromonas[x_best[0][0]] += incremento

print("\n6. ACTUALIZACIÓN DE LA CANTIDAD DE FEROMONA PARA LOS MEJORES CAMINOS\n")
print("Lista Feromonas Actualizada: "+str(feromonas))

# 7. DECAIMIENTO DE FEROMONA

for i in range(total_caminos):
    if i != x_best[0][0]:
        feromonas[i] = (1-rho)*feromonas[i]

print("\n7. DECAIMIENTO DE FEROMONA\n")
print("Lista Feromonas Actualizada: "+str(feromonas))




print("\n\nITERACIONES:")
print("IT: 0"+"\tZ = "+str(f_best)+"\tX = X1"+str(x_best[0][0]+1)+" = "+str(x_best[0][1])+"\thbest="+str([h+1 for h in h_best]))
for itr in range(1,iteraciones+1):

    # 2. AJUSTE PROBABILIDADES (ACTUALIZADAS)

    probabilidades[x_best[0][0]] = feromonas[x_best[0][0]]/total_caminos

    for i in range(total_caminos):
        if i != x_best[0][0]:
            probabilidades[i] = feromonas[i]/total_caminos

    '''if itr == 1:
        print("\n8.\nLista Probabilidades Actualizada: "+str(probabilidades))'''

    # 3. AJUSTE PROBABILIDADES ACUMULADAS

    rangos_prob_acum = []

    for i in range(total_caminos):
        if i==0:
            rangos_prob_acum.append([0, probabilidades[i]])
        elif i==total_caminos-1:
            rangos_prob_acum.append([rangos_prob_acum[i-1][1], 1])
        else:
            rangos_prob_acum.append([rangos_prob_acum[i-1][1], rangos_prob_acum[i-1][1]+probabilidades[i]])

    '''if itr == 1:
        print("Probabilidades Acumuladas")
        print("Variable(Xij)\tRangos de Probabilidades Acumuladas")
        [print("X1"+str(i+1)+" = "+str(caminos[i])+"\t"+str(rangos_prob_acum[i][0])+" - "+str(rangos_prob_acum[i][1])) for i in range(total_caminos)]'''

       
    # 4. SELECCIÓN Y EVALUACIÓN DE LAS HORMIGAS INICIALES

    # Valores de r aleatorios
    vals_r = [random.uniform(0,1) for i in range(num_hormigas)]
    horm_sel = []

    # Se recorren los valores aleatorios obtenidos y se evalúa el rango en el que se encuentran
    # para así agregarlos a la lista de hormigas seleccionadas
    for r in vals_r:
        for i in range(total_caminos):
            if r >= rangos_prob_acum[i][0] and r < rangos_prob_acum[i][1]:
                #Realliza append con la variable y el valor"
                horm_sel.append([i, caminos[i]])

    # Reemplaza la función objetivo
    vals_f_o = [reemplazar_valores(funcion_objetivo, x[1]) for x in horm_sel]

    x_best = [horm_sel[i] for i in range(num_hormigas) if vals_f_o[i] == f_best]
    h_best = [i for i in range(num_hormigas) if vals_f_o[i] == f_best]
    f_worst = max(vals_f_o)
    h_worst = [i for i in range(num_hormigas) if vals_f_o[i] == f_worst]
    x_worst = [horm_sel[i] for i in range(num_hormigas) if vals_f_o[i] == f_worst]

    # 5. CÁLCULO DEL INCREMENTO DE FEROMONA PARA LOS MEJORES CAMINOS

    # Num de hormigas que tienen el mejor camino
    N = 0

    for val in vals_f_o:
        if val == f_best:
            N += 1

    # Incremento de feromona
    incremento = abs(N*((zeta*f_best)/f_worst))


    # 6. ACTUALIZACIÓN DE LA CANTIDAD DE FEROMONA PARA LOS MEJORES CAMINOS
    feromonas[x_best[0][0]] += incremento


    # 7. DECAIMIENTO DE FEROMONA

    for i in range(total_caminos):
        if i != x_best[0][0]:
            feromonas[i] = (1-rho)*feromonas[i]

    print("IT: "+str(itr)+"\tZ = "+str(f_best)+"\tX = X1"+str(x_best[0][0]+1)+" = "+str(x_best[0][1])+"\thbest="+str([h+1 for h in h_best]))







