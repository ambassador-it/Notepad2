import tkinter as tk
from tkinter import filedialog as fd
import datetime as dt
from tkinter import messagebox as mb


class About(tk.Toplevel):
    def __init__(self):
        super(About, self).__init__()
        self.title('Блокнот: сведения')
        self.geometry('300x200')
        self.label = tk.Label(self, text='Всплывающее окно')
        self.btn = tk.Button(self, text='    OK    ', command=self.destroy)
        self.label.pack()
        self.btn.pack(anchor=tk.SE, side=tk.RIGHT, ipadx=3, pady=5, padx=5)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Блокнот')
        self.geometry('750x450')
        self.iconbitmap('ico1.ico')
        self.protocol('WM_DELETE_WINDOW', self.save_yes_no_cancel)
        self.menu = tk.Menu(self, tearoff=0)
        self.menu2 = tk.Menu(self) # То меню которое одно для всех
        #self.menu3 = tk.Menu(self)
        self.menu.add_command(label='Отменить', command=None)
        self.menu.add_separator()
        self.menu.add_command(label='Вырезать', command=self.cut_text)
        self.menu.add_command(label='Копировать', command=self.copy_text)
        self.menu.add_command(label='Вставить', command=self.paste_text)
        self.menu.add_command(label='Удалить', command=self.delete_text)
        self.submenu1 = tk.Menu(self.menu2, tearoff=0)
        self.submenu1.add_command(label='Cоздать')
        self.submenu1.add_command(label='Новое окно', command=self.create_window)
        self.submenu1.add_command(label='Сохранить', command=self.save)
        self.submenu1.add_command(label='Сохранить как', command=self.save_as)
        self.submenu1.add_separator()
        self.submenu1.add_command(label='Выход', command=self.save_yes_no_cancel)
        self.submenu2 = tk.Menu(self.menu2, tearoff=0)
        self.submenu2.add_command(label='Отменить', command=None)
        self.submenu2.add_separator()
        self.submenu2.add_command(label='Время и дата', command=self.date_insert)
        self.submenu2.add_command(label='Выделить всё')
        self.menu2.add_cascade(label='Файл', menu=self.submenu1)
        self.menu2.add_cascade(label='Правка', menu=self.submenu2)

        self.submenu3 = tk.Menu(self.menu2, tearoff=0)
        self.submenu3.add_command(label='Перенос со словами', command=None)

        self.menu2.add_cascade(label='Формат', menu=self.submenu3)
        self.menu2.add_cascade(label='Вид')


        self.submenu5 = tk.Menu(self.menu2, tearoff=0)
        self.submenu5.add_command(label='О программе', command=self.about)
        self.menu2.add_cascade(label='Справка', menu=self.submenu5)
        self.config(menu=self.menu2)
        #self.config(menu=self.menu3)

        self.yscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.xscrollbar = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.text = tk.Text(self, xscrollcommand=self.xscrollbar.set,
                            yscrollcommand=self.yscrollbar.set, wrap=tk.NONE,
                            height='1024', width='680')
        self.text.bind("<Button-3>", self.show_popup)
        self.yscrollbar.config(command=self.text.yview)
        self.xscrollbar.config(command=self.text.xview)
        # self.text.grid(row=0, column=0, sticky=tk.EW)

        self.yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        # self.scrollbar.grid(row=0, column=1, sticky=tk.NS)
        self.text.bind("<Control-Key-a>", self.select_all)
        self.text.bind("<Control-Key-A>", self.select_all)
        self.text.pack()

    def select_all(self, event):
        self.text.tag_add(tk.SEL, "1.0", tk.END)
        self.text.mark_set(tk.INSERT, "1.0")
        self.text.see(tk.INSERT)
        return 'break'

    def save_yes_no_cancel(self):
        if self.text.get(0.1, tk.END) != '\n':
            status = mb.askyesnocancel(title='Блокнот', message=f'Вы хотите сохранить изменения в файле ""?')
            if status:
                self.save()
                self.destroy()
            elif status == None:
                pass
            else:
                self.destroy()
        else:
            self.destroy()

    def date_insert(self):
        self.text.insert(tk.INSERT, str(dt.datetime.now().strftime('%H:%M %d.%m.%Y')))

    def about(self):
        about = About()
        about.grab_set()

    def select(self):
        #text = self.text.get(0.1, tk.END)
        self.widget.select_range(0, 'end')

    def save(self):

        file = fd.askopenfilename()
        text = self.text.get(0.1, tk.END)
        if text:
            file.write(text)
        file.close()

    def save_as(self):
        types = (('Текстовые документы', '.txt'), ('Все файлы', '*.*'))
        file = fd.asksaveasfile(defaultextension='.txt', filetypes=types)
        text = self.text.get(0.1, tk.END)
        if text:
            file.write(text)
        file.close()

    def show_popup(self, event):
        self.menu.post(event.x_root, event.y_root)

    def cut_text(self):
        self.copy_text()
        self.delete_text()
        print(self.clipboard_get())

    def copy_text(self):
        select = self.text.tag_ranges(tk.SEL)
        if select:
            self.clipboard_clear()
            self.clipboard_append(self.text.get(*select))

    def paste_text(self):
        self.text.insert(tk.INSERT, self.clipboard_get())

    def delete_text(self):
        select = self.text.tag_ranges(tk.SEL)
        self.text.delete(*select)

    def create_window(self):
        app = App()



if __name__ == "__main__":
    app = App()
    app.mainloop()
