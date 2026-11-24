from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
import random
import string
from datetime import datetime

app = FastAPI(title="TransitDeals - Metro Ticketing & Brand Rewards")
templates = Jinja2Templates(directory="templates")

ticket_database = {}

STATION_INDEX = {
    "Ameerpet": 1,
    "HITEC City": 4,
    "Madhapur": 3,
    "Miyapur": 5,
    "Secunderabad": 2,
    "LB Nagar": 6
}

def calculate_fare(source: str, destination: str) -> int:
    if source == "Ameerpet" and destination == "HITEC City":
        return 0
    diff = abs(STATION_INDEX.get(source, 1) - STATION_INDEX.get(destination, 2))
    return max(15, diff * 10)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # Port 8000 meeda open ayithe Passenger App vasthundi
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/kiosk", response_class=HTMLResponse)
async def kiosk_page(request: Request):
    # Port 8001 leda /kiosk open ayithe Kiosk App vasthundi
    return templates.TemplateResponse("kiosk.html", {"request": request})

@app.post("/api/book-ticket")
async def book_ticket(data: dict):
    source = data.get("source")
    destination = data.get("destination")
    booking_mode = data.get("booking_mode", "Mobile App")
    payment_method = data.get("payment_method", "No Payment")
    mobile_number = data.get("mobile_number", "").strip()

    if not source or not destination:
        raise HTTPException(status_code=400, detail="Source and Destination are required.")

    fare = calculate_fare(source, destination)
    random_digits = ''.join(random.choices(string.digits, k=5))
    ticket_number = f"HYD-{random_digits}"

    brands = [
        {"brand": "Coca-Cola", "offer": "50% OFF on 500ml Bottle", "code": f"COKE-{random.randint(100,999)}"},
        {"brand": "Pepsi", "offer": "Buy 1 Get 1 Free on 300ml Can", "code": f"PEPSI-{random.randint(100,999)}"},
        {"brand": "Snickers / Lay's", "offer": "Flat ₹10 OFF at Vending Kiosk", "code": f"SNACK-{random.randint(100,999)}"}
    ]
    assigned_promo = random.choice(brands)
    timestamp = datetime.now().strftime("%d-%b-%Y %I:%M %p")

    ticket_record = {
        "ticket_number": ticket_number,
        "source": source,
        "destination": destination,
        "fare": fare,
        "booking_mode": booking_mode,
        "payment_method": payment_method,
        "mobile_number": mobile_number if mobile_number else "N/A",
        "brand": assigned_promo["brand"],
        "brand_offer": assigned_promo["offer"],
        "coupon_code": assigned_promo["code"],
        "booked_at": timestamp,
        "is_redeemed": False
    }

    ticket_database[ticket_number] = ticket_record
    return {"success": True, "ticket": ticket_record}

@app.post("/api/validate-ticket")
async def validate_ticket(data: dict):
    query_code = data.get("ticket_number", "").strip().upper()
    matched_ticket = None
    for t_no, info in ticket_database.items():
        if query_code == t_no or query_code == info["coupon_code"]:
            matched_ticket = info
            break

    if not matched_ticket:
        raise HTTPException(status_code=404, detail="Invalid Ticket Number or Coupon Code!")

    if matched_ticket["is_redeemed"]:
        return {"success": False, "message": f"Offer ({matched_ticket['coupon_code']}) has already been redeemed!"}

    matched_ticket["is_redeemed"] = True
    return {
        "success": True,
        "message": "Coupon Verified & Discount Applied!",
        "brand": matched_ticket["brand"],
        "offer": matched_ticket["brand_offer"],
        "coupon_code": matched_ticket["coupon_code"]
    }
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001)