import matplotlib.pyplot as plt
from math import sqrt

from numpy import log, histogram, diff

from utils import gen_sticks_steps


def getVelocityOnSquare(photon_velocity, width, ceil_count):
    ceil_width = width/ceil_count
    velocity_on_square = photon_velocity/(ceil_width**2)
    return velocity_on_square


def makeWeightMap(size, max_radius, matrix, photon_velocity):
    # Инициализация списка-дублёра переданного списка
    matrix_data = []

    # Данные для гистограммы распределения света от источника
    plot_data_X, plot_data_Y = [], []

    # Задание размеров списка-дублёра и заполнение пустыми значениями
    for i in range(size):
        i = []
        matrix_data.append(i)
        for j in range(size):
            k = []
            i.append(k)

    def calculate_avg_distantion(index1, index2):
        ind1_dist = (index1 - size / 2) * 2 * max_radius / size
        ind2_dist = (index2 - size / 2) * 2 * max_radius / size
        dist = sqrt(ind1_dist**2 + ind2_dist**2)
        return dist

    hist_ceils = round(max_radius * sqrt(2)*20)
    weight_velocity_coef = getVelocityOnSquare(photon_velocity, 2 * max_radius, size)

    # Заполнение списка-дублёра данными, логарифмированными для наглядности
    for jindex in range(size):
        for index in range(size):
            matrix_data[jindex][index] = log(matrix[jindex][index] + 0.001)
            if matrix[jindex][index] > 0:
                plot_data_X.append(calculate_avg_distantion(jindex, index))
                plot_data_Y.append(matrix[jindex][index] * weight_velocity_coef)

    hist_data_Y, hist_data_X = histogram(plot_data_X, bins=hist_ceils, weights=plot_data_Y)

    # Создание фигуры (окна), которая будет хранить данные о весе отражённых фотонов
    figure1 = plt.figure()
    ax1 = figure1.add_subplot(111)
    # ax1.set_title("Вес отражённых фотонов")
    ax1.set_xticklabels(gen_sticks_steps(max_radius * 2))
    ax1.set_yticklabels(gen_sticks_steps(max_radius * 2))
    im1 = ax1.pcolormesh(matrix_data, cmap='inferno', antialiased=False)
    plt.xlabel('Расстояние по оси X, мм')
    plt.ylabel('Расстояние по оси Y, мм')
    figure1.colorbar(im1, ax=ax1, label="Натуральный логарифм от веса фотонов")

    figure2 = plt.figure()
    ax2 = figure2.add_subplot(111)
    # ax2.set_title(f'Распределение веса от удалённости от источника')
    plt.xlabel('Расстояние до источника, мм')
    plt.ylabel('Интенсивность света, мВт/мм²')

    ax2.bar(hist_data_X[:-1], hist_data_Y, width=diff(hist_data_X), align='edge')


def makeDepthMap(cylinder_size, max_depth, max_radius, fix_radius, cylinder, fix_radius_accuracy, photon_velocity):
    # Инициализация списка-дублёра переданного списка
    cylinder_data = []

    # Данные для четырёх кривых фиксированного радиуса
    plot_data_X1, plot_data_Y1 = [], []
    plot_data_X2, plot_data_Y2 = [], []
    plot_data_X3, plot_data_Y3 = [], []
    plot_data_X4, plot_data_Y4 = [], []

    def get_fix_radius_condition(idx, jdx, fix):
        return abs((idx * round(max_radius) / cylinder_size) - fix) <= fix_radius_accuracy/1000 and \
            jdx * max_depth / cylinder_size < 5

    weight_velocity_coef = getVelocityOnSquare(photon_velocity, 2 * max_radius, cylinder_size)

    # Задание размеров списка-дублёра и заполнение пустыми значениями
    for i in range(cylinder_size):
        i = []
        cylinder_data.append(i)
        for j in range(cylinder_size):
            k = []
            i.append(k)

    # Заполнение списка-дублёра данными, логарифмированными для наглядности
    for jindex in range(cylinder_size):
        for index in range(cylinder_size):
            cylinder_data[jindex][index] = log(cylinder[jindex][index]+0.001)
            if get_fix_radius_condition(index, jindex, fix_radius):
                plot_data_X1.append(jindex * max_depth / cylinder_size)
                plot_data_Y1.append(cylinder[jindex][index] * weight_velocity_coef)
            if get_fix_radius_condition(index, jindex, fix_radius * 2):
                plot_data_X2.append(jindex * max_depth / cylinder_size)
                plot_data_Y2.append(cylinder[jindex][index] * weight_velocity_coef)
            if get_fix_radius_condition(index, jindex, fix_radius * 3):
                plot_data_X3.append(jindex * max_depth / cylinder_size)
                plot_data_Y3.append(cylinder[jindex][index] * weight_velocity_coef)
            if get_fix_radius_condition(index, jindex, fix_radius * 4):
                plot_data_X4.append(jindex * max_depth / cylinder_size)
                plot_data_Y4.append(cylinder[jindex][index] * weight_velocity_coef)

    # Создание фигуры (окна), которая будет хранить данные
    # о распределении глубины пролёта фотона в зависимости от расстояния до центра пучка
    figure5 = plt.figure()
    ax5 = figure5.add_subplot(111)
    ax5.set_xticklabels(gen_sticks_steps(max_radius, 5))
    ax5.set_yticklabels(gen_sticks_steps(max_depth, 5))
    im5 = ax5.pcolormesh(cylinder_data, cmap='inferno', antialiased=False)
    plt.xlabel('Расстояние до центра пучка, мм')
    plt.ylabel('Глубина, мм')
    figure5.colorbar(im5, ax=ax5, label="Натуральный логарифм от веса фотонов")

    figure6 = plt.figure()
    ax6 = figure6.add_subplot(111)
    # ax6.set_title(f'Распределение веса от глубины при радиусе {round(fix_radius, 1)} мм')

    ax6.plot(plot_data_X1, plot_data_Y1, label=f'r = {round(fix_radius, 1)}мм', color='blue')
    ax6.plot(plot_data_X2, plot_data_Y2, label=f'r = {round(fix_radius*2, 1)}мм', color='red')
    ax6.plot(plot_data_X3, plot_data_Y3, label=f'r = {round(fix_radius*3, 1)}мм', color='green')
    ax6.plot(plot_data_X4, plot_data_Y4, label=f'r = {round(fix_radius*4, 1)}мм', color='orange')

    ax6.axvspan(0.3, 1.5, alpha=0.15, color='red', label='Кровенаполненные слои')

    plt.xlabel('Глубина, мм')
    plt.ylabel('Интенсивность света, мВт/мм²')
    plt.legend()


# Функция, выводящая окна с информацией об отражённых назад из среды фотонах
# Информация берётся напрямую из calculation.py
def openmatrix(size, cylinder_size, max_depth, max_radius, fix_radius, matrix, cylinder, fix_radius_accuracy,
               photon_velocity):

    makeWeightMap(size, max_radius, matrix, photon_velocity)
    makeDepthMap(cylinder_size, max_depth, max_radius, fix_radius, cylinder, fix_radius_accuracy, photon_velocity)

    # Зацикливание работы matplotlib, чтобы окно с данными не закрывалось без указания пользователя
    plt.show()
