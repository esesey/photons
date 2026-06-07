import matplotlib.pyplot as plt
import json
import os
from tkinter import *

from layer_presets import Ma_light_map
from matrix import makeWeightMap, makeDepthMap


# Данный модуль используется для построения только одной матрицы по txt файлу
def load_specification(spec_hash):
    """Загружает спецификацию из JSON файла по хешу"""
    spec_file = f'archive/spec_{spec_hash}.json'
    if os.path.exists(spec_file):
        with open(spec_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def parse_spec(spec, fix_radius, fix_radius_accuracy, velocity, hash):
    amount = spec.get('amount')
    parameters = spec.get('parameters')
    plot_size = spec.get('plot_size')
    rad_size = spec.get('rad_size')

    layers_count = len(parameters)
    params = f"Количество фотонов: {amount}\n" \
             f"Количество слоёв: {layers_count}\n" \
             f"Максимальная глубина: {plot_size}мм\n" \
             f"Максимальный радиус: {rad_size}мм\n" \
             f"Фиксированный радиус: {fix_radius}мм\n" \
             f"Погрешность фиксированного радиуса: {fix_radius_accuracy}мкм\n" \
             f"Мощность источника: {velocity}Вт\n" \
             f"Хэш генерации: {hash}"

    layer_index = 1
    for layer in parameters:
        Mua = layer.get('mu_a')
        layer_info = f"\nСлой №{layer_index}\n" \
                     f"μ_s = {layer.get('mu_s')} мм^(-1)\n" \
                     f"μ_a = {Mua} мм^(-1)\n" \
                     f"n = {layer.get('n')}\n" \
                     f"n_out = {layer.get('n_out')}\n" \
                     f"g = {layer.get('g')}\n" \
                     f"Толщина: {layer.get('thickness')}мм\n" \
                     f"Цвет: {layer.get('color')}\n"
        params += layer_info
        layer_index += 1
        if layer_index == layers_count + 1:
            light = f"\nλ = {Ma_light_map.get(f'{Mua}')}нм"
            params += light

    return params

def create_info_window(information: str):
    info = Tk()
    info.title('Информация')
    info.geometry("300x500")
    info_frame = Frame(info)

    info_title = Label(info_frame, text="Информация о генерации: ")
    info_title.grid(row=0, column=0)

    info_text = Label(info_frame, text=information)
    info_text.grid(row=1, column=0)

    info_frame.pack(anchor="n")

def rebuild_from_file(filepath, fix_radius=None, fix_radius_accuracy=None, velocity=None):
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
        if velocity is None:
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

    info = parse_spec(spec, fix_radius, fix_radius_accuracy, velocity, spec_hash)

    if map_type == 'ref':
        for i in range(size):
            z = []
            matrix_data.append(z)
            for j in range(size):
                k = float(m_data[i * size + j])
                z.append(k)
        makeWeightMap(size, rad, matrix_data, velocity/amount)
        create_info_window(info)
        plt.show()

    elif map_type == 'dis':
        for i in range(cylinder_size):
            z = []
            matrix_data.append(z)
            for j in range(cylinder_size):
                k = float(m_data[i * cylinder_size + j])
                z.append(k)
        makeDepthMap(cylinder_size, dep, rad, fix_radius, matrix_data, fix_radius_accuracy, velocity/amount)
        create_info_window(info)
        plt.show()

    else:
        print('Ошибка: неизвестный тип матрицы')
        return
