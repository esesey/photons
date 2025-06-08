import colorsys
import tkinter.messagebox
from tkinter import *
from tkinter import ttk
from math import sqrt,  floor

from photon import photon_calculation
from get_result import open


# Основная функция, использует значения переменных, переданных из главного меню (main.py)
# Создаёт окно, на котором показываются траектории первых 100 пролетевших фотонов
# Рассчитывает полёт всех фотонов, а так же заносит данные о глубине и весе в соответствующие списки
def drawing(parameters: list[dict[str, float]], amount: int,
            is_show_load: bool, max_deep_int: int, max_rad_int: int, fix_rad: float, layers: int):
    # Инициализация списков обратного отражения, MATRIX для занесения значений веса,
    # Cylinder для значений зависимости глубины пролёта фотона от расстояния до центра пучка
    MATRIX = []
    Cylinder = []
    # Рассчёт длины радиуса циллиндра в зависимости от размера матрицы отражения
    # max_cylinder = floor(size/2)
    size = 200
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

    # Значения высоты и радиуса циллиндра, переданные параметрами
    max_depth = float(max_deep_int)
    max_radius = float(max_rad_int)

    # Начальные x, y и z
    x_start = 100.0
    y_start = 100.0
    z_start = 0.0
    # Начальные значения направляющих косинусов
    Gx_start = 0.0
    Gy_start = 0.0
    Gz_start = 1.0

    # Функция, заносящая вес отражённых фотонов в список MATRIX
    def get_matrix(x_next, y_next, P):
        index_1: int = int(size/2) + floor((x_next - x_start) * size / (2 * max_radius))
        index_2: int = int(size/2) + floor((y_next - y_start) * size / (2 * max_radius))
        if (index_1 < size and index_2 < size and index_1 > 0 and index_2 > 0):
            MATRIX[index_1][index_2] += P

    # Функция, заполняющая список Cylinder
    def log_at(x, y, P, deepest_z):
        index_1: int = floor(max_cylinder * (deepest_z / max_depth))
        index_2: int = floor(max_cylinder * (sqrt(abs(x - x_start) * abs(x - x_start) +
                                                  abs(y - y_start) * abs(y - y_start)) / max_radius))
        if (index_1 < max_cylinder and index_2 < max_cylinder):
            Cylinder[index_1][index_2] += P

    # Количество прошедших фотонов
    counter = 0
    # Количество отражённых фотонов
    photo_count = 0

    # Если разрешён показ загрузки, создаём окно загрузки
    if (is_show_load):
        # Создание окна прогресса выполнения программы
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

    def loading_update(counter, amount, photo_count):
        if (not is_show_load): return
        if (counter % (amount / 1000) == 0):
            # Обновление прогресса для окна загрузки
            load_pr['value'] = counter
            percent_number.configure(text=int(counter * 100 / amount))
            count_number.configure(text=counter)
            ref_count_number.configure(text=photo_count)
            loading.update()
        # По достижению загрузки за один фотон до конца, числа становятся конечными
        if (counter == (amount - 1)):
            load_pr['value'] = amount
            percent_number.configure(text=100)
            count_number.configure(text=amount)
            ref_count_number.configure(text=photo_count)
            loading.update()

    # Создание главного окна и холста с траекториями
    root = Tk()
    root.title('Траектории')
    c = Canvas(root, width=600, height=600, bg='white')
    c.pack()

    strip_height = 600 // layers

    # Красим в разные цвета каждый слой среды
    for layer in range(layers):
        hue = layer / layers
        # Преобразование HSV в RGB
        r, g, b = colorsys.hsv_to_rgb(hue, 0.15, 1.0)

        # Конвертация в HEX
        hex_color = "#{:02x}{:02x}{:02x}".format(
            int(r * 255),
            int(g * 255),
            int(b * 255)
        )
        c.create_rectangle(0, layer * strip_height, 600, (layer + 1) * strip_height, fill=hex_color, outline='')

    # Создание рамки для кнопок
    dr_frame = Frame(root)

    # Создание кнопки, вызывающей функцию open
    show_button = Button(dr_frame, text="Открыть матрицу отражения", command=lambda: open(
        MATRIX, Cylinder,
        parameters,
        amount, size, fix_rad, photo_count,
        max_radius, max_depth, max_cylinder
    ))
    show_button.grid(row=0, column=1, padx=3, pady=3)
    # Создание кнопки, закрывающей текущее окно с траекториями
    quit_pic_button = Button(dr_frame, text="Закрыть картинку", command=root.destroy)
    quit_pic_button.grid(row=0, column=2, padx=3, pady=3)

    # Компиляция рамки для кнопок и её прилипание к верхней границе
    dr_frame.pack(anchor="n")

    # Основной цикл рассчёта полёта фотонов (1 итерация = 1 фотон)
    while counter < amount:
        # Обновление прогресса загрузки происходит только если разрешён показ загрузки
        loading_update(counter, amount, photo_count)
        # За один фотон до конца высвечивается оповещение о завершении работы
        if (counter == (amount - 1)):
            tkinter.messagebox.showinfo(title="Готово!",
                message="Все фотоны выпущены, можно просматривать результаты")
            
        result = photon_calculation(
            c, counter, get_matrix, log_at,
            x_start, y_start, z_start,
            Gx_start, Gy_start, Gz_start,
            max_x, max_y, max_z,
            parameters, layers
        )

        if (result == "get_back"):
            photo_count += 1

        # По окончанию обработки фотона, обновляем число прошедших обработку фотонов
        counter += 1

    # Зацикливание работы Tkinter, чтобы окно с данными не закрывалось без указания пользователя
    root.mainloop()
