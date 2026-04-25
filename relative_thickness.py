import colorsys
from tkinter import Canvas


# Этот модуль посвящён расчётам, связанным с толщиной слоёв


# Рассчитывает относительную толщину слоя (в у.е. вместо мм)
def relative_thickness(thickness: float, total_thickness: float, maximum: float):
    return (thickness / total_thickness) * maximum


# Создаёт цветные прямоугольники для визуального представления слоёв
def create_color_layer_presentation(parameters: list[dict[str, float]], c: Canvas, canvas_height: float, canvas_width: float):
    total_thickness = sum(layer["thickness"] for layer in parameters)
    # Переменная для накопления толщины предыдущих слоёв
    cumulative_thickness = 0

    # Красим в разные цвета каждый слой среды
    for index, layer in enumerate(parameters):
        layer_thickness = relative_thickness(layer["thickness"], total_thickness, canvas_height)
        previous_layers_thickness = relative_thickness(cumulative_thickness, total_thickness, canvas_height)

        cumulative_thickness += layer["thickness"]

        hue = (index + 1) / len(parameters)
        # Преобразование HSV в RGB
        r, g, b = colorsys.hsv_to_rgb(hue, 0.15, 1.0)

        # Конвертация в HEX
        hex_color = "#{:02x}{:02x}{:02x}".format(
            int(r * 255),
            int(g * 255),
            int(b * 255)
        )

        c.create_rectangle(0, previous_layers_thickness, canvas_width, (index + 1) * layer_thickness, fill=hex_color, outline='')


# Возвращает массив с координатами границ слоёв
def get_breakpoints(parameters: list[dict[str, float]], max_depth: float):
    breakpoints = [0]
    total_thickness = sum(layer["thickness"] for layer in parameters)
    cumulative_thickness = 0
    for layer in parameters:
        layer_thickness = relative_thickness(layer["thickness"], total_thickness, max_depth)
        previous_layers_thickness = relative_thickness(cumulative_thickness, total_thickness, max_depth)
        cumulative_thickness += layer["thickness"]
        breakpoints.append(layer_thickness + previous_layers_thickness)
    breakpoints[len(breakpoints) - 1] = max_depth
    return breakpoints
