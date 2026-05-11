import numpy
from matrix import openmatrix
import hashlib
import json


# Функция, выводящая статистику в консоль, сохраняющая файлы с матрицами
# и открывающая карты значений (matrix.py)
def open_(
        MATRIX, Cylinder,
        parameters: list[dict[str, float]],
        amount, size, fix_rad, fix_rad_acc, photo_count,
        max_radius, max_depth, max_cylinder
):
    # Расчёт толщины среды
    total_thickness = sum(layer["thickness"] for layer in parameters)
    plot_size = min(total_thickness, max_depth)
    rad_size = min(total_thickness/2, max_radius)

    spec = {
        'amount': amount,
        'parameters': parameters,
        'plot_size': plot_size,
        'rad_size': rad_size,
        'fix_rad': fix_rad,
        'fix_rad_acc': fix_rad_acc,
        'max_radius': max_radius,
        'max_depth': max_depth,
        'max_cylinder': max_cylinder,
        'photo_count': photo_count
    }

    spec_str = json.dumps(spec, sort_keys=True)
    spec_hash = hashlib.md5(spec_str.encode()).hexdigest()[:8]

    with open(f'archive/spec_{spec_hash}.json', 'w') as f:
        json.dump(spec, f, indent=2)

    amountStr = f'amount={amount}'
    numpy.savetxt(f'archive/matrix_ref_{spec_hash}_{amountStr}.txt', MATRIX)
    numpy.savetxt(f'archive/matrix_dis_{spec_hash}_{amountStr}.txt', Cylinder)

    print(f"Сохранено с хешем: {spec_hash}")
    print("Всего фотонов выпущено:", amount, "Фотонов отражено:", photo_count)
    openmatrix(size, max_cylinder, plot_size, rad_size, fix_rad, MATRIX, Cylinder, fix_rad_acc)

