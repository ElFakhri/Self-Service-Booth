from datetime import datetime as dt
import os

menu = {}

Table = dict[str, dict[str, str | int]]


def format_menu(filename: str) -> Table:
    raw = read_txt(filename)
    rows = raw.split("\n")
    for row in rows:
        if row[0] == "_" and filename == "menu.txt":
            category = row.replace("_", "")
        elif row[0] == "#" and filename == "menu.txt":
            nama_kedai = row.replace("#", "")
        else:
            columns = row.split(";")
            code = columns[0]
            name = columns[1]
            price = int(columns[2])
            menu[code] = {"name": name, "price": price, "category": category}
    return menu, nama_kedai


def format_order(filename: str) -> Table:
    order = Table()
    raw = read_txt(filename)
    rows = raw.split("\n")
    for row in rows:
        columns = row.split(";")
        code = columns[0]
        name = columns[1]
        price = int(columns[2])
        qty = int(columns[3])
        order[code] = {"name": name, "price": price, "Qty": qty}
    return order


def int_input(high: int, low: int, prompt: str):
    """inputs and check if there's an error
    Note: there are two input types, 'option' and 'qty'"""
    enter = "\nTekan tombol 'Enter' untuk melanjutkan\n"
    error_msg = "Respon harus berupa angka, bukan huruf"
    try:
        option = int(input(prompt))
        if option > high:
            error_msg = "Angka tidak bisa lebih besar dari " + str(high)
            raise ValueError
            input(enter)
            return None
        elif option < low:
            error_msg = "Angka tidak bisa lebih kecil dari " + str(low)
            raise ValueError
            input(enter)
        else:
            return option
    except ValueError:
        print("\nError: " + error_msg)
        input(enter)
        clear()


def code_input(dic: dict, prompt: str):
    option = input(prompt).upper()
    if option in dic:
        return option
    else:
        print("\nError: Kode tidak ditemukan")
        input("\nTekan tombol 'Enter' untuk melanjutkan\n")
        clear()
        return None


def ver_border(start_char: str, between_char: str, end_char, space_list: list):
    border = start_char
    for i in range(len(space_list)):
        border += (2 + space_list[i]) * "━"
        if i < len(space_list) - 1:
            border += between_char
        else:
            border += end_char
    border += "\n"
    return border


def table_content(content: list, space_list: list) -> str:
    line = "┃"
    for ix, val in enumerate(content):
        line += " {:^{x}} ┃".format(val, x=space_list[ix])
    line += "\n"
    return line


def read_txt(filename: str):
    with open(filename, "r") as f:
        raw = f.read()
    return raw


def menu_disp(menu: dict, space_list: list) -> str:
    curr_cat = "FOOD"
    space_total = 2 * len(space_list) + total(space_list)
    menu_table = ver_border("┏", "━", "┓", [space_total])
    menu_table += table_content([curr_cat], [space_total])
    menu_table += ver_border("┣", "┳", "┫", space_list)
    for ix, code in enumerate(menu.keys()):
        name = menu[code]["name"]
        price = format_price(menu[code]["price"], space_list[2])
        if curr_cat != menu[code]["category"]:
            curr_cat = menu[code]["category"]
            menu_table += ver_border("┣", "┻", "┫", space_list)
            menu_table += table_content([curr_cat], [space_total])
            menu_table += ver_border("┣", "┳", "┫", space_list)
        menu_table += table_content([code, name, price], space_list)
        if ix >= len(menu) - 1:
            menu_table += ver_border("┗", "┻", "┛", space_list)
    return menu_table


def order_disp(order: dict, space_list: list) -> str:
    new_space = space_list.copy()
    new_space.append(3)
    new_space.append(new_space[2] + 3)
    total = 0
    order_table = ver_border("┏", "┳", "┓", new_space)
    order_table += table_content(
        ["Kode", "Nama", "Harga", "Qty", "Subtotal"], new_space
    )
    order_table += ver_border("┣", "╋", "┫", new_space)
    for code in order.keys():
        name = order[code]["name"]
        price = order[code]["price"]
        qty = order[code]["Qty"]
        subtotal = order[code]["subtotal"] = price * qty
        total += subtotal
        order_table += table_content(
            [code, name, format_price(price, space_list[2]), qty,
             format_price(subtotal, space_list[2])],
            new_space,
        )
    order_table += ver_border("┗", "┻", "┛", new_space)
    order_table += "Total: " + format_price(total, space_list[2])
    return order_table


def deformat_txt(content: dict) -> str:
    txt = ""
    for val, code in enumerate(content.keys()):
        txt += f"{code};{content[code]['name']};{content[code]['price']};{content[code]['Qty']}"
        if val < len(content)-1:
            txt += "\n"
    return txt


def create_receipt(content: dict):
    now = dt.now()
    filename = now.strftime("%Y-%m-%d %H:%M:%S.txt")
    deformatted = deformat_txt(content)
    create_txt(f"Receipt History/{filename}", deformatted)


def create_txt(filename: str, content: str):
    with open(filename, "w") as f:
        f.write(content)


def get_max_len(content: dict) -> list:
    """get the max len of a dict and turn it into a list of spaces"""
    highest = [4, 0, 0]
    for code in content.keys():
        name = len(content[code]["name"])
        price = len(format_price(content[code]["price"], 0))
        if name > highest[1]:
            highest[1] = name
        if price > highest[2]:
            highest[2] = price

    return highest


def format_price(price: int, length):
    length -= 4
    formatted_price = "Rp. {:>{x},}".format(price, x=length)
    formatted_price = formatted_price.replace(",", ".")
    return formatted_price


def total(lol: list) -> int:
    """get the total of a list"""
    total = 0
    for i in lol:
        total += i
    return total


def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
