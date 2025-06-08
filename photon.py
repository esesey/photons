from math import cos, sin, pi, log, sqrt, acos, asin, tan
from random import uniform
from numpy import sign


def photon_calculation(c, counter: int, get_matrix, log_at,
                       x_start: float, y_start: float, z_start: float,
                       Gx_start: float, Gy_start: float, Gz_start: float,
                       max_x: float, max_y: float, max_z: float,
                       parameters: list[dict[str, float]], layers: int):
    breakpoints = [0]
    strip_length = max_z // layers
    for layer in range(layers):
        breakpoints.append(strip_length * (layer + 1))
    breakpoints[len(breakpoints)-1] = max_z

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
    # Средняя длина свободного пробега
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
    # Предыдущие направляющие косинусы -- направляющие косинусы на старте
    current_Gx = Gx_start
    current_Gy = Gy_start
    current_Gz = Gz_start

    # Рассчёт длины свободного пробега на нулевом шаге
    length = length_average * (- log(1.0 - Epsilon))
    # Рассчёт новых координат на нулевом шаге
    x_next = x_previous + length * current_Gx
    y_next = y_previous + length * current_Gy
    z_next = z_previous + length * current_Gz

    # Отрисовка траектории на нулевом шаге, если это один из первых 100 фотонов
    if counter < 100:
        c.create_line(3 * x_previous, 3 * z_previous, 3 * x_next, 3 * z_next)

    # Цикл жизни одного фотона (1 итерация = 1 единичный рассеиватель)
    while P > P_min:
        Ms = parameters[currentLayer - 1]["mu_s"]
        Ma = parameters[currentLayer - 1]["mu_a"]
        n = parameters[currentLayer - 1]["n"]
        n_out_up = n_out_up_list[currentLayer - 1]
        n_out_down = n_out_down_list[currentLayer - 1]
        g = parameters[currentLayer - 1]["g"]
        # Пересчёт длины среднего свободного пробега на случай, если поменялись параметры среды
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

        # Рассчёт случайной длины свободного пробега
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
        x_next = x_previous + length * current_Gx
        y_next = y_previous + length * current_Gy
        z_next = z_previous + length * current_Gz

        # Отрисовка траектории на этом шаге, если это один из первых 100 фотонов
        if counter < 100:
            c.create_line(3 * x_previous, 3 * z_previous, 3 * x_next, 3 * z_next)

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

        # Проверка вылета или отражения по z-координате
        if z_next < minZ or z_next > maxZ:
            # Вытаскиваем угол к нормали по z-координате из направляющего косинуса
            Az = acos(current_Gz)

            # Если угол больше 90 градусов, обрезаем его
            if Az > (pi / 2):
                Az = Az - pi / 2

            if z_next < minZ:
                n_out = n_out_up
            if z_next > maxZ:
                n_out = n_out_down

            # Проверка на отражение по формулам Френеля
            if Az == 0:
                Frenel = ((n_out - n) / (n_out + n)) ** 2
            # Проверка на полное отражение
            elif (((n * sin(Az)) / n_out) >= 1):
                Frenel = 1.0
            else:
                # Переменная условного угла отражения
                Aref = asin((n * sin(Az)) / n_out)

                Frenel = 0.5 * (
                        (sin(Az - Aref) ** 2) /
                        (sin(Az + Aref) ** 2)
                        +
                        (tan(Az - Aref) ** 2) /
                        (tan(Az + Aref) ** 2)
                )
            # Случайное число от 0 до 1
            Epsilon = uniform(0, 1.0)
            # Число Френеля является вероятностью отражения, поэтому, чтобы определить,
            # произошло ли отражение, сравниваем число Френеля со случайным числом
            if Frenel < Epsilon:
                # Отражение не произошло, фотон вылетел, если он вылетел в обратную сторону,
                # фиксируем его данные с помощью функций.
                if z_next <= minZ:
                    if z_next <= 0:
                        get_matrix(x_next, y_next, P)
                        log_at(x_next, y_next, P, deepest_z)
                        # Возвращаем информацию, что фотон отразился
                        return ("get_back")
                    else:
                        # Пересчёт координат для преломления
                        y_next = (y_next - y_previous) * (
                                (minZ - z_previous) / (z_next - z_previous) + y_previous / (y_next - y_previous))
                        x_next = (x_next - x_previous) * (
                                (minZ - z_previous) / (z_next - z_previous) + x_previous / (x_next - x_previous))
                        z_next = minZ
                        minZ = breakpoints[currentLayer - 2]
                        maxZ = breakpoints[currentLayer - 1]
                        currentLayer -= 1
                else:
                    if z_next >= max_z:
                        break
                    else:
                        # Пересчёт координат для преломления
                        y_next = (y_next - y_previous) * (
                                (maxZ - z_previous) / (z_next - z_previous) + y_previous / (y_next - y_previous))
                        x_next = (x_next - x_previous) * (
                                (maxZ - z_previous) / (z_next - z_previous) + x_previous / (x_next - x_previous))
                        z_next = maxZ
                        minZ = breakpoints[currentLayer]
                        maxZ = breakpoints[currentLayer + 1]
                        currentLayer += 1
                # Пересчёт направляющего косинуса после преломления
                current_Gz = cos(asin(sin(Az) * n/n_out))
            else:
                # Отражение произошло
                # Пересчёт всех координат, в зависимости от того, с какой из сторон пришёл фотон
                if z_next < minZ:
                    y_next = (y_next - y_previous) * (
                            (minZ - z_previous) / (z_next - z_previous) + y_previous / (y_next - y_previous))
                    x_next = (x_next - x_previous) * (
                            (minZ - z_previous) / (z_next - z_previous) + x_previous / (x_next - x_previous))
                    z_next = minZ
                else:
                    y_next = (y_next - y_previous) * (
                            (maxZ - z_previous) / (z_next - z_previous) + y_previous / (y_next - y_previous))
                    x_next = (x_next - x_previous) * (
                            (maxZ - z_previous) / (z_next - z_previous) + x_previous / (x_next - x_previous))
                    z_next = maxZ

                # Отражаем старый угол
                current_Gz = - current_Gz

        # Если глубина прохода фотона больше, чем наибольшая, обновляем данные
        if z_next > deepest_z:
            deepest_z = z_next
    return ("get_out")