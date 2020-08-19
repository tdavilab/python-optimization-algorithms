'''
SIMULATED ANNEALING - RECOCIDO SIMULADO
Hecho por Thomas Daniel Avila Blenkey - 20151020012
Para la clase de cibernética cualitativa III
Universidad Distrital - Facultad de Ingeniería
'''

import math
import random
import numpy as np

### Método para hallar la solución vecina, retorna los valores de x1 y x2 vecinos, y la función objetivo evaluada en esa solución
def hallar_solucion_vecina(sol_inicial, funcion_objetivo, ra):
	# 5. SOLUCION VECINA

	# Numeros aleatorios
	u = [random.uniform(0,1) for i in range(2)]

	# Matriz vecina

	v1 = [sol_inicial[0]+rango for rango in ra]
	v2 = [sol_inicial[1]+rango for rango in ra]

	v = np.matrix([v1,v2])

	v11 = v.item((0,0))
	v12 = v.item((0,1))
	v21 = v.item((1,0))
	v22 = v.item((1,1))

	# Solucion Vecina

	r1 = v11+u[0]*(v12-v11)
	r2 = v21+u[1]*(v22-v21)

	sol_vecina = [r1,r2]

	# Se evalua la función objetivo en la solución vecina

	z_vecina = evaluar_funcion_objetivo(funcion_objetivo, sol_vecina)

	return sol_vecina, z_vecina

### Método para evaluar el criterio de metrópolis, retorna los valores de x1 y x2 obtenidos y el nuevo valor de la temperatura
def criterio_metropolis(z_inicial, z_vecina, solucion, sol_vecina, temperatura_inicial, c, k, opt):

	# 6. CRITERIO DE METROPOLIS

	# Se evalua si la solucion vecina es menor a la solucion anterior

	delta_z = z_vecina - z_inicial

	# Criterio de Metropolis
	if (delta_z >= 0 and opt == "min") or (delta_z < 0 and opt == "max"):

		# Probabilidad de Boltzman
		p = np.exp(-delta_z/(k*temperatura_inicial))
		
		# Numero aleatorio A
		a = random.uniform(0, 1)
		
		if a < p:
			# Se acepta solucion vecina como nuevo punto de diseno
			solucion = sol_vecina
			temperatura_inicial = temperatura_inicial * c
			return solucion, temperatura_inicial
	elif (delta_z < 0 and opt == "min") or (delta_z >= 0 and opt == "max"):
		solucion = sol_vecina
		temperatura_inicial = temperatura_inicial * c
		return solucion, temperatura_inicial

	return solucion, temperatura_inicial


### Método para evaluar la función objetivo a partir de una lista de valores dados
def evaluar_funcion_objetivo(z, vals):
	exec('x1='+str(vals[0]))
	exec('x2='+str(vals[1]))
	eval_f = eval(z)
	return eval_f



### FUNCIÓN MAIN
def main():

	# 1. FORMULACION DEL PROBLEMA

	opt = "max"

	funcion_objetivo = "9*x1+24*x2+x1*x2-x1**2-6*x2**2"
	phi = "9*x1+24*x2+x1*x2-x1**2-6*x2**2-10*abs(x1+5*x2-30)"

	x_inf = 0
	x_sup = 30


	# 2. DEFINICIÓN DE VARIABLES

	# Rango variación de las variables
	ra = [-0.05,0.05]

	# Factor de reduccion de temperatura
	c = 0.8

	# Constante de Boltzman k
	k = 1

	# Constante penalización de la restricción q
	q = 10

	# Numero de iteraciones
	n = 10000

	# 3. HALLAR TEMPERATURA INICIAL

	# Soluciones al azar

	x1 = [random.uniform(x_inf, x_sup) for i in range(4)]
	x2 = [random.uniform(x_inf, x_sup) for i in range(4)]

	# Se evalua la funcion objetivo
	z = [evaluar_funcion_objetivo(phi, [x1[j] , x2[j]]) for j in range(len(x1))]

	# Ecuacíon temperatura inicial
	temperatura_inicial = sum(z)/len(z)


	# 4. SOLUCION INICIAL

	sol_inicial = [random.uniform(x_inf, x_sup) for i in range(2)]

	solucion = sol_inicial

	for i in range(n+1):

		# Evaluar funcion objetivo en la solución restandole restriccion penalizada
		z_inicial = evaluar_funcion_objetivo(phi, solucion)

		# Hallar solucíon vecina
		sol_vecina, z_vecina = hallar_solucion_vecina(solucion, phi, ra)

		# Verificar solucion mediante el criterio de metropolis si es necesario
		solucion, temperatura_inicial = criterio_metropolis(z_inicial, z_vecina, solucion, sol_vecina, temperatura_inicial, c, k, opt)

		
	# Se evalúa la función objetivo para obtener su valor en la ultima iteracion, para imprimirla
	z_print = evaluar_funcion_objetivo(funcion_objetivo, solucion)
	# Se calcula el valor de la restricción, para imprimirla la ultima iteración
	restriccion = solucion[0]+5*solucion[1]
	# Se imprimen los valores resultantes
	print("Z = "+str(z_print)+", X1 = "+str(solucion[0])+", X2 = "+str(solucion[1])+", Temperatura = "+str(temperatura_inicial)+", Restricción = "+str(restriccion)+", Iteración = "+str(i))

main()










