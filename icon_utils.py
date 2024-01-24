import os
from typing import Dict

IMGS_PATH = os.path.join(os.pardir, 'imgs')

ICONS = {
    "default": os.path.join(IMGS_PATH, "default_circle_2.png"),
    "-1": os.path.join(IMGS_PATH, "interested_seller_1.png"),
    "dif_clus": os.path.join(IMGS_PATH, "dif_clus_seller.png"), 
    "2": os.path.join(IMGS_PATH, "related_bad_seller.png"),
    "1": os.path.join(IMGS_PATH, "bad_seller.png"),
    "0": os.path.join(IMGS_PATH, "good_seller.png"),
    "bank_account": os.path.join(IMGS_PATH, "bank.png"),
    "email": os.path.join(IMGS_PATH, "email.png"),
    "credit_card": os.path.join(IMGS_PATH, "credit_card.png"),
    "cis_sign_in": os.path.join(IMGS_PATH, "sign_in.png"),
    "fingerprint": os.path.join(IMGS_PATH, "fingerprint.png"), 
    "flash_ubid": os.path.join(IMGS_PATH, "credit_card.png"),
    "ip": os.path.join(IMGS_PATH, "ip.png"),
    "phone": os.path.join(IMGS_PATH, "phone.png"),
    "siv_id_poc": os.path.join(IMGS_PATH, "id_poc.png"),
    "tims_tin_id": os.path.join(IMGS_PATH, "tin_id.png"),
    "ubid": os.path.join(IMGS_PATH, "ubid.png"),
    "verified_phone": os.path.join(IMGS_PATH, "verified_phone.png"),
    "gcor_id": os.path.join(IMGS_PATH, "verified_phone.png"), 
    "international_bank_account": os.path.join(IMGS_PATH, "international_bank_account.png"),
    "siv_name_poc": os.path.join(IMGS_PATH, "siv_name_poc.png"),
    "similar_email": os.path.join(IMGS_PATH, "email.png"),
    "similar_account_name": os.path.join(IMGS_PATH, "account_details.png"),
    "similar_store_front": os.path.join(IMGS_PATH, "account_details.png")
}

def get_node_icon(ntype: str) -> str:
    return ICONS.get(ntype, ICONS["-1"])