C3S Press Review
================


This repository stores files and information related to the press review page
of the C3S website [1]_.



The Concept
-----------


Due to the lack of a suitable plugin for managing a press review section on a
WordPress webpage, we came up with our own solution. The data is shown in a
HTML table using the DataTables [2]_ JavaScript library to provide sorting,
searching and paging functionality. The data is loaded from a JSON [3]_ file
which is stored on GitHub and which can collaboratively be maintained.



press-review.json
-----------------


The file is JSON [3]_ formatted and contains entries of press reviews which
are related to the C3S or related topics. In order to conform to the
DataTables [2]_ API the file contains a single "data" element at the top level
which is an array of all press review entries.

Each entry must contain the following attributes:

- date: an ISO formatted publication date of the press review
- language: an ISO code in lower case of the language of the press review
- source: the name of the source of the press review
- title: the title of the press review
- url: the URL of the press review

In addition each entry may contain the following optional attributes:

- tags: an array of tags (keywords, categories) associated with the press
  review



tiki-html-to-datatables-json-converter.py
-----------------------------------------


This script was written for a one time convertion of the existing press review
collection from Tiki [4]_ HTML into DataTables [2]_ JSON [3]_. It is just only
kept in the repository for documentation purposes and not intended for
reusability.



References
----------


.. [1] C3S press review, https://c3s.cc/en/press-review

.. [2] DataTables, https://datatables.net

.. [3] Wikipedia, JSON, https://en.wikipedia.org/wiki/JSON

.. [4] Tiki, https://tiki.org
