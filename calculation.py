import tkinter.messagebox
from tkinter import *
from tkinter import ttk
from math import sqrt,  floor

from photon import photon_calculation
from get_result import open
from relative_thickness import create_color_layer_presentation

# Основная функция, использует значения переменных, переданных из главного меню (main.py)
# Создаёт окно, на котором показываются траектории первых 100 пролетевших фотонов
# Расчитывает полёт всех фотонов, а так же заносит данные о глубине и весе в соответствующие списки
def drawing(parameters: list[dict[str, float]], amount: int,
            is_show_load: bool, thickness: float, max_depth: float, max_radius: float, fix_rad: float):
    # Инициализация списков обратного отражения, MATRIX для занесения значений веса,
    # Cylinder для значений зависимости глубины пролёта фотона от расстояния до центра пучка
    MATRIX = []
    Cylinder = []
    # Размеры дискретных ячеек в матрицах отражения и глубины
    size = 200
    max_cylinder = 100

    # Инициализация матриц
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

    # Константа размера холста
    canvas_max = 600

    # Коэффициент для перевода миллиметров в микрометры для большей площади координат.
    coord_coefficient = 1000

    def log_photon(x_next, y_next, x_start, y_start, P, deepest_z):
        # Расчёт индексов для внесения веса отражённого фотона
        def get_matrix_reflection_index(coord: float, start_coord: float):
            center: int = int(size / 2)
            distantion_coord: float = coord - start_coord
            distantion: float = distantion_coord/coord_coefficient
            width: float = min(thickness, (2 * max_radius))
            index: int = center + floor(distantion * size / width)
            return index

        index_1: int = get_matrix_reflection_index(x_next, x_start)
        index_2: int = get_matrix_reflection_index(y_next, y_start)
        if size > index_1 >= 0 and size > index_2 >= 0:
            MATRIX[index_1][index_2] += P

        # Расчёт индексов для внесения веса от глубины отражённого фотона
        # Индекс максимальной достигнутой глубины
        depth: float = min(thickness, max_depth)
        neared_depth_mm: float = deepest_z/coord_coefficient
        index_1: int = floor(max_cylinder * (neared_depth_mm / depth))
        # Индекс расстояния от центра
        x_distantion_sqr = (x_next - x_start) ** 2
        y_distantion_sqr = (y_next - y_start) ** 2
        ro_distantion_coord = sqrt(x_distantion_sqr + y_distantion_sqr)
        ro = ro_distantion_coord/coord_coefficient
        radius = min(thickness / 2, max_radius)
        index_2: int = floor(max_cylinder * (ro / radius))
        if index_1 < max_cylinder and index_2 < max_cylinder:
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
    c = Canvas(root, width=canvas_max, height=canvas_max, bg='white')
    c.pack()

    create_color_layer_presentation(parameters, c, canvas_max, canvas_max)

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
            
        result = photon_calculation(c, counter, log_photon, parameters, thickness, canvas_max, coord_coefficient)

        if (result == "get_back"):
            photo_count += 1

        # По окончанию обработки фотона, обновляем число прошедших обработку фотонов
        counter += 1
    # Зацикливание работы Tkinter, чтобы окно с данными не закрывалось без указания пользователя
    root.mainloop()
