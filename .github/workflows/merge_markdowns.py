#!/usr/bin/python

# Some dirty python code here to generate *.md file for its further use as a LaTeX source

# Someday you'll see here a 'class' declaration but not this time

import os
import re


MARKDOWN_TMP  = './.github/workflows/md_to_latex_tmp.md'
LATEX_TMP     = './.github/workflows/latex_tmp.tex'
MARKDOWN_MAIN = './README.md'
MARKDOWN_ROOT = './Pages'
HEADER_LINK   = '# [to Main](../../README.md)'

HEADER_PTRN = re.compile('[\s*]?\#\s+\[to Main\]\([\.\/]+README\.md\)')
COMMNT_PTRN = re.compile('(<!--.+?-->)')

BDGE_PTRN = re.compile('\[!\[.+\]\(.+\.svg\)\]\(.+\.yml\)') # only beginning
TITL_PTRN = re.compile('([\ \t]+)?[\-\*]\s+([0-9a-zA-Z\ \t.:;!?@\-\+\'\"\(\)\*\/]+)')
LINK_PTRN = re.compile('\[(.+?)\]\((.+?)\)')
PATH_PTRN = re.compile('([ \t]+?)[\-\*]\s+\[(.+?)\]\((.+?\.md)\)')

class TEXT_COLORS:
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
        print('File was not open in {0}'.format(check_markdown_has_return_to_main.__name__))
        return

    has_header = False
    for line in file:
        line = line.strip()
        # skip lines that are empty or has comments in the beginning
        if (len(line) == 0 or re.match(COMMNT_PTRN, line)):
            continue

        header_match = re.match(HEADER_PTRN, line)
        if header_match:
            has_header = True
        else:
            print('{0}WARNING{1}: {2} missing header\nLine \'{3}\''.format(TEXT_COLORS.WARNING, TEXT_COLORS.ENDC, filepath, line))
        break 

    if not has_header:
        print('{0}WARNING{1}: {2} file is empty'.format(TEXT_COLORS.WARNING, TEXT_COLORS.ENDC, filepath))
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

        # exclude badges as there are no images
        if not re.match(BDGE_PTRN, line):
            tmp_file.write(line)

        line_match = re.match(TITL_PTRN, line)
        # print(line_match)
        if line_match:
            if len(line_match.groups()) == 2:
                table_of_contents_references_as_tuples.append((line_match.group(1), line_match.group(2)))
            # elif len(line_match.groups()) == 1:
            #     print(line_match)
            #     table_of_contents_references_as_tuples.append(( '', (line_match.group(1) )))
            continue

        line_match = re.match(PATH_PTRN, line)
        if line_match:
            table_of_contents_references_as_tuples.append(
                ( line_match.group(1), line_match.group(2), line_match.group(3) ))
                
    file.close()
    # closed README.md 

    # Once TOC is finished, add pages listed in TOC
    for item in table_of_contents_references_as_tuples:
        # Only for Chapters
        if (item[0] == None or len(item[0]) < 2):
            tmp_file.write('# ' + item[1])
            continue

        relative_path = item[2]

        if relative_path.startswith('./'):
            relative_path = relative_path[len('./'):]
        new_path = os.path.abspath(os.path.join(os.curdir, relative_path))
        file = open(new_path, 'r')
        if not file:
            print('Could not open relative: {0}'.format(relative_path))
            continue
        
        for line in file:
            header_match = re.match(HEADER_PTRN, line)
            if header_match:
                continue

            tmp_file.write(line)

    tmp_file.close()


def main():
    if (not os.path.exists(MARKDOWN_MAIN)):
        print('{0}ERROR{1}: {2} does not exist'.format(TEXT_COLORS.FAIL, TEXT_COLORS.ENDC, MARKDOWN_MAIN))
        return

    print('\nChecking headers with return link to README.md \'{0}\'in all *.md files'.format(HEADER_LINK))
    for root, dirs, files in os.walk(MARKDOWN_ROOT):
        for file in files:
            if file.endswith(".md"):
                check_markdown_has_return_to_main(os.path.join(root, file))
                
    print('Making single Markdown file')
    assemble_single_markdown(MARKDOWN_MAIN)

    print('{0}COMPLETE{1}: {2}'.format(TEXT_COLORS.OKGREEN, TEXT_COLORS.ENDC, main.__name__))


# Lets pray it works
if __name__ == "__main__":
    main()
