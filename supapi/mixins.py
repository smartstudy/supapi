# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.db.models import Q, FieldDoesNotExist
from django.utils.dateparse import parse_date


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


class QueryStringMixin(object):
    def query_string(self):
        query_dict = self.request.GET.copy()
        if 'page' in query_dict:
            del query_dict['page']
        return '&{}'.format(query_dict.urlencode()) if query_dict.urlencode() else ''

    def get_context_data(self, **kwargs):
        context = super(QueryStringMixin, self).get_context_data(**kwargs)
        context['query_string'] = self.query_string()
        return context


def is_datefield(model, field):
    try:
        return model._meta.get_field(field).get_internal_type() == 'DateField'
    except FieldDoesNotExist:
        return False


class SearchMixin(QueryStringMixin):
    search_keys = []
    search_form = None

    def get_queryset(self):
        queryset = super(SearchMixin, self).get_queryset()
        q = Q()
        query_string = self.request.GET.get('query')
        if query_string:
            queries = query_string.split('+')
            for query in queries:
                iq = Q()
                for item in self.search_keys:
                    wq = Q()
                    words = query.split(' ')
                    for word in words:
                        if is_datefield(self.model, item):
                            if parse_date(query):
                                wq = Q(**{'{}'.format(item): query})
                        else:
                            wq = wq & Q(**{'{}__icontains'.format(item): word})
                    iq = iq | wq
                q = q & iq
            queryset = queryset.filter(q).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(SearchMixin, self).get_context_data(**kwargs)
        if self.search_form:
            context['search_form'] = self.search_form(self.request.GET)
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


def _query(query):
    query_rule = {
        '_blank': '',
        '_false': False,
        '_true': True,
    }
    if query in query_rule:
        query = query_rule[query]
    return query


class FilterMixin(object):
    filter_keys = []

    def get_queryset(self):
        queryset = super(FilterMixin, self).get_queryset()
        q = Q()
        for fk in self.filter_keys:
            fq = Q()
            query_string = self.request.GET.get(fk)
            if not query_string:
                continue
            queries = query_string.split(',')
            for query in queries:
                iq = Q()
                iq = iq | Q(**{'{}'.format(fk): _query(query)})
                fq = fq | iq
            q = q & fq
        try:
            queryset = queryset.filter(q).distinct()
        except (ValueError, ValidationError):
            pass

        return queryset


class AjaxChangeTemplateMixin(object):
    ajax_template_name = None
    ajax_paginate_by = None

    def get_template_names(self):
        name = super(AjaxChangeTemplateMixin, self).get_template_names()
        if self.request.is_ajax() and self.ajax_template_name:
            name = self.ajax_template_name
        return name

    def get_paginate_by(self, queryset):
        page = super(AjaxChangeTemplateMixin, self).get_paginate_by(queryset)
        if self.request.is_ajax() and self.ajax_paginate_by:
            page = self.ajax_paginate_by
        return page