# EC530-REST-API-In-class-exercise
# Exercise 1 – FDA Food Enforcement API

## User Story

As a user, I want to search food recall reports by classification
so that I can quickly identify high-risk recalls (Class I).

---

## API Endpoint

https://api.fda.gov/food/enforcement.json

---

## Query Parameters Used

- search
- limit
- skip

---

## Example 1 – Basic Query

Command:

python exercise1_food_api.py --field classification --value "Class I" --limit 3 --skip 0

Result:

- total_available: 12533
- returned_count: 3
- Fields extracted:
  - recall_number
  - product_description
  - reason_for_recall
  - classification
  - recalling_firm
  - state
  - country

---

## Example 2 – Pagination

Command:

python exercise1_food_api.py --field classification --value "Class I" --limit 3 --skip 3

Result:

- Different records returned
- Demonstrates pagination using skip

---

## Example 3 – Empty Result Handling

Command:

python exercise1_food_api.py --field recalling_firm --value asdfqwerzxcv --limit 3 --skip 0

Result:

- total_available: 0
- returned_count: 0
- items: []

Demonstrates handling empty results.
