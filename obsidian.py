from gd import *
from zot import *
import os
import re

item = items[1]
collection_path = None

def add_literature_pdf(item, collection_path = None, locale_path = "literature_pdfs") -> None:
    if collection_path is None:
        collection_path = "papers"
        for _ in item["data"]["data"]["collections"]:
            if full_path_from_key(_) != "":
                collection_path = full_path_from_key(_)
                break

    filename = f'{item["key"]}.pdf'

    # check if exists
    if not os.path.exists(locale_path):
        os.mkdir(locale_path)

    gd = gd_file(filename)

    # check if file exists
    if not os.path.exists(f"{locale_path}/{filename}"):
        if gd:
            download_file(gd[0], f"{locale_path}/{filename}")
            print(f"file {filename} downloaded from Google Drive")
        
        else:
            export_pdf(item, path = locale_path)
            # check if exists
            if os.path.exists(f"{locale_path}/{filename}"):
                print("File {filename} exported from Zotero")
            else:
                print(f"No PDF found for {item['key']}")
    else:
        print(f"File {filename} already exists")

    if not gd and os.path.exists(f"{locale_path}/{filename}"):
        upload_file(filename, collection_path, locale_path)
        print(f"File {locale_path}/{filename} uploaded to Google Drive")

def add_literature_md(item, locale_path = "literature_notes") -> None:
    if not os.path.exists(locale_path):
        os.mkdir(locale_path)

    filename = f"{item["key"]}.md"
    if not os.path.exists(f"{locale_path}/{filename}"):
        with open(f"{locale_path}/{filename}", "w") as f:
            f.write(item["yaml"])
        print(f"File {filename} exported to {locale_path}")
    else:
        print(f"File {filename} already exists")

def add_literature_bib(item, reference_file = "reference.bib") -> None:
    if not os.path.exists(reference_file):
        with open(reference_file, "w") as f:
            f.write(item["bib_entry"])
        print(f"File {reference_file} exported")
    else:
        with open(reference_file, "r") as f:
            content = f.read()
        if item["key"] not in content:
            with open(reference_file, "a") as f:
                f.write("\n\n" + item["bib_entry"])
            print(f"File {item['key']} appended to {reference_file}")
        else:
            print(f"File {item['key']} already exists in {reference_file}")

def add_literature(item):
    add_literature_pdf(item)
    add_literature_md(item)
    add_literature_bib(item)

def add_collection(collection_name):
    key = key_from_name(collection_name)
    zot_items = get_zot().collection_items_top(key, limit=30)

    items = []  
    for item in zot_items:
        items.append({
            "key": generate_bibtex_key(item),
            "yaml": generate_yaml(item),
            "bib_entry": generate_bibtex_entry(item),
            "data": item
        })

    for item in items:
        add_literature(item)
    
# TODO TLDR to notes if not exists

