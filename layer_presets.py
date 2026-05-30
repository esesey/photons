EPIDERMIS_MANUAL_PRESET = {
    "n": 1.37,
    "n_out": 1.0,
    "g": 0.9,
    "thickness": 0.1,
    "color": "#edc095"
}
DERMAL_MANUAL_PRESET = {
    "n": 1.4,
    "n_out": 1.0,
    "g": 0.9,
    "thickness": 10,
    "color": "#ff7c6b"
}

# ИК свет
EPIDERMIS_940NM_PARAMS = {
    "Ms": 33.23,
    "Ma": 0.199,
}
DERMAL_940NM_PARAMS = {
    "Ms": 15.44,
    "Ma": 0.058,
}
# Красный свет
EPIDERMIS_655NM_PARAMS = {
    "Ms": 52.99,
    "Ma": 0.852,
}
DERMAL_655NM_PARAMS = {
    "Ms": 28.94,
    "Ma": 0.065,
}
# Зелёный свет
EPIDERMIS_530NM_PARAMS = {
    "Ms": 71.03,
    "Ma": 1.454,
}
DERMAL_530NM_PARAMS = {
    "Ms": 40.19,
    "Ma": 0.21,
}

EPIDERMIS_LAYER_PRESET_940 = EPIDERMIS_MANUAL_PRESET | EPIDERMIS_940NM_PARAMS
DERMAL_LAYER_PRESET_940 = DERMAL_MANUAL_PRESET | DERMAL_940NM_PARAMS
EPIDERMIS_LAYER_PRESET_655 = EPIDERMIS_MANUAL_PRESET | EPIDERMIS_655NM_PARAMS
DERMAL_LAYER_PRESET_655 = DERMAL_MANUAL_PRESET | DERMAL_655NM_PARAMS
EPIDERMIS_LAYER_PRESET_530 = EPIDERMIS_MANUAL_PRESET | EPIDERMIS_530NM_PARAMS
DERMAL_LAYER_PRESET_530 = DERMAL_MANUAL_PRESET | DERMAL_530NM_PARAMS

GEN_ONE_LAYER_PRESET_530 = [DERMAL_LAYER_PRESET_530]
GEN_ONE_LAYER_PRESET_655 = [DERMAL_LAYER_PRESET_655]
GEN_ONE_LAYER_PRESET_940 = [DERMAL_LAYER_PRESET_940]
GEN_TWO_LAYER_PRESET_530 = [EPIDERMIS_LAYER_PRESET_530, DERMAL_LAYER_PRESET_530]
GEN_TWO_LAYER_PRESET_655 = [EPIDERMIS_LAYER_PRESET_655, DERMAL_LAYER_PRESET_655]
GEN_TWO_LAYER_PRESET_940 = [EPIDERMIS_LAYER_PRESET_940, DERMAL_LAYER_PRESET_940]

MAIN_GEN_PRESETS = {
    "1 слой, зелёный свет (λ = 530нм)": {
        "code": "530_1l",
        "layers": GEN_ONE_LAYER_PRESET_530
    },
    "1 слой, красный свет (λ = 655нм)": {
        "code": "655_1l",
        "layers": GEN_ONE_LAYER_PRESET_655
    },
    "1 слой, ИК свет (λ = 940нм)": {
        "code": "940_1l",
        "layers": GEN_ONE_LAYER_PRESET_940
    },
    "2 слоя, зелёный свет (λ = 530нм)": {
        "code": "530_2l",
        "layers": GEN_TWO_LAYER_PRESET_530
    },
    "2 слоя, красный свет (λ = 655нм)": {
        "code": "655_2l",
        "layers": GEN_TWO_LAYER_PRESET_655
    },
    "2 слоя, ИК свет (λ = 940нм)": {
        "code": "940_2l",
        "layers": GEN_TWO_LAYER_PRESET_940
    },
}