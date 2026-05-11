import matplotlib.pyplot as plt
import json
import os
import glob
from numpy import log

# Данный модуль используется для построения только одной матрицы по txt файлу


def list_all_specifications():
    """Выводит список всех сохраненных спецификаций"""
    spec_files = glob.glob('archive/spec_*.json')

    if not spec_files:
        print("Спецификации не найдены")
        return

    print("\n=== Доступные спецификации ===\n")
    for spec_file in spec_files:
        spec_hash = os.path.basename(spec_file).replace('spec_', '').replace('.json', '')
        try:
            with open(spec_file, 'r', encoding='utf-8') as f:
                spec = json.load(f)

            print(f"Хеш: {spec_hash}")
            print(f"  Фотонов: {spec.get('amount', 0)}")
            print(f"  Слоев: {len(spec.get('parameters', []))}")
            print(f"  Радиус: {spec.get('rad_size', 0):.2f} мм")
            print(f"  Глубина: {spec.get('plot_size', 0):.2f} мм")
            print(f"  fix_rad: {spec.get('fix_rad', 0):.2f} мм")
            print()
        except Exception as e:
            print(f"Ошибка чтения {spec_file}: {e}")


def load_specification(spec_hash):
    """Загружает спецификацию из JSON файла по хешу"""
    spec_file = f'archive/spec_{spec_hash}.json'
    if os.path.exists(spec_file):
        with open(spec_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def parse_old_format(filename):
    """Парсинг старого формата имени файла для обратной совместимости"""
    try:
        # Извлекаем rad и dep из старого формата
        rad_start = filename.find('rad = ')
        if rad_start != -1:
            rad_part = filename[rad_start + 6:]
            rad = float(rad_part.split(',')[0])
        else:
            rad = 0

        dep_start = filename.find('dep = ')
        if dep_start != -1:
            dep_part = filename[dep_start + 6:]
            dep = float(dep_part.split(']')[0])
        else:
            dep = 0

        return rad, dep
    except:
        return 0, 0


# Старая версия
def rebuild(name, data, fix_radius):
    size = 200
    cylinder_size = 100
    map_type = name[name.index('_') + 1:name.index('_') + 4]
    rad = float(name[name.index('rad = ') + 6:len(name)].split(',')[0])
    dep = float(name[name.index('dep = ') + 6:len(name)].split(']')[0])
    matrix_data = []
    plot_data_X = []
    plot_data_Y = []
    m_data = data.split()
    sum = 0

    if map_type == 'ref':
        for i in range(size):
            z = []
            matrix_data.append(z)
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
                if (j*rad/cylinder_size == fix_radius and i*dep/cylinder_size<=2):
                    plot_data_X.append(i*dep/cylinder_size)
                    plot_data_Y.append(float(m_data[i * cylinder_size + j]))

        figure5 = plt.figure()
        ax5 = figure5.add_subplot(111)
        ax5.set_title("Распределение глубины по циллиндру")
        ax5.set_xticklabels([0, dep / 5, 2 * dep / 5, 3 * dep / 5, 4 * dep / 5, dep])
        ax5.set_yticklabels([0, rad / 5, 2 * rad / 5, 3 * rad / 5, 4 * rad / 5, rad])
        im5 = ax5.pcolormesh(matrix_data, cmap='inferno', antialiased=False)
        plt.xlabel('Глубина, мм')
        plt.ylabel('Расстояние до центра пучка, мм')
        figure5.colorbar(im5, ax=ax5, label="Натуральный логарифм от веса фотонов")

        figure6 = plt.figure()
        ax6 = figure6.add_subplot(111)
        ax6.set_title('Распределение веса от глубины при радиусе' + str(fix_radius))
        ax6.plot(plot_data_X, plot_data_Y)
        plt.xlabel('Глубина, мм')
        plt.ylabel('Вес фотонов')

        print(sum)
        plt.show()

    if map_type != 'dis' and map_type != 'ref':
        print('Raised error while reading map type')

# TODO: Актуализировать с основным построением
def rebuild_from_file(filepath, fix_radius=None):
    """
    Универсальная функция для построения графиков из файла матрицы

    Параметры:
    - filepath: путь к файлу с матрицей
    - fix_radius: фиксированный радиус для графика распределения (если None, берется из спецификации)
    """

    # Получаем только имя файла без пути
    filename = os.path.basename(filepath)

    # Определяем тип матрицы (ref или dis)
    if 'matrix_ref' in filename:
        map_type = 'ref'
    elif 'matrix_dis' in filename:
        map_type = 'dis'
    else:
        # Проверяем старый формат
        if '_ref_' in filename:
            map_type = 'ref'
        elif '_dis_' in filename:
            map_type = 'dis'
        else:
            print('Ошибка: не удалось определить тип матрицы')
            return

    # Пытаемся загрузить данные из файла
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = f.read()
    except Exception as e:
        print(f"Ошибка при чтении файла {filepath}: {e}")
        return

    # Пытаемся найти хеш и загрузить спецификацию
    spec = None
    spec_hash = None

    # Ищем хеш в имени файла (формат: matrix_ref_XXXXXXXX_amount=...)
    parts = filename.split('_')
    if len(parts) >= 3 and len(parts[2]) >= 8 and parts[2][:8].isalnum():
        spec_hash = parts[2][:8]
        spec = load_specification(spec_hash)

    # Если спецификация не найдена, пробуем старый формат
    if spec is None:
        print("Спецификация не найдена, использую парсинг из имени файла (старый формат)")
        rad, dep = parse_old_format(filename)
        # Для старого формата fix_radius должен быть передан явно
        if fix_radius is None:
            print("Внимание: для старого формата необходимо указать fix_radius")
            fix_radius = 0
    else:
        # Извлекаем параметры из спецификации
        rad = spec.get('rad_size', 0)
        dep = spec.get('plot_size', 0)
        if fix_radius is None:
            fix_radius = spec.get('fix_rad', 0)
        amount = spec.get('amount', 0)
        parameters = spec.get('parameters', [])

        print(f"Загружена спецификация с хешем {spec_hash}")
        print(f"Параметры: amount={amount}, rad={rad:.3f}, dep={dep:.3f}, fix_rad={fix_radius}")
        if parameters:
            print(f"Количество слоев: {len(parameters)}")

    size = 200
    cylinder_size = 100

    matrix_data = []
    plot_data_X = []
    plot_data_Y = []
    m_data = data.split()

    if map_type == 'ref':
        # Построение карты отражений
        for i in range(size):
            z = []
            matrix_data.append(z)
            for j in range(size):
                if i * size + j < len(m_data):
                    k = log(float(m_data[i * size + j]) + 0.001)
                    z.append(k)
                else:
                    z.append(0)

        figure1 = plt.figure(figsize=(10, 8))
        ax1 = figure1.add_subplot(111)
        ax1.set_title("Вес отражённых фотонов")

        # Настройка подписей осей
        ticks = [0, rad / 8, 2 * rad / 8, 3 * rad / 8, 4 * rad / 8, 5 * rad / 8, 6 * rad / 8, 7 * rad / 8, rad]
        tick_labels = [f'{tick:.2f}' for tick in ticks]
        ax1.set_xticks(range(0, size + 1, size // 8))
        ax1.set_yticks(range(0, size + 1, size // 8))
        ax1.set_xticklabels(tick_labels)
        ax1.set_yticklabels(tick_labels)

        im1 = ax1.pcolormesh(matrix_data, cmap='inferno', antialiased=False)
        plt.xlabel('Расстояние по оси X, мм')
        plt.ylabel('Расстояние по оси Y, мм')
        figure1.colorbar(im1, ax=ax1, label="Натуральный логарифм от веса фотонов")

        plt.show()

    elif map_type == 'dis':
        # Построение распределения глубины
        for i in range(cylinder_size):
            z = []
            matrix_data.append(z)
            for j in range(cylinder_size):
                idx = i * cylinder_size + j
                if idx < len(m_data):
                    k = log(float(m_data[idx]) + 0.001)
                    z.append(k)
                    # Собираем данные для графика по фиксированному радиусу
                    if fix_radius and abs(j * rad / cylinder_size - fix_radius) < (rad / cylinder_size / 2):
                        if i * dep / cylinder_size <= 2:
                            plot_data_X.append(i * dep / cylinder_size)
                            plot_data_Y.append(float(m_data[idx]))
                else:
                    z.append(0)

        # График 1: 2D карта распределения
        figure5 = plt.figure(figsize=(10, 8))
        ax5 = figure5.add_subplot(111)
        ax5.set_title("Распределение глубины по цилиндру")

        # Настройка подписей осей
        depth_ticks = [0, dep / 5, 2 * dep / 5, 3 * dep / 5, 4 * dep / 5, dep]
        rad_ticks = [0, rad / 5, 2 * rad / 5, 3 * rad / 5, 4 * rad / 5, rad]
        depth_labels = [f'{tick:.2f}' for tick in depth_ticks]
        rad_labels = [f'{tick:.2f}' for tick in rad_ticks]

        ax5.set_xticks(range(0, cylinder_size + 1, cylinder_size // 5))
        ax5.set_yticks(range(0, cylinder_size + 1, cylinder_size // 5))
        ax5.set_xticklabels(depth_labels)
        ax5.set_yticklabels(rad_labels)

        im5 = ax5.pcolormesh(matrix_data, cmap='inferno', antialiased=False)
        plt.xlabel('Глубина, мм')
        plt.ylabel('Расстояние до центра пучка, мм')
        figure5.colorbar(im5, ax=ax5, label="Натуральный логарифм от веса фотонов")

        # График 2: Распределение веса от глубины
        if plot_data_X and plot_data_Y:
            figure6 = plt.figure(figsize=(10, 6))
            ax6 = figure6.add_subplot(111)
            ax6.set_title(f'Распределение веса от глубины при радиусе {fix_radius:.2f} мм')
            ax6.plot(plot_data_X, plot_data_Y, 'b-', linewidth=2)
            ax6.grid(True, alpha=0.3)
            plt.xlabel('Глубина, мм')
            plt.ylabel('Вес фотонов')

        # Добавляем информацию о параметрах
        if spec and plot_data_X and plot_data_Y:
            info_text = f"Фотонов: {spec.get('amount', 0)}\nРадиус: {fix_radius:.2f} мм"
            ax6.text(0.02, 0.98, info_text, transform=ax6.transAxes,
                     fontsize=8, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        plt.show()

    else:
        print('Ошибка: неизвестный тип матрицы')
