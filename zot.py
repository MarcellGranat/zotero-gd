from pyzotero import zotero
from dotenv import load_dotenv
from betterbib import *
import os

load_dotenv(".env")

zot = zotero.Zotero(os.environ["library_id"], "user", os.environ["zotero_api_key"])

def get_zot():
    global zot
    return zot

collections = zot.collections()

# find collection key from name
def name_from_key(key: str, collections: list = collections):
    for _ in collections:
        if _["data"]["key"] == key:
            return _["data"]["name"]
    return None

def parent_from_key(key: str, collections: list = collections):
    for _ in collections:
        if _["data"]["key"] == key:
            parentCollection = _["data"]["parentCollection"]
            if parentCollection:
                return parentCollection
            else:
                return None
    raise ValueError("Collection not found")

def parents_from_key(key: str, collections: list = collections):
    parent_keys = []
    while True:
        parent_key = parent_from_key(key, collections)
        if parent_key:
            parent_keys.append(parent_key)
            key = parent_key
        else:
            break
    return reversed(parent_keys)

def full_path_from_key(key: str, collections: list = collections):
    full_path = []
    for _ in parents_from_key(key, collections):
        full_path.append(name_from_key(_, collections))
    return "/".join(full_path)

def key_from_name(path: str, collections: list = collections):
    name = path.split("/")[-1]
    keys = []
    for _ in collections:
        if _["data"]["name"] == name:
            keys.append(_["data"]["key"])
    if len(keys) > 1:
        keys = [_ for _ in keys if full_path_from_key(_, collections) + "/" + name == path]
        if len(keys) > 1:
            raise ValueError("Multiple collections with the same name")
        if len(keys) == 0:
            raise ValueError("Collection with this path not found")
    if keys:
        return keys[0]
    else:
        raise ValueError("Collection not found")

    
key = key_from_name("hasznaltauto")

def export_pdf(item, path = "literature_pdfs", zot=zot, force = False) -> None:
    # check if path exists
    if not os.path.exists(path):
        os.makedirs(path)
    filename = f"{path}/{item['key']}.pdf"
    if os.path.exists(path + "/" + filename) and force == False:
        print(f"File {filename} already exists")
    else:
        zot_children = zot.children(item["data"]["key"])
        pdf_children = [_ for _ in zot_children if _.get("data", {}).get("contentType") == "application/pdf"]
        if pdf_children:
            with open(filename, "wb") as f:
                f.write(zot.file(pdf_children[0]["key"]))
            print(f"PDF exported for {item['key']}")
        else:
            print(f"No PDF found for {item['key']}")



