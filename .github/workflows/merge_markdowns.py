#!/usr/bin/python

import os
import re


MARKDOWN_TMP  = r'./.github/workflows/md_to_latex_tmp.md'
MARKDOWN_MAIN = r'./README.md'
MARKDOWN_ROOT = r'./Pages'
HEADER_LINK = '# [to Main](../../README.md)'

HEADER_PTRN = re.compile(HEADER_LINK)
COMMNT_PTRN = re.compile('(<!--.+?-->)')
LINK_PTRN = re.compile('\[(.+?)\]\((.+?)\)')
PATH_PTRN = re.compile('\*\s+\[(.+?)\]\((.+?\.md)\)')

class fcol:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# 
def check_markdown_has_return_to_main(filepath):
    file = open(filepath, 'r')
    if not file:
        print()
        return

    for line in file:
        # skip lines that are empty or has comments in the beginning
        if (len(line.strip()) == 0) or re.match(COMMNT_PTRN, line):
            continue

        if not re.match(HEADER_PTRN, line):
            print('{0}WARNING{1}: {2} missing header'.format(fcol.WARNING, fcol.ENDC, filepath))
            break
    else:
        print('{0}WARNING{1}: {2} file is empty'.format(fcol.WARNING, fcol.ENDC, filepath))

    file.close()


def assemble_single_markdown(filepath):

    # try open write-to file
    tmp_file = open(MARKDOWN_TMP, 'w')
    if not tmp_file:
        print('Could not open: {0}'.format(MARKDOWN_TMP))
        return

    # try open README.md, write-from file
    file = open(filepath, 'r')
    if not file:
        print('Could not open: {0}'.format(filepath))
        return

    # TODO: Add MakeTitle.md

    # Generate files based on Table of Contents
    table_of_contents_references_as_tuples = list()
    # TODO: Make Recursive
    for line in file:
        tmp_file.write(line)

        line_match = re.findall(PATH_PTRN, line)
        if line_match:
            for item in line_match:
                table_of_contents_references_as_tuples.append(item)
    file.close()
    # closed README.md 

    # Once TOC is finished, add pages listed in TOC
    for item in table_of_contents_references_as_tuples:
        relative_path = item[1]
        if relative_path.startswith('./'):
            relative_path = relative_path[len('./'):]
        new_path = os.path.abspath(os.path.join(os.curdir, relative_path))
        file = open(new_path, 'r')
        if not file:
            print('Could not open relative: {0}'.format(relative_path))
            continue
        
        for line in file:
            tmp_file.write(line)

    tmp_file.close()


def main():
    if (not os.path.exists(MARKDOWN_MAIN)):
        print('{0}ERROR{1}: {2} does not exist'.format(fcol.FAIL, fcol.ENDC, MARKDOWN_MAIN))
        return

    print('\nChecking headers with return link to README.md \'{0}\'in all *.md files'.format(HEADER_LINK))
    for root, dirs, files in os.walk(MARKDOWN_ROOT):
        for file in files:
            if file.endswith(".md"):
                check_markdown_has_return_to_main(os.path.join(root, file))
                
    assemble_single_markdown(MARKDOWN_MAIN)


    print('{0}COMPLETE{1}: {2}'.format(fcol.OKGREEN, fcol.ENDC, main.__name__))

if __name__ == "__main__":
    main()