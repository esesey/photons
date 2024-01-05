import matplotlib.pyplot as plt
from numpy import log

# Функция, выводящая окна с информацией об отражённых назад из среды фотонах
# Информация берётся напрямую из drawing.py
def openmatrix(size, cylinder_size, matrix=[[]], cylinder=[[]]):
    # Инициализация списков-дублёров переданных списков
    matrix_data = []
    cylinder_data = []

    # Задание размеров списков-дублёров и заполнение пустыми значениями
    for i in range(size):
        i = []
        matrix_data.append(i)
        for j in range(size):
            k = []
            i.append(k)
    for i in range(cylinder_size):
        i = []
        cylinder_data.append(i)
        for j in range(cylinder_size):
            k = []
            i.append(k)

    # Заполнение списков-дублёров данными, логарифмезированными для наглядности
    for jindex in range(size):
        for index in range(size):
            matrix_data[jindex][index] = log(matrix[jindex][index]+0.001)
    for jindex in range(cylinder_size):
        for index in range(cylinder_size):
            cylinder_data[jindex][index] = log(cylinder[jindex][index]+0.001)

    # Создание фигуры (окна), которая будет хранить данные о весе отражённых фотонов
    figure1 = plt.figure()
    ax1 = figure1.add_subplot(111)
    ax1.set_title("Вес отражённых фотонов")
    im1 = ax1.pcolormesh(matrix_data, cmap='inferno', antialiased=False)
    plt.xlabel('Расстояние по оси X, мкм')
    plt.ylabel('Расстояние по оси Y, мкм')
    figure1.colorbar(im1, ax=ax1, label="Натуральный логарифм от веса фотонов")
    # Создание фигуры (окна), которая будет хранить данные
    # о распределении глубины пролёта фотона в зависимости от расстояния до центра пучка
    figure5 = plt.figure()
    ax5 = figure5.add_subplot(111)
    ax5.set_title("Распределение глубины по циллиндру")
    im5 = ax5.pcolormesh(cylinder_data, cmap='inferno', antialiased=False)
    plt.xlabel('Глубина, мкм')
    plt.ylabel('Расстояние до центра пучка, мкм')
    figure1.colorbar(im5, ax=ax5, label="Натуральный логарифм от веса фотонов")

    # Зацикливание работы matplotlib.pyplot, чтобы окно с данными не закрывалось без указания пользователя
    plt.show()
