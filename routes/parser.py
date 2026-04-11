from fastapi import APIRouter
from service.parser import mixed_parser
from typing import List

router = APIRouter()


@router.post("/")
def root(sentences: List[str]):
    result = mixed_parser(sentences)
    return result
