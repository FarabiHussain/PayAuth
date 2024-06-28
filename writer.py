import os
import datetime
import re
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from Path import *
from Doc import *
from icecream import ic
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from dotenv import load_dotenv

def write_auth(doc, data):

    client_info_top = [
        {
            "label": "first name",
            "info": data["first name"],
        },
        {
            "label": "last name",
            "info": data["last name"],
        },
        {
            "label": "address",
            "info": data["address"],
        }
    ]

    client_info_bottom = [
        {
            "label_l": "province",
            "info_l": data["province"],
            "label_r": "city",
            "info_r": data["city"],
        },
        {
            "label_l": "postal code",
            "info_l": data["postal code"],
            "label_r": "email",
            "info_r": data["email"],
        },
        {
            "label_l": "phone",
            "info_l": data["phone"],
            "label_r": "",
            "info_r": "",
        },
    ]

    card_info_4col = [
        {
            "label_l": "card type",
            "info_l": data["card type"],
            "label_r": "expiration",
            "info_r": data["expiration"],
        },
    ]

    card_info_2col = [
        {
            "label": "card number",
            "info": data["card number"],
        },
        {
            "label": "security code",
            "info": cfb_encrypt(data["security code"]),
        },
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
        curr_amount = f"${data[f"payment {i+1}"]['amount']}" if f"payment {i+1}" in data else "N/A"
        curr_date = data[f"payment {i+1}"]['date'] if f"payment {i+1}" in data else "N/A"

        payment_info.append(
            {
                "label_l": f"payment {i+1}",
                "info_l": curr_amount,
                "label_r": "           on date",
                "info_r": curr_date,
            }
        )

    insert_2col_table(document=doc, table_heading="Client Information".upper(), table_items=client_info_top)
    insert_4col_table(document=doc, table_heading="".upper(), table_items=client_info_bottom)
    insert_4col_table(document=doc, table_heading="\n\n\nCard Information".upper(), table_items=card_info_4col)
    insert_2col_table(document=doc, table_heading="", table_items=card_info_2col)
    insert_4col_table(document=doc, table_heading="\n\n\n\nPayment Information (including applicable GST and PST)".upper(), table_items=payment_info)
    save_doc(doc, data)

# https://onboardbase.com/blog/aes-encryption-decryption/
def cfb_encrypt(plain_text):
    load_dotenv()

    KEY = os.getenv('KEY')
    IV = os.getenv('IV')

    plain_text_bytes = bytes(plain_text, 'utf-8')
    key_bytes = bytes(KEY, 'utf-8')
    iv_bytes = bytes(IV, 'utf-8')

    cipher = AES.new(key_bytes, AES.MODE_CFB, iv=iv_bytes)
    cipher_text = cipher.encrypt(plain_text_bytes)

    ic(plain_text)
    decrypt_cipher = AES.new(key_bytes, AES.MODE_CFB, iv=iv_bytes)
    
    ic(str(decrypt_cipher.decrypt(cipher_text))[2:-1])

    return(str(cipher_text)[2:-1])
