import numpy as np
import time
# Creamos dos vectores aleatorios
size = 10000
np.random.seed(0)
vec_1 = np.random.random(size)
vec_2 = np.random.random(size)
# Implementación del producto vectorial en Python
tic = time.process_time()
python_product = np.zeros((size, size))
for i in range(size):
    for j in range(size):
        python_product[i][j] = vec_1[i] * vec_2[j]
phyton_time = time.process_time() - tic
# Implementación del producto vectorial Numpy
tic = time.process_time()
numpy_product = np.outer(vec_1, vec_2)
numpy_time = time.process_time() - tic
# Evaluación de resultados
if (numpy_product == python_product).all():
    print('Los resultados son iguales')
else:
    print('Los resultados son diferentes')
print('Tiempo de Python', phyton_time)
print('Tiempo de Numpy', numpy_time)
print('Mejora con Numpy', phyton_time / numpy_time)