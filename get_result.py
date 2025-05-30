import numpy
from matrix import openmatrix


def get_field_values_string(data: list[dict[str, float]], field: str) -> str:
    values = [item[field] for item in data if field in item]
    values_str = ", ".join(str(v) for v in values)
    return f"({values_str})"

# Функция, выводящая статистику в консоль, сохраняющая файлы с матрицами
# и открывающая карты значений (matrix.py)
def open(
        MATRIX, Cylinder,
        parameters: list[dict[str, float]],
        amount, size, fix_rad, photo_count,
        max_radius, max_depth, max_cylinder
):

    amountStr = 'amount = ' + str(amount)
    parametersStr = ', Ms = ' + get_field_values_string(parameters, "mu_s") +\
                    ', Ma = ' + get_field_values_string(parameters, "mu_a") +\
                    ', n = ' + get_field_values_string(parameters, "n") +\
                    ', n_out = ' + get_field_values_string(parameters, "n_out") +\
                    ', g = ' + get_field_values_string(parameters, "g")
    fixParametersStr = ', rad = ' + str(max_radius) + ', dep = ' + str(max_depth)

    numpy.savetxt('archive/matrix_ref ' + '[' + amountStr + parametersStr + fixParametersStr + ']' + '.txt', MATRIX)
    numpy.savetxt('archive/matrix_dis ' + '[' + amountStr + parametersStr + fixParametersStr + ']' + '.txt', Cylinder)
    print("Всего фотонов выпущено:", amount, " Фотонов отражено:", photo_count)
    openmatrix(size, max_cylinder, max_depth, max_radius, fix_rad, MATRIX, Cylinder)