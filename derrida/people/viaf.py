import re
import requests
from rdflib.graph import Graph
from .namespaces import schema


class ViafAPI(object):
    """Wrapper for VIAF API.

    https://platform.worldcat.org/api-explorer/apis/VIAF
    """

    # NOTE: API urls use www prefix, but VIAF URIs do not

    #: base url for VIAF API methods
    api_base = "https://www.viaf.org/viaf"
    #: base url for VIAF URIs
    uri_base = "https://viaf.org/viaf"

    def suggest(self, query):
        """Get VIAF suggestions for the specified query string.
        For ease of processing, returns an empty list if no suggestions
        are found or something goes wrong."""
        url = '/'.join([self.api_base, 'AutoSuggest'])
        resp = requests.get(url, params={'query': query})
        # NOTE: could consider adding logging here if we find
        # we are getting lots of unexpected errors
        if resp.status_code == requests.codes.ok:
            return resp.json().get('result', None) or []
        return []

    def get_RDF(self, viaf_id):
        """Get RDF record using known viaf_id to pull other information
        Uses requests to standardize pulling the response stream"""
        url = '/'.join([self.api_base, viaf_id])
        headers = {'accept': 'application/rdf+xml'}
        resp = requests.get(url, headers=headers)

        # Returns an empty XML graph if bad result, to mimic behavior of suggest
        if resp.status_code == requests.codes.ok:
            return resp.text
        graph = Graph()
        return graph.serialize()

    @staticmethod
    def parse_date(graph, pred):
        """Parse the date using a regex to pull the year and return as an
        integer. If ambiguous (i.e. more than one!), return None instead"""
        regex = re.compile(r'(\-|^)\d+?(?=-|$)')
        date_list = []
        for subj, pred, obj in graph.triples((None, pred, None)):
            # Dates come in YYYY-MM-DD or just YYYY for antiquity
            date_list.append(obj)
        if (len(date_list) > 1) or not date_list:
            date = None
        else:
            date = re.search(regex, date_list[0])
            if date:
                date = int(date.group(0))

        return date

    def get_years(self, rdf):
        """Take RDF XML string/file-like and attempt to parse out birth and death dates
        Returns birth, death as integers or tuple with year only, None on bad
        match"""

        graph = Graph()
        graph.parse(data=rdf)

        birthdate = self.parse_date(graph, schema.birthDate)
        deathdate = self.parse_date(graph, schema.deathDate)

        return birthdate, deathdate

    @classmethod
    def uri_from_id(cls, viaf_id):
        """Generate a VIAF URI for the specified id"""
        return "%s/%s/" % (cls.uri_base, viaf_id)
