import os
import datetime
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from Path import *
from Doc import *
from icecream import ic


def write_auth(doc, data):

    client_info = [
        {
            "label_l": "first name",
            "info_l": data["first name"],
            "label_r": "last name",
            "info_r": data["last name"],
        },
        {
            "label_l": "address",
            "info_l": data["address"],
            "label_r": "city",
            "info_r": data["city"],
        },
        {
            "label_l": "province",
            "info_l": data["province"],
            "label_r": "postal code",
            "info_r": data["postal code"],
        },
        {
            "label_l": "phone",
            "info_l": data["phone"],
            "label_r": "email",
            "info_r": data["email"],
        },
    ]

    card_info_4col = [
        {
            "label_l": "card type",
            "info_l": data["card type"],
            "label_r": "expiration",
            "info_r": data["expiration"],
        },
        {
            "label_l": "card number",
            "info_l": data["card number"],
            "label_r": "security code",
            "info_r": data["security code"],
        },
        {
            "label_l": "expiration",
            "info_l": data["expiration"],
            "label_r": "",
            "info_r": "",
        }
    ]

    card_info_2col = [
        {
            "label": "cardholder name",
            "info": data["cardholder name"],
        },
        {
            "label": "billing address",
            "info": data["billing address"],
        },
    ]

    payment_info = []

    for i in range(12):
        payment_info.append(
            {
                "label_l": f"payment {i+1}",
                "info_l": "$",
                "label_r": "within date",
                "info_r": "-",
            }
        )

    insert_4col_table(document=doc, table_heading="Client Information", table_items=client_info)
    insert_4col_table(document=doc, table_heading="\n\nCard Information", table_items=card_info_4col)
    insert_2col_table(document=doc, table_heading="", table_items=card_info_2col)
    insert_4col_table(document=doc, table_heading="\n\nPayment Information", table_items=payment_info)

    save_doc(doc, data)
