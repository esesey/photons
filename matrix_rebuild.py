import matplotlib.pyplot as plt
from numpy import log

# Данный модуль используется для построения только одной матрицы по txt файлу

def rebuild(name, data):
    size = 200
    cylinder_size = 100
    map_type = name[name.index('_') + 1:name.index('_') + 4]
    rad = float(name[name.index('rad = ') + 6:len(name)].split(',')[0])
    dep = float(name[name.index('dep = ') + 6:len(name)].split(']')[0])
    matrix_data = []
    m_data = data.split()

    if map_type == 'ref':

        for i in range(size):
            z = []
            matrix_data.append(z)
            print('hi')
            for j in range(size):
                k = log(float(m_data[i * size + j]) + 0.001)
                z.append(k)

        figure1 = plt.figure()
        ax1 = figure1.add_subplot(111)
        ax1.set_title("Вес отражённых фотонов")
        ax1.set_xticklabels([0, rad / 8, 2 * rad / 8, 3 * rad / 8, 4 * rad / 8,
                             5 * rad / 8, 6 * rad / 8, 7 * rad / 8, rad])
        ax1.set_yticklabels([0, rad / 8, 2 * rad / 8, 3 * rad / 8, 4 * rad / 8,
                             5 * rad / 8, 6 * rad / 8, 7 * rad / 8, rad])
        im1 = ax1.pcolormesh(matrix_data, cmap='inferno', antialiased=False)
        plt.xlabel('Расстояние по оси X, мм')
        plt.ylabel('Расстояние по оси Y, мм')
        figure1.colorbar(im1, ax=ax1, label="Натуральный логарифм от веса фотонов")

        plt.show()

    if map_type == 'dis':
        for i in range(cylinder_size):
            z = []
            matrix_data.append(z)
            for j in range(cylinder_size):
                k = log(float(m_data[i * cylinder_size + j]) + 0.001)
                z.append(k)
        print('hi there')
        figure5 = plt.figure()
        ax5 = figure5.add_subplot(111)
        ax5.set_title("Распределение глубины по циллиндру")
        ax5.set_xticklabels([0, dep / 5, 2 * dep / 5, 3 * dep / 5, 4 * dep / 5, dep])
        ax5.set_yticklabels([0, rad / 5, 2 * rad / 5, 3 * rad / 5, 4 * rad / 5, rad])
        im5 = ax5.pcolormesh(matrix_data, cmap='inferno', antialiased=False)
        plt.xlabel('Глубина, мм')
        plt.ylabel('Расстояние до центра пучка, мм')
        figure5.colorbar(im5, ax=ax5, label="Натуральный логарифм от веса фотонов")
        plt.show()

    if map_type != 'dis' or map_type != 'ref':
        print('Raised error while writing map type')

