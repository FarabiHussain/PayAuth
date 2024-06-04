import customtkinter as ctk
from Path import *
from Img import *
from GUI import *
from App import *

imgs = Img("md")
app = App()
app.set_size(w=512, h=520)

blueprint = app.get_blueprint()
tabview = Tabview(app.root, list(blueprint.keys()))
tabs = tabview.get_tabs()

for tab_obj, tab_name in zip(tabs.values(), tabs.keys()):

    frame = ctk.CTkFrame(master=tab_obj, fg_color="white", border_width=1, height=400, width=480)
    frame.place(x=2, y=2)
    master = frame

    if len(blueprint[tab_name].keys()) > 10:
        scr_frame = ctk.CTkScrollableFrame(master=frame, fg_color="white", border_width=0, height=380, width=450)
        scr_frame.place(x=2, y=2)
        master = scr_frame
    else:
        scr_frame = ctk.CTkFrame(master=frame, fg_color="white", border_width=0, height=380, width=480)
        scr_frame.place(x=8, y=8)
        master = scr_frame

    offset = 0

    for specs, label in zip(blueprint[tab_name].values(), blueprint[tab_name].keys()):

        new_component = None

        if specs['type'] == "entry":
            new_component = Entry(master=master, label_text=label, left_offset=10, top_offset=offset)
        elif specs['type'] == "datepicker":
            new_component = DatePicker(master=master, label_text=label, left_offset=10, top_offset=offset)
        elif specs['type'] == "paymentinfo":
            new_component = PaymentInfo(master=master, label_text=label, left_offset=10, top_offset=offset)
        elif specs['type'] == "combo":
            new_component = ComboBox(master=master, label_text=label, left_offset=10, top_offset=offset, options=specs['options'])

        app.add_component(label, new_component)

        offset += 1

btn_frame = ctk.CTkFrame(master=app.root, fg_color="white", border_width=0, height=50, width=480)
btn_frame.place(x=10, y=455)

ActionButton(master=btn_frame, action="clear", app=app, image=imgs.get("clear.png"), btn_color="red", row=0, col=0)
ActionButton(master=btn_frame, action="docx", app=app, image=imgs.get("docx.png"), btn_color="blue", row=0, col=1)
ActionButton(master=btn_frame, action="folder", app=app, image=imgs.get("folder.png"), btn_color="gray", row=0, col=2)
ActionButton(master=btn_frame, action="test", app=app, image=imgs.get("test.png"), btn_color="lightgray", row=0, col=3)

app.start()
