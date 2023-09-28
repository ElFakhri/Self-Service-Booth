import os
from order import (
    format_menu,
    menu_disp,
    order_disp,
    create_receipt,
    get_max_len,
    clear,
    int_input,
    code_input,
    create_txt,
    format_order)

password = "pass1234"


def setup():
    if not os.path.isdir("Receipt History"):
        os.mkdir("Receipt History")


def start_page():
    clear()
    line_len = 22
    if line_len < len(nama_kedai) + 4:
        line_len = len(nama_kedai) + 4
    print(f"┏{'━'*line_len}┓")
    print("┃{:^{x}}┃".format("SELF SERVICE BOOTH", x=line_len))
    print("┃{:^{x}}┃".format(nama_kedai, x=line_len))
    print(f"┗{'━'*line_len}┛")
    answer = input("Tekan tombol 'Enter' untuk melanjutkan.. ")
    return answer


def menu_page(menu: dict):
    clear()
    menu_table = menu_disp(menu, space_list)
    print(menu_table)
    code_inp = code_input(menu, "Kode: ")
    if code_inp is None:
        return
    qty_inp = int_input(75, 0, "Jumlah: ")
    if qty_inp is None:
        return
    if code_inp in order:
        order[code_inp]["Qty"] += qty_inp
    else:
        order[code_inp] = menu[code_inp]
        order[code_inp].update({"Qty": qty_inp})
    clear()


def order_page(order: dict) -> int:
    clear()
    if len(order.keys()) > 0:
        global order_table
        order_table = order_disp(order, space_list)
        print(order_table)
        print("")
    print("1. Tambah pesanan")
    print("2. Ubah jumlah pesanan")
    print("3. Hapus pesanan")
    print("4. Batalkan pesanan")
    print("5. Konfirmasi pesanan")
    order_option = int_input(5, 1, "\nPilih opsi: ")
    if order_option is None or order_option == 1 or order_option > 3:
        return order_option
    code_inp = code_input(order, "Kode: ")
    if code_inp is None:
        return None
    if order_option == 2:
        qty_inp = int_input(75, 0, "Jumlah: ")
        if qty_inp is None:
            return None
        order[code_inp]["Qty"] = qty_inp
    if order_option == 3:
        order.pop(code_inp)

    clear()


def main():
    global nama_kedai
    menu, nama_kedai = format_menu("menu.txt")
    global order
    order = {}
    start = True
    global space_list
    space_list = get_max_len(menu)
    while True:
        if start is True:
            answer = start_page()
            start = False
            if answer == "admin":
                pass_attempt = input("Password: ")
                if pass_attempt == password:
                    return "admin"
        action = order_page(order)
        if action is None:
            action = order_page(order)
        if action == 1:
            menu_page(menu)
        if action == 4:
            order.clear()
            start = True
        if action == 5:
            create_receipt(order)
            create_txt("output.txt", order_table)
            order.clear()
            start = True


def admin():
    clear()
    print(
        "1. Edit menu (WIP)",
        "2. Ganti nama kedai (WIP)",
        "3. lihat history struk",
        "4. Kembali ke program",
        "5. Exit program",
        sep="\n",
    )
    option = int_input(5, 1, "\nPilih opsi: ")
    if option is not None:
        if option == 3:
            read_receipt()
        if option == 4:
            return "main"
        if option == 5:
            return


def read_receipt():
    try:
        year_inp = int(input("\nTahun: "))
        print("")
        months = ("Januari", "Februari", "Maret",
                  "April", "Mei", "Juni", "Juli",
                  "Agustus", "September", "Oktober",
                  "November", "December")
        for ix, month in enumerate(months):
            print(f"{ix+1}. {month}")
        month_inp = int(input("\nBulan: "))
        date_inp = int(input("\nTanggal: "))
        all_receipts = os.listdir("Receipt History/")
        date_format = f"{year_inp}-{month_inp:02}-{date_inp:02}"
        counter = 0
        for receipt in all_receipts:
            date_list = receipt.split(" ")
            date_list[1] = date_list[1].replace(".txt", "")
            if date_list[0] == date_format:
                counter += 1
                print(f"{counter}. {date_list[1]}")
        time_inp = int(input("\n Waktu: ")) - 1
        file_input = f"{date_format} {date_list[time_inp]}.txt"
        clear()
        orderr = format_order(f"Receipt History/{file_input}")
        order_table = order_disp(orderr, space_list)
        print(order_table)
    except FileNotFoundError:
        print("Tahun/bulan/tanggal tidak ditemukan")
        input("\nTekan tombol 'Enter' untuk melanjutkan\n")
    except ValueError:
        print("Tahun/bulan/tanggal tidak ditemukan")
        input("\nTekan tombol 'Enter' untuk melanjutkan\n")


if __name__ == "__main__":
    setup()
    decision = main()
    while True:
        if decision == "main":
            decision = main()
        elif decision == "admin":
            decision = admin()
        else:
            break
