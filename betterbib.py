import unicodedata
import re

def normalize_string(s):
    """
    Normalize a string by replacing accented characters with their English equivalents.
    """
    nfkd_form = unicodedata.normalize('NFKD', s)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

def generate_bibtex_key(data, long: bool = True):
    item = data['data']
    creators = item.get('creators', [])
    title = item.get('title', '')
    year = item.get('date', '')

    # Handle authors
    if creators:
        first_creator = creators[0]
        if first_creator['creatorType'] == 'author':
            first_author_last_name = normalize_string(first_creator.get('lastName', '')).lower()
        else:
            # Assume it's an institutional author
            first_author_last_name = normalize_string(first_creator.get('name').lower())
    else:
        first_author_last_name = 'unknown'

    # Handle year
    if year:
        year = year.split('-')[0]
        if len(year) != 4: # eg.: 06/2012
            year = re.search(r'\d{4}', year).group()
    else:
        year = ""

    # Handle title
    if title:
        words = re.sub(r'[^\w\s]', '', title).split()
        stopwords = ['', 'and', 'of', 'in', 'on', 'for', 'to', 'with', 'by', 'a', 'an', 'the']
        words = [normalize_string(_) for _ in words if _.lower() not in stopwords]
        # Remove leading articles
        if long:
            words = words[:3]
            words = [word.title() for word in words]
            title = ''.join(words)
        else:
            title = words[0]
    else:
        title = 'untitled'

    if long:
        return f"{first_author_last_name}{title}{year}"
    else:
        return f"{first_author_last_name}{year}{title}"

def generate_bibtex_entry(data, long: bool = True):
    item = data['data']
    creators = item.get('creators', [])

    # Format authors
    authors = ' and '.join([f"{normalize_string(author.get('lastName', ''))}, {normalize_string(author.get('firstName', ''))}" 
                            if author['creatorType'] == 'author' 
                            else normalize_string(author['name'])
                            for author in creators])

    # Format BibTeX entry with conditional inclusion
    bibtex_key = generate_bibtex_key(data, long=long)
    bibtex_entry = f"@article{{{bibtex_key},\n"
    
    if 'title' in item:
        bibtex_entry += f"  title={{ {item['title']} }},\n"
    
    if authors:
        bibtex_entry += f"  author={{ {authors} }},\n"
    
    if 'publicationTitle' in item:
        bibtex_entry += f"  journal={{ {item['publicationTitle']} }},\n"
    
    if 'volume' in item:
        bibtex_entry += f"  volume={{ {item['volume']} }},\n"
    
    if 'issue' in item:
        bibtex_entry += f"  number={{ {item['issue']} }},\n"
    
    if 'pages' in item:
        bibtex_entry += f"  pages={{ {item['pages']} }},\n"
    
    if 'date' in item:
        year = item['date'].split('-')[0]
        if len(year) != 4: # eg.: 06/2012
            year = re.search(r'\d{4}', year).group()
        bibtex_entry += f"  year={{{year}}},\n"
    
    if 'DOI' in item:
        bibtex_entry += f"  doi={{ {item['DOI']} }},\n"

    if "ISSN" in item:
        bibtex_entry += f"  issn={{ {item['ISSN']} }},\n"
    
    if 'url' in item:
        bibtex_entry += f"  url={{ {item['url']} }}\n"

    bibtex_entry += "}"

    return bibtex_entry

def generate_yaml(data):
    item = data['data']
    creators = item.get('creators', [])

    # Format authors
    authors = ' and '.join([f"{normalize_string(author.get('lastName', ''))}, {normalize_string(author.get('firstName', ' ')[0])}" 
                            if author['creatorType'] == 'author' 
                            else normalize_string(author['name'])
                            for author in creators])

    # Format YAML entry with conditional inclusion
    yaml_entry = f"---\ntitle: {item.get('title', '')}\n"
     
    if 'date' in item:
        yaml_entry += f"year: {item['date'].split('-')[0]}\n"

    if authors:
        yaml_entry += f"authors: {authors}\n"
    
    if 'publicationTitle' in item:
        yaml_entry += f"journal: {item['publicationTitle']}\n"

    yaml_entry += "---\n"

    return yaml_entry

if __name__ == '__main__':
    data = {
        'key': 'AKAR5JEW',
        'version': 9657,
        'library': {'type': 'user', 'id': 9040741, 'name': 'MarcellGranat',
                    'links': {'alternate': {'href': 'https://www.zotero.org/marcellgranat', 'type': 'text/html'}}},
        'links': {'self': {'href': 'https://api.zotero.org/users/9040741/items/AKAR5JEW', 'type': 'application/json'},
                'alternate': {'href': 'https://www.zotero.org/marcellgranat/items/AKAR5JEW', 'type': 'text/html'},
                'attachment': {'href': 'https://api.zotero.org/users/9040741/items/ZA67DXQL', 'type': 'application/json',
                                'attachmentType': 'application/pdf', 'attachmentSize': 1646624}},
        'meta': {'creatorSummary': 'Csillag et al.', 'parsedDate': '2022', 'numChildren': 1},
        'data': {'key': 'AKAR5JEW', 'version': 9657, 'itemType': 'journalArticle',
                'title': 'Media Attention to Environmental Issues and ESG Investing',
                'creators': [{'creatorType': 'author', 'firstName': 'J. Balázs', 'lastName': 'Csillag'},
                            {'creatorType': 'author', 'firstName': 'P. Marcell', 'lastName': 'Granát'},
                            {'creatorType': 'author', 'firstName': 'Gábor', 'lastName': 'Neszveda'}],
                'abstractNote': 'We analyse how ESG scores affect future returns when environmental issues receive higher media coverage. Investors might take environmental aspects into account if they are confronted with the issue of global warming more frequently in the press. We assess the prevalence of environmental issues in the media with a machine learning-based Structural Topic Modelling (STM) methodology, using a news archive published in the USA. Running Fama-MacBeth regressions, we find that in periods when the media actively report on environmental issues, ESG scores have a significant negative impact on future returns, whereas, in months when fewer such articles are published, investors do not take sustainability measures into account, and ESG scores have no explanatory power.',
                'publicationTitle': 'Financial and Economic Review', 'volume': '21', 'issue': '4', 'pages': '129-149',
                'date': '2022', 'series': '', 'seriesTitle': '', 'seriesText': '',
                'journalAbbreviation': 'Financial and Economic Review', 'language': '', 'DOI': '10.33893/FER.21.4.129',
                'ISSN': '24159271, 2415928X', 'shortTitle': '',
                'url': 'https://en-hitelintezetiszemle.mnb.hu/letoltes/fer-21-4-st5-csillag-granat-neszveda.pdf',
                'accessDate': '2023-07-08T23:51:07Z', 'archive': '', 'archiveLocation': '', 'libraryCatalog': 'DOI.org (Crossref)',
                'callNumber': '', 'rights': '', 'extra': '', 'tags': [], 'collections': ['KY78PX8A'], 'relations': {},
                'dateAdded': '2023-07-08T23:51:07Z', 'dateModified': '2023-07-08T23:51:07Z'}
    }

    # Generate BibTeX key
    bibtex_key = generate_bibtex_key(data)
    print(bibtex_key)

    # Generate BibTeX entry
    bibtex_entry = generate_bibtex_entry(data, bibtex_key)
    print(bibtex_entry)

    # Generate YAML entry
    yaml_entry = generate_yaml(data)
    print(yaml_entry)
