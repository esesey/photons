import numpy
from matrix import openmatrix


# Функция, выводящая статистику в консоль, сохраняющая файлы с матрицами
# и открывающая карты значений (matrix.py)
def open(
        MATRIX, Cylinder,
        Ma, Ms, n, n_out, g,
        amount, size, fix_rad, photo_count,
        max_radius, max_depth, max_cylinder
):
    numpy.savetxt('archive/matrix_ref ' + '[' + 'amount = ' + str(amount) + ', Ms = ' + str(Ms) + ', Ma = ' + str(Ma)
                  + ', n = ' + str(n) + ', n_out = ' + str(n_out) + ', g = ' + str(g)
                  + ', rad = ' + str(max_radius) + ', dep = ' + str(max_depth) + ']' + '.txt', MATRIX)
    numpy.savetxt('archive/matrix_dis ' + '[' + 'amount = ' + str(amount) + ', Ms = ' + str(Ms) + ', Ma = ' + str(Ma)
                  + ', n = ' + str(n) + ', n_out = ' + str(n_out) + ', g = ' + str(g)
                  + ', rad = ' + str(max_radius) + ', dep = ' + str(max_depth) + ']' + '.txt', Cylinder)
    print("Всего фотонов выпущено:", amount, " Фотонов отражено:", photo_count)
    openmatrix(size, max_cylinder, max_depth, max_radius, fix_rad, MATRIX, Cylinder)