#!/usr/bin/env python3

import sys
import json
import requests
import bs4


def guess_field(field, contact):
    link = field.find('a')
    href = link.get('href') if link is not None else None
    if href is not None and contact.get('href') == href:
        return {'surname': link.text}

    return ()


def name_field(field, contact):
    link = field.find('a')
    return {'name': link.text, 'href': link.get('href')}


def opt_field(key):
    def extract(field, contact):
        link = field.find('a')
        return {key: link.text} if link is not None else ()

    return extract


FIELDS = {
    '': guess_field,
    'name': name_field,
    'telephone': opt_field('tel'),
    'email': opt_field('email'),
}

ROOT = 'https://www.tec.ac.cr'

session = requests.Session()


def http_get(uri):
    global session

    response = session.get(f'{ROOT}/{uri}')
    assert response.status_code == 200

    return bs4.BeautifulSoup(response.text, 'lxml')


page_no = 0
staff = []

while True:
    table = http_get(f'directorio-contactos-0?page={page_no}').find('table')
    if table is None:
        break

    print('\rEnumerating page', 1 + page_no,
          end='...', flush=True, file=sys.stderr)
    for element in table.find('tbody').find_all('tr'):
        contact = {}
        for field in element.find_all('td'):
            klass = field.get('class') or ('',)
            if len(klass) == 1:
                contact.update((FIELDS.get(klass[0]) or (
                    lambda *_: ()))(field, contact))

        staff.append(contact)

    page_no += 1

total = len(staff)
print('\nFound', total, 'staff members', file=sys.stderr)

depts = []
dept_indices = {}


def dept_idx(roles):
    global depts, dept_indices

    link = roles.find('h3').find('a')
    href = link.get('href')

    idx = dept_indices.get(href)
    if idx is None:
        idx = len(depts)
        depts.append({'href': href, 'name': link.text})
        dept_indices[href] = idx
        print('\nNew dept [', idx, '] ', href, ': ',
              link.text, sep='', file=sys.stderr)

    return idx


staff_types = []
staff_type_indices = {}


def row_types(row, klass):
    global staff_type_indices

    div = row.find('div', {'class': klass})
    if div is None:
        return []

    types = []
    for tag in div.text.split(', '):
        idx = staff_type_indices.get(tag)
        if idx is None:
            idx = len(staff_types)
            staff_types.append(tag)
            staff_type_indices[tag] = idx
            print('\nNew staff type [', idx, '] ',
                  tag, sep='', file=sys.stderr)

        types.append(idx)

    return types


locations = []


def row_location(row):
    global locations

    div = row.find('div', {'class': 'campus'})
    if div is None:
        return None

    link = div.find('a')
    href = link.get('href').replace(ROOT, '')

    for idx, location in enumerate(locations):
        if location['href'] == href:
            break
    else:
        idx = len(locations)
        locations.append({'href': href, 'name': link.text})
        print('\nNew location [', idx, '] ', href,
              ': ', link.text, sep='', file=sys.stderr)

    return idx


for i, contact in enumerate(staff):
    print('\rQuerying member ', i + 1, '/', total, '...',
          sep='', end='', flush=True, file=sys.stderr)

    href = contact.get('href')
    if href is None:
        print('\nError: no href in contact:', contact, file=sys.stderr)
        continue

    soup = http_get(href)
    pane = soup.find(
        'div', {'class': 'pane-staff-relations-per-contact-panel-pane-1'})
    if pane is None:
        print('\nError: no info pane in contact href:', href, file=sys.stderr)
        continue

    roles = []
    for row in pane.find_all('div', {'class': 'views-row'}):
        role = {'dept': dept_idx(row)}

        types = row_types(row, 'type')
        if types:
            role['types'] = types

        functions = row_types(row, 'rol')
        if functions:
            role['functions'] = functions

        location = row_location(row)
        if location:
            role['location'] = location

        roles.append(role)

    contact['roles'] = roles

out = {
    'staff': staff,
    'depts': depts,
    'staff_types': staff_types,
    'locations': locations,
}

json.dump(out, sys.stdout)
