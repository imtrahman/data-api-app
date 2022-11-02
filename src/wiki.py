#!/usr/bin/env python3

import wikipedia
import sys


class WikiSummarySearch(object):

    def __init__(self):
        self.wiki = wikipedia.wikipedia

    def format_error_response(self, ex_type, ex_response):
        error_type = str(ex_type).split('.')[2].strip('\'>')
        response = str(ex_response)
        if error_type == 'PageError':
            return {
                "Status": "NotFound",
                "Response": response
            }
        elif error_type == 'DisambiguationError':
            return {
                "Status": "NotFoundWithSuggestions",
                "Response": response.split("\n")[1:]
            }
        else:
            raise 

    def get_summary(self, search_value):
        if search_value == "":
            return {
                "Status": "Error",
                "Response": "Please provide a search value"
            }
        try:
            summary = self.wiki.summary(search_value)
            return {
                "Status": "Success",
                "Response": str(summary)
            }
        except (wikipedia.exceptions.DisambiguationError, wikipedia.exceptions.PageError) as e:
            ex_type, ex_value, _ = sys.exc_info()
            return self.format_error_response(ex_type, ex_value)

if __name__ == '__main__':
    w = WikiSummarySearch()
    print(w.get_summary('jfilpesjfldjkl3'))
    print(w.get_summary('Amazon'))
    print(w.get_summary('Amazon.com'))