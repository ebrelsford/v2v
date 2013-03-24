from tastypie.api import Api

from lots.api import LotResource, LotListResource

v1_api = Api(api_name='v1')
v1_api.register(LotResource())
v1_api.register(LotListResource())
