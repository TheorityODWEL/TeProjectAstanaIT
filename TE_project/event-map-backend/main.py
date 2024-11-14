from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import math

app = FastAPI()

# Set up templates with the path to your frontend folder
templates = Jinja2Templates(directory="../event-map-frontend")

# Mount the static files directory
app.mount("/styles", StaticFiles(directory="../event-map-frontend/styles"), name="styles")
app.mount("/icons", StaticFiles(directory="../event-map-frontend/icons"), name="icons")
app.mount("/Event_Images", StaticFiles(directory="../event-map-frontend/Event_Images"), name="Event_Images")


# Dummy event data
events = [
    {
        "lat": 51.097851,
        "lon": 71.419007,
        "title": "Music Concert",
        "description": "Live music in Central Park this Saturday evening.",
        "type": "music",
        "image": "Event_Images/music_concert.jpg",
        "date": "July 27, 2024",
        "price": "18000 тг",
        "rating": "⭐ 4.9 (112 reviews)",
        "url": "/music_concert",
    },
        {
        "lat": 51.1510,
        "lon": 71.4412,
        "title": "Art Exhibition",
        "description": "Discover contemporary art at the National Museum.",
        "type": "art",
        "image": "Event_Images/art_exhibition.jpg",
        "date": "August 15, 2024",
        "price": "10000 тг",
        "rating": "⭐ 4.7 (85 reviews)",
        "url": "/event/art-exhibition"
    },
    {
        "lat": 51.1730,
        "lon": 71.4052,
        "title": "Tech Meetup",
        "description": "Join local tech experts at the annual meetup.",
        "type": "tech",
        "image": "Event_Images/tech_meetup.jpg",
        "date": "September 10, 2024",
        "price": "5000 тг",
        "rating": "⭐ 4.8 (60 reviews)",
        "url": "/event/tech-meetup"
    },
    {
        "lat": 51.1800,
        "lon": 71.4200,
        "title": "Food Festival",
        "description": "Taste local and international cuisines.",
        "type": "food",
        "image": "Event_Images/food_festival.jpg",
        "date": "October 5, 2024",
        "price": "15000 тг",
        "rating": "⭐ 4.6 (150 reviews)",
        "url": "/event/food-festival"
    },
    {
        "lat": 51.088296,
        "lon":  71.41376,
        "title": "Startup Pitch",
        "description": "Witness new startup ideas from young entrepreneurs.",
        "type": "tech",
        "image": "Event_Images/startup_pitch.jpg",
        "date": "November 20, 2024",
        "price": "2000 тг",
        "rating": "⭐ 4.5 (90 reviews)",
        "url": "/event/startup-pitch"
    },
    {
        "lat": 51.1700,
        "lon": 71.4300,
        "title": "Classical Music Night",
        "description": "Enjoy a night of classical symphonies.",
        "type": "music",
        "image": "Event_Images/classical_music_night.jpg",
        "date": "December 15, 2024",
        "price": "12000 тг",
        "rating": "⭐ 4.9 (110 reviews)",
        "url": "/event/classical-music-night"
    },
    {
        "lat": 51.1600,
        "lon": 71.4000,
        "title": "Art Workshop",
        "description": "Learn painting techniques from experts.",
        "type": "art",
        "image": "Event_Images/art_workshop.jpg",
        "date": "January 10, 2025",
        "price": "8000 тг",
        "rating": "⭐ 4.8 (75 reviews)",
        "url": "/event/art-workshop"
    },
    {
        "lat": 51.109248,
        "lon": 71.395751,
        "title": "Барыс - Металург МГ",
        "description": "Матч КХЛ",
        "type": "sport",
        "image": "Event_Images/hockey.jpg",
        "date": "November 20, 2024",
        "price": "5000 тг",
        "rating": "⭐ 4.1 (886 reviews)",
        "url": "/Barys"
    }
]

def haversine(lat1, lon1, lat2, lon2):
    # Haversine formula implementation
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1 
    dlon = lon2 - lon1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Radius of Earth in kilometers
    return c * r

@app.get("/", response_class=HTMLResponse)
async def get_signin(request: Request):
    return templates.TemplateResponse("signin.html", {"request": request})

@app.get("/home", response_class=HTMLResponse)
async def get_home_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/index", response_class=HTMLResponse)
async def get_index_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/signup", response_class=HTMLResponse)
async def get_signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.get("/Barys", response_class=HTMLResponse)
async def get_Barys_page(request: Request):
    return templates.TemplateResponse("Barys.html", {"request": request})

@app.get("/music_concert", response_class=HTMLResponse)
async def get_music_concert_page(request: Request):
    return templates.TemplateResponse("music_concert.html", {"request": request})

@app.get("/buy_ticket", response_class=HTMLResponse)
async def get_buy_ticket_page(request: Request):
    return templates.TemplateResponse("buy_ticket.html", {"request": request})

@app.get("/about", response_class=HTMLResponse)
async def get_buy_ticket_page(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/api/events")
async def get_events(radius: float = Query(50000.0), event_types: str = Query("all")):
    user_lat, user_lon = 51.091013, 71.418085
    event_type_list = event_types.split(",") if event_types != "all" else ["music", "art", "tech", "food "]

    radius_in_km = radius / 1000.0
    filtered_events = []

    for event in events:
        distance = haversine(user_lat, user_lon, event["lat"], event["lon"])
        if distance <= radius_in_km and (event["type"] in event_type_list):
            filtered_events.append(event)

    return {"events": filtered_events}

# Run the server with: uvicorn event-map-backend.main:app --reload