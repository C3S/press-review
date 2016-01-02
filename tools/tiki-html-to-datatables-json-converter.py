# -*- coding: utf-8 -*-

"""
Tiki HTML to DataTables JSON converter.
"""

import json
import operator
import re

TIKI_FILES = [
    '../../Tiki/01.htm',
    '../../Tiki/02.htm',
    '../../Tiki/03.htm',
    '../../Tiki/04.htm',
    '../../Tiki/05.htm',
    '../../Tiki/06.htm',
    '../../Tiki/07.htm',
]
PATTERNS = {
    'date_title_source_language_type_quality': re.compile(
        '<a class="tablename" href=".*">(.*)</a>'),
    'url': re.compile(
        '<a target="_blank" class="wiki external" href=".*">(.+)'
        '<img src=".*"></a>'),
    'tag': re.compile(
        '<a href="https://tiki.c3s.cc/tiki-browse_freetags.php.*">(.+)</a>'),
}
MATCH_ORDER = {
    0: 'date',
    1: 'title',
    2: 'url',
    3: 'source',
    4: 'language',
    5: 'type',
    6: 'quality'
}



def lexer(content, patterns):
    """
    Read the HTML content line by line and add tokens which match the patterns
    to the token list.
    """
    tokens = []
    for line in content.split('\n'):
        for (pattern_key, pattern_value) in patterns.items():
            pattern_match = pattern_value.match(line.strip())
            if pattern_match:
                tokens.append({
                    'pattern': pattern_key,
                    'value': pattern_match.group(1)})
    return tokens



def parser(values, match_order):
    """"
    Parse the tokens from the lexer and transform them into press review
    entries.
    """
    regular_patterns = ['date_title_source_language_type_quality', 'url']
    press_reviews = []
    press_review = {}
    token_counter = 0
    for value in values:
        # all attributes except for the tags appear in a defined order which
        # is configured in match_order
        if value['pattern'] in regular_patterns:
            # type and quality are ignored as they don't provide useful
            # information
            if match_order[token_counter] not in ['type', 'quality']:
                press_review[match_order[token_counter]] = value['value']
            token_counter = (token_counter + 1) % len(match_order)
            # add press review to list after all attributes are added
            if token_counter == 0:
                press_reviews.append(press_review)
                press_review = {}
        # append mulitple tags if present
        if value['pattern'] == 'tag':
            press_review.setdefault('tags', []).append(value['value'])
    return press_reviews



def parse_tiki_files(tiki_files, patterns, match_order):
    """
    Parses a list of Tiki HTML files and returns press review entries as an
    array of dicts.
    """
    result = []
    for filename in tiki_files:
        tiki_file = open(filename)
        tokens = lexer(tiki_file.read(), patterns)
        press_reviews = parser(tokens, match_order)
        result.extend(press_reviews)
        tiki_file.close()
    result = sorted(result, key=operator.itemgetter('date'), reverse=True)
    return result



datatables_press_reviews = {
    'data': parse_tiki_files(TIKI_FILES, PATTERNS, MATCH_ORDER)
}
datatables_json_file = open('../press-review.json', 'w')
json.dump(
    datatables_press_reviews,
    datatables_json_file,
    indent=4,
    sort_keys=True)
datatables_json_file.close()

print('Converted ' + str(len(datatables_press_reviews['data'])) + \
    ' press review entries from Tiki html to DataTables JSON.')
