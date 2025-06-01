from fastapi import FastAPI, APIRouter

from sqlalchemy.exc import NoResultFound

from src.exceptions import no_result_exception_handler
from src.organizations.router import router as purchases_router


app = FastAPI()

api_router = APIRouter(prefix="/api")
api_router.include_router(purchases_router)
app.include_router(api_router)

app.add_exception_handler(NoResultFound, no_result_exception_handler)
