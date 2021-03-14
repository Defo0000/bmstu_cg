from tkinter import *
from tkinter import messagebox as mb
import tkinter.ttk as ttk
from math import *

x = []
y = []

WIDTH = 1000
HEIGHT = 400
R = 20

i = 0

#Нахождение максимального расстояния
def find_max_dist():
    
    max_dist = -1
    dist_points = [0, 0, 0, 0, 0]
    ans_x = []
    ans_y = []
    pos = []

    for a in range(len(x)):
        for b in range(a+1, len(x)):
            for c in range(b+1, len(x)):
                side_ab = sqrt((x[a] - x[b]) ** 2 + (y[a] - y[b]) ** 2)
                side_bc = sqrt((x[c] - x[b]) ** 2 + (y[c] - y[b]) ** 2)
                side_ca = sqrt((x[a] - x[c]) ** 2 + (y[a] - y[c]) ** 2)
                if (side_ab + side_bc) > side_ca and (side_ab + side_ca) > side_bc and (side_ca + side_bc) > side_ab:
                    
                    a_1 = y[a] - y[b]
                    a_2 = y[b] - y[c]
                    b_1 = x[b] - x[a]
                    b_2 = x[c] - x[b]
                    c_1 = x[a]*y[b]-x[b]*y[a]
                    c_2 = x[b]*y[c]-x[c]*y[b]

                    if y[a] != y[b] and y[b] != y[c]:

                        k1 = (x[a]-x[b])/(y[b]-y[a])
                        k2 = (x[b]-x[c])/(y[c]-y[b])

                        x_dist = (y[a]-y[c]+k1*x[c]-k2*x[a])/(k1-k2)
                        y_dist = k1 * (x_dist - x[c]) + y[c]

                    elif y[a] != y[c] and y[c] != y[b]:

                        k1 = (x[a]-x[c])/(y[c]-y[a])
                        k2 = (x[c]-x[b])/(y[b]-y[c])

                        x_dist = (y[a]-y[b]+k1*x[b]-k2*x[a])/(k1-k2)
                        y_dist = k1 * (x_dist - x[b]) + y[b]
                        
                    else: #bac
                        
                        k1 = (x[b]-x[a])/(y[a]-y[b])
                        k2 = (x[a]-x[c])/(y[c]-y[a])

                        x_dist = (y[b]-y[c]+k1*x[c]-k2*x[b])/(k1-k2)
                        y_dist = k1 * (x_dist - x[c]) + y[c]

                        

                    dist = sqrt(x_dist ** 2 + y_dist ** 2)
                    
                    if dist > max_dist:
                        max_dist = dist
                        dist_points[0] = a
                        dist_points[1] = b
                        dist_points[2] = c
                        dist_points[3] = x_dist
                        dist_points[4] = y_dist

    if max_dist != -1:
        pos.append(dist_points[0])
        pos.append(dist_points[1])
        pos.append(dist_points[2])
        
        ans_x.append(x[dist_points[0]])
        ans_x.append(x[dist_points[1]])
        ans_x.append(x[dist_points[2]])
        ans_y.append(y[dist_points[0]])
        ans_y.append(y[dist_points[1]])
        ans_y.append(y[dist_points[2]])
        ans_x.append(dist_points[3])
        ans_y.append(dist_points[4])

    return ans_x, ans_y, pos, max_dist

def draw_plot(ans_x, ans_y, pos, max_dist):
    X_C = WIDTH//2 + R
    Y_C = HEIGHT//2 + R

    #Определяем уровень ОХ, возможны 3 случая
    if min(ans_y) >= 0:
        Y_C = HEIGHT+R
        cnv.create_line(0, HEIGHT + R, WIDTH + 2*R, HEIGHT + R, arrow=BOTH, width=3)
    elif max(ans_y) <= 0:
        Y_C = R
        cnv.create_line(0, R, WIDTH + 2*R, R, arrow=BOTH, width=3)
    else:
        k = max(ans_y)/abs(max(ans_y) - min(ans_y))
        k = ceil((HEIGHT) * k)
        Y_C = k + R
        cnv.create_line(0, k + R, WIDTH + 2*R, k + R, arrow=BOTH, width=3)

    #Определяем уровень ОУ, возможны 3 случая
    if min(ans_x) >=0:
        X_C = R
        cnv.create_line(R, 0, R, HEIGHT + 2*R, arrow=BOTH, width=3)
    elif max(ans_x) <= 0:
        X_C = WIDTH + R
        cnv.create_line(WIDTH+R, 0, WIDTH+R, HEIGHT+2*R, arrow=BOTH, width=3)
    else:
        k = max(ans_x)/abs(max(ans_x) - min(ans_x))
        k = WIDTH - ceil((WIDTH) * k)
        X_C = k + R
        cnv.create_line(k+R, 0, k+R, HEIGHT+2*R, arrow=BOTH, width=3)

    if min(ans_x) > 0:
        w = max(ans_x)
    elif abs(max(ans_x)-min(ans_x)):
        w = abs(max(ans_x)-min(ans_x))
    else:
        w = abs(max(ans_x))

    if min(ans_y) > 0:
        h = max(ans_y)
    elif abs(max(ans_y)-min(ans_y)):
        h = abs(max(ans_y)-min(ans_y))
    else:
        h = abs(max(ans_y))

    #Сетка

    step = int(w / 10)
    step = step / w * WIDTH

    if step:
        
        temp = X_C
        while (temp <= WIDTH):
            cnv.create_line(temp, R, temp, HEIGHT + R, fill='#9ad2fc')
            cnv.create_text(temp, Y_C - R, text=str("%.2f" % ((temp - X_C) * w / WIDTH)))
            temp += step
        temp = X_C
        while (temp >= 0):
            cnv.create_line(temp, R, temp, HEIGHT + R, fill='#9ad2fc')
            cnv.create_text(temp, Y_C - R, text=str("%.2f" % ((temp - X_C) * w / WIDTH)))
            temp -= step

    step = int(h/10)
    step = step / h * HEIGHT

    if step:
    
        temp = Y_C
        while (temp > 0):
            cnv.create_line(R, temp, WIDTH + R, temp, fill='#9ad2fc')
            cnv.create_text(X_C + 2*R, temp, text=str("%.2f" % (-(temp - Y_C) * h / HEIGHT)))
            temp -= step

        temp = Y_C
        while (temp <= HEIGHT):
            cnv.create_line(R, temp, WIDTH+R, temp, fill='#9ad2fc')
            cnv.create_text(X_C + 2*R, temp, text=str("%.2f" % (-(temp - Y_C) * h / HEIGHT)))
            temp += step
        
    
    for j in range(len(ans_x)):
        x_j = X_C + ans_x[j] / w * WIDTH
        y_j = Y_C - ans_y[j] / h * HEIGHT
        cnv.create_oval(x_j - 4, y_j - 4, x_j + 4, y_j + 4, fill="lightgreen")


    x_ = X_C + ans_x[0] / w * WIDTH
    x__ = X_C + ans_x[1] / w * WIDTH
    y_ = Y_C - ans_y[0] / h * HEIGHT
    y__ = Y_C - ans_y[1] / h * HEIGHT
                    
    cnv.create_line(x_, y_, x__, y__, fill="red", width=2)
    
    cnv.create_text(x_, y_, text = "A("+str("%.2f" % (ans_x[0]))+";"+str("%.2f" % (ans_y[0]))+")", font = 16)
    cnv.create_text(x__, y__, text = "B("+str("%.2f" % (ans_x[1]))+";"+str("%.2f" % (ans_y[1]))+")", font = 16)

    x_ = X_C + ans_x[1] / w * WIDTH
    x__ = X_C + ans_x[2] / w * WIDTH
    y_ = Y_C - ans_y[1] / h * HEIGHT
    y__ = Y_C - ans_y[2] / h * HEIGHT

    cnv.create_text(x__, y__, text = "C("+str("%.2f" % (ans_x[2]))+";"+str("%.2f" % (ans_y[2]))+")", font = 16)
        
    cnv.create_line(x_, y_, x__, y__, fill="red", width=2)

    x_ = X_C + ans_x[0] / w * WIDTH
    x__ = X_C + ans_x[2] / w * WIDTH
    y_ = Y_C - ans_y[0] / h * HEIGHT
    y__ = Y_C - ans_y[2] / h * HEIGHT
        
    cnv.create_line(x_, y_, x__, y__, fill="red", width=2)


    x_ = X_C + ans_x[3] / w * WIDTH
    y_ = Y_C - ans_y[3] / h * HEIGHT

    cnv.create_text(x_, y_, text = "D("+str("%.2f" % (ans_x[3]))+";"+str("%.2f" % (ans_y[3]))+")", font = 16)
        
    cnv.create_line(x_, y_, X_C, Y_C, fill="green", width=3)

    answer_label["text"] = "Результат:\nВершины:\n[№"+str(pos[0] + 1)+"]A("+str("%.2f" % (ans_x[0]))+";"+str("%.2f" % (ans_y[0]))+\
                               ")\n[№"+str(pos[1] + 1)+"]B(" + str("%.2f" % (ans_x[1]))+";"+str("%.2f" % (ans_y[1]))+ ")\n[№"+str(pos[2] + 1)+"]C("+\
                               str("%.2f" % (ans_x[2]))+";"+str("%.2f" % (ans_y[2]))+")\n"+\
                               "Точка пересечения: \nD(" + str("%.2f" % (ans_x[3]))+";"+str("%.2f" % (ans_y[3]))+ \
                               ")\nРасстояние: " + str("%.2f" % (max_dist))

#Отрисовка всех точек
def draw(event):
    cnv.delete("all")

    ans_x = []
    ans_y = []
    pos = []
    max_dist = -1

    ans_x, ans_y, pos, max_dist = find_max_dist()

    if max_dist != -1:
        draw_plot(ans_x, ans_y, pos, max_dist)
    else:
         mb.showerror(title = "Ошибка", message = "Ни одна тройка чисел не образует треугольник.")


def info(event):
    mb.showinfo(title="Справка о программе", message="Автор программы: Сироткина Полина, ИУ7-46\nДата: 22.02.2021\n\n"
                "Задача, решаемая программой: из заданного на плоскости множества точек найти треугольник, у которого расстояние от "
                "начала системы координат до точки пересечения высот максимальное.\n\nСоветы:\n\n"
                "• Для того, чтобы запустить расчет, сначала необходимо ввести все точки, а затем нажать кнопку Вычислить.\n\n"
                "• После редактирования точек необходимо заново нажать кнопку Вычислить, чтобы увидеть результат.")

#Ввод данных
def entry(event):
    temp_x = x_entry.get()
    temp_y = y_entry.get()
    flag = 0
    try:
        temp_x = float(temp_x)
    except:
        if not x:
            mb.showerror(title = "Ошибка", message = "Ошибка ввода в поле X: пустое поле ввода.")
        else:
            mb.showerror(title = "Ошибка", message = "Ошибка ввода в поле X: должно быть введено вещественное число.")
        flag = 1
    if not flag:
        try:
            temp_y = float(temp_y)
            x.append(temp_x)
            y.append(temp_y)
        except:
            if not y:
                mb.showerror(title = "Ошибка", message = "Ошибка ввода в поле X: пустое поле ввода.")
            else:
                mb.showerror(title = "Ошибка", message = "Ошибка ввода в поле Y: должно быть введено вещественное число.")
    x_entry.delete(0, END)
    y_entry.delete(0, END)
    add_data()

#Изменения таблицы
def del_all(event):
    n = len(x)
    x.clear()
    y.clear()
    global i
    i = 0
    for i in range(n):
        table.delete(i)
    cnv.delete("all")
    draw_sheet()

def edit_item(event):
    row = row_entry.get()
    temp_x = xvalue_entry.get()
    temp_y = yvalue_entry.get()
    flag = 0
    try:
        row = int(row)
        if row <= 0:
            flag = 1
            mb.showerror(title = "Ошибка", message = "Ошибка ввода в поле ввода номера строки: должно быть введено положительное число.")
        if row > len(x):
            flag = 1
            mb.showerror(title = "Ошибка", message = "Ошибка ввода в поле ввода номера строки: превышен максимально допустимый номер.")
    except:
        flag = 1
        mb.showerror(title = "Ошибка", message = "Ошибка ввода в поле ввода номера строки:"
                     " должно быть введено целое положительное число, не превышающиее количество действительно введенных строк.")
    if not flag:
        try:
            temp_x = float(temp_x)
        except:
            if not temp_x:
                mb.showerror(title = "Ошибка", message = "Ошибка ввода в поле X: пустое поле ввода.")
            else:
                mb.showerror(title = "Ошибка", message = "Ошибка ввода в поле X: должно быть введено вещественное число.")
            flag = 1
        if not flag:
            try:
                temp_y = float(temp_y)
            except:
                flag = 1
                if not temp_y:
                    mb.showerror(title = "Ошибка", message = "Ошибка ввода в поле Y: пустое поле ввода.")
                else:
                    mb.showerror(title = "Ошибка", message = "Ошибка ввода в поле Y: должно быть введено вещественное число.")
    if not flag:
        x[row-1] = temp_x
        y[row-1] = temp_y
        edit_row(row)
    xvalue_entry.delete(0, END)
    yvalue_entry.delete(0, END)
    row_entry.delete(0, END)

def edit_row(row):
    row -= 1
    table.item(row, values=[row+1, str(x[row]), str(y[row])])

def del_item(event):
    row = del_entry.get()
    flag = 0
    global i
    try:
        row = int(row)
        if row <= 0:
            flag = 1
            mb.showerror(title = "Ошибка", message = "Ошибка ввода в поле ввода номера строки: должно быть введено положительное число.")
        if row > len(x):
            flag = 1
            mb.showerror(title = "Ошибка", message = "Ошибка ввода в поле ввода номера строки: превышен максимально допустимый номер.")
    except:
        flag = 1
        mb.showerror(title = "Ошибка", message = "Ошибка ввода в поле ввода номера строки:"
                     " должно быть введено целое положительное число, не превышающиее количество действительно введенных строк.")
    del_entry.delete(0, END)
    if not flag:
        for k in range(len(x)):
            table.delete(k)
        for k in range(row, len(x) - 1):
            x[k] = x[k+1]
            y[k] = y[k+1]
        x.pop()
        y.pop()
        i -= 1
        for k in range(len(x)):
            table.insert('', k, k, values=[k+1, str(x[k]), str(y[k])])
        

def add_data():
    global i
    table.insert('', i, i, values=[i+1, str(x[i]), str(y[i])])
    i += 1


##
#Тестирование
##

def rectangle_test(event):
    n = len(x)
    x.clear()
    y.clear()
    global i
    i = 0
    for i in range(n):
        table.delete(i)
    cnv.delete("all")
    x.append(-20)
    x.append(-20)
    x.append(40)
    y.append(20)
    y.append(-30)
    y.append(20)
    i = 3
    for k in range(3):
        table.insert("", k, k, values = [k + 1, str(x[k]), str(y[k])])

    ans_x = []
    ans_y = []
    pos = []
    max_dist = -1

    ans_x, ans_y, pos, max_dist = find_max_dist()

    draw_plot(ans_x, ans_y, pos, max_dist)

def rectangle_test(event):
    n = len(x)
    x.clear()
    y.clear()
    global i
    i = 0
    for i in range(n):
        table.delete(i)
    cnv.delete("all")
    x.append(-20)
    x.append(-20)
    x.append(40)
    y.append(20)
    y.append(-30)
    y.append(20)
    i = 3
    for k in range(3):
        table.insert("", k, k, values = [k + 1, str(x[k]), str(y[k])])

    ans_x = []
    ans_y = []
    pos = []
    max_dist = -1

    ans_x, ans_y, pos, max_dist = find_max_dist()

    draw_plot(ans_x, ans_y, pos, max_dist)

def oxygon_test(event):
    n = len(x)
    x.clear()
    y.clear()
    global i
    i = 0
    for i in range(n):
        table.delete(i)
    cnv.delete("all")
    x.append(20)
    x.append(80)
    x.append(70)
    y.append(30)
    y.append(50)
    y.append(70)
    i = 3
    for k in range(3):
        table.insert("", k, k, values = [k + 1, str(x[k]), str(y[k])])

    ans_x = []
    ans_y = []
    pos = []
    max_dist = -1

    ans_x, ans_y, pos, max_dist = find_max_dist()

    draw_plot(ans_x, ans_y, pos, max_dist)

def obtuse_test(event):
    n = len(x)
    x.clear()
    y.clear()
    global i
    i = 0
    for i in range(n):
        table.delete(i)
    cnv.delete("all")
    x.append(-40)
    x.append(60)
    x.append(20)
    y.append(-20)
    y.append(0)
    y.append(30)
    i =3
    for k in range(3):
        table.insert("", k, k, values = [k + 1, str(x[k]), str(y[k])])

    ans_x = []
    ans_y = []
    pos_x = []
    pos_y = []
    max_dist = -1

    ans_x, ans_y, pos, max_dist = find_max_dist()

    draw_plot(ans_x, ans_y, pos, max_dist)
    

def open_window(event):
    top_window = Tk()
    top_window.title("Тестирование программы")

    top_window.wm_geometry("+%d+%d" % (450, 200))
    
    rectangle_btn = Button(top_window, text = "Прямоугольный треугольник", width=30, font = ("segoe print", 11), bg = "#ffffff", relief=GROOVE, activebackground = "#ffffff")
    rectangle_btn.bind("<Button-1>", rectangle_test)
    rectangle_btn.grid(row = 0, column = 0)

    oxygon_btn = Button(top_window, text = "Остроугольный треугольник", width=30, font = ("segoe print", 11), bg = "#ffffff", relief=GROOVE, activebackground = "#ffffff")
    oxygon_btn.bind("<Button-1>", oxygon_test)
    oxygon_btn.grid(row = 1, column = 0)

    obtuse_btn = Button(top_window, text = "Тупоугольный треугольник", width=30, font = ("segoe print", 11), bg = "#ffffff", relief=GROOVE, activebackground = "#ffffff")
    obtuse_btn.bind("<Button-1>", obtuse_test)
    obtuse_btn.grid(row = 2, column = 0)

    quit_btn = Button(top_window, text = "Выход", width=30, font = ("segoe print", 11), bg = "#ffffff", relief=GROOVE, activebackground = "#ffffff")
    quit_btn.config(command=top_window.destroy)
    quit_btn.grid(row = 3, column = 0)
    
    top_window.mainloop()


def draw_sheet():
    
    temp = R
    count = WIDTH//50
    for k in range(count):
        cnv.create_line(temp, R, temp, HEIGHT+R, fill='#9ad2fc')
        temp += 50

    temp = R
    count = HEIGHT//50
    for k in range(count):
        cnv.create_line(R, temp, WIDTH+R, temp, fill='#9ad2fc')
        temp += 50

    cnv.create_line(WIDTH//2 + R, R, WIDTH//2 + R, HEIGHT + R, arrow=BOTH, width=3)
    cnv.create_line(R, HEIGHT//2 + R, WIDTH + R, HEIGHT//2 + R, arrow=BOTH, width=3)
    

window = Tk()

#Рисовка холста

cnv = Canvas(window, width=WIDTH+2*R, height=HEIGHT+2*R, bg='white')
cnv.grid(row = 0, column = 0, columnspan = 3)

draw_sheet()

#Рисовка поля подсказок

answer_label = Label(window, text = "Результат:\n\nОтсутствует.\nОжидается ввод данных...\n", bg="#3d3b3b", fg="white", font = ("segoe print", 11))
answer_label.grid(row = 1, column = 0, rowspan = 2)

#Рисовка таблицы

table_label = Label(window, text = "Таблица с введенными данными      ", font = ("segoe print", 11), bg="#3d3b3b", fg="white")
table_label.grid(row = 1, column = 1, columnspan=2)

table = ttk.Treeview(window, show="headings", columns=("#1", "#2", "#3"))
ysb = ttk.Scrollbar(window, orient=VERTICAL, command=table.yview)
ysb.grid(row = 2, column = 2)
table.configure(yscrollcommand=ysb.set)
table.config(height=6)
table.heading("#1", text="№")
table.heading("#2", text="X")
table.heading("#3", text="Y")
table.grid(row = 2, column = 1)

#Рисовка кнопок

btn_frame = Frame(window)
btn_frame.grid(row = 0, column = 3, rowspan=3)

x_label = Label(btn_frame, text = "X:", bd = 0.5, width = 10, justify=CENTER, bg="#3d3b3b", fg="white", relief=GROOVE)
x_label.grid(row = 0, column = 0)

x_entry = Entry(btn_frame, width=12, font = 16)
x_entry.grid(row = 0, column = 1)

y_label = Label(btn_frame, text = "Y:", bd = 0.5, width = 10, justify=CENTER, bg="#3d3b3b", fg="white", relief=GROOVE)
y_label.grid(row = 1, column = 0)

y_entry = Entry(btn_frame, width=12, font = 16)
y_entry.grid(row = 1, column = 1)

add_btn = Button(btn_frame, text="Добавить точку  ", height = 2, width=18, font = ("segoe print", 11), bg = "#ffffff", relief=GROOVE, activebackground = "#ffffff")
add_btn.bind("<Button-1>", entry)
add_btn.grid(row = 2, column = 0, columnspan = 2)

row_label = Label(btn_frame, text="№:", bd = 0.5, width = 10, justify=CENTER, bg="#3d3b3b", fg="white", relief=GROOVE)
row_label.grid(row = 3, column = 0)

row_entry = Entry(btn_frame, width=12, font = 16)
row_entry.grid(row = 3, column = 1)

xvalue_label = Label(btn_frame, text = "X:", bd = 0.5, width = 10, justify=CENTER, bg="#3d3b3b", fg="white", relief=GROOVE)
xvalue_label.grid(row = 4, column = 0)

xvalue_entry = Entry(btn_frame, width=12, font = 16)
xvalue_entry.grid(row = 4, column = 1) 

yvalue_label = Label(btn_frame, text = "Y:", bd = 0.5, width = 10, justify=CENTER, bg="#3d3b3b", fg="white", relief=GROOVE)
yvalue_label.grid(row = 5, column = 0)

yvalue_entry = Entry(btn_frame, width=12, font = 16)
yvalue_entry.grid(row = 5, column = 1) 

edit_btn = Button(btn_frame, text="Изменить точку  ", height = 1, width=18, font = ("segoe print", 11), bg = "#ffffff", relief=GROOVE, activebackground = "#ffffff")
edit_btn.bind("<Button-1>", edit_item)
edit_btn.grid(row = 6, column = 0, columnspan=2)

del_label = Label(btn_frame, text = "№:", bd = 0.5, width = 10, justify=CENTER, bg="#3d3b3b", fg="white", relief=GROOVE)
del_label.grid(row = 7, column = 0)
                  
del_entry = Entry(btn_frame, width=12, font = 16)
del_entry.grid(row = 7, column = 1)

del_btn = Button(btn_frame, text="Удалить точку  ", height = 1, width=18, font = ("segoe print", 11), bg = "#ffffff", relief=GROOVE, activebackground = "#ffffff")
del_btn.bind("<Button-1>", del_item)
del_btn.grid(row = 8, column = 0, columnspan=2)

calc_btn = Button(btn_frame, text="Вычислить  ", height = 1, width=18, font = ("segoe print", 11), bg = "#ffffff", relief=GROOVE, activebackground = "#ffffff")
calc_btn.bind("<Button-1>", draw)
calc_btn.grid(row = 9, column = 0, columnspan = 2)

test_btn = Button(btn_frame, text="Запустить тест  ", height = 1, width=18, font = ("segoe print", 11), bg = "#ffffff", relief=GROOVE, activebackground = "#ffffff")
test_btn.bind("<Button-1>", open_window)
test_btn.grid(row = 10, column = 0, columnspan = 2)

clear_btn = Button(btn_frame, text="Очистить поле  ", height = 1, width=18, font = ("segoe print", 11), bg = "#ffffff", relief=GROOVE, activebackground = "#ffffff")
clear_btn.bind("<Button-1>", del_all)
clear_btn.grid(row = 11, column = 0, columnspan = 2)

help_btn = Button(btn_frame, text="Помощь  ", height = 1, width=18, font = ("segoe print", 11), bg = "#ffffff", relief=GROOVE, activebackground = "#ffffff")
help_btn.bind("<Button-1>", info)
help_btn.grid(row = 12, column = 0, columnspan = 2)

exit_btn = Button(btn_frame, text="Выход  ", height = 1, width=18, font = ("segoe print", 11), bg = "#ffffff", relief=GROOVE, activebackground = "#ffffff")
exit_btn.config(command=window.destroy)
exit_btn.grid(row = 13, column = 0, columnspan = 2)

window.title("Лабораторная работа №1")
window["bg"] = "#3d3b3b"
window.state('zoomed')
window.mainloop()

