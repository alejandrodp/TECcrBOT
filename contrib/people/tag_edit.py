#!/usr/bin/env python3

import sys
import json
import argparse


def update_dept(contact, updater):
    roles = contact.get('roles')
    if roles is None:
        return

    role_no = 0
    while role_no < len(roles):
        role = roles[role_no]
        new_dept = updater(role['dept'])
        if new_dept is None:
            del roles[role_no]
            continue

        role['dept'] = new_dept
        role_no += 1


def update_role_ty(types, updater):
    type_no = 0
    while type_no < len(types):
        ty = updater(types[type_no])
        if ty is None:
            del types[type_no]
            continue

        types[type_no] = ty
        type_no += 1


save = False


def update(store, args, updater):
    global save
    for contact in store['staff']:
        if args.is_dept:
            update_dept(contact, updater)
            continue

        for role in contact.get('roles', ()):
            types, functions = role.get('types'), role.get('functions')
            if types:
                update_role_ty(types, updater)
            if functions:
                update_role_ty(functions, updater)

    save = True

    if args.log is not None:
        try:
            with open(args.log) as log:
                cmds = json.load(log)
        except FileNotFoundError:
            cmds = []

        ns = vars(args).copy()
        del ns['file'], ns['log']
        cmds.append(ns)

        with open(args.log, 'w') as log:
            json.dump(cmds, log, indent=2)


def get_id(store, args, tag):
    if args.is_dept:
        tags = store['depts']
        def name(dept): return dept['name']
    else:
        tags = store['staff_types']
        def name(ty): return ty

    for idx, elem in enumerate(tags):
        if name(elem) == tag:
            return tags, idx

    return tags, None


def require_id(store, args, tag):
    tags, tag_id = get_id(store, args, tag)
    if tag_id is None:
        print('Error:', ty_name(args), 'not found:', repr(tag), file=sys.stderr)
        sys.exit(1)

    return tags, tag_id


def ty_name(args):
    return 'department' if args.is_dept else 'staff role'


def after_delete(deleted, ref):
    if ref == deleted:
        return None
    elif ref > deleted:
        return ref - 1
    else:
        return ref


def delete_tag(store, args):
    tags, tag_id = require_id(store, args, args.tag)
    del tags[tag_id]

    update(store, args, lambda ref: after_delete(tag_id, ref))
    print('Delete', ty_name(args), repr(args.tag),
          'with id', tag_id, file=sys.stderr)


def rename_tag(store, args):
    tags, tag_id = require_id(store, args, args.old)

    _, sanity_test_id = get_id(store, args, args.new)
    if sanity_test_id is not None:
        print('Error:', ty_name(args), repr(args.new),
              'already exists', file=sys.stderr)
        sys.exit(1)

    if args.is_dept:
        tags[tag_id]['name'] = args.new
    else:
        tags[tag_id] = args.new

    update(store, args, lambda x: x)
    print('Rename', ty_name(args), repr(args.old),
          'as', repr(args.new), file=sys.stderr)


def merge_tag(store, args):
    tags, src_id = require_id(store, args, args.src)
    _, dest_id = require_id(store, args, args.dest)
    if src_id == dest_id:
        print('Error: attempted to merge tag with itself', file=sys.stderr)
        sys.exit(1)

    del tags[src_id]

    update(store, args, lambda ref: after_delete(
        src_id, ref if ref != src_id else dest_id))
    print('Merge', ty_name(args), repr(args.src),
          'into', repr(args.dest), file=sys.stderr)


def replay_log(store, args):
    with open(args.log) as log:
        cmds = json.load(log)

    for replay_args in cmds:
        replay_args['file'] = args.file
        replay_args['out'] = args.out
        replay_args['log'] = None

        ns = argparse.Namespace()
        ns.__dict__ = replay_args

        dispatch(store, ns)


def dispatch(store, args):
    if args.cmd == 'delete':
        delete_tag(store, args)
    elif args.cmd == 'rename':
        rename_tag(store, args)
    elif args.cmd == 'merge':
        merge_tag(store, args)
    elif args.cmd == 'replay':
        replay_log(store, args)


parser = argparse.ArgumentParser()
parser.add_argument('-f', dest='file', required=True)
parser.add_argument('-l', dest='log', required=True)
parser.add_argument('-o', dest='out')

ty = parser.add_mutually_exclusive_group(required=True)
ty.add_argument('--role', dest='is_dept', action='store_false')
ty.add_argument('--dept', dest='is_dept', action='store_true')

sub = parser.add_subparsers()
sub.required = True
sub.dest = 'cmd'

delete = sub.add_parser('delete')
delete.add_argument('tag')

rename = sub.add_parser('rename')
rename.add_argument('old')
rename.add_argument('new')

merge = sub.add_parser('merge')
merge.add_argument('src')
merge.add_argument('dest')

sub.add_parser('replay')

args = parser.parse_args()
with open(args.file) as file:
    store = json.load(file)

dispatch(store, args)

if save:
    with open(args.out or args.file, 'w') as file:
        json.dump(store, file)
