from fastapi import FastAPI

from api.v1.routes.batch import router as router_batch
from api.v1.routes.order import router as router_order


api_v1 = FastAPI(
    title='Made.com (v1)',
    root_path='/v1',
    docs_url='/',
)

api_v1.include_router(router_batch)
api_v1.include_router(router_order)
