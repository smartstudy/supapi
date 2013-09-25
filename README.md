supapi
======
django와 django-rest-framework를 사용하는 환경에서 SMARTSTUDY의 API 제작 및 연동을 위한 지원 모듈


설치
----

    pip install git+https://github.com/smartstudy/supapi.git#egg=SSAPI-Supapi

예제
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
        
더 이상 자세한 설명은 생략한다.
