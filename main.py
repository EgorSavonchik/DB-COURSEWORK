import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import psycopg2
from datetime import time
import logging

student_username = ""

class Database:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    @staticmethod
    def connect():
        return psycopg2.connect(
            dbname="db",
            user="postgres",
            password="12345678",
            host="localhost",
            port="5433"
        )

    @staticmethod
    def execute_query(query, parameters=None):
        conn = Database.connect()
        try:
            cursor = conn.cursor()
            if parameters:
                cursor.execute(query, parameters)
            else:
                cursor.execute(query)
            conn.commit()
            logging.info("Query executed successfully: %s", query)
        except Exception as e:
            logging.error("Error executing query: %s", str(e))
            messagebox.showerror("Ошибка", str(e))
        finally:
            if conn:
                conn.close()

    @staticmethod
    def fetch_data(query, parameters=None):
        conn = Database.connect()
        try:
            cursor = conn.cursor()
            if parameters:
                cursor.execute(query, parameters)
            else:
                cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
            return []
        finally:
            if conn:
                conn.close()

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.label_username = tk.Label(self, text="Логин:")
        self.label_password = tk.Label(self, text="Пароль:")

        self.entry_username = tk.Entry(self)
        self.entry_password = tk.Entry(self, show="*")

        self.label_username.grid(row=0, column=0, pady=5)
        self.entry_username.grid(row=0, column=1, pady=5)
        self.label_password.grid(row=1, column=0, pady=5)
        self.entry_password.grid(row=1, column=1, pady=5)

        self.login_button = tk.Button(self, text="Войти", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        global student_username
        student_username = username

        # Ваш код для проверки логина и пароля
        # Доступ к базе данных для проверки суперпользователя или студента
        # Проверьте роль и переключитесь на соответствующую страницу
        role = self.check_user_credentials(username, password)

        if role == "superuser":
            self.controller.show_frame(SuperuserPage)
        elif role == "student":
            self.controller.show_frame(StudentPage)  
        else:
            messagebox.showerror("Ошибка", "Неверные логин или пароль")

    def check_user_credentials(self, username, password):
        result = Database.fetch_data("SELECT get_user_role(%s, %s)", (username, password))
  
        if result != []:
            return result[0][0]
        else:
            return None

class SuperuserPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Добавьте элементы управления и логику для суперпользователя
        # Например, кнопки для создания аккаунтов, добавления преподавателей и т.д.

        # Пример кнопки для добавления пары
        add_class_button = tk.Button(self, text="Добавить пару", command=self.show_add_lesson_popup)
        add_class_button.grid(row=0, column=0, sticky="w")

        # Пример кнопки для создания аккаунта
        create_account_button = tk.Button(self, text="Создать аккаунт студента", command=self.create_account)
        create_account_button.grid(row=1, column=0, sticky="w")

        # Пример кнопки для добавления преподавателя
        add_teacher_button = tk.Button(self, text="Добавить преподавателя", command=self.show_teacher_creation_popup)
        add_teacher_button.grid(row=2, column=0, sticky="w")

        # Пример кнопки для добавления материалов курса
        add_material_button = tk.Button(self, text="Добавить курс", command=self.show_add_course_popup)
        add_material_button.grid(row=3, column=0, sticky="w")

        # Пример кнопки для добавления материалов курса
        add_material_button = tk.Button(self, text="Добавить материалы курса", command=self.show_add_material_popup)
        add_material_button.grid(row=4, column=0, sticky="w")

        course_button = tk.Button(self, text="Назначить курс", command=self.show_course_assignment_window)
        course_button.grid(row=6, column=0, sticky="w")

        # Пример кнопки для выставления оценки за экзамен
        grade_exam_button = tk.Button(self, text="Выставить оценку за экзамен", command=self.show_exam_popup)
        grade_exam_button.grid(row=7, column=0, sticky="w")

        # Пример кнопки для выставления оценки за экзамен
        group_button = tk.Button(self, text="Создать группу", command=self.show_group_creation_popup)
        group_button.grid(row=8, column=0, sticky="w")

        # Пример кнопки для выхода из аккаунта
        logout_button = tk.Button(self, text="Выйти из аккаунта", command=self.logout)
        logout_button.grid(row=9, column=0, sticky="w")

    def show_group_creation_popup(self):
        # Создайте всплывающее окно для создания преподавателя
        group_creation_popup = tk.Toplevel(self.master)
        group_creation_popup.title("Создание преподавателя")

        # Поля ввода для имени, фамилии, почты и номера телефона
        ttk.Label(group_creation_popup, text="Название группы: ").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        group_name_entry = ttk.Entry(group_creation_popup)
        group_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Кнопка для создания преподавателя
        create_button = ttk.Button(group_creation_popup, text="Создать", command=lambda: self.create_group(
            group_name_entry.get(), group_creation_popup
        ))
        create_button.grid(row=1, column=0, columnspan=2, pady=10)

    def create_group(self, group_name, group_creation_popup):
        # Ваш код для создания преподавателя (добавьте сюда вашу логику)
        print(group_name)
        Database.execute_query('INSERT INTO Groups(group_name) VALUES(%s)', (group_name,))
        # Закройте всплывающее окно после создания преподавателя
        group_creation_popup.destroy()

    def show_course_assignment_window(self):
        # Создаем всплывающее окно для назначения курса
        assignment_window = tk.Toplevel(self)
        assignment_window.title("Назначение курса")

        # Создаем селект с курсами (замените на данные из вашей базы данных)
        course_label = ttk.Label(assignment_window, text="Выберите предмет:")
        course_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        courses = self.get_subjects_from_database()
        course_var = tk.StringVar()
        course_combobox = ttk.Combobox(assignment_window, textvariable=course_var, values=courses)
        course_combobox.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Создаем селект со групами (замените на данные из вашей базы данных)
        groups_label = ttk.Label(assignment_window, text="Выберите группу:")
        groups_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        groups = self.get_group_names()
        group_var = tk.StringVar()
        group_combobox = ttk.Combobox(assignment_window, textvariable=group_var, values=groups)
        group_combobox.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Создаем селект с выбором семестра
        semester_label = ttk.Label(assignment_window, text="Выберите семестр:")
        semester_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        
        semester_var = tk.IntVar()
        semester_var.set(1)
        semester_combobox = ttk.Combobox(assignment_window, textvariable=semester_var, values=[1, 2, 3, 4, 5, 6, 7, 8])
        semester_combobox.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Кнопка для сохранения назначения курса
        save_button = ttk.Button(assignment_window, text="Сохранить", command=lambda: self.save_course_assignment(
            course_var.get(), group_var.get(), semester_var.get(), assignment_window
        ))
        save_button.grid(row=3, column=0, columnspan=2, pady=10)

    def save_course_assignment(self, course, group, semester, assignment_window):
        Database.execute_query('CALL enroll_student(%s, %s, %s)', (group, course, semester))

        assignment_window.destroy()


    def get_group_names(self):
        result = Database.fetch_data("SELECT group_name from Groups");
        result = tuple(item[0] for item in result)

        return result

    # Пример функции для получения списка предметов из базы данных
    def get_subjects_from_database(self):
        
        subjects_list = Database.fetch_data("SELECT course_name FROM Courses")
        print(subjects_list)
        return subjects_list

    # Пример функции для получения списка преподавателей из базы данных
    def get_teachers_from_database(self):
        
        teachers_list = Database.fetch_data("SELECT first_name, last_name FROM Teachers")
        print(teachers_list)
        return teachers_list

    def get_buildings_from_database(self):
        buildings_list = Database.fetch_data("SELECT building_name, room_number FROM Classrooms ")
        print(buildings_list)
        return(buildings_list)

    def show_add_lesson_popup(self):
        # Создайте всплывающее окно для добавления занятия
        self.add_lesson_popup = tk.Toplevel(self)
        self.add_lesson_popup.title("Добавить занятие")

        # Список групп (замените его на данные из вашей базы данных)
        group_list = self.get_group_names()
        subjects_list = self.get_subjects_from_database()
        teachers_list = self.get_teachers_from_database()
        building_list = self.get_buildings_from_database()

        # Создание и размещение элементов управления
        group_label = ttk.Label(self.add_lesson_popup, text="Группа:")
        group_var = tk.StringVar()
        group_combobox = ttk.Combobox(self.add_lesson_popup, textvariable=group_var, values=group_list)

        week_label = ttk.Label(self.add_lesson_popup, text="Неделя:")
        week_var = tk.IntVar()
        week_var.set(1)
        week_combobox = ttk.Combobox(self.add_lesson_popup, textvariable=week_var, values=[1, 2, 3, 4])

        day_label = ttk.Label(self.add_lesson_popup, text="День недели:")
        day_var = tk.StringVar()
        day_combobox = ttk.Combobox(self.add_lesson_popup, textvariable=day_var, values=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

        time_label = ttk.Label(self.add_lesson_popup, text="Время занятий:")
        time_var = tk.StringVar()
        time_combobox = ttk.Combobox(self.add_lesson_popup, textvariable=time_var, values=['09:00-10:20', '10:35-11:55', '12:25-13:45', '14:00-15:20', '15:50-17:10', '17:25-18:45', '19:00-20:20', '20:40-22:00'])

        subject_label = ttk.Label(self.add_lesson_popup, text="Предмет:")
        subject_var = tk.StringVar()
        subject_combobox = ttk.Combobox(self.add_lesson_popup, textvariable=subject_var, values=subjects_list)

        teacher_label = ttk.Label(self.add_lesson_popup, text="Преподаватель:")
        teacher_var = tk.StringVar()
        teacher_combobox = ttk.Combobox(self.add_lesson_popup, textvariable=teacher_var, values=teachers_list)

        couple_type_label = ttk.Label(self.add_lesson_popup, text="Тип занятия:")
        couple_type_var = tk.StringVar()
        couple_type_combobox = ttk.Combobox(self.add_lesson_popup, textvariable=couple_type_var, values=["Лекция", "Лабораторная", "Практика"])

        building_label = ttk.Label(self.add_lesson_popup, text="Здание, кабинет:")
        building_var = tk.StringVar()
        building_combobox = ttk.Combobox(self.add_lesson_popup, textvariable=building_var, values=building_list)

        add_button = ttk.Button(self.add_lesson_popup, text="Добавить", command=lambda: self.add_lesson(
            group_var.get(), week_var.get(), day_var.get(), time_var.get(), subject_var.get(), teacher_var.get(),
            couple_type_var.get(), building_var.get()
        ))

        # Размещение элементов с использованием grid
        group_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        group_combobox.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        week_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        week_combobox.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        day_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        day_combobox.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        time_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        time_combobox.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        subject_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
        subject_combobox.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        teacher_label.grid(row=5, column=0, padx=10, pady=5, sticky="e")
        teacher_combobox.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        couple_type_label.grid(row=6, column=0, padx=10, pady=5, sticky="e")
        couple_type_combobox.grid(row=6, column=1, padx=10, pady=5, sticky="w")

        building_label.grid(row=7, column=0, padx=10, pady=5, sticky="e")
        building_combobox.grid(row=7, column=1, padx=10, pady=5, sticky="w")

        add_button.grid(row=8, column=0, columnspan=2, pady=10)

    def add_lesson(self, group, week, day, time, subject, teacher, type, building):
        # Реализуйте добавление занятия в базу данных здесь
        couple_type_translate = {
            "Лекция" : 'lecture', 
            "Лабораторная" : 'laboratory', 
            "Практика" : 'practice'
        }
        print(subject, *teacher.split(" "), group, *building.split(" "), 
                                                        day, couple_type_translate.get(type), time[0:5], time[6:11], week)
        Database.execute_query("CALL add_schedule_with_names(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (subject, *teacher.split(" "), group, *building.split(" "), 
                                                        day, couple_type_translate.get(type), time[0:5], time[6:11], week))
        print(f"Добавление занятия: Группа: {group}, Неделя: {week}, День: {day}, Время: {time}")

        self.add_lesson_popup.destroy()

    def create_account(self):
        self.create_user_window = tk.Toplevel(self)
        self.create_user_window.title("Создание аккаунта")

        # Создаем и размещаем элементы интерфейса
        tk.Label(self.create_user_window, text="Логин:").grid(row=0, column=0, sticky="w")
        self.login_entry = tk.Entry(self.create_user_window)
        self.login_entry.grid(row=0, column=1)

        tk.Label(self.create_user_window, text="Пароль:").grid(row=1, column=0, sticky="w")
        self.password_entry = tk.Entry(self.create_user_window, show="*")
        self.password_entry.grid(row=1, column=1)

        tk.Label(self.create_user_window, text="Почта:").grid(row=2, column=0, sticky="w")
        self.email_entry = tk.Entry(self.create_user_window)
        self.email_entry.grid(row=2, column=1)

        tk.Label(self.create_user_window, text="Имя:").grid(row=3, column=0, sticky="w")
        self.first_name_entry = tk.Entry(self.create_user_window)
        self.first_name_entry.grid(row=3, column=1)

        tk.Label(self.create_user_window, text="Фамилия:").grid(row=4, column=0, sticky="w")
        self.last_name_entry = tk.Entry(self.create_user_window)
        self.last_name_entry.grid(row=4, column=1)

        tk.Label(self.create_user_window, text="Номер телефона:").grid(row=5, column=0, sticky="w")
        self.phone_number_entry = tk.Entry(self.create_user_window)
        self.phone_number_entry.grid(row=5, column=1)

        # Добавляем выпадающий список для групп
        tk.Label(self.create_user_window, text="Группа:").grid(row=6, column=0, sticky="w")
        self.group_var = tk.StringVar(self.create_user_window)
        self.group_var.set("Выберите группу")
        self.group_dropdown = tk.OptionMenu(self.create_user_window, self.group_var, *self.get_group_names())
        self.group_dropdown.grid(row=6, column=1)

        create_button = tk.Button(self.create_user_window, text="Создать", command=self.create_user)
        create_button.grid(row=7, column=0, columnspan=2)

        cancel_button = tk.Button(self.create_user_window, text="Отмена", command=self.create_user_window.destroy)
        cancel_button.grid(row=8, column=0, columnspan=2)

    def create_user(self):
        # Получаем данные из полей ввода
        login = self.login_entry.get()
        password = self.password_entry.get()
        email = self.email_entry.get()
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        phone_number = self.phone_number_entry.get()
        group_name = self.group_var.get()

        Database.execute_query("CALL add_student_with_group_name(%s, %s, %s, %s, %s, %s, %s)",
                       (login, password, first_name, last_name, email, phone_number, group_name))

        # Опционально: вывод подтверждения или другой логики
        messagebox.showinfo("Успех", "Пользователь успешно создан")
        print(f"Добавлен новый пользователь:\nЛогин: {login}\nПароль: {password}\nПочта: {email}\nИмя: {first_name}\nФамилия: {last_name}\nНомер телефона: {phone_number}\n Группа: {group_name}")

        # Закрываем окно создания пользователя
        self.create_user_window.destroy()

    def show_teacher_creation_popup(self):
        # Создайте всплывающее окно для создания преподавателя
        teacher_creation_popup = tk.Toplevel(self.master)
        teacher_creation_popup.title("Создание преподавателя")

        # Поля ввода для имени, фамилии, почты и номера телефона
        ttk.Label(teacher_creation_popup, text="Имя:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        first_name_entry = ttk.Entry(teacher_creation_popup)
        first_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(teacher_creation_popup, text="Фамилия:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        last_name_entry = ttk.Entry(teacher_creation_popup)
        last_name_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(teacher_creation_popup, text="Почта:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        email_entry = ttk.Entry(teacher_creation_popup)
        email_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(teacher_creation_popup, text="Номер телефона:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        phone_number_entry = ttk.Entry(teacher_creation_popup)
        phone_number_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Кнопка для создания преподавателя
        create_button = ttk.Button(teacher_creation_popup, text="Создать", command=lambda: self.create_teacher(
            first_name_entry.get(), last_name_entry.get(), email_entry.get(), phone_number_entry.get(), teacher_creation_popup
        ))
        create_button.grid(row=4, column=0, columnspan=2, pady=10)

    def create_teacher(self, first_name, last_name, email, phone_number, teacher_creation_popup):
        # Ваш код для создания преподавателя (добавьте сюда вашу логику)
        Database.execute_query('INSERT INTO Teachers(first_name, last_name, email, phone_number) VALUES(%s, %s, %s, %s)',
                                    (first_name, last_name, email, phone_number))
        # Закройте всплывающее окно после создания преподавателя
        teacher_creation_popup.destroy()

    def show_add_material_popup(self):
        # Создайте всплывающее окно для добавления материалов
        add_material_popup = tk.Toplevel(self)
        add_material_popup.title("Добавить материалы курса")

        # Создание и размещение элементов управления
        course_label = ttk.Label(add_material_popup, text="Выберите курс:")
        course_var = tk.StringVar()
        course_combobox = ttk.Combobox(add_material_popup, textvariable=course_var, values=self.get_subjects_from_database())

        hours_label = ttk.Label(add_material_popup, text="Заголовок материалов:")
        hours_entry = ttk.Entry(add_material_popup)

        material_label = ttk.Label(add_material_popup, text="Введите материалы:")
        material_text = tk.Text(add_material_popup, height=10, width=40)

        add_button = ttk.Button(add_material_popup, text="Добавить материалы", command=lambda: self.add_materials(course_var.get(), hours_entry.get(),
                                    material_text.get("1.0", tk.END), add_material_popup))

        # Размещение элементов с использованием grid
        course_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        course_combobox.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        hours_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        hours_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        material_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        material_text.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        add_button.grid(row=3, column=0, columnspan=2, pady=10)

    def add_materials(self, selected_course, title, materials, add_material_popup):
        Database.execute_query('CALL add_material(%s, %s, %s)', (selected_course, title, materials))
        print(f"Добавлены материалы курса '{selected_course}':\n{materials}")

        # Закрытие всплывающего окна после добавления материалов
        add_material_popup.destroy()
    
    def show_add_course_popup(self):
        add_course_popup = tk.Toplevel(self)
        add_course_popup.title("Добавить курс")

        name_label = ttk.Label(add_course_popup, text="Название курса:")
        name_entry = ttk.Entry(add_course_popup)

        description_label = ttk.Label(add_course_popup, text="Описание курса:")
        description_entry = ttk.Entry(add_course_popup)

        hours_label = ttk.Label(add_course_popup, text="Количество часов:")
        hours_entry = ttk.Entry(add_course_popup)

        add_button = ttk.Button(add_course_popup, text="Добавить", command=lambda: self.add_course(
            name_entry.get(), description_entry.get(), hours_entry.get(), add_course_popup
        ))

        name_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        description_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        description_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        hours_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        hours_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        add_button.grid(row=3, column=0, columnspan=2, pady=10)

    def add_course(self, name, description, hours, add_course_popup):
        Database.execute_query("CALL add_course(%s, %s, %s)", (name, description, hours))
        print(f"Добавлен курс: {name}, Описание: {description}, Часы: {hours}")

        add_course_popup.destroy()

    def show_exam_popup(self):
        # Создаем всплывающее окно
        exam_popup = tk.Toplevel(self)
        exam_popup.title("Выставить оценку")

        # Получаем данные (группы, студенты, предметы и т.д.) из базы данных
        groups = self.get_group_names()
        subjects = self.get_subjects_from_database()

        # Создаем элементы управления
        group_label = ttk.Label(exam_popup, text="Выберите группу:")
        group_var = tk.StringVar()
        group_combobox = ttk.Combobox(exam_popup, textvariable=group_var, values=groups)
        group_combobox.bind("<<ComboboxSelected>>", lambda event: self.update_students(group_var.get(), student_combobox))

        student_label = ttk.Label(exam_popup, text="Выберите студента:")
        student_var = tk.StringVar()
        student_combobox = ttk.Combobox(exam_popup, textvariable=student_var, values=[])

        semester_label = ttk.Label(exam_popup, text="Выберите семестр:")
        semester_var = tk.StringVar()
        semester_combobox = ttk.Combobox(exam_popup, textvariable=semester_var, values=[1, 2, 3, 4, 5, 6, 7, 8])
        semester_combobox.set(1)  # Установите начальное значение на 1 (или любое другое по умолчанию)

        subject_label = ttk.Label(exam_popup, text="Выберите предмет:")
        subject_var = tk.StringVar()
        subject_combobox = ttk.Combobox(exam_popup, textvariable=subject_var, values=subjects)

        grade_label = ttk.Label(exam_popup, text="Введите оценку:")
        grade_var = tk.StringVar()
        grade_entry = ttk.Entry(exam_popup, textvariable=grade_var)

        save_button = ttk.Button(exam_popup, text="Сохранить", command=lambda: self.save_grade(group_var.get(), student_var.get(), semester_var.get(), subject_var.get(), grade_var.get(), exam_popup))

        #(group_var.get(), student_var.get(), semester_var.get(), subject_var.get(), grade_var.get()
        # Размещение элементов с использованием grid
        group_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        group_combobox.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        student_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        student_combobox.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        semester_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        semester_combobox.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        subject_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        subject_combobox.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        grade_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
        grade_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        save_button.grid(row=5, column=0, columnspan=2, pady=10)

    def update_students(self, selected_group, student_combobox):
        # Получаем студентов для выбранной группы (замените на данные из базы данных)
        #selected_group = self.group_var.get()
        print(selected_group, student_combobox)
        students_for_group = Database.fetch_data('SELECT first_name, last_name, email FROM get_students_in_group(%s)', (selected_group,))
        print(students_for_group)
        student_combobox["values"] = students_for_group

    def save_grade(self, group, student, semester, subject, grade, exam_popup):
        Database.execute_query("CALL add_exam(%s, %s, %s, %s, %s, %s, %s)", (group, *student.split(' '), subject, semester, grade))
        print(f"Группа: {group}, Студент: {student}, Семестр: {semester}, "
              f"Предмет: {subject}, Оценка: {grade}")
        
        exam_popup.destroy()

    def logout(self):
        # Логика для выхода из аккаунта
        self.controller.show_frame(LoginPage)

class StudentPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Добавить выпадающий список для выбора группы
        group_label = tk.Label(self, text="Выберите группу:")
        group_label.pack()
        self.group_var = tk.StringVar()
        group_dropdown = tk.OptionMenu(self, self.group_var, *self.get_group_names())
        group_dropdown.pack()

        # Добавить радиокнопки для выбора недели
        week_label = tk.Label(self, text="Выберите неделю:")
        week_label.pack()
        self.week_var = tk.IntVar()
        for week_number in range(1, 5):
            week_radio = tk.Radiobutton(self, text=f"Неделя {week_number}", variable=self.week_var, value=week_number)
            week_radio.pack()

        # Добавьте кнопку для отображения расписания
        show_schedule_button = tk.Button(self, text="Показать расписание", command=self.show_schedule)
        show_schedule_button.pack()

        show_grades_button = tk.Button(self, text="Показать оценки", command=self.show_grades_window)
        show_grades_button.pack()

               # Пример кнопки для выхода
        logout_button = tk.Button(self, text="Выйти", command=self.logout)
        logout_button.pack()

    def show_schedule(self):
        group = self.group_var.get()
        week = self.week_var.get()

        schedule_data = self.get_schedule_from_database(group, week)

        # Создайте новое окно для отображения таблицы
        schedule_window = tk.Toplevel(self)
        schedule_window.title("Расписание")

        # Отобразите таблицу расписания в новом окне
        self.display_schedule_table(schedule_window, schedule_data, group, week)

    def display_schedule_table(self, parent, schedule_data, group, week):
        columns = ["Расписание", "Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]

        tree = ttk.Treeview(parent, columns=columns, show="headings")

        # Настройка заголовков
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")

        # Вставляем данные в таблицу
        for day_schedule in schedule_data:
            day, *lessons = day_schedule
            tree.insert("", "end", values=[day] + lessons)

        # Прокрутка таблицы
        tree.pack(fill="both", expand=True)
        tree.bind("<ButtonRelease-1>", lambda event: self.show_info_popup(tree, group, week))

    def show_info_popup(self, tree, group, week):
        selected_item = tree.selection()

        if selected_item:
            # Получаем данные выбранной строки
            values = tree.item(selected_item, "values")
            print(group, week, values[0][0:5], values[0][6:11])
            couple = Database.fetch_data("SELECT * FROM get_schedule_for_group_week_time(%s, %s, %s, %s)", (group, week, values[0][0:5], values[0][6:11]))
            if(couple != []) :
                print(couple)
                couple = couple[0]

                type_translate = {
                    'lecture' : 'Лекция',
                    'practice' : 'Практика',
                    'laboratory' : 'Лабараторная',
                }

                info_text = f"Неделя {couple[1]}\nДень: {couple[0]}\nВремя: {values[0]}\nПредмет: {type_translate.get(couple[2])} {couple[5]}\nКабинет: {couple[8]}\nПреподаватель: {couple[6]} {couple[7]}"
            else :
                info_text = "В это время пары нету"

            # Выводим информацию в всплывающем окне
            tk.messagebox.showinfo("Информация о паре", info_text)


    def get_schedule_from_database(self, group, week):
        # ... логика запроса к базе данных для получения расписания ...
        # Вам нужно использовать ваш класс Database и вызвать нужный метод для запроса данных
        schedule = Database.fetch_data("SELECT * FROM get_schedule_for_group_week(%s, %s)", (group, week))
        print(schedule)

        times = ('09:00-10:20', '10:35-11:55', '12:25-13:45', '14:00-15:20', '15:50-17:10', '17:25-18:45', '19:00-20:20', '20:40-22:00')
        day_to_number = {
            'Monday': 1,
            'Tuesday': 2,
            'Wednesday': 3,
            'Thursday': 4,
            'Friday': 5,
            'Saturday': 6,
            'Sunday': 7
        }
        
        schedule_data = [
            ['09:00-10:20', '', '', '', '', '', '', '', ''],
            ['10:35-11:55', '', '', '', '', '', '', '', ''],
            ['12:25-13:45', '', '', '', '', '', '', '', ''],
            ['14:00-15:20', '', '', '', '', '', '', '', ''],
            ['15:50-17:10', '', '', '', '', '', '', '', ''],
            ['17:25-18:45', '', '', '', '', '', '', '', ''],
            ['19:00-20:20', '', '', '', '', '', '', '', ''],
            ['20:40-22:00', '', '', '', '', '', '', '', ''],
        ]

        for couple in schedule:

            try : 
                print(couple[3])
                print(couple[4])
                print(couple[3].strftime("%H:%M") + '-' + couple[4].strftime("%H:%M"))
                pos = times.index(couple[3].strftime("%H:%M") + '-' + couple[4].strftime("%H:%M"))
            except ValueError :
                pos = -1
            
            print(pos)
            if(pos != -1):
                schedule_data[pos][day_to_number.get(couple[0])] = couple[5]

        return schedule_data

    def logout(self):
        self.controller.show_frame(LoginPage)

    def get_group_names(self):
        result = Database.fetch_data("SELECT group_name from Groups");
        result = tuple(item[0] for item in result)

        return result
    
    def show_grades_window(self):
        # Создайте всплывающее окно для отображения оценок
        grades_window = tk.Toplevel(self)
        grades_window.title("Оценки")

        # Создайте Combobox для выбора семестра
        semester_var = tk.StringVar()
        semester_combobox = ttk.Combobox(grades_window, textvariable=semester_var, values=[1, 2, 3, 4, 5, 6, 7, 8])
        semester_combobox.pack(padx=10, pady=10)

        # Создайте кнопку для отображения оценок
        show_grades_button = tk.Button(grades_window, text="Показать оценки", command=lambda: self.show_grades(grades_window, semester_var.get(), tree))
        show_grades_button.pack()

        # Создайте грид для отображения оценок
        tree = ttk.Treeview(grades_window, columns=["Предмет", "Оценка"], show="headings")
        tree.heading("Предмет", text="Предмет")
        tree.heading("Оценка", text="Оценка")
        tree.pack()

    def show_grades(self, grades_window, semester, tree):
        # Получите оценки из базы данных для выбранного семестра
        global student_username;

        grades = Database.fetch_data("SELECT * FROM get_grades_by_username_by_semester(%s, %s)", (student_username, semester))
        print(grades)

        # Вам нужно использовать ваш класс Database и вызвать нужный метод для запроса данных
        grades_data = [("Предмет 1", "Оценка 1"), ("Предмет 2", "Оценка 2"), ("Предмет 3", "Оценка 3")]

        # Очистите грид перед обновлением данных
        for item in tree.get_children():
            tree.delete(item)

        # Вставьте данные об оценках в грид
        for subject, grade in grades:
            tree.insert("", "end", values=[subject, grade])



class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginPage, SuperuserPage, StudentPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

if __name__ == "__main__":
    app = MainApp()
    app.geometry("400x300")  # Задайте желаемый размер окна
    app.mainloop()
