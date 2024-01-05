from tkinter import *
from tkinter import ttk
from drawing import drawing
from idlelib.tooltip import Hovertip

# Создание стартового окна и рамки для кнопок
window = Tk()
window.title("Панель управления")
window.geometry("300x460")
buttonFrame = Frame(window)

# Создание панели ввода параметра количества выпускаемых фотонов
amount = IntVar(value=100000)
amount_label = Label(buttonFrame, text="Кол-во выпускаемых фотонов")
amount_label.grid(row=3, column=1)
amount_take = Entry(buttonFrame, textvariable=amount, width=10)
amount_take.grid(row=4, column=1, padx=3, pady=3)
amount_tip = Hovertip(amount_take, "от 1 до 100m")

# Создание панели ввода параметра коэффициента рассеяния среды
Ms = DoubleVar(value=0.1)
mu_s_label = Label(buttonFrame, text="μs (Коэфф. рассеяния)")
mu_s_label.grid(row=5, column=1)
mu_s_take = Entry(buttonFrame, textvariable=Ms, width=10)
mu_s_take.grid(row=6, column=1, padx=3, pady=3)
mu_s_tip = Hovertip(mu_s_take, "от ~0 до 10")

# Создание панели ввода параметра коэффициента поглощения среды
Ma = DoubleVar(value=0.002)
mu_a_label = Label(buttonFrame, text="μa (Коэфф. поглощения)")
mu_a_label.grid(row=7, column=1)
mu_a_take = Entry(buttonFrame, textvariable=Ma, width=10)
mu_a_take.grid(row=8, column=1, padx=3, pady=3)
mu_a_tip = Hovertip(mu_a_take, "от ~0 до 0.5")

# Создание панели ввода параметра коэффициента преломления среды
n = DoubleVar(value=1.5)
n_label = Label(buttonFrame, text="n (Коэфф. преломления среды)")
n_label.grid(row=9, column=1)
n_take = Entry(buttonFrame, textvariable=n, width=10)
n_take.grid(row=10, column=1, padx=3, pady=3)
n_tip = Hovertip(n_take, "от 1 до 2")

# Создание панели ввода параметра коэффициента преломления окружающей среды
n_out = DoubleVar(value=1.0)
n_out_label = Label(buttonFrame, text="n_out (Коэфф. преломления окр. среды)")
n_out_label.grid(row=11, column=1)
n_out_take = Entry(buttonFrame, textvariable=n_out, width=10)
n_out_take.grid(row=12, column=1, padx=3, pady=3)
n_out_tip = Hovertip(n_out_take, "от 1 до 2")

# Создание панели ввода параметра коэффициента анизотропии
g = DoubleVar(value=0.9)
g_label = Label(buttonFrame, text="g (Коэфф. анизотропии)")
g_label.grid(row=13, column=1)
g_take = Entry(buttonFrame, textvariable=g, width=10)
g_take.grid(row=14, column=1, padx=3, pady=3)
g_tip = Hovertip(g_take, "от ~0 до 1")

# Создание панели ввода размера списка со значениями для вернувшихся фотонов
size = IntVar(value=200)
size_label = Label(buttonFrame, text="Размер матрицы возврата")
size_label.grid(row=15, column=1)
size_take = Entry(buttonFrame, textvariable=size, width=10)
size_take.grid(row=16, column=1, padx=3, pady=3)
size_tip = Hovertip(size_take, "от 1 до 400")

# Создание кнопки выбора, показывать ли окно с прогрессом выполнения программы
# Может быть полезно при разных ситуациях, т.к. прогресс содержит
# Интересную информацию, но отнимает производительность
is_show_load = BooleanVar(value=True)
is_show_load_check = ttk.Checkbutton(buttonFrame, variable=is_show_load, text="Показывать прогресс")
is_show_load_check.grid(row=2, column=1)
is_show_load_tip = Hovertip(is_show_load_check, 'Окно прогресса содержит много полезной информации, \n'
                                                'однако существенно снижает производительность')


# Функция, переносящая введённые параметры в файл drawing.py
def start():
    drawing(float(mu_s_take.get()), float(mu_a_take.get()), float(n_take.get()),
            float(n_out_take.get()), float(g_take.get()), int(amount_take.get()),
            int(size_take.get()), bool(is_show_load.get()))

# Создание приветственной надписи
info = Label(buttonFrame, text="Добро пожаловать! Выберите настройки:")
info.grid(row=0, column=1)

# Создание кнопки, активирующей функцию start
button2 = Button(buttonFrame, text="Нарисовать траектории", command=start)
button2.grid(row=1, column=1, padx=10, pady=10)

# Создание кнопки, закрывающей основное окно
button5 = Button(buttonFrame, text="Выйти из программы", command=window.destroy)
button5.grid(row=17, column=1, padx=10, pady=10)

# Компиляция рамки для кнопок и её прилипание к верхней границе
buttonFrame.pack(anchor="n")

# Зацикливание работы Tkinter, чтобы окно с данными не закрывалось без указания пользователя
window.mainloop()
