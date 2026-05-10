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
    # Расчёт толщины среды
    total_thickness = sum(layer["thickness"] for layer in parameters)
    plot_size = min(total_thickness, max_depth)
    rad_size = min(total_thickness/2, max_radius)

    amountStr = 'amount = ' + str(amount)
    parametersStr = ', Ms = ' + get_field_values_string(parameters, "mu_s") +\
                    ', Ma = ' + get_field_values_string(parameters, "mu_a") +\
                    ', n = ' + get_field_values_string(parameters, "n") +\
                    ', n_out = ' + get_field_values_string(parameters, "n_out") +\
                    ', g = ' + get_field_values_string(parameters, "g")
    fixParametersStr = ', rad = ' + str(rad_size) + ', dep = ' + str(plot_size)

    # TODO: Исправить то, что при создании среды с 5 и более слоями, имя файла становится слишком длинным для сохранения
    #  Как вариант, можно сохранять спецификацию отдельным файлом, а в имени файла с матрицей давать ссылку на спецификацию.
    numpy.savetxt('archive/matrix_ref ' + '[' + amountStr + parametersStr + fixParametersStr + ']' + '.txt', MATRIX)
    numpy.savetxt('archive/matrix_dis ' + '[' + amountStr + parametersStr + fixParametersStr + ']' + '.txt', Cylinder)
    print("Всего фотонов выпущено:", amount, " Фотонов отражено:", photo_count)
    openmatrix(size, max_cylinder, plot_size, rad_size, fix_rad, MATRIX, Cylinder)

