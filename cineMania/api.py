from ninja import NinjaAPI
from cineflixx.views import router as flixx_router

api = NinjaAPI()

api.add_router('/',flixx_router)