import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText
import os

# إنشاء قاعدة بيانات والجداول (إذا لم تكن موجودة بالفعل)
def create_tables():
    conn = sqlite3.connect('team_activity.db')
    cursor = conn.cursor()
    
    # إنشاء جدول المستخدمين
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            role TEXT,
            branch TEXT
        )
    ''')
    
    # إنشاء جدول الأنشطة
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            activity TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    conn.commit()
    conn.close()

# دالة لإضافة مستخدم جديد
def add_user(name, role, branch):
    if not name or not role or not branch:
        messagebox.showwarning("تحذير", "يرجى ملء جميع الحقول.")
        return
    conn = sqlite3.connect('team_activity.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO users (name, role, branch) VALUES (?, ?, ?)''', (name, role, branch))
    conn.commit()
    conn.close()
    messagebox.showinfo("نجاح", f"تم إضافة المستخدم: {name}")

# دالة لتسجيل نشاط جديد
def add_activity(user_id, activity):
    if not user_id or not activity:
        messagebox.showwarning("تحذير", "يرجى ملء جميع الحقول.")
        return
    conn = sqlite3.connect('team_activity.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT id FROM users WHERE id = ?''', (user_id,))
    user = cursor.fetchone()
    if user:
        cursor.execute('''INSERT INTO activities (user_id, activity) VALUES (?, ?)''', (user_id, activity))
        conn.commit()
        messagebox.showinfo("نجاح", f"تم تسجيل النشاط للمستخدم رقم {user_id}")
    else:
        messagebox.showwarning("خطأ", f"معرف المستخدم {user_id} غير موجود.")
    conn.close()

# دالة لعرض الأنشطة
def view_activities():
    conn = sqlite3.connect('team_activity.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT users.name, activities.activity, activities.timestamp
        FROM activities
        JOIN users ON users.id = activities.user_id
    ''')
    rows = cursor.fetchall()
    activity_list.delete(*activity_list.get_children())
    for row in rows:
        activity_list.insert("", tk.END, values=row)
    conn.close()

# دالة لتصدير الأنشطة إلى ملف Excel
def export_to_excel():
    conn = sqlite3.connect('team_activity.db')
    query = '''
        SELECT users.name, users.role, users.branch, activities.activity, activities.timestamp
        FROM activities
        JOIN users ON users.id = activities.user_id
    '''
    df = pd.read_sql(query, conn)
    excel_file = 'team_activities.xlsx'
    df.to_excel(excel_file, index=False)
    conn.close()
    messagebox.showinfo("نجاح", "تم تصدير الأنشطة إلى ملف Excel.")
    send_email_with_attachment(excel_file)

# دالة لإرسال البريد الإلكتروني مع المرفق
def send_email_with_attachment(filename):
    sender = 'your_email@example.com'
    receiver = 'islam.hassan@isonxperiences.com'
    subject = "تقرير الأنشطة"
    body = "مرحبًا،\n\nيرجى العثور على تقرير الأنشطة المرفق في هذا البريد.\n\nتحياتي."

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # إرفاق ملف Excel
    with open(filename, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(filename)}')
        msg.attach(part)

    # إعداد SMTP وإرسال البريد
    try:
        smtp_server = smtplib.SMTP('smtp.example.com', 587)  # أدخل إعدادات SMTP الخاصة بمزود البريد الإلكتروني
        smtp_server.starttls()
        smtp_server.login(sender, 'your_password')  # أدخل كلمة المرور الخاصة بك
        smtp_server.sendmail(sender, receiver, msg.as_string())
        smtp_server.quit()
        messagebox.showinfo("نجاح", f"تم إرسال البريد الإلكتروني إلى {receiver}")
    except Exception as e:
        messagebox.showerror("خطأ", f"حدث خطأ أثناء إرسال البريد: {str(e)}")

# إنشاء الواجهة الرسومية باستخدام Tkinter
def setup_gui():
    root = tk.Tk()
    root.title("Team Activity Tracker")
    root.geometry("600x400")

    tab_control = ttk.Notebook(root)

    # التبويب الخاص بإضافة المستخدمين
    tab1 = ttk.Frame(tab_control)
    tab_control.add(tab1, text="إضافة مستخدم")

    lbl_name = ttk.Label(tab1, text="اسم المستخدم:")
    lbl_name.grid(column=0, row=0, padx=10, pady=10)
    name_entry = ttk.Entry(tab1)
    name_entry.grid(column=1, row=0, padx=10, pady=10)

    # ComboBox لاختيار الفريق
    lbl_role = ttk.Label(tab1, text="الفريق:")
    lbl_role.grid(column=0, row=1, padx=10, pady=10)
    role_combo = ttk.Combobox(tab1, values=["VoIP Team", "Noc Team", "System admin team", "Helpdesk Team"], state="readonly")
    role_combo.grid(column=1, row=1, padx=10, pady=10)

    # ComboBox لاختيار الفرع
    lbl_branch = ttk.Label(tab1, text="الفرع:")
    lbl_branch.grid(column=0, row=2, padx=10, pady=10)
    branch_combo = ttk.Combobox(tab1, values=["Korba", "Assuit", "TT", "Togareen"], state="readonly")
    branch_combo.grid(column=1, row=2, padx=10, pady=10)

    # زر إضافة المستخدم
    add_user_button = ttk.Button(tab1, text="إضافة مستخدم", command=lambda: add_user(name_entry.get(), role_combo.get(), branch_combo.get()))
    add_user_button.grid(column=1, row=3, padx=10, pady=10)

    # التبويب الخاص بتسجيل الأنشطة
    tab2 = ttk.Frame(tab_control)
    tab_control.add(tab2, text="تسجيل نشاط")

    lbl_user_id = ttk.Label(tab2, text="معرف المستخدم:")
    lbl_user_id.grid(column=0, row=0, padx=10, pady=10)
    user_id_entry = ttk.Entry(tab2)
    user_id_entry.grid(column=1, row=0, padx=10, pady=10)

    lbl_activity = ttk.Label(tab2, text="النشاط:")
    lbl_activity.grid(column=0, row=1, padx=10, pady=10)
    activity_entry = ttk.Entry(tab2)
    activity_entry.grid(column=1, row=1, padx=10, pady=10)

    add_activity_button = ttk.Button(tab2, text="تسجيل النشاط", command=lambda: add_activity(user_id_entry.get(), activity_entry.get()))
    add_activity_button.grid(column=1, row=2, padx=10, pady=10)

    # التبويب الخاص بعرض الأنشطة
    tab3 = ttk.Frame(tab_control)
    tab_control.add(tab3, text="عرض الأنشطة")

    global activity_list
    activity_list = ttk.Treeview(tab3, columns=("اسم المستخدم", "النشاط", "التاريخ"), show="headings")
    activity_list.heading("اسم المستخدم", text="اسم المستخدم")
    activity_list.heading("النشاط", text="النشاط")
    activity_list.heading("التاريخ", text="التاريخ")
    activity_list.pack(fill=tk.BOTH, expand=True)

    view_activities_button = ttk.Button(tab3, text="عرض الأنشطة", command=view_activities)
    view_activities_button.pack(pady=10)

    # زر تصدير الأنشطة إلى Excel وإرسال البريد الإلكتروني
    export_button = ttk.Button(tab3, text="تصدير وإرسال بالبريد", command=export_to_excel)
    export_button.pack(pady=10)

    tab_control.pack(expand=1, fill='both')
    root.mainloop()

# استدعاء الدوال اللازمة
create_tables()
setup_gui()
