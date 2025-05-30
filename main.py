from tkinter import *
from tkinter import ttk
from calculation import drawing
from idlelib.tooltip import Hovertip
from tkinter.filedialog import askopenfile
from matrix_rebuild import rebuild

# Создание стартового окна и рамки для кнопок
window = Tk()
window.title("Панель управления")
window.geometry("1024x800")
buttonFrame = Frame(window)

# Массив для хранения виджетов слоёв
widgets = []
# Глобальная переменная, обозначающая количество слоёв
layers = 0

# Создание панели ввода параметра количества выпускаемых фотонов
amount = IntVar(value=100000)
amount_label = Label(buttonFrame, text="Кол-во выпускаемых фотонов")
amount_label.grid(row=3, column=1)
amount_take = Entry(buttonFrame, textvariable=amount, width=10)
amount_take.grid(row=4, column=1, padx=3, pady=3)
amount_tip = Hovertip(amount_take, "от 1 до 100m")

# Создание панели ввода параметра максимальной глубины
max_d = DoubleVar(value=20)
max_d_label = Label(buttonFrame, text="Максимальная глубина")
max_d_label.grid(row=27, column=1)
max_d_take = Entry(buttonFrame, textvariable=max_d, width=10)
max_d_take.grid(row=28, column=1, padx=3, pady=3)
max_d_tip = Hovertip(max_d_take, "от 1 до 200")

# Создание панели ввода параметра максимального радиуса
max_r = DoubleVar(value=20)
max_r_label = Label(buttonFrame, text="Максимальный радиус")
max_r_label.grid(row=29, column=1)
max_r_take = Entry(buttonFrame, textvariable=max_r, width=10)
max_r_take.grid(row=30, column=1, padx=3, pady=3)
max_r_tip = Hovertip(max_r_take, "от 1 до 100")

# Создание панели ввода радиуса для фиксирования
fix_r = DoubleVar(value=4.9)
fix_r_label = Label(buttonFrame, text="Зафиксировать радиус")
fix_r_label.grid(row=31, column=1)
fix_r_take = Entry(buttonFrame, textvariable=fix_r, width=10)
fix_r_take.grid(row=32, column=1, padx=3, pady=3)
fix_r_tip = Hovertip(fix_r_take, "от 1 до 100")

# Создание кнопки выбора, показывать ли окно с прогрессом выполнения программы
# Может быть полезно при разных ситуациях, т.к. прогресс содержит
# Интересную информацию, но отнимает производительность
is_show_load = BooleanVar(value=True)
is_show_load_check = ttk.Checkbutton(buttonFrame, variable=is_show_load, text="Показывать прогресс")
is_show_load_check.grid(row=2, column=1)
is_show_load_tip = Hovertip(is_show_load_check, 'Окно прогресса содержит много полезной информации, \n'
                                                'однако существенно снижает производительность')


# Функция, переносящая введённые параметры в файл calculation.py
def start():
    global widgets
    parameters = []
    for widget in widgets:
        if widget["active"]:
            parameters.append({
                "mu_s": float(widget["mu_s"]["mu_s_take"].get()),
                "mu_a": float(widget["mu_a"]["mu_a_take"].get()),
                "n": float(widget["n"]["n_take"].get()),
                "n_out": float(widget["n_out"]["n_out_take"].get()),
                "g": float(widget["g"]["g_take"].get()),
            })

    drawing(parameters, int(amount_take.get()), bool(is_show_load.get()),
            int(max_d.get()), int(max_r_take.get()), float(fix_r_take.get()), layers)

def takeFromFile():
    file = askopenfile(parent=buttonFrame, filetypes=[('Text Files', '*.txt')])
    if file is not None:
        content = file.read()
        name = file.name
        rebuild(name, content, float(fix_r_take.get()))


def deleteLayer(index):
    global widgets, layers
    for widget_info in widgets:
        if widget_info["index"] == index and widget_info["active"]:
            widget_info["active"] = False
            widget_info["mu_s"]["mu_s_label"].destroy()
            widget_info["mu_s"]["mu_s_take"].destroy()
            widget_info["mu_a"]["mu_a_label"].destroy()
            widget_info["mu_a"]["mu_a_take"].destroy()
            widget_info["n"]["n_label"].destroy()
            widget_info["n"]["n_take"].destroy()
            widget_info["n_out"]["n_out_label"].destroy()
            widget_info["n_out"]["n_out_take"].destroy()
            widget_info["g"]["g_label"].destroy()
            widget_info["g"]["g_take"].destroy()
            widget_info["buttons"]["button_del"].destroy()
            widget_info["buttons"]["button_add"].destroy()
            layers -= 1
            break

def addLayer():
    global layers, widgets

    index = layers + 1
    # Создание панели ввода параметра коэффициента рассеяния среды
    Ms = DoubleVar(value=10.0)
    mu_s_label = Label(buttonFrame, text="μs (Коэфф. рассеяния)")
    mu_s_label.grid(row=5, padx=3, column=index)
    mu_s_take = Entry(buttonFrame, textvariable=Ms, width=10)
    mu_s_take.grid(row=6, column=index, padx=3, pady=3)
    mu_s_tip = Hovertip(mu_s_take, "от ~0 до 20")

    # Создание панели ввода параметра коэффициента поглощения среды
    Ma = DoubleVar(value=0.002)
    mu_a_label = Label(buttonFrame, text="μa (Коэфф. поглощения)")
    mu_a_label.grid(row=7, padx=3, column=index)
    mu_a_take = Entry(buttonFrame, textvariable=Ma, width=10)
    mu_a_take.grid(row=8, column=index, padx=3, pady=3)
    mu_a_tip = Hovertip(mu_a_take, "от ~0 до 0.5")

    # Создание панели ввода параметра коэффициента преломления среды
    n = DoubleVar(value=1.37)
    n_label = Label(buttonFrame, text="n (Коэфф. преломления среды)")
    n_label.grid(row=9, padx=3, column=index)
    n_take = Entry(buttonFrame, textvariable=n, width=10)
    n_take.grid(row=10, column=index, padx=3, pady=3)
    n_tip = Hovertip(n_take, "от 1 до 2")

    # Создание панели ввода параметра коэффициента преломления окружающей среды
    n_out = DoubleVar(value=1.0)
    n_out_label = Label(buttonFrame, text="n_out (Коэфф. преломления окр. среды)")
    n_out_label.grid(row=11, padx=3, column=index)
    n_out_take = Entry(buttonFrame, textvariable=n_out, width=10)
    n_out_take.grid(row=12, column=index, padx=3, pady=3)
    n_out_tip = Hovertip(n_out_take, "от 1 до 2")

    # Создание панели ввода параметра коэффициента анизотропии
    g = DoubleVar(value=0.9)
    g_label = Label(buttonFrame, text="g (Коэфф. анизотропии)")
    g_label.grid(row=13, padx=3, column=index)
    g_take = Entry(buttonFrame, textvariable=g, width=10)
    g_take.grid(row=14, column=index, padx=3, pady=3)
    g_tip = Hovertip(g_take, "от ~0 до 1")

    # Создание кнопки, добавляющей ещё один слой
    button_add = Button(buttonFrame, text="➕ Добавить слой среды", command=addLayer)
    button_add.grid(row=15, column=index, padx=10, pady=10)

    # Создание кнопки, с пеомощью которой можно будет удалить слой
    button_del = Button(buttonFrame, text="❌ Удалить слой среды", command=lambda: deleteLayer(index))
    button_del.grid(row=16, column=index, padx=10, pady=10)

    layer_info = {
        "mu_s": {
            "mu_s_label": mu_s_label,
            "mu_s_take": mu_s_take,
            "mu_s_tip": mu_s_tip
        },
        "mu_a": {
            "mu_a_label": mu_a_label,
            "mu_a_take": mu_a_take,
            "mu_a_tip": mu_a_tip
        },
        "n": {
            "n_label": n_label,
            "n_take": n_take,
            "n_tip": n_tip
        },
        "n_out": {
            "n_out_label": n_out_label,
            "n_out_take": n_out_take,
            "n_out_tip": n_out_tip
        },
        "g": {
            "g_label": g_label,
            "g_take": g_take,
            "g_tip": g_tip
        },
        "buttons": {
            "button_del": button_del,
            "button_add": button_add
        },
        "index": index,
        "active": True,
    }

    widgets.append(layer_info)

    layers = index

# Создание приветственной надписи
info = Label(buttonFrame, font='Bold', text="Добро пожаловать! Выберите настройки:")
info.grid(row=0, column=1, pady=10)

map_label = Label(buttonFrame, font='Bold', text="Параметры для отрисовки карт")
map_label.grid(row=26, column=1, pady=10)

# Создание кнопки, активирующей функцию start
button2 = Button(buttonFrame, text="Нарисовать траектории", command=start)
button2.grid(row=17, column=1, padx=10, pady=10)

# Создание кнопки, вызывающая функцию takeFromFile
button3 = Button(buttonFrame, text="Построить карту из файла", command=takeFromFile)
button3.grid(row=33, column=1, padx=10, pady=10)

# Создание кнопки, закрывающей основное окно
button5 = Button(buttonFrame, text="Выйти из программы", command=window.destroy)
button5.grid(row=34, column=1)

addLayer()

# Компиляция рамки для кнопок и её прилипание к верхней границе
buttonFrame.pack(anchor="n")

# Зацикливание работы Tkinter, чтобы окно с данными не закрывалось без указания пользователя
window.mainloop()
