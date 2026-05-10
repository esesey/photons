from math import cos, sin, pi, acos, asin, tan
from random import uniform


# Этот модуль посвящён расчётам при столкновении фотона с границей среды/слоя


# Расчёт числа Френеля
def calculate_Frenel(angle: float, n: float, n_out: float):
    if angle == 0:
        Frenel = ((n_out - n) / (n_out + n)) ** 2
    # Проверка на полное отражение
    elif (((n * sin(angle)) / n_out) >= 1):
        Frenel = 1.0
    else:
        # Переменная условного угла отражения
        Aref = asin((n * sin(angle)) / n_out)

        Frenel = 0.5 * (
                (sin(angle - Aref) ** 2) /
                (sin(angle + Aref) ** 2)
                +
                (tan(angle - Aref) ** 2) /
                (tan(angle + Aref) ** 2)
        )
    return Frenel


# Расчёт данных при отражении по оси z
def calculate_reflection_z(x_previous, y_previous, z_previous, x_next, y_next, z_next, minZ, maxZ, current_Gz):
    # Пересчёт всех координат, в зависимости от того, с какой из сторон пришёл фотон
    # print(f"Ф{f'0{counter}' if counter < 10 else counter}", "REFL_S                              ",
    #       f"z1={round(z_next, 1):<6.1f}", f"y1={round(y_next, 1):<6.1f}",
    #       f"x1={round(x_next, 1):<6.1f}", f"Gz={round(current_Gz, 3):<6.3f}",
    #       f"acos(Gz)={round(acos(current_Gz) * 57.3, 1):<5.1f}°")
    if z_next < minZ:
        y = (y_next - y_previous) * (
                (minZ - z_previous) / (z_next - z_previous) + y_previous / (y_next - y_previous))
        x = (x_next - x_previous) * (
                (minZ - z_previous) / (z_next - z_previous) + x_previous / (x_next - x_previous))
        z = minZ
    else:
        y = (y_next - y_previous) * (
                (maxZ - z_previous) / (z_next - z_previous) + y_previous / (y_next - y_previous))
        x = (x_next - x_previous) * (
                (maxZ - z_previous) / (z_next - z_previous) + x_previous / (x_next - x_previous))
        z = maxZ

    # Отражаем старый угол
    current_Gz = - current_Gz
    # print(f"Ф{f'0{counter}' if counter < 10 else counter}", "REFL_E                              ",
    #       f"z1={round(z_next, 1):<6.1f}", f"y1={round(y_next, 1):<6.1f}",
    #       f"x1={round(x_next, 1):<6.1f}", f"Gz={round(current_Gz, 3):<6.3f}",
    #       f"acos(Gz)={round(acos(current_Gz) * 57.3, 1):<5.1f}°")
    return [current_Gz, x, y, z]


# Расчёт данных при преломлении по оси z
def calculate_refraction_z(x_previous, y_previous, z_previous, x_next, y_next, z_next, minZ, maxZ, current_Gz, n, n_out, angle, breakpoints, currentLayer):
    # Пересчёт координат для преломления
    if z_next <= minZ:
        y = (y_next - y_previous) * (
                (minZ - z_previous) / (z_next - z_previous) + y_previous / (y_next - y_previous))
        x = (x_next - x_previous) * (
                (minZ - z_previous) / (z_next - z_previous) + x_previous / (x_next - x_previous))
        z = minZ
        minZ = breakpoints[currentLayer - 2]
        maxZ = breakpoints[currentLayer - 1]
        currentLayer -= 1
    else:
        y = (y_next - y_previous) * (
                (maxZ - z_previous) / (z_next - z_previous) + y_previous / (y_next - y_previous))
        x = (x_next - x_previous) * (
                (maxZ - z_previous) / (z_next - z_previous) + x_previous / (x_next - x_previous))
        z = maxZ
        minZ = breakpoints[currentLayer]
        maxZ = breakpoints[currentLayer + 1]
        currentLayer += 1
    # print(f"Ф{f'0{counter}' if counter < 10 else counter}", "REFR  ", f"z0={round(z_previous, 1):<6.1f}",
    #       f"y0={round(y_previous, 1):<6.1f}",
    #       f"x0={round(x_previous, 1):<6.1f}", f"z1={round(z_next, 1):<6.1f}",
    #       f"y1={round(y_next, 1):<6.1f}", f"x1={round(x_next, 1):<6.1f}", f"Gz={round(current_Gz, 3):<6.3f}",
    #       f"acos(Gz)={round(acos(current_Gz) * 57.3, 1):<5.1f}°",
    #       f"Gz1={round(cos(asin(sin(Az) * n / n_out)) * direction, 3):<6.3f}",
    #       f"acos(Gz1)={round(asin(sin(Az) * n / n_out) * 57.3, 1):<5.1f}°")
    # Пересчёт направляющего косинуса после преломления
    direction = -1 if current_Gz < 0 else 1
    current_Gz = cos(asin(sin(angle) * n / n_out)) * direction
    return [current_Gz, x, y, z, minZ, maxZ, currentLayer]


# Расчёт данных при столкновении с границей по оси z
def collide_handler_z(x_previous, y_previous, z_previous, x_next, y_next, z_next, minZ, maxZ, current_Gz, n,
                      n_out_up, n_out_down, log_photon, P, deepest_z, breakpoints, currentLayer, max_z, x_start, y_start):
    # Вытаскиваем угол к нормали по z-координате из направляющего косинуса
    Az = acos(current_Gz)

    # Если угол больше 90 градусов, берём угол меньшего размера
    if Az > (pi / 2):
        Az = pi - Az

    if z_next < minZ:
        n_out = n_out_up
    else:
        n_out = n_out_down

    # Проверка на отражение по формулам Френеля
    Frenel = calculate_Frenel(Az, n, n_out)
    # Случайное число от 0 до 1
    Epsilon = uniform(0, 1.0)
    # Число Френеля является вероятностью отражения, поэтому, чтобы определить,
    # произошло ли отражение, сравниваем число Френеля со случайным числом
    if Frenel < Epsilon:
        # Отражение не произошло, фотон вылетел, если он вылетел в обратную сторону,
        # фиксируем его данные с помощью функций.
        # print(f"Ф{f'0{counter}' if counter < 10 else counter}", "OUT   ", f"z0={round(z_previous, 1):<6.1f}",
        #       f"y0={round(y_previous, 1):<6.1f}",
        #       f"x0={round(x_previous, 1):<6.1f}", f"z1={round(z_next, 1):<6.1f}",
        #       f"y1={round(y_next, 1):<6.1f}", f"x1={round(x_next, 1):<6.1f}", f"Gz={round(current_Gz, 3):<6.3f}",
        #       f"acos(Gz)={round(acos(current_Gz) * 57.3, 1):<5.1f}°")
        if z_next <= minZ:
            if z_next <= 0:
                log_photon(x_next, y_next, x_start, y_start, P, deepest_z)
                # Возвращаем информацию, что фотон вылетел назад
                return ("get_back", [current_Gz, x_next, y_next, z_next, minZ, maxZ, currentLayer])
            else:
                [current_Gz, x_next, y_next, z_next, minZ, maxZ, currentLayer] = calculate_refraction_z(
                    x_previous, y_previous, z_previous, x_next, y_next, z_next, minZ, maxZ, current_Gz, n,
                    n_out, Az, breakpoints, currentLayer)
        else:
            if z_next >= max_z:
                return ["skip", [current_Gz, x_next, y_next, z_next, minZ, maxZ, currentLayer]]
            else:
                [current_Gz, x_next, y_next, z_next, minZ, maxZ, currentLayer] = calculate_refraction_z(
                    x_previous, y_previous, z_previous, x_next, y_next, z_next, minZ, maxZ, current_Gz, n,
                    n_out, Az, breakpoints, currentLayer)

    else:
        # Отражение произошло
        [current_Gz, x_next, y_next, z_next] = calculate_reflection_z(x_previous, y_previous, z_previous,
                                                                      x_next, y_next, z_next, minZ, maxZ,
                                                                      current_Gz)
    return ["continue", [current_Gz, x_next, y_next, z_next, minZ, maxZ, currentLayer]]
