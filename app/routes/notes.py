from fastapi import APIRouter, HTTPException
import requests
from app.models import CreateNoteRequest, Note
from app.main import store

router = APIRouter(prefix="/users/{user_id}/notes", tags=["notes"])

ALLOWED_FIELDS = [
    "classification",
    "status",
    "recalling_firm",
    "state",
    "country",
    "distribution_pattern",
    "reason_for_recall",
]

FDA_ENDPOINT = "https://api.fda.gov/food/enforcement.json"


@router.post("", response_model=Note, status_code=201)
def add_note(user_id: int, req: CreateNoteRequest):
    try:
        return store.add_note(user_id=user_id, text=req.text, source=req.source)
    except KeyError:
        raise HTTPException(status_code=404, detail="user not found")


@router.get("", response_model=list[Note])
def list_notes(user_id: int):
    try:
        return store.list_notes(user_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="user not found")


@router.post("/import-food-recalls", response_model=Note, status_code=201)
def import_food_recalls_as_note(
    user_id: int,
    field: str,
    value: str,
    limit: int = 3,
    skip: int = 0,
):
    if field not in ALLOWED_FIELDS:
        raise HTTPException(status_code=400, detail=f"field must be one of: {ALLOWED_FIELDS}")

    params = {
        "search": f'{field}:"{value}"',
        "limit": limit,
        "skip": skip,
    }

    r = requests.get(FDA_ENDPOINT, params=params, timeout=15)

    if r.status_code == 404:
        text = (
            f"FDA Food Enforcement import\n"
            f"search={params['search']}\n"
            f"limit={limit} skip={skip}\n\n"
            f"No results (FDA returned 404)."
        )
        source = f"FDA food/enforcement | {params['search']}"
        try:
            return store.add_note(user_id=user_id, text=text, source=source)
        except KeyError:
            raise HTTPException(status_code=404, detail="user not found")

    try:
        r.raise_for_status()
    except requests.HTTPError:
        raise HTTPException(status_code=502, detail="FDA API error")

    data = r.json()
    total = data.get("meta", {}).get("results", {}).get("total", 0)
    results = data.get("results", [])

    lines = []
    for item in results:
        lines.append(
            f"- recall_number: {item.get('recall_number')}\n"
            f"  recalling_firm: {item.get('recalling_firm')}\n"
            f"  classification: {item.get('classification')}\n"
            f"  status: {item.get('status')}\n"
            f"  state/country: {item.get('state')}/{item.get('country')}\n"
            f"  report_date: {item.get('report_date')}\n"
            f"  product_description: {item.get('product_description')}\n"
            f"  reason_for_recall: {item.get('reason_for_recall')}\n"
        )

    text = (
        f"FDA Food Enforcement import\n"
        f"search={params['search']}\n"
        f"limit={limit} skip={skip}\n"
        f"total_available={total}\n\n"
        + "\n".join(lines)
    )

    source = f"FDA food/enforcement | {params['search']}"

    try:
        return store.add_note(user_id=user_id, text=text, source=source)
    except KeyError:
        raise HTTPException(status_code=404, detail="user not found")