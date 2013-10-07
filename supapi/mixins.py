# -*- coding: utf-8 -*-
from django.db.models import Q


class DelimitedIdListMixin(object):
    uid_key = 'uid'
    uid_query_key = 'uids'
    separated_word = ','

    def get_queryset(self):
        queryset = super(DelimitedIdListMixin, self).get_queryset()
        query_string = self.request.GET.get(self.uid_query_key, None)
        q = Q()
        if query_string:
            q = Q(**{'{}__in'.format(self.uid_key): query_string.split(self.separated_word)})
        return queryset.filter(q)


class SearchMixin(object):
    search_keys = []
    search_form = None

    def get_queryset(self):
        queryset = super(SearchMixin, self).get_queryset()
        q = Q()
        query_string = self.request.GET.get('query', None)
        if query_string:
            queries = query_string.split(' ')
            for item in self.search_keys:
                iq = Q()
                for query in queries:
                    iq = iq | Q(**{'{}__contains'.format(item): query})
                q = q | iq
        return queryset.filter(q).distinct()

    def query_string(self):
        query_dict = self.request.GET.copy()
        if 'page' in query_dict:
            del query_dict['page']
        return '&{}'.format(query_dict.urlencode()) if query_dict.urlencode() else ''

    def get_context_data(self, **kwargs):
        context = super(SearchMixin, self).get_context_data(**kwargs)
        if self.search_form:
            context['search_form'] = self.search_form(self.request.GET)
            context['query_string'] = self.query_string()
        return context


class OrderMixin(object):
    order_keys = []

    def get_queryset(self):
        queryset = super(OrderMixin, self).get_queryset()
        order = self.request.GET.get('order', None)
        if order and order in self.order_keys:
            queryset = queryset.order_by(order)
        elif self.order_keys:
            queryset = queryset.order_by(self.order_keys[0])
        return queryset


class FilterMixin(object):
    filter_keys = []

    def get_queryset(self):
        queryset = super(FilterMixin, self).get_queryset()
        q = Q()
        query_string = self.request.GET.get('filter', None)

        if query_string:
            queries = query_string.split(' ')
            for item in self.filter_keys:
                iq = Q()
                for query in queries:
                    iq = iq | Q(**{'{}__iexact'.format(item): query})
                q = q | iq
        return queryset.filter(q).distinct()
