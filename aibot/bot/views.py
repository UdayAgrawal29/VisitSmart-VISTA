from django.shortcuts import render
from django.http import JsonResponse
from .models import Museum
import json
from django.contrib.auth.decorators import login_required

@login_required
def chatbot_view(request):
    return render(request, 'bot.html')

import json
from django.http import JsonResponse
import logging
import re
from .models import Museum

# Setup logging
import json
from django.http import JsonResponse
import logging
import re
from .models import Museum

# Setup logging
logging.basicConfig(level=logging.DEBUG)

import json
from django.http import JsonResponse
import logging
import re
from .models import Museum
import logging
logger = logging.getLogger(__name__)


# Setup logging
logging.basicConfig(level=logging.DEBUG)


@login_required

def chat_response(request):
    if request.method != 'POST':
        return JsonResponse({'response': 'Invalid request method.'})

    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip().lower()
        user_id = request.session.get('user_id')
        last_museum_id = request.session.get('last_museum_id')
        booking_id = request.session.get('booking_id')

        # Default response template
        response = (
            "I'm still learning to understand better. Could you please try asking in a different way? "
            "You can type 'museum', 'state', or 'city' to start exploring!"
        )

        # Detect greetings
        if any(greeting in user_message for greeting in GREETING_KEYWORDS):
            response = "👋 Hello! Welcome! How can I assist you today? Type 'museum', 'state', or 'city' to get started."

        # Detect goodbyes
        elif any(goodbye in user_message for goodbye in GOODBYE_KEYWORDS):
            response = "👋 Goodbye! Have a fantastic day ahead! Feel free to come back if you have more questions."

        # Museum query handling
        elif "museum" in user_message:
            response = handle_museum_query()
        
        # More info about the last accessed museum
        elif "more info" in user_message or "about" in user_message or "more" in user_message:
            if last_museum_id:
                try:
                    museum = Museum.objects.get(id=last_museum_id)
                    response = (
                        f"🖼 **More Information about the Museum**:\n\n"
                        f"**Name**: {museum.name}\n"
                        f"**Website**: {museum.weblinks}\n"
                        f"Feel free to ask more or book tickets!"
                    )
                except Museum.DoesNotExist:
                    response = "⚠️ Sorry, I can't find information for the previously accessed museum. Please try again."
            else:
                response = "⚠️ I don't have a record of the last museum you accessed. Please provide a museum ID."

        # Booking info handling
        elif "booking info" in user_message:
            response = booking_query(last_museum_id)
            response += (
                ">>>Please enter the date of Booking in DD/MM/YYYY format."
            )

        # State and city handling
        elif "state" in user_message:
            response = handle_state_query(user_message)
        elif "city" in user_message:
            response = handle_city_query(user_message)

        # Direct state or city queries
        elif user_message.startswith("unique_s "):
            state_name = user_message.replace("unique_s ", "").strip().title()
            response = handle_direct_state_query(state_name)
        elif user_message.startswith("unique_c "):
            city_name = user_message.replace("unique_c ", "").strip().title()
            response = handle_direct_city_query(city_name)

        # Museum ID handling
        elif user_message.startswith("id: "):
            try:
                museum_id = int(user_message.replace("id: ", "").strip())
                response = handle_museum_by_id(museum_id, request)
            except ValueError:
                response = "⚠️ Please provide a valid museum ID."

        # Date input handling
        elif user_message.startswith("date: "):
            date = str(user_message.replace("date: ", "").strip())
            response = handle_date_input(request, date, user_id, last_museum_id)
            response += " In order to book tickets type 'date: DD/MM/YYYY'"

        # Slot input handling
        elif user_message.startswith("s"):
            slot_code = user_message.strip().lower()
            response = handle_slot_input(slot_code, last_museum_id, user_id, request)

        # Ticket input handling
        elif user_message.startswith("tickets: "):
           response = handle_ticket_input(user_message, last_museum_id, request)
           logger.debug(f"Response content: {response.content}")

        elif user_message.startswith("yes"):
            response=f"http://127.0.0.1:8000/payment"
        else:
            response = handle_unknown_query(user_message)

    except json.JSONDecodeError:
        response = 'Invalid JSON in request body.'
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        if user_message.startswith("date: "):
            response = 'Transaction Created. Type the slot s1, s2.... s9'
        else:
            response='Booking confirmed. Type "yes" for payment or Type "hi" to restart.'
        

    logging.debug(f"Response data type: {type(response)}")
    logging.debug(f"Response data content: {response}")

    # Ensure response is a string
    if not isinstance(response, str):
        response = str(response)

    return JsonResponse({'response': response})# Greeting and Goodbye Keywords
GREETING_KEYWORDS = [
    "hello", "hi", "hey", "greetings", "howdy", "what's up", "good morning", 
    "good afternoon", "good evening", "how are you?", "how's it going?", "nice to meet you"
]
SLOT_MAPPING = {
    's1': {'time': '9:00 to 10:00', 'seat_field': 'slot_9_to_10_seats', 'queue_field': 'slot_9_to_10_queue'},
    's2': {'time': '10:00 to 11:00', 'seat_field': 'slot_10_to_11_seats', 'queue_field': 'slot_10_to_11_queue'},
    's3': {'time': '11:00 to 12:00', 'seat_field': 'slot_11_to_12_seats', 'queue_field': 'slot_11_to_12_queue'},
    's4': {'time': '12:00 to 13:00', 'seat_field': 'slot_12_to_13_seats', 'queue_field': 'slot_12_to_13_queue'},
    's5': {'time': '13:00 to 14:00', 'seat_field': 'slot_13_to_14_seats', 'queue_field': 'slot_13_to_14_queue'},
    's6': {'time': '14:00 to 15:00', 'seat_field': 'slot_14_to_15_seats', 'queue_field': 'slot_14_to_15_queue'},
    's7': {'time': '15:00 to 16:00', 'seat_field': 'slot_15_to_16_seats', 'queue_field': 'slot_15_to_16_queue'},
    's8': {'time': '16:00 to 17:00', 'seat_field': 'slot_16_to_17_seats', 'queue_field': 'slot_16_to_17_queue'},
    's9': {'time': '17:00 to 18:00', 'seat_field': 'slot_17_to_18_seats', 'queue_field': 'slot_17_to_18_queue'},
}


GOODBYE_KEYWORDS = ["bye", "goodbye", "see you", "take care", "farewell"]

# Response Templates
def handle_museum_query():
    logging.debug(f"Fetching all museums from the database.")
    museums = Museum.objects.all()  # Get all museums
    if museums.exists():
        response = "🏛 **Available Museums**:\n" + "\n\n".join(
            [f"----- **Museum ID**: {museum.id}, **Name**: {museum.name}" for museum in museums]
        )
        response += "\n\nPlease provide the ID of the museum you're interested in."
    else:
        response = "⚠️ No museums found in the database. Please try again later."

    return response


def handle_state_query(user_message):
    unique_states = [
        "Andhra Pradesh", "Assam", "Bihar", "Goa", "Gujarat",
        "Haryana", "Himachal Pradesh", "Karnataka", "Kerala",
        "Madhya Pradesh", "Maharashtra", "New Delhi", "Odisha",
        "Tamil Nadu", "Uttar Pradesh", "West Bengal"
    ]
    state_list = "\n".join([f"- {state}" for state in unique_states])
    state_count = len(unique_states)
    response = f"🗺 **Total Unique States**: {state_count}\n\n{state_list}\n\nYou can ask for museums in a specific state by typing 'unique_s <state_name>'."
    return response

def handle_city_query(user_message):
    cities = [
        "Kolkata", "Patna", "Siliguri", "Purulia", "Bardhaman", "Digha", 
        "Bhubaneswar", "Dhenkanal", "New Delhi", "Lucknow", "Kurukshetra",
        "Palampur", "Mumbai", "Nagpur", "Bhopal", "Panjim", "Dharampur",
        "Bangalore", "Kozhikode", "Tirupati", "Gulbarga", "Tirunelveli", "Guwahati"
    ]
    unique_cities = sorted(set(cities))
    city_list = "\n".join([f"----- {city}" for city in unique_cities])
    city_count = len(unique_cities)
    response = f"🏙 **Total Unique Cities**: {city_count}\n\n{city_list}\n\n--------You can ask for museums in a specific city by typing 'unique_c <city_name>'."
    return response

def handle_direct_state_query(state_name):
    museums_in_state = Museum.objects.filter(state__icontains=state_name)
    if museums_in_state.exists():
        response = f"🏛 **Museums in {state_name}**:\n\n" + "\n".join(
            [f"- **Museum ID**: {museum.id}, **Name**: {museum.name}" for museum in museums_in_state]
        )
    else:
        response = f"⚠️ No museums found in {state_name}. Please check the state name or ask about another location."
    return response

def handle_direct_city_query(city_name):
    museums_in_city = Museum.objects.filter(city__icontains=city_name)
    if museums_in_city.exists():
        response = f"🏛 **Museums in {city_name}**:\n\n" + "\n".join(
            [f"- **Museum ID**: {museum.id}, **Name**: {museum.name}" for museum in museums_in_city]
        )
    else:
        response = f"⚠️ No museums found in {city_name}. Please check the city name or ask about another location."
    return response

def handle_museum_by_id(museum_id, request):
    try:
        museum = Museum.objects.get(id=museum_id)

        request.session['last_museum_id'] = museum.id

        response = (
            f"🖼 **Museum Details**>>>\n\n"
            f"**ID**: {museum.id}\n"
            f">>>**Name**: {museum.name}\n"
            f">>>**City**: {museum.city}\n"
            f">>>**State**: {museum.state}\n"
            f">>>**Description**: {museum.description}\n\n"
            f"In order to book tickets, type 'booking info'."
        )

    except Museum.DoesNotExist:
        response = "⚠️ No museum found with the provided ID. Please check the ID and try again."
    
    return response


def handle_unknown_query(user_message):
    response = (
        "🤔 I'm sorry, I didn't understand that. You can ask me about museums, states, or cities, "
        "or say 'hello' to start a conversation. Let's try again!"
    )
    return response

def booking_query(last_museum_id):
    try:
        # Retrieve the museum object using the provided ID
        museum = Museum.objects.get(id=last_museum_id)
        
        # Initialize the response with basic museum details
        response_lines = [
            f"📍 Museum Information >>>",
            f">>>Name: {museum.name}>>>",
            f">>>Opening Time: {museum.opening_time.strftime('%H:%M')}>>>",
            f">>>Closing Time: {museum.closing_time.strftime('%H:%M')}>>>",
            "",

        ]

        # Time slots mapping with respective fields in the model
        slots = [
            {"time": "09:00 to 10:00", "seats_field": "slot_9_to_10_seats", "queue_field": "slot_9_to_10_queue"},
            {"time": "10:00 to 11:00", "seats_field": "slot_10_to_11_seats", "queue_field": "slot_10_to_11_queue"},
            {"time": "11:00 to 12:00", "seats_field": "slot_11_to_12_seats", "queue_field": "slot_11_to_12_queue"},
            {"time": "12:00 to 13:00", "seats_field": "slot_12_to_13_seats", "queue_field": "slot_12_to_13_queue"},
            {"time": "13:00 to 14:00", "seats_field": "slot_13_to_14_seats", "queue_field": "slot_13_to_14_queue"},
            {"time": "14:00 to 15:00", "seats_field": "slot_14_to_15_seats", "queue_field": "slot_14_to_15_queue"},
            {"time": "15:00 to 16:00", "seats_field": "slot_15_to_16_seats", "queue_field": "slot_15_to_16_queue"},
            {"time": "16:00 to 17:00", "seats_field": "slot_16_to_17_seats", "queue_field": "slot_16_to_17_queue"},
            {"time": "17:00 to 18:00", "seats_field": "slot_17_to_18_seats", "queue_field": "slot_17_to_18_queue"},
        ]

        # Iterate through each slot and check availability
        for slot in slots:
            seats = getattr(museum, slot["seats_field"])
            queue = getattr(museum, slot["queue_field"])
            
            # Append the slot information to the response
            if seats > 0:
                response_lines.append(f">>>Slot {slot['time']}: {seats} seats available.>>>")
            else:
                response_lines.append(f">>>Slot {slot['time']}: No seats available. Queue length: {queue}.>>>")
        
        return "\n".join(response_lines)

    except Museum.DoesNotExist:
        return "⚠️ The specified museum ID does not exist."
    except Exception as e:
        return f"🚨 An error occurred: {str(e)}"
    
def handle_yes(user_message,request):
    if user_message.startswith("yes"):
        return render(request,"payment.html")

from datetime import datetime
from .models import Login,Transaction
from django.utils.dateparse import parse_date
from datetime import datetime

from django.utils.dateparse import parse_date
from datetime import datetime
from datetime import datetime



    # Check if the user and museum details are valid
from datetime import datetime
from django.shortcuts import render
from .models import Login, Museum, Transaction

import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from django.http import JsonResponse

from django.http import JsonResponse

def handle_date_input(request, date_str, user_id, last_museum_id):
    try:
        date_obj = datetime.strptime(date_str, '%d/%m/%Y')
    except ValueError:
        try:
            date_obj = datetime.strptime(date_str, '%d-%m-%Y')
        except ValueError:
            return JsonResponse({
                'error': 'Invalid date format. Please enter the date in DD/MM/YYYY or DD-MM-YYYY format.'
            }, status=400)

    formatted_date = date_obj.date()
    logger.debug(f"Parsed date: {formatted_date}")

    request.session['last_date_used'] = formatted_date.strftime('%Y-%m-%d')
    logger.debug(f"Stored date in session: {request.session['last_date_used']}")

    user = Login.objects.filter(id=user_id).first()
    museum = Museum.objects.filter(id=last_museum_id).first()

    if not user:
        logger.error(f"User not found: ID {user_id}")
        return JsonResponse({'error': 'User information not found. Please check your user ID.'}, status=404)
    if not museum:
        logger.error(f"Museum not found: ID {last_museum_id}")
        return JsonResponse({'error': 'Museum information not found. Please check your last museum ID.'}, status=404)

    existing_transaction = Transaction.objects.filter(
        date=formatted_date,
        museum_name_id=museum.name,
        username=user.username
    ).first()

    if existing_transaction:
        logger.info(f"Transaction already exists: {existing_transaction.id}")
        return JsonResponse({'message': 'A transaction for this date and user already exists.'}, status=200)

    new_transaction = Transaction(
        username=user.username,
        date=formatted_date,
        museum_name_id=museum.name,
        no_of_tickets=0,
        booking_status='pending',
        payment_status='unpaid',
        waiting_list=0,
    )
    new_transaction.save()
    logger.info(f"Created new transaction: {new_transaction.id}")

    return JsonResponse({'message': 'Transaction created.'}, status=200)

from django.shortcuts import get_object_or_404
from .models import Bookings

def handle_slot_input(slot_code, last_museum_id, user_id, request):
    # Validate museum selection
    if not last_museum_id:
        return "Please select a museum first before checking slot availability."

    # Validate the slot code
    if slot_code not in SLOT_MAPPING:
        return "Invalid slot code. Please provide a valid slot (e.g., 's1' for 9:00 to 10:00)."

    # Fetch the museum details using the last_museum_id
    try:
        museum = Museum.objects.get(id=last_museum_id)
    except Museum.DoesNotExist:
        return "Museum information not found for the selected ID."

    # Get the slot information from the SLOT_MAPPING dictionary
    slot_info = SLOT_MAPPING[slot_code]
    slot_time = slot_info['time']
    
    # Format the slot time for the field names
    slot_time_formatted = slot_time.replace(':00', '').replace(' ', '_')
    slot_descriptive = f"slot_{slot_time_formatted}"
    seat_field = f"{slot_descriptive}_seats"
    queue_field = f"{slot_descriptive}_queue"

    # Get the number of available seats and queue length for the selected slot
    available_seats = getattr(museum, seat_field, 0)
    queue_length = getattr(museum, queue_field, 0)

    # Determine the response based on seat availability
    if available_seats > 0:
        response = f"Slot {slot_time} has {available_seats} seats available. Tell the number of tickets you want to book:"
    else:
        response = f"Slot {slot_time} is full. Current queue length is {queue_length}."

    # Retrieve the date from session
    last_date_str = request.session.get('last_date_used')
    if not last_date_str:
        return response + " No booking date found. Please provide a valid date first."

    # Parse date from the session
    last_date_used = parse_date(last_date_str)
    if not last_date_used:
        return response + " Invalid date format in session. Please re-enter the date."

    # Fetch user details using user_id
    try:
        user = Login.objects.get(id=user_id)
    except Login.DoesNotExist:
        return "User information not found. Please check your user ID."

    # Get museum name and username
    museum_name = museum.name
    username = user.username

    # Fetch or create a transaction for the user, museum, and date
    transaction, created = Transaction.objects.get_or_create(
        username=username,
        museum_name_id=museum_name,
        date=last_date_used,
        defaults={'slot': slot_descriptive}  # Initialize with the descriptive slot if created
    )
    request.session['last_slot_code'] = slot_descriptive


    # If the transaction already exists, update the slot field
    if not created:
        transaction.slot = slot_descriptive
        transaction.save()

    # Save the slot information to the session

    # Return the response about slot availability and confirmation
    return response

from django.http import JsonResponse
from django.utils.dateparse import parse_date
from .models import Transaction, Museum
import logging

logger = logging.getLogger(__name__)


def handle_ticket_input(user_message, last_museum_id, request):
    # Extract ticket count from the user message (format: "tickets: <int>")
    if user_message.startswith("tickets: "):
        ticket_count_str = user_message.replace("tickets: ", "").strip()
        try:
            # Validate and convert ticket count to an integer
            count = int(ticket_count_str)
        except ValueError:
            return JsonResponse({'error': 'Invalid number of tickets. Please provide a valid integer.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid input format. Please use "tickets: <number>".'}, status=400)

    # Validate last_museum_id
    if not last_museum_id:
        return JsonResponse({'error': 'Museum ID is required to book tickets.'}, status=400)

    # Retrieve the last date and slot information from session
    last_date_str = request.session.get('last_date_used')
    last_slot_code = request.session.get('last_slot_code')

    if not last_date_str or not last_slot_code:
        return JsonResponse({'error': 'Date and slot information is required. Please select a museum and slot first.'}, status=400)

    # Parse date from the session
    last_date_used = parse_date(last_date_str)
    if not last_date_used:
        return JsonResponse({'error': 'Invalid date format in session. Please re-enter the date.'}, status=400)

    # Fetch the museum details using the last_museum_id
    try:
        museum = Museum.objects.get(id=last_museum_id)
    except Museum.DoesNotExist:
        return JsonResponse({'error': 'Museum information not found.'}, status=404)

    # Determine the seat and queue fields dynamically using the slot_code
    seat_field = f"{last_slot_code}_seats"  # e.g., 's1_seats'
    queue_field = f"{last_slot_code}_queue"  # e.g., 's1_queue'

    # Get available seats and queue length for the selected slot
    available_seats = getattr(museum, seat_field, 0)
    current_queue_length = getattr(museum, queue_field, 0)

    # Fetch or create the transaction for the current booking context
    transaction, created = Transaction.objects.get_or_create(
        username=request.user.username,
        museum_name_id=museum.name,
        date=last_date_used,
        slot=last_slot_code,
        defaults={'no_of_tickets': 0, 'waiting_list': 0, 'booking_status': 'pending', 'payment_status': 'unpaid'}
    )

    # Calculate the number of tickets to be booked and waiting list
    if count <= available_seats:
        tickets_to_book = count  # Enough seats are available
        waiting_list_count = 0
    else:
        tickets_to_book = available_seats  # Book what is available
        waiting_list_count = count - available_seats  # Remaining goes to the waiting list

    # Update the transaction with the number of tickets and waiting list
    transaction.no_of_tickets += tickets_to_book
    transaction.waiting_list += waiting_list_count
    transaction.booking_status = 'confirmed' if tickets_to_book > 0 else 'waiting'
    transaction.payment_status = 'unpaid'
    transaction.save()

    # Update the Museum model: Deduct the booked seats and update the queue
    setattr(museum, seat_field, available_seats - tickets_to_book)  # Deduct the seats
    setattr(museum, queue_field, current_queue_length + waiting_list_count)  # Update the queue
    museum.save()

    # Provide a payment link to the user
    payment_link = f"http://127.0.0.1:8000/payment"
    request.session['booking_id'] = transaction.id  # Assuming booking_id is transaction.id

    return JsonResponse({
        'message': f"Booking confirmed for {tickets_to_book} tickets. {waiting_list_count} added to the waiting list. Please proceed to payment.",
        'payment_link': payment_link
    })

from django.shortcuts import render

def ticket_view(request):
    if request.method == "POST":
        user_message = request.POST.get('user_message', '')
        if user_message.startswith("tickets: "):
            ticket_count = user_message.replace("tickets: ", "").strip()
            response = handle_ticket_input(ticket_count, request)
            return response

    return render(request, 'home.html')




from django.shortcuts import render

from django.shortcuts import redirect


from django.shortcuts import render, get_object_or_404, redirect
from .models import Transaction  # Make sure the Transaction model is imported
def payment_view(request):
    return render(request, 'payment.html')



def home(request):
    return render(request,'home.html')




# views.py

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .forms import UserCreationForm

from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm  # Make sure to use your custom form

User = get_user_model()  # Gets the custom user model

def sign_up(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # Use the custom form
        if form.is_valid():
            user = form.save()  # This will call the save method from your model and set the booking_id
            auth_login(request, user)  # Automatically log the user in after registration
            return redirect('login')  # Redirect to home page or any other page
        else:
            print(form.errors)  # Debugging purpose: Print form errors to console
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'sign_up.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponse



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Debug: Print received values
        print(f"Received username: {username}")
        print(f"Received password: {password}")

        if not username or not password:
            return HttpResponse('Username and password are required')

        user = authenticate(request, username=username, password=password)
        request.session['user_id'] = user.id
        
        if user is not None:
            auth_login(request, user)
            return redirect('chatbot_view')  # Redirect to home page or dashboard after successful login
        else:
            return HttpResponse('Invalid login credentials')
    return render(request, 'login.html')

def admin_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Debug: Print received values
        print(f"Received username: {username}")
        print(f"Received password: {password}")

        if not username or not password:
            return HttpResponse('Username and password are required')

        user = authenticate(request, username=username, password=password)
        request.session['user_id'] = user.id
        
        if user is not None:
            auth_login(request, user)
            return render(request,'admin.html')
        else:
            return HttpResponse('Invalid login credentials')
    return render(request,'admin_login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

from django.shortcuts import render, get_object_or_404
from .models import Transaction

from django.shortcuts import render, get_object_or_404

from django.shortcuts import render, get_object_or_404
from .models import Transaction

def success(request):
    # Retrieve the transaction from the database using the booking_id
    
    return render(request, 'success.html')


@login_required
def admin_view(request):
    return render(request,'admin.html')

def generate_response_data(request):
    # Create response data
    response = {"message": "This is a valid response"}
    return response
