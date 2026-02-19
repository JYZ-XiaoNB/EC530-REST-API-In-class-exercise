import argparse
import requests

ENDPOINT = "https://api.fda.gov/food/enforcement.json"

ALLOWED_FIELDS = [
    "classification",
    "status",
    "recalling_firm",
    "state",
    "country",
    "distribution_pattern",
    "reason_for_recall",
]

def fetch_food_enforcement(search_field: str, search_value: str, limit: int, skip: int) -> dict:
    params = {
        "search": f'{search_field}:"{search_value}"',
        "limit": limit,
        "skip": skip,
    }

    r = requests.get(ENDPOINT, params=params, timeout=15)

    if r.status_code == 404:
        return {
            "endpoint": ENDPOINT,
            "query": {"search": params["search"], "limit": limit, "skip": skip},
            "total_available": 0,
            "returned_count": 0,
            "items": [],
        }

    r.raise_for_status()
    data = r.json()

    total = data.get("meta", {}).get("results", {}).get("total", 0)
    results = data.get("results", [])

    items = []
    for item in results:
        items.append(
            {
                "recall_number": item.get("recall_number"),
                "product_description": item.get("product_description"),
                "reason_for_recall": item.get("reason_for_recall"),
                "classification": item.get("classification"),
                "status": item.get("status"),
                "recalling_firm": item.get("recalling_firm"),
                "distribution_pattern": item.get("distribution_pattern"),
                "report_date": item.get("report_date"),
                "recall_initiation_date": item.get("recall_initiation_date"),
                "state": item.get("state"),
                "country": item.get("country"),
            }
        )

    return {
        "endpoint": ENDPOINT,
        "query": {"search": params["search"], "limit": limit, "skip": skip},
        "total_available": total,
        "returned_count": len(items),
        "items": items,
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--field", choices=ALLOWED_FIELDS, required=True)
    p.add_argument("--value", required=True)
    p.add_argument("--limit", type=int, default=5)
    p.add_argument("--skip", type=int, default=0)
    args = p.parse_args()

    out = fetch_food_enforcement(
        search_field=args.field,
        search_value=args.value,
        limit=args.limit,
        skip=args.skip,
    )
    print(out)

if __name__ == "__main__":
    main()