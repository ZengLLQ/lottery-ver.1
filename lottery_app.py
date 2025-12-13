import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from datetime import datetime


class LotteryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DOORPRIZE - Debora x Ling-Ling's Workspace #371")

        # set fullscreen
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='#0a0a0a')

        # bind key untuk toggle fullscreen
        self.root.bind('<Escape>', lambda e: self.toggle_fullscreen())
        self.root.bind('<F11>', lambda e: self.toggle_fullscreen())

        # load data nomor yang udah dipake
        self.data_file = 'lottery_used_numbers.json'
        self.history_file = 'lottery_history.json'
        self.used_numbers = self.load_used_numbers()
        self.history = self.load_history()

        # init variables
        self.quantity_var = tk.StringVar(value='11')
        self.min_var = tk.StringVar(value='1')
        self.max_var = tk.StringVar(value='180')
        self.no_repeat_var = tk.BooleanVar(value=False)
        self.is_generating = False
        self.history_window = None  # track history window

        self.setup_ui()

    def toggle_fullscreen(self):
        current = self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', not current)

    def load_used_numbers(self):
        # load dari file json
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_used_numbers(self):
        # save ke file json
        with open(self.data_file, 'w') as f:
            json.dump(self.used_numbers, f)

    def load_history(self):
        # load history dari file json
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_history(self):
        # save history ke file json
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)

    def add_to_history(self, numbers, no_repeat):
        # tambah ke history
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {
            "timestamp": timestamp,
            "numbers": numbers,
            "no_repeat": no_repeat,
            "quantity": len(numbers),
            "max_value": int(self.max_var.get())
        }
        self.history.append(entry)
        self.save_history()

        # auto refresh history window jika sedang terbuka
        if self.history_window and self.history_window.winfo_exists():
            self.refresh_history_window()

    def setup_ui(self):
        # main frame dark theme
        main_frame = tk.Frame(self.root, bg='#1c1c1e')
        main_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        # title
        title_label = tk.Label(
            main_frame,
            text="DOORPRIZE",
            font=('Montserrat', 56, 'bold'),
            bg='#1c1c1e',
            fg='#ffffff'
        )
        title_label.pack(pady=30)

        # frame input
        input_frame = tk.Frame(main_frame, bg='#1c1c1e')
        input_frame.pack(pady=20)

        # quantity input
        qty_frame = tk.Frame(input_frame, bg='#1c1c1e')
        qty_frame.grid(row=0, column=0, padx=30)
        tk.Label(
            qty_frame,
            text="Quantity:",
            font=('Montserrat', 16),
            bg='#1c1c1e',
            fg='#ffffff'
        ).pack()

        qty_entry = tk.Entry(
            qty_frame,
            textvariable=self.quantity_var,
            font=('Montserrat', 20),
            width=10,
            justify='center',
            relief='flat',
            bg='#2c2c2e',
            fg='#ffffff',
            borderwidth=0,
            highlightthickness=1,
            highlightbackground='#3a3a3c',
            highlightcolor='#0a84ff',
            insertbackground='#ffffff'
        )
        qty_entry.pack(pady=5, ipady=8)

        # total kupon input
        max_frame = tk.Frame(input_frame, bg='#1c1c1e')
        max_frame.grid(row=0, column=1, padx=30)
        tk.Label(
            max_frame,
            text="Total Kupon:",
            font=('Montserrat', 16),
            bg='#1c1c1e',
            fg='#ffffff'
        ).pack()

        max_entry = tk.Entry(
            max_frame,
            textvariable=self.max_var,
            font=('Montserrat', 20),
            width=10,
            justify='center',
            relief='flat',
            bg='#2c2c2e',
            fg='#ffffff',
            borderwidth=0,
            highlightthickness=1,
            highlightbackground='#3a3a3c',
            highlightcolor='#0a84ff',
            insertbackground='#ffffff'
        )
        max_entry.pack(pady=5, ipady=8)

        # checkbox tanpa pengulangan
        checkbox_frame = tk.Frame(main_frame, bg='#1c1c1e')
        checkbox_frame.pack(pady=15)

        check_style = ttk.Style()
        check_style.configure(
            'Dark.TCheckbutton',
            font=('Montserrat', 14),
            background='#1c1c1e',
            foreground='#ffffff'
        )

        no_repeat_check = ttk.Checkbutton(
            checkbox_frame,
            text="Tanpa Pengulangan",
            variable=self.no_repeat_var,
            style='Dark.TCheckbutton'
        )
        no_repeat_check.pack()

        # button generate
        self.generate_btn = tk.Button(
            main_frame,
            text="UNDI",
            font=('Montserrat', 18, 'bold'),
            bg='#a59ed6',
            fg='#1c1c1e',
            width=15,
            height=2,
            cursor='hand2',
            relief='flat',
            borderwidth=0,
            activebackground='#9589cc',
            activeforeground='#1c1c1e',
            command=self.start_generate_animation
        )
        self.generate_btn.pack(pady=20)

        # frame hasil
        self.result_frame = tk.Frame(main_frame, bg='#1c1c1e')
        self.result_frame.pack(pady=20, fill='both', expand=True)

        # canvas untuk scroll (tanpa scrollbar visible)
        self.result_canvas = tk.Canvas(
            self.result_frame,
            bg='#1c1c1e',
            highlightthickness=0
        )
        self.result_canvas.pack(fill='both', expand=True)

        # bind mouse wheel untuk scroll di result area
        def on_result_mousewheel(event):
            self.result_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.result_canvas.bind_all("<MouseWheel>", on_result_mousewheel)

        # container untuk grid nomor
        self.numbers_container = tk.Frame(self.result_canvas, bg='#1c1c1e')
        self.result_canvas_window = self.result_canvas.create_window(
            (self.result_canvas.winfo_width() // 2, 0),
            window=self.numbers_container,
            anchor='n'
        )

        # update canvas saat resize
        def configure_result_canvas(event):
            self.result_canvas.coords(self.result_canvas_window, event.width // 2, 0)

        self.result_canvas.bind('<Configure>', configure_result_canvas)

        # bottom buttons
        bottom_frame = tk.Frame(main_frame, bg='#1c1c1e')
        bottom_frame.pack(side='bottom', pady=10)

        # history button
        history_btn = tk.Button(
            bottom_frame,
            text="HISTORY",
            font=('Montserrat', 13),
            bg='#a59ed6',
            fg='#1c1c1e',
            width=15,
            cursor='hand2',
            relief='flat',
            borderwidth=0,
            activebackground='#9589cc',
            activeforeground='#1c1c1e',
            command=self.show_history
        )
        history_btn.pack(side='left', padx=10, ipady=5)

        # reset button
        reset_btn = tk.Button(
            bottom_frame,
            text="RESET DATA",
            font=('Montserrat', 13),
            bg='#a59ed6',
            fg='#1c1c1e',
            width=15,
            cursor='hand2',
            relief='flat',
            borderwidth=0,
            activebackground='#9589cc',
            activeforeground='#1c1c1e',
            command=self.reset_data
        )
        reset_btn.pack(side='left', padx=10, ipady=5)

        # info label
        self.info_label = tk.Label(
            bottom_frame,
            text="",
            font=('Montserrat', 11),
            bg='#1c1c1e',
            fg='#8e8e93'
        )
        self.info_label.pack(side='left', padx=10)

        # tombol exit
        exit_btn = tk.Button(
            bottom_frame,
            text="EXIT (ESC)",
            font=('Montserrat', 13),
            bg='#a59ed6',
            fg='#1c1c1e',
            width=15,
            cursor='hand2',
            relief='flat',
            borderwidth=0,
            activebackground='#9589cc',
            activeforeground='#1c1c1e',
            command=self.root.quit
        )
        exit_btn.pack(side='left', padx=10, ipady=5)

        self.update_info()

    def update_info(self):
        # update info label
        if self.no_repeat_var.get():
            try:
                min_val = 1
                max_val = int(self.max_var.get())
                total_numbers = max_val - min_val + 1
                used_count = len(self.used_numbers)
                remaining = total_numbers - used_count
                self.info_label.config(
                    text=f"Angka terpakai: {used_count} | Sisa: {remaining}/{total_numbers}"
                )
            except:
                self.info_label.config(text="")
        else:
            self.info_label.config(text="")

    def show_history(self):
        # jika window sudah ada dan masih terbuka, focus aja
        if self.history_window and self.history_window.winfo_exists():
            self.history_window.focus()
            return

        # window untuk history
        self.history_window = tk.Toplevel(self.root)
        self.history_window.title("History Pengundian")
        self.history_window.attributes('-fullscreen', True)
        self.history_window.configure(bg='#1c1c1e')

        # bind key untuk toggle fullscreen di history window
        self.history_window.bind('<Escape>', lambda e: self.close_history_window())
        self.history_window.bind('<F11>', lambda e: self.toggle_history_fullscreen())

        # bind saat window ditutup
        self.history_window.protocol("WM_DELETE_WINDOW", self.close_history_window)

        # title
        title_label = tk.Label(
            self.history_window,
            text="HISTORY PENGUNDIAN",
            font=('Montserrat', 28, 'bold'),
            bg='#1c1c1e',
            fg='#ffffff'
        )
        title_label.pack(pady=15)

        # frame untuk scrollable list
        self.history_list_frame = tk.Frame(self.history_window, bg='#1c1c1e')
        self.history_list_frame.pack(fill='both', expand=True, padx=20, pady=5)

        # canvas untuk scroll (tanpa scrollbar visible)
        self.history_canvas = tk.Canvas(
            self.history_list_frame,
            bg='#1c1c1e',
            highlightthickness=0
        )
        self.history_canvas.pack(fill='both', expand=True)

        # bind mouse wheel untuk scroll
        def on_mousewheel(event):
            self.history_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.history_canvas.bind_all("<MouseWheel>", on_mousewheel)

        # frame di dalam canvas
        self.history_content_frame = tk.Frame(self.history_canvas, bg='#1c1c1e')
        self.history_canvas.create_window((0, 0), window=self.history_content_frame, anchor='nw')

        # populate history
        self.populate_history_content()

        # button frame
        btn_frame = tk.Frame(self.history_window, bg='#1c1c1e')
        btn_frame.pack(pady=10)

        # clear history button
        clear_btn = tk.Button(
            btn_frame,
            text="CLEAR HISTORY",
            font=('Montserrat', 14, 'bold'),
            bg='#a59ed6',
            fg='#1c1c1e',
            width=20,
            cursor='hand2',
            relief='flat',
            borderwidth=0,
            activebackground='#9589cc',
            activeforeground='#1c1c1e',
            command=self.clear_history
        )
        clear_btn.pack(side='left', padx=10, ipady=10)

        # close button
        close_btn = tk.Button(
            btn_frame,
            text="TUTUP (ESC)",
            font=('Montserrat', 14, 'bold'),
            bg='#a59ed6',
            fg='#1c1c1e',
            width=20,
            cursor='hand2',
            relief='flat',
            borderwidth=0,
            activebackground='#9589cc',
            activeforeground='#1c1c1e',
            command=self.close_history_window
        )
        close_btn.pack(side='left', padx=10, ipady=10)

    def toggle_history_fullscreen(self):
        if self.history_window:
            current = self.history_window.attributes('-fullscreen')
            self.history_window.attributes('-fullscreen', not current)

    def close_history_window(self):
        # tutup history window
        if self.history_window:
            self.history_window.destroy()
            self.history_window = None

    def populate_history_content(self):
        # clear existing content
        for widget in self.history_content_frame.winfo_children():
            widget.destroy()

        # tampilkan history
        if not self.history:
            no_data_label = tk.Label(
                self.history_content_frame,
                text="Belum ada history pengundian",
                font=('Montserrat', 14),
                bg='#1c1c1e',
                fg='#8e8e93'
            )
            no_data_label.pack(pady=50)
        else:
            # tampilkan dari yang terbaru
            for idx, entry in enumerate(reversed(self.history)):
                # hitung nomor pengundian dari belakang
                draw_number = len(self.history) - idx

                # nomor yang diundi
                numbers_text = ', '.join(map(str, entry['numbers']))

                # frame untuk satu entry
                entry_frame = tk.Frame(
                    self.history_content_frame,
                    bg='#2c2c2e',
                    highlightbackground='#3a3a3c',
                    highlightthickness=2
                )
                entry_frame.pack(fill='x', padx=20, pady=8)

                # container untuk label dengan mixed font
                label_container = tk.Frame(entry_frame, bg='#2c2c2e')
                label_container.pack(fill='x', padx=25, pady=18)

                # label "Pengundian Ke-X" dengan bold dan warna #a59ed6
                title_label = tk.Label(
                    label_container,
                    text=f"Pengundian Ke-{draw_number} :",
                    font=('Montserrat', 32, 'bold'),
                    bg='#2c2c2e',
                    fg='#a59ed6'
                )
                title_label.pack(side='left')

                # label angka tanpa bold
                numbers_label = tk.Label(
                    label_container,
                    text=f" {numbers_text}",
                    font=('Montserrat', 32),
                    bg='#2c2c2e',
                    fg='#ffffff'
                )
                numbers_label.pack(side='left')

        # update scroll region
        self.history_content_frame.update_idletasks()
        self.history_canvas.config(scrollregion=self.history_canvas.bbox('all'))

    def refresh_history_window(self):
        # refresh content di history window yang sudah terbuka
        if self.history_window and self.history_window.winfo_exists():
            self.populate_history_content()

    def clear_history(self):
        # clear history
        if not self.history:
            return

        response = messagebox.askyesno(
            "Konfirmasi Clear History",
            f"Apakah Anda yakin ingin menghapus semua history?\n\n"
            f"Total: {len(self.history)} pengundian akan dihapus.",
            icon='warning',
            parent=self.history_window
        )

        if response:
            self.history = []
            self.save_history()
            # refresh tampilan history tanpa popup
            if self.history_window and self.history_window.winfo_exists():
                self.populate_history_content()

    def start_generate_animation(self):
        # mulai animasi loading
        if self.is_generating:
            return

        # validasi input
        try:
            quantity = int(self.quantity_var.get())
            max_val = int(self.max_var.get())

            if max_val <= 1:
                messagebox.showerror("Error", "Total Kupon harus lebih dari 1!")
                return

            if quantity <= 0:
                messagebox.showerror("Error", "Quantity harus lebih dari 0!")
                return

            total_numbers = max_val

            if quantity > total_numbers:
                messagebox.showerror("Error", f"Quantity tidak boleh lebih dari {total_numbers}!")
                return

            # cek nomor tersedia untuk mode no repeat
            if self.no_repeat_var.get():
                all_numbers = set(range(1, max_val + 1))
                available = list(all_numbers - set(self.used_numbers))

                if len(available) < quantity:
                    response = messagebox.askyesno(
                        "Angka Habis!",
                        f"Hanya tersisa {len(available)} angka.\n\n"
                        "Apakah Anda ingin mereset data dan mulai dari awal?",
                        icon='warning'
                    )
                    if response:
                        self.reset_data()
                        # tidak otomatis undi lagi, user harus klik manual
                    return
        except ValueError:
            messagebox.showerror("Error", "Masukkan angka yang valid!")
            return

        self.is_generating = True

        # disable button
        self.generate_btn.config(state='disabled', bg='#5a5a5c')

        # clear previous results
        for widget in self.numbers_container.winfo_children():
            widget.destroy()

        # show loading
        self.show_loading_animation()

        # generate setelah 2 detik
        self.root.after(2000, self.finish_generate_animation)

    def show_loading_animation(self):
        # loading animation
        loading_container = tk.Frame(self.numbers_container, bg='#1c1c1e')
        loading_container.pack(expand=True)

        # canvas untuk spinner
        self.spinner_canvas = tk.Canvas(
            loading_container,
            width=80,
            height=80,
            bg='#1c1c1e',
            highlightthickness=0
        )
        self.spinner_canvas.pack(pady=20)

        # loading text
        loading_label = tk.Label(
            loading_container,
            text="MENGUNDI",
            font=('Montserrat', 32, 'bold'),
            bg='#1c1c1e',
            fg='#ffffff'
        )
        loading_label.pack()

        # start spinner
        self.spinner_angle = 0
        self.animate_spinner()
        self.animate_loading_text(loading_label, 0)

    def animate_spinner(self):
        # rotate spinner
        if not self.is_generating:
            return

        self.spinner_canvas.delete("all")

        # draw rotating arc
        self.spinner_canvas.create_arc(
            10, 10, 70, 70,
            start=self.spinner_angle,
            extent=280,
            outline='#ffffff',
            width=4,
            style='arc'
        )

        # update angle
        self.spinner_angle = (self.spinner_angle + 15) % 360

        # continue animation
        if self.is_generating:
            self.root.after(50, self.animate_spinner)

    def animate_loading_text(self, label, dots):
        # animate dots
        if not self.is_generating:
            return

        texts = ["MENGUNDI", "MENGUNDI.", "MENGUNDI..", "MENGUNDI..."]
        label.config(text=texts[dots % 4])

        # continue
        if self.is_generating:
            self.root.after(400, lambda: self.animate_loading_text(label, dots + 1))

    def finish_generate_animation(self):
        # selesai loading
        self.is_generating = False

        # enable button
        self.generate_btn.config(state='normal', bg='#a59ed6')

        # generate
        self.generate_numbers()

    def generate_numbers(self):
        # generate random numbers
        try:
            quantity = int(self.quantity_var.get())
            min_val = 1
            max_val = int(self.max_var.get())

            # basic validation
            if min_val >= max_val:
                return

            if quantity <= 0:
                return

            total_numbers = max_val - min_val + 1

            if quantity > total_numbers:
                return

            # generate sesuai mode
            if self.no_repeat_var.get():
                # no repeat mode
                all_numbers = set(range(min_val, max_val + 1))
                available = list(all_numbers - set(self.used_numbers))

                # random sample
                generated = random.sample(available, quantity)
                generated.sort()

                # save ke used numbers
                self.used_numbers.extend(generated)
                self.save_used_numbers()
            else:
                # dengan pengulangan
                generated = [random.randint(min_val, max_val) for _ in range(quantity)]
                generated.sort()

            # save ke history
            self.add_to_history(generated, self.no_repeat_var.get())

            # display hasil
            self.display_numbers_grid(generated)

            # update info
            self.update_info()

        except ValueError:
            messagebox.showerror("Error", "Masukkan angka yang valid!")

    def display_numbers_grid(self, numbers):
        # display dalam bentuk grid
        for widget in self.numbers_container.winfo_children():
            widget.destroy()

        total = len(numbers)

        # tentukan jumlah kolom
        if total <= 12:
            max_cols = 4
        elif total <= 24:
            max_cols = 6
        elif total <= 40:
            max_cols = 8
        else:
            max_cols = 10

        # wrapper untuk center grid
        grid_wrapper = tk.Frame(self.numbers_container, bg='#1c1c1e')
        grid_wrapper.pack(expand=True, pady=20)

        # calculate rows
        rows = (total + max_cols - 1) // max_cols

        # create grid
        for idx, num in enumerate(numbers):
            row = idx // max_cols
            col = idx % max_cols

            # center last row jika tidak penuh
            items_in_row = total - (row * max_cols)
            if items_in_row < max_cols and row == rows - 1:
                col_offset = (max_cols - items_in_row) // 2
                actual_col = col + col_offset
            else:
                actual_col = col

            # frame per nomor
            box_frame = tk.Frame(
                grid_wrapper,
                bg='#2c2c2e',
                highlightbackground='#3a3a3c',
                highlightthickness=1
            )
            box_frame.grid(row=row, column=actual_col, padx=15, pady=15)

            # label nomor
            num_label = tk.Label(
                box_frame,
                text=str(num),
                font=('BBH Hegarty', 70, 'bold'),
                bg='#2c2c2e',
                fg='#ffffff',
                width=5,
                height=1
            )
            num_label.pack(padx=35, pady=30)

        # update scroll region setelah grid dibuat
        self.numbers_container.update_idletasks()
        self.result_canvas.config(scrollregion=self.result_canvas.bbox('all'))

    def reset_data(self):
        # reset used numbers
        response = messagebox.askyesno(
            "Konfirmasi Reset",
            "Apakah Anda yakin ingin mereset semua data?\n\n"
            "Semua angka yang sudah digunakan akan dihapus.",
            icon='warning'
        )

        if response:
            self.used_numbers = []
            self.save_used_numbers()

            # clear display
            for widget in self.numbers_container.winfo_children():
                widget.destroy()

            self.update_info()


def main():
    root = tk.Tk()
    app = LotteryApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()