import matplotlib.pyplot as plt
import json
import os

from matrix import makeWeightMap, makeDepthMap


# Данный модуль используется для построения только одной матрицы по txt файлу
def load_specification(spec_hash):
    """Загружает спецификацию из JSON файла по хешу"""
    spec_file = f'archive/spec_{spec_hash}.json'
    if os.path.exists(spec_file):
        with open(spec_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def rebuild_from_file(filepath, fix_radius=None, fix_radius_accuracy=None):
    # Получаем только имя файла без пути
    filename = os.path.basename(filepath)

    # Определяем тип матрицы (ref или dis)
    if 'matrix_ref' in filename:
        map_type = 'ref'
    elif 'matrix_dis' in filename:
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

    # Ищем хеш в имени файла (формат: matrix_ref_XXXXXXXX_amount=...)
    parts = filename.split('_')
    if len(parts) >= 3 and len(parts[2]) >= 8 and parts[2][:8].isalnum():
        spec_hash = parts[2][:8]
        spec = load_specification(spec_hash)

    # Если спецификация не найдена, пробуем старый формат
    if spec is None:
        print("Спецификация не найдена")
        return
    else:
        # Извлекаем параметры из спецификации
        rad = spec.get('rad_size', 0)
        dep = spec.get('plot_size', 0)
        velocity = spec.get('velocity', 1)
        if fix_radius is None:
            fix_radius = spec.get('fix_rad', 0)
        if fix_radius_accuracy is None:
            fix_radius_accuracy = spec.get('fix_rad_acc', 5)
        amount = spec.get('amount', 0)
        parameters = spec.get('parameters', [])

    size = 200
    cylinder_size = 100

    m_data = data.split()
    matrix_data = []

    if map_type == 'ref':
        for i in range(size):
            z = []
            matrix_data.append(z)
            for j in range(size):
                k = float(m_data[i * size + j])
                z.append(k)
        makeWeightMap(size, rad, matrix_data, velocity/amount)
        plt.show()

    elif map_type == 'dis':
        for i in range(cylinder_size):
            z = []
            matrix_data.append(z)
            for j in range(cylinder_size):
                k = float(m_data[i * cylinder_size + j])
                z.append(k)
        makeDepthMap(cylinder_size, dep, rad, fix_radius, matrix_data, fix_radius_accuracy, velocity/amount)
        print(cylinder_size, dep, rad, fix_radius, matrix_data, fix_radius_accuracy, velocity/amount)
        plt.show()

    else:
        print('Ошибка: неизвестный тип матрицы')
        return

