import customtkinter as ctk
import datetime
import os
import random
import names
from Path import *
from docx import Document
from CTkMessagebox import CTkMessagebox
from tkinter import StringVar
from icecream import ic
from subprocess import DEVNULL, STDOUT, check_call
from writer import obscure, write_auth, unobscure
from dotenv import load_dotenv


class GUI:
    def __init__(self, master=None, label_text="", left_offset=0, top_offset=0) -> None:
        # no label text was passed
        if label_text == "":
            label_text = f"Component_{datetime.datetime.now().timestamp()}"

        self.stringvar = StringVar(value="")
        self.component = None

        self.label = ctk.CTkLabel(master, width=190, text=label_text, anchor="w")
        self.label.grid(row=top_offset, column=0, pady=5, padx=5, columnspan=1)

    def get(self) -> str:
        field = self.component
        return field.get()

    def set(self, new_text: str = "") -> None:
        self.stringvar.set(new_text)

    def reset(self) -> None:
        self.stringvar.set("")


class ComboBox(GUI):
    def __init__(self, master=None, label_text="", options=None, left_offset=0, top_offset=0) -> None:
        """create a new GUI ComboBox object"""

        super().__init__(master, label_text, left_offset, top_offset)

        self.options = options

        self.stringvar = StringVar(value="no options added" if options is None else 'click to select')

        self.component = ctk.CTkComboBox(
            master,
            width=250,
            height=32,
            border_width=0,
            corner_radius=2,
            bg_color="#fff",
            fg_color="#ddd",
            values=options,
            variable=self.stringvar,
        )

        # self.component.place(x=left_offset + 210, y=top_offset + 8)
        self.component.grid(row=top_offset, column=1, pady=5, padx=5, columnspan=3)

    def get(self) -> str:
        """returns the first option if nothing was selected"""
        if self.component.get() == 'click to select':
            return self.options[0]
        else:
            return self.component.get()

    def set(self, opt) -> None:
        self.stringvar.set(opt)


    def reset(self) -> None:
        textvar = self.component
        textvar.set('click to select')


class Entry(GUI):
    def __init__(self, master=None, label_text="", left_offset=0, top_offset=0) -> None:
        """create a new GUI Entry object"""

        super().__init__(master, label_text, left_offset, top_offset)

        self.stringvar = StringVar(value="")

        self.component = ctk.CTkEntry(
            master,
            width=250,
            height=32,
            border_width=0,
            corner_radius=2,
            bg_color="#fff",
            fg_color="#ddd",
            textvariable=self.stringvar,
        )

        self.component.grid(row=top_offset, column=1, pady=5, padx=5, columnspan=3)


class DatePicker(GUI):
    def __init__(self, master=None, label_text="", left_offset=0, top_offset=0, show_day=True) -> None:
        """create a new GUI DatePicker object"""

        super().__init__(master, label_text, left_offset, top_offset)

        self.today = datetime.datetime.now()
        self.show_day = show_day

        self.stringvar_month = StringVar(value=self.today.strftime("%b"))
        self.stringvar_day = StringVar(value=self.today.strftime("%d"))
        self.stringvar_year = StringVar(value=self.today.strftime("%Y"))

        self.component_day = ctk.CTkComboBox(
            master,
            width=70,
            height=32,
            border_width=0,
            corner_radius=2,
            bg_color="#fff",
            fg_color="#ddd",
            values=self.populate_days(),
            variable=self.stringvar_day,
        )

        # in some cases, like credit card expirations, the day is not needed
        if show_day is True:
            self.component_day.grid(row=top_offset, column=1, pady=5, padx=5)
        else:
            ctk.CTkLabel(master, height=32, width=70, text="").grid(row=top_offset, column=1, pady=5, padx=5)


        self.component_month = ctk.CTkComboBox(
            master,
            width=80,
            height=32,
            border_width=0,
            corner_radius=2,
            bg_color="#fff",
            fg_color="#ddd",
            values=self.populate_months(),
            variable=self.stringvar_month,
            command=self.repopulate_days
        )

        self.component_month.grid(row=top_offset, column=2, pady=5, padx=5)

        self.component_year = ctk.CTkComboBox(
            master,
            width=80,
            height=32,
            border_width=0,
            corner_radius=2,
            bg_color="#fff",
            fg_color="#ddd",
            values=self.populate_years(),
            variable=self.stringvar_year,
            command=self.repopulate_days
        )

        self.component_year.grid(row=top_offset, column=3, pady=5, padx=5)


    # returns a list of days depending on the month
    def populate_days(self) -> list:
        days=[]

        months = {
            "Jan": "31",
            "Feb": "29" if (int(self.stringvar_year.get()) % 4 == 0) else "28",
            "Mar": "31",
            "Apr": "30",
            "May": "31",
            "Jun": "30",
            "Jul": "31",
            "Aug": "31",
            "Sep": "30",
            "Oct": "31",
            "Nov": "30",
            "Dec": "31",
        }

        selected_month = months[(self.stringvar_month.get())]

        for i in range(1, int(selected_month)+1):
            days.append(str(i))

        return days


    # returns a list of month names
    def populate_months(self) -> list:
        return ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


    # returns a list of years
    def populate_years(self) -> list:
        years = []

        for i in range(10):
            next_year = int(self.stringvar_year.get()) - 10 + i
            years.append(str(next_year))

        for i in range(11):
            next_year = int(self.stringvar_year.get()) + i
            years.append(str(next_year))

        return years


    # recalculates the number of days to pick from, based on the month
    def repopulate_days(self, _) -> None:
        self.component_day.configure(values=self.populate_days())


    # set the date picker back to the current date
    def reset(self) -> None:
        self.stringvar_month.set(self.today.strftime("%b"))
        self.stringvar_day.set(self.today.strftime("%d"))
        self.stringvar_year.set(self.today.strftime("%Y"))


    # return a formatted date
    def get(self) -> str:
        m = self.stringvar_month.get()
        d = self.stringvar_day.get()
        y = self.stringvar_year.get()

        if self.show_day is True:
            return f"{m} {d}, {y}"

        return f"{m}, {y}"


    # set the date 
    def set(self, m: str|int = None, d: str|int = None, y: str|int = None) -> str:
        if m is None:
            m = self.today.strftime("%b")
        if d is None:
            d = self.today.strftime("%d")
        if y is None:
            y = self.today.strftime("%Y")

        if type(m) is str:
            self.stringvar_month.set(m)
        else:
            monthnames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            self.stringvar_month.set(monthnames[m])

        self.stringvar_day.set(str(d))
        self.stringvar_year.set(str(y))

        return self.get()


class PaymentInfo(GUI):
    def __init__(self, master=None, label_text="", left_offset=0, top_offset=0) -> None:

        super().__init__(master, label_text, left_offset, top_offset)

        self.pay_amount = Entry(master=master, label_text=label_text, left_offset=10, top_offset=top_offset)
        self.pay_amount.component.configure(width=70)
        self.pay_amount.stringvar.set(value="$")
        self.pay_amount.component.grid(row=top_offset, column=1, pady=5, padx=5, columnspan=1)

        self.pay_date = DatePicker(master=master, label_text=label_text, left_offset=10, top_offset=top_offset)
        self.pay_date.component_day.grid(row=top_offset, column=2, pady=5, padx=5)
        self.pay_date.component_month.grid(row=top_offset, column=3, pady=5, padx=5)
        self.pay_date.component_year.grid(row=top_offset, column=4, pady=5, padx=5)

        # shorten the width of the label to fit the window
        self.label.configure(width=100, text=label_text)

        # get rid of the labels that come with the Entry and DatePicker objects
        self.pay_amount.label.destroy()
        self.pay_date.label.destroy()


    def reset(self) -> None:
        self.pay_amount.reset()
        self.pay_date.reset()


    def get(self) -> dict[str, str]:
        payment = {
            "amount": self.pay_amount.get(),
            "date": self.pay_date.get()
        }

        return payment


    def set(self, amount, year, month, date) -> None:
        self.pay_amount.set(amount)
        self.pay_date.set(y=year, m=month, d=date)


class InfoPopup():
    def __init__(self, msg="InfoPopup") -> None:
        CTkMessagebox(title="Info", message=f"\n{msg}\n", height=250)


class ErrorPopup():
    def __init__(self, msg="ErrorPopup") -> None:
        CTkMessagebox(title="Error", message=f"\n{msg}\n", icon="cancel", height=250)


class PromptPopup():
    def __init__(self, msg="PromptPopup", func=lambda:()) -> None:
        self.prompt = CTkMessagebox(title="Confirm", message=f"\n{msg}\n", icon="question", option_1="Yes", option_2="Cancel", height=250)
        self.func = func

        if (self.prompt.get() == "Yes"):
            func()


    def execute(self):
        self.func()


    def get(self):
        return True if self.prompt.get() == "Yes" else False


class AppButton():
    def __init__(self, app=None, master=None, image=None, left_offset=0, top_offset=0, app_name="", width=72, height=72, desc="", row=0) -> None:

        self.component = ctk.CTkButton(
            master=master,
            text="",
            image=image,
            border_width=0,
            corner_radius=2,
            fg_color="transparent",
            command=lambda:self.__open_app(app_name=app_name, app=app),
            width=width,
            height=height,
        ).grid(row=row, column=0, pady=5, padx=5)

        self.desc_frame = ctk.CTkFrame(
            master=master, 
            corner_radius=8, 
            border_width=1, 
            width=256, 
            height=68, 
            fg_color="#ffffff",
        )
        
        self.desc_frame.grid(row=row, column=1, pady=5, padx=5)

        bold_font = ctk.CTkFont(family="Roboto Bold", weight="bold")
        normal_font = ctk.CTkFont(family="Roboto")
        self.desc_text = ctk.CTkLabel(master=self.desc_frame, text=app_name, width=240, wraplength=256, anchor="w", font=bold_font).place(x=10, y=8)
        self.desc_text = ctk.CTkLabel(master=self.desc_frame, text=desc, width=240, wraplength=256, anchor="w", font=normal_font, text_color="#777777").place(x=10, y=32)


    def __open_app(self, app_name, app):
        owd = os.getcwd()

        try:
            os.chdir(f"{os.getcwd()}\\assets\\apps\\{app_name}\\")
            app.hide()
            check_call([f"{app_name}.exe"])
        except Exception as e:
            ErrorPopup(msg=f"Could not find {app_name} in path:\n\n{os.getcwd()}\\assets\\apps\\{app_name}\\")

        app.unhide()
        os.chdir(owd)


class ActionButton():
    def __init__(self, app=None, action="", master=None, image=None, btn_text="", btn_color="transparent", width=87, height=40, row=0, col=0) -> None:

        self.component = ctk.CTkButton(
            master=master,
            text=btn_text,
            image=image,
            border_width=0,
            corner_radius=2,
            fg_color=btn_color,
            command=lambda:self.assign_action(app, action),
            width=width,
            height=height,
        ).grid(row=row, column=col, pady=5, padx=5)


    def assign_action(self, app, action) -> None:
        if ("reset" == action):
            for component in app.get_all_components().values():
                component.reset()

        elif ("create" == action):
            self.docx_button(app)

        elif ("test" == action):
            self.test_button(app)

        elif ("decrypt" == action):
            self.decrypt_button(app)

        elif ("output" == action):
            try:
                os.startfile(os.getcwd() + "\\output")
            except Exception as e:
                ErrorPopup(msg=f'Output folder not found')


    def decrypt_button(self, app):
        # retrieve object from app.components
        decrypt_tool = app.get_window("decrypt tool")

        # check whether the object contains a window
        if (decrypt_tool is not None) and (not decrypt_tool.body.winfo_exists()):
            decrypt_tool = None

        # create a new object if None was found
        if decrypt_tool is None:
            decrypt_tool = WindowView(ws=app.root.winfo_screenwidth(), hs=app.root.winfo_screenheight())
            app.add_window("decrypt tool", decrypt_tool)

            decrypt_tool.__password_strvar = ctk.StringVar(value="")
            decrypt_tool.__encrypted_strvar = ctk.StringVar(value="")
            decrypt_tool.__decrypted_strvar = ctk.StringVar(value="")

            decrypt_tool.body.title("Decrypt CVV")

            ctk.CTkLabel(decrypt_tool.body, text="Encrypted CVV", bg_color='transparent').place(x=20, y=5)
            decrypt_tool.doc_id_search = ctk.CTkEntry(decrypt_tool.body, width=260, border_width=1, corner_radius=2, textvariable=decrypt_tool.__encrypted_strvar)
            decrypt_tool.doc_id_search.place(x=20, y=28)

            ctk.CTkLabel(decrypt_tool.body, text="Password", bg_color='transparent').place(x=20, y=70)
            decrypt_tool.client_name_search = ctk.CTkEntry(decrypt_tool.body, width=260, border_width=1, corner_radius=2, textvariable=decrypt_tool.__password_strvar, show="*")
            decrypt_tool.client_name_search.place(x=20, y=93)

            ctk.CTkLabel(decrypt_tool.body, text="Decrypted CVV", bg_color='transparent').place(x=20, y=135)
            decrypt_tool.client_name_search = ctk.CTkEntry(decrypt_tool.body, width=260, border_width=1, corner_radius=2, textvariable=decrypt_tool.__decrypted_strvar)
            decrypt_tool.client_name_search.place(x=20, y=158)

            ctk.CTkButton(decrypt_tool.body, text="Run", border_width=0, corner_radius=2, fg_color="#23265e", command=lambda:self.run_decryptor(decrypt_tool), width=72, height=36).place(x=20, y=205)

            decrypt_tool.body.after(202, lambda: decrypt_tool.body.focus())

        # bring the window forward if found
        else:
            decrypt_tool.focus()


    def run_decryptor(self, decrypt_tool) -> str:
        load_dotenv()

        cipher_text=decrypt_tool.__encrypted_strvar.get()
        input_password=decrypt_tool.__password_strvar.get()
        # input_password="viewp0rt"

        if os.getenv('PW') == obscure(input_password):
            plain_text = unobscure(cipher_text)
            decrypt_tool.__decrypted_strvar.set(plain_text)
        else:
            ErrorPopup(msg=f'Wrong password')


    def docx_button(self, app):
        # initiate the data and document
        try:
            cardholder = {}
            comp_vals = app.get_all_components().values()
            comp_names = app.get_all_components().keys()

            for comp_name, comp_val in zip(comp_names, comp_vals):
                if ("payment" in comp_name):
                    pay_amount = comp_val.get()['amount']
                    if (pay_amount != "$" and len(pay_amount) != 0):
                        cardholder[comp_name] = comp_val.get()
                else:
                    cardholder[comp_name] = comp_val.get()

            doc = Document(resource_path("assets\\templates\\auth.docx"))

            write_auth(doc, cardholder)

        except Exception as e:
            ErrorPopup(msg=f'Exception while initializing data:\n\n{str(e)}')
            return False


    def test_button(self, app):

        for component in app.get_all_components().values():
            component.reset()

        legal_name = names.get_full_name(gender=random.choice(['male', 'female']))

        app.components['address'].set("Address")
        app.components['billing address'].set("Address, Winnipeg, MB")
        app.components['card number'].set(f"{str(random.randint(1000000000000000, 9999999999999999))}")
        app.components['card type'].set("Visa")
        app.components['cardholder name'].set(legal_name)
        app.components['city'].set("Winnipeg")
        app.components['email'].set(f"{legal_name.lower().replace(" ","")}@gmail.com")
        app.components['expiration'].set(y="2026", m="Dec", d="31")
        app.components['first name'].set(legal_name.split(" ")[0])
        app.components['last name'].set(legal_name.split(" ")[1])
        app.components['phone'].set(f"+1 {random.choice(["(431)", "(204)"])} {str(random.randint(100, 999))}-{str(random.randint(1000, 9999))}")
        app.components['postal code'].set(f"X1X Y2Y")
        app.components['province'].set(f"Manitoba")
        app.components['security code'].set(f"{str(random.randint(100, 999))}")

        for i in range(random.randint(1,12)):
            app.components[f'payment {i+1}'].set("100", "2025", "Jan", i)


class Tabview:
    def __init__(self, master, new_tabs=[]) -> None:

        self.tabview = ctk.CTkTabview(master, corner_radius=2, fg_color="#fff")
        self.tabview.pack(expand=True, fill="both", padx=10, pady=10)

        if len(new_tabs) > 0:
            self.tabs = {}
            self.set_tabs(new_tabs)

    def set_tabs(self, new_tabs):
        for tab in new_tabs:
            tab_obj = self.tabview.add(tab)
            self.tabs[tab] = tab_obj

    def get_tabs(self):
        tabs = {}

        for tab_name in self.tabs:
            tabs[tab_name] = self.tabview.tab(name=tab_name) 

        return tabs


class WindowView:
    def __init__(self, ws, hs) -> None:
        self.body = ctk.CTkToplevel()

        w = 300
        h = 260
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)

        self.body.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.body.resizable(False, False)
        self.body.configure(fg_color='white')

    def focus(self) -> None:
        self.body.focus()

