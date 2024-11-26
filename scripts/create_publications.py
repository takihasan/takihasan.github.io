import json
import re


# research.md page template
web_template = '''
# Publications
---

<table class="researchtable">
<tbody>

{web_entries}

</tbody>
</table>
'''.strip()

# research.md table entry template
web_entry_template = '''
<tr>
<td class="img"> <img src="{thumbnail}"> </td>
<td markdown="span">
**{title}**  
{authors}  
{venue}{notes}  
**{links}**
</td>
</tr>
'''.strip()


cv_template = '''
\\section{{Publications}}
\\begin{{cvitems}}{{\\cvbullet}}

{cv_entries}

\\end{{cvitems}}
'''

# Latex CV \pubitem template
cv_entry_template = '''
\\pubitem
    {{{authors}}}
    {{{title}}}
    {{{venue}}}
    {{{notes}}}
'''.strip()


def create_research_md():

    data = json.load(open('pages/publications.json'))

    web_entries = []
    for entry in data:

        # placeholder entries
        if entry['venue']['year'] is None:
            continue
        
        authors = ', '.join(entry['authors'])
        authors = authors.replace('Tushar Nagarajan', '<ins>Tushar Nagarajan</ins>')
        authors = authors.replace('*', '\\*')

        venue = f"{entry['venue']['name']} {entry['venue']['year']}"
        if 'remark' in entry['venue']:
            venue = f'{venue} {entry["venue"]["remark"]}'

        notes = ''
        if 'notes' in entry:
            notes = f'\n{entry["notes"]}  '

        links = [f'[[{key}]]({val})' for key, val in entry['links'].items()]
        links = '\n'.join(links)

        web_entry = web_entry_template.format(
            title=entry['title'],
            thumbnail=entry['thumbnail'],
            authors=authors,
            venue=venue,
            notes=notes,
            links=links
        )

        web_entries.append(web_entry)


    web_entries = '\n\n'.join(web_entries)
    web_page = web_template.format(web_entries=web_entries)
    with open('pages/research.md', 'w') as f:
        f.write(web_page)


def create_cv_tex():

    data = json.load(open('pages/publications.json'))

    cv_entries = []
    for entry in data:

        # placeholder entries
        if entry['venue']['year'] is None:
            continue
        
        authors = ', '.join(entry['authors'])
        authors = authors.replace('Tushar Nagarajan', '\\textbf{Tushar Nagarajan}')

        venue = f"{entry['venue']['name']} {entry['venue']['year']}"

        notes = [entry['venue'].get('remark', ''), entry.get('notes', '')]
        notes = ' '.join(notes).strip()
        notes = re.sub(r'\*{2}(.*)\*{2}', r'\\textbf{\1}', notes)

        title = entry['title'].replace('&', '\\&')

        cv_entry = cv_entry_template.format(
            title=title,
            authors=authors,
            venue=venue,
            notes=notes,
        )

        cv_entries.append(cv_entry)

    cv_entries = '\n\n'.join(cv_entries)
    cv_tex = cv_template.format(cv_entries=cv_entries)
    with open('pages/cv.tex', 'w') as f:
        f.write(cv_tex)


if __name__ == "__main__":

    create_research_md()
    # create_cv_tex()



