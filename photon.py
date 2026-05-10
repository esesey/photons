from math import cos, sin, pi, log, sqrt, acos
from random import uniform
from numpy import sign

from border_collide import collide_handler_z
from relative_thickness import get_breakpoints


# Этот модуль посвящён жизненному циклу одного фотона


def photon_calculation(c, counter: int, log_photon,
                       parameters: list[dict[str, float]], thickness, canvas_max, coord_coefficient):

    # Начальные значения направляющих косинусов
    Gx_start = 0.0
    Gy_start = 0.0
    Gz_start = 1.0

    # Толщина среды является максимальным значением по одной из осей, а поскольку среда рассматривается в виде куба,
    # каждая из осей будет иметь именно такое максимальное значение.
    max_x = max_y = max_z = thickness * coord_coefficient
    x_start = max_x / 2
    y_start = max_y / 2
    z_start = 0.0

    # Коэффициент для визуального представления траекторий на холсте.
    canvas_coefficient = canvas_max/(thickness * coord_coefficient)

    # Брейкпоинты - список из координат по оси z, по которым находится пересечение слоёв среды
    breakpoints = get_breakpoints(parameters, max_z)

    n_out_up_list = [
        parameters[0]["n_out"] if i == 0 else parameters[i - 1]["n"]
        for i in range(len(parameters))
    ]
    n_out_down_list = [
        parameters[i]["n_out"] if i == len(parameters) - 1 else parameters[i + 1]["n"]
        for i in range(len(parameters))
    ]

    minZ = breakpoints[0]
    maxZ = breakpoints[1]
    currentLayer = 1

    Ms = parameters[0]["mu_s"]
    Ma = parameters[0]["mu_a"]

    # Зануление наибольшей глубины пролёта фотона
    deepest_z = 0.0
    # Средняя длина свободного пробега (в мм)
    length_average = 1.0 / (Ms + Ma)

    # Текущий вес фотона
    P = 1.0
    # Минимальный вес фотона до поглощения
    P_min = 0.00001 * P
    # Случайное число от 0 до 1
    Epsilon = uniform(0, 1.0)

    # Предыдущие координаты фотона -- координаты старта
    x_previous = x_start
    y_previous = y_start
    z_previous = z_start
    # Текущие направляющие косинусы -- направляющие косинусы на старте
    current_Gx = Gx_start
    current_Gy = Gy_start
    current_Gz = Gz_start

    # Рассчёт длины свободного пробега на нулевом шаге (в мм)
    length = length_average * (- log(1.0 - Epsilon))
    # Рассчёт новых координат на нулевом шаге
    x_next = x_previous + length * current_Gx * coord_coefficient
    y_next = y_previous + length * current_Gy * coord_coefficient
    z_next = z_previous + length * current_Gz * coord_coefficient

    # Отрисовка траектории на нулевом шаге, если это один из первых 100 фотонов
    if counter < 100:
        c.create_line(canvas_coefficient * x_previous,
                      canvas_coefficient * z_previous,
                      canvas_coefficient * x_next,
                      canvas_coefficient * z_next)

    # Цикл жизни одного фотона (1 итерация = 1 единичный рассеиватель)
    while P > P_min:
        Ms = parameters[currentLayer - 1]["mu_s"]
        Ma = parameters[currentLayer - 1]["mu_a"]
        n = parameters[currentLayer - 1]["n"]
        n_out_up = n_out_up_list[currentLayer - 1]
        n_out_down = n_out_down_list[currentLayer - 1]
        g = parameters[currentLayer - 1]["g"]
        # Пересчёт длины среднего свободного пробега на случай, если поменялись параметры среды (в мм)
        length_average = 1.0 / (Ms + Ma)
        # Изменение веса фотона в единичном рассеивателе
        P_diff = (P * Ma) / (Ms + Ma)
        # Присвоение значения переменной Тета в зависимости от параметра анизотропии и случайного числа от 0 до 1
        Epsilon = uniform(0, 1.0)
        if g == 0:
            Theta = acos(2 * Epsilon - 1)
        elif g > 0:
            Theta = acos((1 / (2 * g)) * (1 + g * g - ((1 - g * g) / (1 - g + 2 * g * Epsilon)) ** 2))
        else:
            g = abs(g)
            Theta = acos((1 / (2 * g)) * (1 + g * g - ((1 - g * g) / (1 - g + 2 * g * Epsilon)) ** 2))
        # Присвоение значения переменной Фи случайно от 0 до 2*пи
        Phi = uniform(0, 2 * pi)

        # Рассчёт случайной длины свободного пробега (в мм)
        Epsilon = uniform(0, 1.0)
        length = length_average * (- log(1.0 - Epsilon))

        # Передача значений направляющих косинусов прошлого шага в соответствующие переменные
        Gx_previous = current_Gx
        Gy_previous = current_Gy
        Gz_previous = current_Gz
        # Пересчёт нынешних направляющих косинусов по формуле
        if abs(Gz_previous) > 0.99999:
            current_Gx = cos(Phi) * sin(Theta)
            current_Gy = sin(Phi) * sin(Theta)
            current_Gz = sign(Gz_previous) * cos(Theta)
        else:
            current_Gx = (sin(Theta) * (Gx_previous * Gz_previous * cos(Phi) - Gy_previous * sin(Phi))) / \
                         sqrt(1.0 - Gz_previous * Gz_previous) + Gx_previous * cos(Theta)
            current_Gy = (sin(Theta) * (Gy_previous * Gz_previous * cos(Phi) + Gx_previous * sin(Phi))) / \
                         sqrt(1.0 - Gz_previous * Gz_previous) + Gy_previous * cos(Theta)
            current_Gz = -sin(Theta) * cos(Phi) * sqrt(1.0 - Gz_previous * Gz_previous) + Gz_previous * cos(Theta)

        # Передача старых координат в соответствующие переменные и пересчёт новых
        x_previous = x_next
        y_previous = y_next
        z_previous = z_next
        x_next = x_previous + length * current_Gx * coord_coefficient
        y_next = y_previous + length * current_Gy * coord_coefficient
        z_next = z_previous + length * current_Gz * coord_coefficient

        # Отрисовка траектории на этом шаге, если это один из первых 100 фотонов
        if counter < 100:
            c.create_line(canvas_coefficient * x_previous,
                          canvas_coefficient * z_previous,
                          canvas_coefficient * x_next,
                          canvas_coefficient * z_next)

        # Рассеяние: фотон теряет часть "веса"
        P = P - P_diff
        # fix: при больших Ma фотон мог потерять веса больше, чем имеет
        if P < 0:
            break

        # Проверка вылета по y-координате
        if y_next < 0 or y_next > max_y:
            break

        # Проверка вылета по x-координате
        if x_next < 0 or x_next > max_x:
            break

        # Проверка вылета, преломления или отражения по z-координате
        if z_next < minZ or z_next > maxZ:
            [action, [current_Gz, x_next, y_next, z_next, minZ, maxZ, currentLayer]] = collide_handler_z(x_previous,
                                                                                                         y_previous,
                                                                                                         z_previous,
                                                                                                         x_next, y_next,
                                                                                                         z_next, minZ,
                                                                                                         maxZ,
                                                                                                         current_Gz, n,
                                                                                                         n_out_up,
                                                                                                         n_out_down,
                                                                                                         log_photon, P,
                                                                                                         deepest_z,
                                                                                                         breakpoints,
                                                                                                         currentLayer,
                                                                                                         max_z, x_start,
                                                                                                         y_start)
            if action == "get_back":
                return "get_back"
            elif action == "skip":
                break

        # Если глубина прохода фотона больше, чем наибольшая, обновляем данные
        if z_next > deepest_z:
            deepest_z = z_next
    return ("get_out")