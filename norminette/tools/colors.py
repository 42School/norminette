def colors(text, *argv):
    options = {
        "bold": 1,
        "dim": 2,
        "underline": 4,
        "blink": 5,
        "reverse": 7,
        "hidden": 8,
        "reset_bold": 21,
        "reset_dim": 22,
        "reset_underlined": 24,
        "reset_blink": 25,
        "reset_reverse": 27,
        "reset_hidden": 28,
        "default_fg": 39,
        "black": 30,
        "red": 31,
        "green": 32,
        "yellow": 33,
        "blue": 34,
        "magenta": 35,
        "cyan": 36,
        "light_gray": 37,
        "dark_gray": 90,
        "light_red": 91,
        "light_green": 92,
        "light_yellow": 93,
        "light_blue": 94,
        "light_magenta": 95,
        "light_cyan": 96,
        "white": 97,
        "reset_all": 0,
    }
    reset = "\u001b[0m"
    tmp = []
    for arg in argv:
        tmp.append(str(options.get(arg, 0)))
    sep = ";"
    res = f"\u001b[{sep.join(tmp)}m{text}{reset}"
    return res
