from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from config import settings


router = APIRouter()


@router.get('/')
def get_root():
    return RedirectResponse(settings.server_url+'docs')


@router.get('/shedule')
def get_shedule(*, group_name: str, place: str):
    ...