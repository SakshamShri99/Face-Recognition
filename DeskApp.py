from tkinter import *
import Gui_Admin
import Gui_Student
from threading import Thread
from PIL import Image, ImageTk

root = Tk()
root.title("Face Recognition System")
root.geometry("600x600")
root.configure(background="black")


class App(Frame):
    def __init__(self, master, *pargs):
        Frame.__init__(self, master, *pargs)

        self.image = Image.open("crowd.png")
        self.img_copy = self.image.copy()

        self.background_image = ImageTk.PhotoImage(self.image)

        self.background = Label(self, image=self.background_image)
        self.background.pack(fill=BOTH, expand=YES)
        self.background.bind('<Configure>', self._resize_image)

        self.pack(fill=BOTH, expand=YES)

        self.adlogo = Image.open("teacher.png")
        self.admin_button = Button(self, text='Administrator Login', command=self.admin_panel)
        self.stlogo = Image.open("student.png")
        self.student_button = Button(self, text='Student Login', command=self.student_panel)

        self.al = PhotoImage(self.adlogo)
        self.sl = PhotoImage(self.stlogo)

    def _resize_image(self, event):
        new_width = event.width
        new_height = event.height

        self.image = self.img_copy.resize((new_width, new_height))

        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image=self.background_image)

        self.student_button.place(relx=0.7, rely=0.5, anchor='center')
        self.admin_button.place(relx=0.3, rely=0.5, anchor='center')

    # def adminthread(self):
    #     self.at = Thread(target=self.admin_panel())

    def admin_panel(self):
        Gui_Admin.admin()
        admin = Toplevel(app)

        admin.image = Image.open("crowd.png")
        admin.img_copy = admin.image.copy()

        admin.background_image = ImageTk.PhotoImage(admin.image)

        admin.background = Label(admin, image=admin.background_image)
        admin.background.bind('<Configure>', self._resize_image)

        admin.button1 = Button(admin, text='Add Student', command=self.add_student)
        admin.button2 = Button(admin, text='Student Detail', command=Gui_Admin.StudentDetail)
        admin.button3 = Button(admin, text='Delete Student', command=Gui_Admin.DeleteStudent)
        admin.button4 = Button(admin, text='Add Admin', command=Gui_Admin.AddAdmin)
        admin.button5 = Button(admin, text='Delete Admin', command=Gui_Admin.GetAdmin)

        admin.button1.place(relx=0.5, rely=0.1, anchor='center')
        admin.button2.place(relx=0.5, rely=0.3, anchor='center')
        admin.button3.place(relx=0.5, rely=0.5, anchor='center')
        admin.button4.place(relx=0.5, rely=0.7, anchor='center')
        admin.button5.place(relx=0.5, rely=0.9, anchor='center')

        admin.background.pack(fill=BOTH, expand=YES)

    def student_panel(self):
        tet = Gui_Student.student()
        std = Toplevel(app)

        std.image = Image.open("crowd.png")
        std.img_copy = std.image.copy()

        std.label = Label(std, text=tet)
        std.label.pack()

    def add_student(self):
        ad = Toplevel(app)
        ad.image = Image.open("crowd.png")
        ad.img_copy = ad.image.copy()

        ad.background_image = ImageTk.PhotoImage(ad.image)

        ad.background = Label(ad, image=ad.background_image)
        ad.background.bind('<Configure>', self._resize_image)

        a = Label(ad, text="Roll No.").grid(row=0, column=0)
        b = Label(ad, text="Name").grid(row=1, column=0)
        c = Label(ad, text="Branch").grid(row=2, column=0)
        d = Label(ad, text="Year").grid(row=3, column=0)
        a1 = Entry(ad).grid(row=0, column=1)
        b1 = Entry(ad).grid(row=1, column=1)
        c1 = Entry(ad).grid(row=2, column=1)
        d1 = Entry(ad).grid(row=3, column=1)

        def send():
            Gui_Admin.AddStudent(a1.get(), b1.get(), c1.get(), d1.get())

        btn = Button(ad, text="Submit", command=send).grid(row=4, column=0)
        btn.place(S)

app = App(root)

root.mainloop()
