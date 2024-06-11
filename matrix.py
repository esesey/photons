import matplotlib.pyplot as plt
from numpy import log

# Функция, выводящая окна с информацией об отражённых назад из среды фотонах
# Информация берётся напрямую из drawing.py
def openmatrix(size, cylinder_size, max_depth, max_radius, fix_radius, matrix=[[]], cylinder=[[]]):
    # Инициализация списков-дублёров переданных списков
    matrix_data = []
    cylinder_data = []
    plot_data_X = []
    plot_data_Y = []

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
            if (index * max_radius / cylinder_size == fix_radius):
                plot_data_X.append(jindex * max_depth / cylinder_size)
                plot_data_Y.append(cylinder[jindex][index])

    # Создание фигуры (окна), которая будет хранить данные о весе отражённых фотонов
    figure1 = plt.figure()
    ax1 = figure1.add_subplot(111)
    ax1.set_title("Вес отражённых фотонов")
    ax1.set_xticklabels([0, max_radius / 8, 2 * max_radius / 8, 3 * max_radius / 8, 4 * max_radius / 8,
                         5 * max_radius / 8, 6 * max_radius / 8, 7 * max_radius / 8, max_radius])
    ax1.set_yticklabels([0, max_radius / 8, 2 * max_radius / 8, 3 * max_radius / 8, 4 * max_radius / 8,
                         5 * max_radius / 8, 6 * max_radius / 8, 7 * max_radius / 8, max_radius])
    im1 = ax1.pcolormesh(matrix_data, cmap='inferno', antialiased=False)
    plt.xlabel('Расстояние по оси X, мм')
    plt.ylabel('Расстояние по оси Y, мм')
    figure1.colorbar(im1, ax=ax1, label="Натуральный логарифм от веса фотонов")
    # Создание фигуры (окна), которая будет хранить данные
    # о распределении глубины пролёта фотона в зависимости от расстояния до центра пучка
    figure5 = plt.figure()
    ax5 = figure5.add_subplot(111)
    ax5.set_title("Распределение глубины по циллиндру")
    ax5.set_xticklabels([0, max_depth / 5, 2 * max_depth / 5, 3 * max_depth / 5, 4 * max_depth / 5, max_depth])
    ax5.set_yticklabels([0, max_radius / 5, 2 * max_radius / 5, 3 * max_radius / 5, 4 * max_radius / 5, max_radius])
    im5 = ax5.pcolormesh(cylinder_data, cmap='inferno', antialiased=False)
    plt.xlabel('Глубина, мм')
    plt.ylabel('Расстояние до центра пучка, мм')
    figure5.colorbar(im5, ax=ax5, label="Натуральный логарифм от веса фотонов")

    figure6 = plt.figure()
    ax6 = figure6.add_subplot(111)
    ax6.set_title('Распределение веса от глубины при радиусе ' + str(fix_radius))
    ax6.plot(plot_data_X, plot_data_Y)
    plt.xlabel('Глубина, мм')
    plt.ylabel('Вес фотонов')

    # Зацикливание работы matplotlib.pyplot, чтобы окно с данными не закрывалось без указания пользователя
    plt.show()
