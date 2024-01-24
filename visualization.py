from pyvis.network import Network
from PIL import Image
from io import BytesIO
import base64
import os
from icon_utils import ICONS, get_node_icon
from typing import Dict

IMGS_PATH = os.path.join(os.curdir, 'imgs')

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
    return ICONS.get(ntype, ICONS["default"])

def image_formatter(im):
    # Format an image for embedding in HTML
    _img = Image.open(im)
    with BytesIO() as buffer:
        _img.save(buffer, 'png')
        data = base64.encodebytes(buffer.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{data}"

def visualize_graph(nodes_and_edges_list, icons = ICONS):
    # Visualize the graph using PyVis
    net = Network('1200px', '1800px', notebook=True, select_menu=True, filter_menu=True, cdn_resources='in_line')
    seller_node_size = 10
    attribute_node_size = 20
    font_size = '20px arial black'

    for j in nodes_and_edges_list:
        src_label = j['src_node'] if j['src_node_type'] == 'target' else j['src_node_type']
        dst_label = j['dst_node'] if j['dst_node_type'] == 'target' else j['dst_node_type']
        net.add_node(j['src_node'], shape='image', image=image_formatter(get_node_icon(str(j['src_node_type']))), label=src_label, title=j['src_node'], size=seller_node_size, font=font_size)
        net.add_node(j['dst_node'], shape='image', image=image_formatter(get_node_icon(str(j['dst_node_type']))), label=dst_label, title=j['dst_node'], size=attribute_node_size, font=font_size)
        net.add_edge(j['src_node'], j['dst_node'], color='grey', physics=True, title=j['edge_type'], width=2)
    return net.show('nx.html')
    