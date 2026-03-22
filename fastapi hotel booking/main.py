from fastapi import FastAPI, Query, Response, status, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from collections import Counter


app = FastAPI()

rooms = [
    {'room_id': 1, 'room_number': '101', 'type': 'Single', 'price_per_night': 800, 'floor': 1, 'is_available': True},
    {'room_id': 2, 'room_number': '102', 'type': 'Double', 'price_per_night': 1200, 'floor': 1, 'is_available': False},
    {'room_id': 3, 'room_number': '103', 'type': 'Deluxe', 'price_per_night': 2000, 'floor': 4, 'is_available': True},
    {'room_id': 4, 'room_number': '104', 'type': 'Suite', 'price_per_night': 3000, 'floor': 3, 'is_available': False},
    {'room_id': 5, 'room_number': '105', 'type': 'Single', 'price_per_night': 800, 'floor': 2, 'is_available': False},
    {'room_id': 6, 'room_number': '106', 'type': 'Double', 'price_per_night': 1200, 'floor': 2, 'is_available': True},
]

class BookingRequest(BaseModel):
    guest_name : str = Field(..., min_length = 2 )
    room_id    : int = Field(..., gt = 0 )
    nights     : int = Field(..., gt = 0, le = 30)
    phone      : str = Field(..., min_length= 10)
    meal_plan  : str = Field('none')
    early_checkout : bool = Field(False)

class NewRoom(BaseModel):
    room_number     : str = Field(..., min_length = 1 )
    type            : str = Field(..., min_length = 2 )
    price_per_night : int = Field(..., gt = 0)
    floor           : int = Field(..., gt = 0)
    is_available    : bool = Field(True)



# ══ HELPERS ═══════════════════════════════════════════════════════
def find_room(room_id: int):
    for room in rooms:
        if room['room_id'] == room_id:
            return room
    return None

def find_booking(booking_id: int):
    for booking in bookings:
        if booking['booking_id'] == booking_id:
            return booking
    return None

def calculate_stay_cost(price_per_night : int, nights: int, meal_plan : str, early_checkout : bool):
    base_cost = price_per_night * nights
    if meal_plan == 'breakfast':
        extra = 500 * nights
    elif meal_plan == 'all-inclusive':
        extra = 1200 * nights
    else:
        extra = 0
    total_bill = base_cost + extra
    if early_checkout == True:
        discount_amount =  total_bill * 0.10
    else: 
        discount_amount = 0
    final_bill = total_bill - discount_amount
    return {
        'Total cost' : final_bill,
        'discount amount' : discount_amount
    }

def filter_rooms_logic(type, max_price, floor, is_available):
    result = rooms.copy()  
    
    if type is not None:
        result = [room for room in result if room['type'] == type]
    
    if max_price is not None:
        result = [room for room in result if room['price_per_night'] <= max_price]
    
    if floor is not None:
        result = [room for room in result if room['floor'] == floor]

    if is_available is not None:
        result = [room for room in result if room['is_available'] == is_available]
    
    return result

bookings = []
booking_counter = 1

@app.get('/')
def home():
    return{
        'message' : 'Welcome to Grand Stay Hotel'
    }

@app.get('/rooms')
def get_rooms():
    return{
    'total' : len(rooms),
    'available_count' : len([room for room in rooms if room['is_available'] == True]),
    'rooms' : rooms
    }


@app.get('/bookings')
def get_bookings():
    return{
    'total' : len(bookings),
    'bookings' : bookings
    }

@app.get('/rooms/summary')
def get_summary_rooms():
    total = len(rooms)
    available_count = len([room for room in rooms if room['is_available'] == True])
    room_type = [room['type'] for room in rooms]
    occupied_count = total - available_count
    return{
    'total_rooms' : total,
    'available_count' : available_count,
    'occupied_count' : occupied_count,
    'cheapest_room' : min([room['price_per_night'] for room in rooms]),
    'expensive_room' : max([room['price_per_night'] for room in rooms]),
    'room_type' : Counter(room_type)
    }



@app.post('/bookings')
def create_bookings(booking: BookingRequest , response : Response):
    room = find_room(booking.room_id)
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    if room['is_available'] == False:
        raise HTTPException(status_code=400, detail="Room is already booked")
    cost_details = calculate_stay_cost(
        room['price_per_night'], 
        booking.nights, 
        booking.meal_plan, 
        booking.early_checkout
)
    global booking_counter

    booking = {
        'booking_id': booking_counter,
        'guest_name': booking.guest_name,
        'room': room,
        'nights': booking.nights,
        'meal_plan': booking.meal_plan,
        'total_cost': cost_details['Total cost'],
        'discount': cost_details['discount amount'], 
        'status': 'confirmed'
    }

    booking_counter += 1
    bookings.append(booking)
    return booking


@app.get('/rooms/filter')
def filter_rooms(
    type: str = Query(None),
    max_price: int = Query(None),
    floor: int = Query(None),
    is_available: bool = Query(None)
):
    result = filter_rooms_logic(type, max_price, floor, is_available)
    return {
        'total': len(result),
        'rooms': result
    }

@app.post('/rooms')
def create_room(New_room: NewRoom, response: Response):
    exist_room = [room['room_number'] for room in rooms]  
    if New_room.room_number in  exist_room:
        raise HTTPException(status_code= 400,detail='Room with this number already exists')
    next_id = max(room['room_id'] for room in rooms) + 1
    room = {
        'room_id' : next_id,
        'room_number' : New_room.room_number,
        'type'        : New_room.type,
        'price_per_night' : New_room.price_per_night,
        'floor' : New_room.floor,
        'is_available' : True
    }
    rooms.append(room)
    return JSONResponse(status_code=201, content=room)

@app.put('/rooms/{room_id}')
def update_room(
    room_id: int,
    price_per_night: int = Query(None),
    is_available: bool = Query(None)
):
    room =  find_room(room_id)

    if not room:
        raise HTTPException(status_code=404, detail='room not found')
    
    if price_per_night is not None:
        room['price_per_night'] = price_per_night

    if is_available is not None:
        room['is_available'] = is_available

    return {
        'message': 'Room Updated Successfully',
        'room': room
    }

@app.delete('/rooms/{room_id}')
def delete_room(room_id: int, response : Response):
    room =  find_room(room_id)
    if not room:
         raise HTTPException(status_code=404, detail='room not found')
    if room['is_available'] == False:
          raise HTTPException(status_code=400, detail='room already occupied')
    rooms.remove(room)
    return{
        'message': 'Room deleted Successfully',
        'room': room
    }
       
@app.post('/checkin/{booking_id}')
def set_status(booking_id : int, response: Response):
    booking = find_booking(booking_id)
    if not booking:
         raise HTTPException(status_code=404, detail='Booking not found')
    booking['status'] = 'checked_in'
    return{
        'message': 'Room booking Updated',
        'booking': booking
    }  
    
@app.post('/checkout/{booking_id}')
def change_status(booking_id : int, response: Response):
    booking = find_booking(booking_id)
    if not booking:
         raise HTTPException(status_code=404, detail='Booking not found')
    booking['status'] = 'checked_out'
    room = find_room(booking['room']['room_id'])
    room['is_available'] = True
    return{
        'message': 'Room booking Updated',
        'booking': booking
    }  

@app.get('/bookings/active')
def get_active_room():
    room = [booking for booking in bookings if booking['status'] == 'checked_in' or booking['status'] == 'confirmed']
    return room
    

@app.get('/rooms/search')
def search_room(
    keyword :str = Query(..., description='word to search for')
):
    results = [
        room for room in rooms
        if keyword.lower() in room['room_number'].lower() or keyword.lower() in room['type'].lower()
    ]
    if not results:
        return {'message': f'No products found for: {keyword}', 'results': []}
    
    return{
        'keyword' : keyword,
        'total_found' : len(results),
        'rooms' : results
    }

@app.get('/rooms/sort')
def sort_rooms(
    sort_by : str = Query('price_per_night', description = 'price_per_night or floor or type'),
    order   : str = Query('asc',   description='asc or desc')                        
):
    if sort_by not in ['price_per_night', 'floor' ,'type']:
        return {'error': "sort_by must be 'price_per_night' or 'floor' or 'type'"}
    if order not in ['asc', 'desc']:
        return {'error': "order must be 'asc' or 'desc'"}
    sorted_rooms = sorted(rooms, key = lambda room: room[sort_by],reverse=order=='desc')

    return {
        'sort_by':  sort_by,
        'order':    order,
        'rooms': sorted_rooms,
    }

@app.get('/rooms/page')
def get_products_paged(
    page:  int = Query(1, ge=1,  description='Page number'),
    limit: int = Query(2, ge=1, le=20, description='Items per page'),
):
    start = (page - 1) * limit
    end   = start + limit
    paged = rooms[start:end]
    return {
        'page':        page,
        'limit':       limit,
        'total':       len(rooms),
        'total_pages': -(-len(rooms) // limit),   
        'rooms':    paged,
    }

@app.get('/bookings/search')
def search_bookings(
    keyword :str = Query(..., description='word to search for')
):
    results = [
        booking for booking in bookings
        if keyword.lower() in booking['guest_name'].lower()
    ]
    if not results:
        return {'message': f'No products found for: {keyword}', 'results': []}
    
    return{
        'keyword' : keyword,
        'total_found' : len(results),
        'bookings' : results
    }

@app.get('/bookings/sort')
def sort_bookings(
    sort_by : str = Query('total_cost', description = 'total_cost or nights'),
    order   : str = Query('asc',   description='asc or desc')                        
):
    if sort_by not in ['total_cost', 'nights' ]:
        return {'error': "sort_by must be 'total_cost' or 'nights'"}
    if order not in ['asc', 'desc']:
        return {'error': "order must be 'asc' or 'desc'"}
    sorted_bookings = sorted(bookings, key = lambda booking: booking[sort_by],reverse=order=='desc')

    return {
        'sort_by':  sort_by,
        'order':    order,
        'bookings': sorted_bookings,
    }

@app.get('/rooms/browse')
def browse_rooms(
    keyword: str = Query(None),
    sort_by: str = Query('price_per_night'),
    order: str = Query('asc'),
    page: int = Query(1, ge=1),
    limit: int = Query(3, ge=1)
):

    result = rooms.copy()
    if keyword is not None:
        result = [room for room in result if keyword.lower() in room['room_number'].lower() or keyword.lower() in room['type'].lower()]

    if sort_by not in ['price_per_night', 'floor', 'type']:
        return {'error': "sort_by must be 'price_per_night' or 'floor' or 'type'"}
    if order not in ['asc', 'desc']:
        return {'error': "order must be 'asc' or 'desc'"}
    result = sorted(result, key=lambda room: room[sort_by], reverse=order == 'desc')

    total = len(result)
    start = (page - 1) * limit
    end = start + limit
    paged = result[start:end]

    return {
        'keyword': keyword,
        'sort_by': sort_by,
        'order': order,
        'page': page,
        'limit': limit,
        'total': total,
        'total_pages': -(-total // limit),
        'rooms': paged
    }



@app.get('/rooms/{room_id}')
def find_room_id(room_id : int):
    room = find_room(room_id)
    if not room:
        raise HTTPException(status_code=404, detail= 'room not found')
    return{'room':room}
