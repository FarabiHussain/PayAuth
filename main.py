import customtkinter as ctk
from Path import *
from Img import *
from GUI import *
from App import *

imgs = Img("lg")
app = App()
app.set_size(w=512, h=512)

blueprint = app.get_blueprint()
tabview = Tabview(app.root, list(blueprint.keys()))
tabs = tabview.get_tabs()

for tab_obj, tab_name in zip(tabs.values(), tabs.keys()):

    frame = ctk.CTkFrame(master=tab_obj, fg_color="white", border_width=1)
    frame.pack(padx=2, pady=2, fill="both", expand=True)
    master = frame

    if len(blueprint[tab_name].keys()) > 13:
        scr_frame = ctk.CTkScrollableFrame(master=frame, fg_color="white", border_width=0)
        scr_frame.pack(padx=4, pady=4, fill="both", expand=True)
        master = scr_frame

    offset = 0

    for specs, label in zip(blueprint[tab_name].values(), blueprint[tab_name].keys()):

        new_component = None

        if specs['type'] == "entry":
            new_component = Entry(master=master, label_text=label, left_offset=10, top_offset=offset)
        elif specs['type'] == "datepicker":
            new_component = DatePicker(master=master, label_text=label, left_offset=10, top_offset=offset)
        elif specs['type'] == "combo":
            new_component = ComboBox(master=master, label_text=label, left_offset=10, top_offset=offset, options=specs['options'])

        app.add_component(label, new_component)

        offset += 1

app.start()
