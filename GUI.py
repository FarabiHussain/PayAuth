import customtkinter as ctk
import datetime
import os
from CTkMessagebox import CTkMessagebox
from tkinter import StringVar
from icecream import ic
from subprocess import DEVNULL, STDOUT, check_call


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
    def __init__(self, master=None, label_text="", left_offset=0, top_offset=0) -> None:
        """create a new GUI DatePicker object"""

        super().__init__(master, label_text, left_offset, top_offset)

        self.today = datetime.datetime.now()

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

        self.component_day.grid(row=top_offset, column=1, pady=5, padx=5)

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

        return f"{m} {d}, {y}"


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
        
        self.desc_frame.grid(row=row,column=1, pady=5, padx=5)

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

