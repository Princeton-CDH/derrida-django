'''
Haystack does not yet support range facets on Solr.  This module
provides subclasses of SolrSearchQuery and SolrSearchBackend to
patch in range facet functionalty.
'''

from haystack import connections
from haystack.backends.solr_backend import SolrSearchQuery, SolrSearchBackend, \
    SolrEngine
from unidecode import unidecode


class RangeSolrSearchQuery(SolrSearchQuery):

    def __init__(self, *args, **kwargs):
        super(RangeSolrSearchQuery, self).__init__(*args, **kwargs)
        self.range_facets = {}

    def add_field_facet(self, field, **options):
        # extend default facet field method to handle a special
        # range=True case
        if options.get('range', None):
            self.add_range_facet(field, **options)
        else:
            return super(RangeSolrSearchQuery, self).add_field_facet(field, **options)

    def add_range_facet(self, field, **options):
        """Adds a solr range facet on a field.  Options must include
        start, end, and gap."""
        # using same logic as normal facets; for range facets this
        # is probably unnecessary since they have to be numeric anyway
        field_name = connections[self._using].get_unified_index() \
                                             .get_facet_fieldname(field)
        self.range_facets[field_name] = options.copy()

    def build_params(self, *args, **kwargs):
        # extend default build params logic to include any facet range
        # options
        search_kwargs = super(RangeSolrSearchQuery, self).build_params(*args, **kwargs)

        if not self.range_facets:
            return search_kwargs

        range_kwargs = {
            'facet.range': list(self.range_facets.keys())
        }
        for field, opts in self.range_facets.items():
            # NOTE: not exposing other range facet params for now
            for solr_opt in ['start', 'end', 'gap']:
                if solr_opt in opts:
                    range_kwargs['f.%s.facet.range.%s' % (field, solr_opt)] \
                         = opts[solr_opt]

            # support hard end option; convert python boolean to solr bool
            if 'hardend' in opts:
                val = 'true' if bool(opts['hardend']) else 'false'
                range_kwargs['f.%s.facet.range.hardend' % field] = val

        search_kwargs.update(range_kwargs)
        return search_kwargs

    def post_process_facets(self, results):
        # extend post processing logic to include facet range data
        # in returned facets
        facets = super(RangeSolrSearchQuery, self).post_process_facets(results)
        if 'facet_ranges' in results:
            # copy facet range data into existing facet data
            facets['ranges'] = results['facet_ranges'][0]
            for data in facets['ranges'].values():
                # possible to get no counts, in which case we can't calculate a max
                if data['counts']:
                    # find the max value for the facet_ranges
                    data['max'] = max(data['counts'][1::2])

                    # solr returns a list of value, count, value, count
                    # use zip to convert into a list of two-tuples
                    # (thanks to https://stackoverflow.com/questions/14902686/turn-flat-list-into-two-tuples)
                    data['counts'] = list(zip(data['counts'][::2], data['counts'][1::2]))
        return facets

    def _clone(self, *args, **kwargs):
        # extend clone to ensure range facets are preserved
        clone = super(RangeSolrSearchQuery, self)._clone(klass=self.__class__,
            *args, **kwargs)
        clone.range_facets = self.range_facets.copy()
        return clone


class SolrRangeSearchBackend(SolrSearchBackend):
    # extend default solr backend to ensure facet ranges are accessible
    # in the result for processing by RangeSolrSearchQuery

    def _process_results(self, raw_results, *args, **kwargs):
        results = super(SolrRangeSearchBackend, self)._process_results(raw_results,
            *args, **kwargs)

        if hasattr(raw_results, 'facets'):
            results['facet_ranges'] = raw_results.facets.get('facet_ranges', {}),

        return results

    def build_schema(self, fields):
        # haystack doesn't have any customization points for schema generation
        # or types, and Solr won't allow tokenization/customization on
        # the built string field; customize the generated schema here
        # to use local 'string_en' solr field for fields ending in "_isort"
        schema = super(SolrRangeSearchBackend, self).build_schema(fields)
        for field_cfg in schema[1]:
            if field_cfg['field_name'].endswith('_isort'):
                field_cfg['type'] = 'string_en'

        return schema


class RangeSolrEngine(SolrEngine):
    # extend default solr engine to make range backend and query defaults
    backend = SolrRangeSearchBackend
    query = RangeSolrSearchQuery


def facet_sort_ignoreaccents(facets, *fields):
    # update alpha facet so that sorting ignores accents
    # (can't be done in solr because then facets would display without accents)
    for field in fields:
        if field in facets['fields']:
            facets['fields'][field].sort(key=lambda elem: unidecode(elem[0]))
    return facets
