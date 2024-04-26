import tkinter.messagebox
from tkinter import *
from tkinter import ttk
from random import uniform
from math import cos, sin, pi, log, sqrt, acos, asin, tan, floor

import numpy
from numpy import sign
from matrix import openmatrix

# Основная функция, использует значения переменных, переданных из главного меню (main.py)
# Создаёт окно, на котором показываются траектории первых 100 пролетевших фотонов
# Рассчитывает полёт всех фотонов, а так же заносит данные о глубине и весе в соответствующие списки
def drawing(Ms, Ma, n, n_out, g, amount, size, is_show_load):
    # Инициализация списков обратного отражения, MATRIX для занесения значений веса,
    # Cylinder для значений зависимости глубины пролёта фотона от расстояния до центра пучка
    MATRIX = []
    Cylinder = []
    # Рассчёт длины ребра циллиндра в зависимости от размера матрицы отражения
    # max_cylinder = floor(size/2)
    max_cylinder = 100

    # Задание размера списков и заполнение пустыми значениями
    for i in range(size):
        i = []
        MATRIX.append(i)
        for j in range(size):
            i.append(0)
    for i in range(max_cylinder):
        i = []
        Cylinder.append(i)
        for j in range(max_cylinder):
            i.append(0)

    # Значения максимальных координат по x,y и z
    max_x = 200.0
    max_y = 200.0
    max_z = 200.0

    # Значения высоты и радиуса циллиндра (сейчас используется кубический цилиндр)
    max_depth = 10.0
    max_radius = 10.0

    # Начальные x, y и z
    x_start = 100.0
    y_start = 100.0
    z_start = 0.0
    # Начальные значения направляющих косинусов
    Gx_start = 0.0
    Gy_start = 0.0
    Gz_start = 1.0

    # Функция, заносящая вес отражённых фотонов в список MATRIX
    def get_matrix(x_next, max_x, y_next, max_y, P):
        index_1: int = int(size/2) + floor((x_next - x_start) * size / (2 * max_radius))
        index_2: int = int(size/2) + floor((y_next - y_start) * size / (2 * max_radius))
        if (index_1 < size and index_2 < size and index_1 > 0 and index_2 > 0):
            MATRIX[index_1][index_2] += P

    # Функция, заполняющая список Cylinder
    def log_at(x, y, max_d, max_r, P, deepest_z):
        index_1: int = floor(max_cylinder * (deepest_z / max_d))
        index_2: int = floor(max_cylinder * (sqrt(abs(x - x_start) * abs(x - x_start) +
                                                  abs(y - y_start) * abs(y - y_start)) / max_r))
        if (index_1 < max_cylinder and index_2 < max_cylinder):
            Cylinder[index_1][index_2] += P
            # Отладка:
            # print("Фотон зафиксирован в радиусе, индекс глубины (1):", index_1, "Индекс дальности (2)", index_2)
        # else:
            # Отладка:
            # print("Не зафиксирован в радиусе")

    # Функция, выводящая статистику в консоль и открывающая карты значений (matrix.py)
    def open():
        openmatrix(size, max_cylinder, MATRIX, Cylinder)
        numpy.savetxt('matrix1.txt', MATRIX)
        numpy.savetxt('matrix2.txt', Cylinder)
        print("Всего фотонов выпущено:", amount, " Фотонов отражено:", photo_count)

    # Количество прошедших фотонов
    counter = 0
    # Количество отражённых фотонов
    photo_count = 0

    # Средняя длина свободного пробега
    lenght_average = 1.0/(Ms + Ma)

    # Текущий вес фотона
    P = 1.0
    # Изменение веса фотона в единичном рассеивателе
    P_diff = (P * Ma)/(Ms + Ma)
    # Минимальный вес фотона до поглощения
    P_min = 0.00001 * P

    # Если разрешён показ загрузки, создаём окно загрузки
    if (is_show_load):
        # Cоздание окна прогресса выполнения программы
        loading = Tk()
        loading.title('Загрузка')
        loading.geometry("250x100")
        load_frame = Frame(loading)

        # Создание прогресс-бара программы
        load_pr = ttk.Progressbar(load_frame, orient="horizontal", length=150, maximum=amount)
        load_pr.grid(row=0, column=0, pady=5)

        # Cоздание строки, выводящей прогресс в процентах
        percent_text = Label(load_frame, text="Прогресс: ")
        percent_text.grid(row=1, column=0)
        percent_number = Label(load_frame)
        percent_number.grid(row=1, column=1)
        percent_post_text = Label(load_frame, text="%")
        percent_post_text.grid(row=1, column=2)

        # Создание строки, выводящей число выпущенных фотонов
        count_text = Label(load_frame, text="Фотонов выпущено: ")
        count_text.grid(row=2, column=0)
        count_number = Label(load_frame)
        count_number.grid(row=2, column=1)

        # Создание строки, выводящей число отражённых назад фотонов
        ref_count_text = Label(load_frame, text="Фотонов отражено назад: ")
        ref_count_text.grid(row=3, column=0)
        ref_count_number = Label(load_frame)
        ref_count_number.grid(row=3, column=1)

        # Компиляция рамки загрузки и её прилипание к верхней границе
        load_frame.pack(anchor="n")

    # Создание главного окна и холста с траекториями
    root = Tk()
    root.title('Траектории')
    c = Canvas(root, width=600, height=600, bg='white')
    c.pack()

    # Создание рамки для кнопок
    dr_frame = Frame(root)

    # Cоздание кнопки, вызывающей функцию open
    show_button = Button(dr_frame, text="Открыть матрицу отражения", command=open)
    show_button.grid(row=0, column=1, padx=3, pady=3)
    # Cоздание кнопки, закрывающей текущее окно с траекториями
    quit_pic_button = Button(dr_frame, text="Закрыть картинку", command=root.destroy)
    quit_pic_button.grid(row=0, column=2, padx=3, pady=3)

    # Компиляция рамки для кнопок и её прилипание к верхней границе
    dr_frame.pack(anchor="n")

    # Основной цикл рассчёта полёта фотонов (1 итерация = 1 фотон)
    while counter < amount:
        # Зануление наибольшей глубины пролёта фотона
        deepest_z = 0.0
        # Начальный вес фотона
        P = 1.0
        # Случайное число от 0 до 1
        Epsilon = uniform(0, 1.0)

        # Обновление прогресса загрузки происходит только если разрешён показ загрузки
        # Компилятор Питона выдаёт WARN из-за того, что инициализация параметров
        # окна загрузки скрыта под таким же условием
        if(is_show_load and (counter%(amount/1000)==0)):
            # Обновление прогресса для окна загрузки
            load_pr['value'] = counter
            percent_number.configure(text=int(counter * 100 / amount))
            count_number.configure(text=counter)
            ref_count_number.configure(text=photo_count)
            loading.update()

        # По достижению загрузки за один фотон до конца, числа становятся конечными
        if (is_show_load and counter==(amount-1)):
            load_pr['value'] = amount
            percent_number.configure(text=100)
            count_number.configure(text=amount)
            ref_count_number.configure(text=photo_count)
            loading.update()

        # За один фотон до конца высвечивается оповещение о завершении работы
        if (counter==(amount-1)):
            tkinter.messagebox.showinfo(title="Готово!", message="Все фотоны выпущены, можно просматривать результаты")

        # Предыдущие координаты фотона -- координаты старта
        x_previous = x_start
        y_previous = y_start
        z_previous = z_start
        # Предыдущие направляющие косинусы -- направляющие косинусы на старте
        current_Gx = Gx_start
        current_Gy = Gy_start
        current_Gz = Gz_start
        # Булевые значения вылета по одной из координат
        out_x = False
        out_y = False
        out_z = False

        # Рассчёт длины свободного пробега на нулевом шаге
        lenght = lenght_average * (- log(1.0 - Epsilon))
        # Рассчёт новых координат на нулевом шаге
        x_next = x_previous + lenght * current_Gx
        y_next = y_previous + lenght * current_Gy
        z_next = z_previous + lenght * current_Gz

        # Отрисовка траектории на нулевом шаге, если это один из первых 100 фотонов
        if counter < 100:
            c.create_line(3*x_previous, 3*z_previous, 3*x_next, 3*z_next)

        # Цикл жизни одного фотона (1 итерация = 1 единичный рассеиватель)
        while not (out_y or out_x or out_z) and P > P_min:
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
            lenght = lenght_average * (- log(1.0 - Epsilon))

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
                current_Gx = (sin(Theta) * (Gx_previous * Gz_previous * cos(Phi) - Gy_previous * sin(Phi))) /\
                             sqrt(1.0 - Gz_previous * Gz_previous) + Gx_previous * cos(Theta)
                current_Gy = (sin(Theta) * (Gy_previous * Gz_previous * cos(Phi) + Gx_previous * sin(Phi))) /\
                             sqrt(1.0 - Gz_previous * Gz_previous) + Gy_previous * cos(Theta)
                current_Gz = -sin(Theta) * cos(Phi) * sqrt(1.0 - Gz_previous * Gz_previous) + Gz_previous * cos(Theta)

            # Передача старых координат в соответствующие переменные и пересчёт новых
            x_previous = x_next
            y_previous = y_next
            z_previous = z_next
            x_next = x_previous + lenght * current_Gx
            y_next = y_previous + lenght * current_Gy
            z_next = z_previous + lenght * current_Gz

            # Отрисовка траектории на этом шаге, если это один из первых 100 фотонов
            if counter < 100:
                c.create_line(3 * x_previous, 3 * z_previous, 3 * x_next, 3 * z_next)

            # Рассеяние: фотон теряет часть "веса"
            P = P - P_diff

            # Проверка вылета по y-координате
            if y_next < 0 or y_next > max_y:
                out_y = True
                break

            # Проверка вылета по x-координате
            if x_next < 0 or x_next > max_x:
                out_x = True
                break

            # Проверка вылета или отражения по z-координате
            if z_next < 0 or z_next > max_z:
                # Вытаскиваем угол к нормали по z-координате из направляющего косинуса
                Az = acos(current_Gz)

                # Если угол больше 90 градусов, обрезаем его
                if Az > (pi/2):
                    Az = Az - pi/2

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
                # Число Френеля является вероятностью отражения, поэтому, чтобы определить
                # произошло ли отражение, сравниваем число Френеля со случайным числом
                if Frenel < Epsilon:
                    # Отражение не произошло, фотон вылетел, если он вылетел в обратную сторону,
                    # фиксируем его данные с помощью функций.
                    if z_next <= 0:
                        get_matrix(x_next, max_x, y_next, max_y, P)
                        log_at(x_next, y_next, max_depth, max_radius, P, deepest_z)
                        # Добавляем один к счётчику отразившихся назад фотонов
                        photo_count += 1
                        # Отладка:
                        # print("Фотон №", photo_count, "прилетел в точку: (", x_next, ";", y_next, ") Глубина: ", deepest_z)
                        out_z = True
                        break
                    else:
                        out_z = True
                        break
                else:
                    # Отражение произошло
                    # Пересчёт всех координат, в зависимости от того, с какой из сторон пришёл фотон
                    if z_next < 0:
                        y_next = (y_next - y_previous) * (
                                (- z_previous) / (z_next - z_previous) + y_previous / (y_next - y_previous))
                        x_next = (x_next - x_previous) * (
                                (- z_previous) / (z_next - z_previous) + x_previous / (x_next - x_previous))
                        z_next = 0
                    else:
                        y_next = (y_next - y_previous) * (
                                (max_z - z_previous) / (z_next - z_previous) + y_previous / (y_next - y_previous))
                        x_next = (x_next - x_previous) * (
                                (max_z - z_previous) / (z_next - z_previous) + x_previous / (x_next - x_previous))
                        z_next = max_z

                    # Отражаем старый угол (поскольку среда однослойная, мы можем сделать это так)
                    current_Gz = - current_Gz

            # Если глубина прохода фотона больше, чем наибольшая, обновляем данные
            if z_next > deepest_z:
                deepest_z = z_next

        # По окончанию обработки фотона, обновляем число прошедших обработку фотонов
        counter = counter + 1

    # Зацикливание работы Tkinter, чтобы окно с данными не закрывалось без указания пользователя
    root.mainloop()
