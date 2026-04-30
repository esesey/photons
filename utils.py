def gen_sticks_steps(maximum, steps=8, decimals=3):
    return [f"{i * maximum / steps:.{decimals}g}" for i in range(steps + 1)]