supapi
======
django와 django-rest-framework를 사용하는 환경에서 SMARTSTUDY의 API 제작 및 연동을 위한 지원 모듈


Install
----

    pip install git+https://github.com/smartstudy/supapi.git#egg=SSAPI-Supapi

ex
----

Models

    from supapi.models import TimeStampedModel
    
    
    class SampleModel(TimeSteampedModel):
        pass
        #...
    

Mixins
    
    from supapi.mixins import SearchMixin, OrderMixin

    class SampleViewSetCBV(SearchMixin, OrderMixin, viewsets.ModelViewSet):
        pass
        #...


help
----

SearchMixin

- 검색시 + 키워드를 넣으면 field끼리 and 연산 결과를 보여줌


더 이상 자세한 설명은 생략한다.
