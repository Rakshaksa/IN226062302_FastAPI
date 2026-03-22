# 🏨 Grand Stay Hotel - FastAPI Backend

A fully functional Hotel Room Booking REST API built with FastAPI as part of the Innomatics Research Labs internship project.

---

## 🚀 Tech Stack

- **Python**
- **FastAPI**
- **Pydantic**
- **Uvicorn**

---

## ⚙️ Installation & Setup

**1. Clone the repository**
```bash
git clone https://github.com/Rakshaksa/fastapi-hotel-booking.git
cd fastapi-hotel-booking
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the server**
```bash
uvicorn main:app --reload
```

**4. Open Swagger UI**
```
http://127.0.0.1:8000/docs
```

---

## 📁 Project Structure

```
fastapi-hotel-booking/
│
├── main.py
├── requirements.txt
├── README.md
└── screenshots/
```

---

## 📌 API Endpoints

### 🔵 GET APIs
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |
| GET | `/rooms` | Get all rooms |
| GET | `/rooms/{room_id}` | Get room by ID |
| GET | `/rooms/summary` | Rooms summary & stats |
| GET | `/bookings` | Get all bookings |

### 🟢 POST APIs
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/bookings` | Create a new booking |
| POST | `/rooms` | Add a new room |
| POST | `/checkin/{booking_id}` | Check-in a booking |
| POST | `/checkout/{booking_id}` | Check-out a booking |

### 🟡 Filter, Search & Sort
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/rooms/filter` | Filter rooms by type, price, floor |
| GET | `/rooms/search` | Search rooms by keyword |
| GET | `/rooms/sort` | Sort rooms by price, floor, type |
| GET | `/rooms/page` | Paginate rooms |
| GET | `/rooms/browse` | Combined search, sort & paginate |

### 🟠 CRUD Operations
| Method | Endpoint | Description |
|--------|----------|-------------|
| PUT | `/rooms/{room_id}` | Update room details |
| DELETE | `/rooms/{room_id}` | Delete a room |

### 🔴 Booking APIs
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/bookings/active` | Get active bookings |
| GET | `/bookings/search` | Search bookings by guest name |
| GET | `/bookings/sort` | Sort bookings by cost or nights |

---

## ✅ Features Implemented

- ✅ GET APIs with summary and count
- ✅ POST APIs with Pydantic validation
- ✅ Helper functions (find_room, calculate_stay_cost, filter_rooms_logic)
- ✅ CRUD operations (Create, Read, Update, Delete)
- ✅ Multi-step workflow (Booking → Check-in → Check-out)
- ✅ Meal plan cost calculation
- ✅ Early checkout discount (10%)
- ✅ Keyword search (case-insensitive)
- ✅ Sorting with asc/desc order
- ✅ Pagination
- ✅ Combined browse endpoint
- ✅ All APIs tested in Swagger UI

---

## 📸 Screenshots

All API screenshots are available in the `screenshots/` folder.

---

## 🙏 Acknowledgement

Built as part of the **Advanced GenerativeAI Internship** at **Innomatics Research Labs**.
