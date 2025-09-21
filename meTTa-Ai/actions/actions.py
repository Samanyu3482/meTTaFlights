from rasa_sdk import Action, FormValidationAction
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk import Tracker
from datetime import datetime
import requests
from typing import Any, Text, Dict, List
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

gemini_api_key = os.environ.get("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set!")

genai.configure(api_key=gemini_api_key)
gemini_model = genai.GenerativeModel('gemini-2.5-flash-lite')

# IATA code mapping for cities and airports
iata_map = {
    # Albuquerque
    "albuquerque": "ABQ", "abq": "ABQ", "albuquerque international sunport": "ABQ",
    # Nantucket
    "nantucket": "ACK", "ack": "ACK", "nantucket memorial airport": "ACK",
    # Albany
    "albany": "ALB", "alb": "ALB", "albany international airport": "ALB",
    # Atlanta
    "atlanta": "ATL", "atl": "ATL", "hartsfield-jackson atlanta international airport": "ATL",
    # Austin
    "austin": "AUS", "aus": "AUS", "austin-bergstrom international airport": "AUS",
    # Asheville
    "asheville": "AVL", "avl": "AVL", "asheville regional airport": "AVL",
    # Hartford / Connecticut
    "hartford": "BDL", "bdl": "BDL", "bradley international airport": "BDL",
    # Bangor
    "bangor": "BGR", "bgr": "BGR", "bangor international airport": "BGR",
    # Birmingham
    "birmingham": "BHM", "bhm": "BHM", "birmingham-shuttlesworth international airport": "BHM",
    # Nashville
    "nashville": "BNA", "bna": "BNA", "nashville international airport": "BNA",
    # Boston
    "boston": "BOS", "bos": "BOS", "logan": "BOS", "boston logan international airport": "BOS",
    # Aguadilla / Puerto Rico
    "aguadilla": "BQN", "bqn": "BQN", "rafael hernandez airport": "BQN",
    # Burlington
    "burlington": "BTV", "btv": "BTV", "burlington international airport": "BTV",
    # Buffalo
    "buffalo": "BUF", "buf": "BUF", "buffalo niagara international airport": "BUF",
    # Burbank
    "burbank": "BUR", "bur": "BUR", "bob hope airport": "BUR",
    # Baltimore
    "baltimore": "BWI", "bwi": "BWI", "baltimore washington international": "BWI",
    # Bozeman
    "bozeman": "BZN", "bzn": "BZN", "bozeman yellowstone international airport": "BZN",
    # Columbia
    "columbia": "CAE", "cae": "CAE", "columbia metropolitan airport": "CAE",
    # Akron-Canton
    "akron": "CAK", "canton": "CAK", "cak": "CAK", "akron-canton regional airport": "CAK",
    # Charleston
    "charleston": "CHS", "chs": "CHS", "charleston international airport": "CHS",
    # Cleveland
    "cleveland": "CLE", "cle": "CLE", "cleveland hopkins international airport": "CLE",
    # Charlotte
    "charlotte": "CLT", "clt": "CLT", "charlotte douglas international airport": "CLT",
    # Columbus
    "columbus": "CMH", "cmh": "CMH", "john glenn columbus international airport": "CMH",
    # Charleston WV
    "charleston west virginia": "CRW", "crw": "CRW", "yeager airport": "CRW",
    # Cincinnati
    "cincinnati": "CVG", "cvg": "CVG", "cincinnati northern kentucky international": "CVG",
    # Dayton
    "dayton": "DAY", "day": "DAY", "dayton international airport": "DAY",
    # Washington - National
    "washington national": "DCA", "dca": "DCA", "reagan airport": "DCA",
    # Denver
    "denver": "DEN", "den": "DEN", "denver international airport": "DEN",
    # Dallas Fort Worth
    "dallas": "DFW", "fort worth": "DFW", "dfw": "DFW", "dallas/fort worth international airport": "DFW",
    # Des Moines
    "des moines": "DSM", "dsm": "DSM", "des moines international airport": "DSM",
    # Detroit
    "detroit": "DTW", "dtw": "DTW", "detroit metropolitan airport": "DTW",
    # Eagle County
    "eagle county": "EGE", "ege": "EGE", "eagle county regional airport": "EGE",
    # Newark
    "newark": "EWR", "ewr": "EWR", "newark liberty international airport": "EWR",
    # Key West
    "key west": "EYW", "eyw": "EYW", "key west international airport": "EYW",
    # Fort Lauderdale
    "fort lauderdale": "FLL", "fll": "FLL", "fort lauderdale-hollywood international airport": "FLL",
    # Grand Rapids
    "grand rapids": "GRR", "grr": "GRR", "gerald r. ford international airport": "GRR",
    # Greensboro
    "greensboro": "GSO", "gso": "GSO", "piedmont triad international airport": "GSO",
    # Greenville
    "greenville": "GSP", "gsp": "GSP", "greenville-spartanburg international airport": "GSP",
    # Hayden
    "hayden": "HDN", "hdn": "HDN", "yampa valley regional airport": "HDN",
    # Honolulu
    "honolulu": "HNL", "hnl": "HNL", "daniel k. inouye international airport": "HNL",
    # Houston Hobby
    "houston hobby": "HOU", "hou": "HOU", "william p. hobby airport": "HOU",
    # Washington Dulles
    "washington dulles": "IAD", "iad": "IAD", "dulles international airport": "IAD",
    "washington": "IAD",
    # Houston Intercontinental
    "houston": "IAH", "iah": "IAH", "george bush intercontinental airport": "IAH",
    # Wilmington
    "wilmington": "ILM", "ilm": "ILM", "wilmington international airport": "ILM",
    # Indianapolis
    "indianapolis": "IND", "ind": "IND", "indianapolis international airport": "IND",
    # Jackson Hole
    "jackson hole": "JAC", "jac": "JAC", "jackson hole airport": "JAC",
    # Jacksonville
    "jacksonville": "JAX", "jax": "JAX", "jacksonville international airport": "JAX",
    # New York JFK
    "new york": "JFK", "jfk": "JFK", "john f. kennedy international airport": "JFK",
    # Las Vegas
    "las vegas": "LAS", "las": "LAS", "mccarran international airport": "LAS",
    # Los Angeles
    "los angeles": "LAX", "lax": "LAX", "los angeles international airport": "LAX",
    # New York LaGuardia
    "laguardia": "LGA", "lga": "LGA", "new york laguardia airport": "LGA",
    # Long Beach
    "long beach": "LGB", "lgb": "LGB", "long beach airport": "LGB",
    # Kansas City
    "kansas city": "MCI", "mci": "MCI", "kansas city international airport": "MCI",
    # Orlando
    "orlando": "MCO", "mco": "MCO", "orlando international airport": "MCO",
    # Chicago Midway
    "chicago midway": "MDW", "mdw": "MDW", "chicago midway international airport": "MDW",
    # Memphis
    "memphis": "MEM", "mem": "MEM", "memphis international airport": "MEM",
    # Manchester
    "manchester": "MHT", "mht": "MHT", "manchester-boston regional airport": "MHT",
    # Miami
    "miami": "MIA", "mia": "MIA", "miami international airport": "MIA",
    # Milwaukee
    "milwaukee": "MKE", "mke": "MKE", "milwaukee mitchell international airport": "MKE",
    # Madison
    "madison": "MSN", "msn": "MSN", "dane county regional airport": "MSN",
    # Minneapolis
    "minneapolis": "MSP", "st. paul": "MSP", "msp": "MSP", "minneapolis-saint paul international airport": "MSP",
    # New Orleans
    "new orleans": "MSY", "msy": "MSY", "louis armstrong new orleans international airport": "MSY",
    # Montrose
    "montrose": "MTJ", "mtj": "MTJ", "montrose regional airport": "MTJ",
    # Martha's Vineyard
    "martha's vineyard": "MVY", "mvy": "MVY", "martha's vineyard airport": "MVY",
    # Myrtle Beach
    "myrtle beach": "MYR", "myr": "MYR", "myrtle beach international airport": "MYR",
    # Oakland
    "oakland": "OAK", "oak": "OAK", "oakland international airport": "OAK",
    # Oklahoma City
    "oklahoma city": "OKC", "okc": "OKC", "will rogers world airport": "OKC",
    # Omaha
    "omaha": "OMA", "oma": "OMA", "eppley airfield": "OMA",
    # Chicago O'Hare
    "chicago": "ORD", "ohare": "ORD", "ord": "ORD", "o'hare international airport": "ORD",
    # Norfolk
    "norfolk": "ORF", "orf": "ORF", "norfolk international airport": "ORF",
    # Palm Beach
    "palm beach": "PBI", "pbi": "PBI", "palm beach international airport": "PBI",
    # Portland OR
    "portland": "PDX", "pdx": "PDX", "portland international airport": "PDX",
    # Philadelphia
    "philadelphia": "PHL", "phl": "PHL", "philadelphia international airport": "PHL",
    # Phoenix
    "phoenix": "PHX", "phx": "PHX", "phoenix sky harbor international airport": "PHX",
    # Pittsburgh
    "pittsburgh": "PIT", "pit": "PIT", "pittsburgh international airport": "PIT",
    # Ponce / Mercedita
    "ponce": "PSE", "pse": "PSE", "mercedita airport": "PSE",
    # Palm Springs
    "palm springs": "PSP", "psp": "PSP", "palm springs international airport": "PSP",
    # Providence
    "providence": "PVD", "pvd": "PVD", "t.f. green international airport": "PVD",
    # Portland ME
    "portland maine": "PWM", "pwm": "PWM", "portland international jetport": "PWM",
    # Raleigh-Durham
    "raleigh": "RDU", "durham": "RDU", "rdu": "RDU", "raleigh-durham international airport": "RDU",
    # Richmond
    "richmond": "RIC", "ric": "RIC", "richmond international airport": "RIC",
    # Rochester
    "rochester": "ROC", "roc": "ROC", "greater rochester international airport": "ROC",
    # Fort Myers
    "fort myers": "RSW", "rsw": "RSW", "southwest florida international airport": "RSW",
    # San Diego
    "san diego": "SAN", "san": "SAN", "san diego international airport": "SAN",
    # San Antonio
    "san antonio": "SAT", "sat": "SAT", "san antonio international airport": "SAT",
    # Savannah
    "savannah": "SAV", "sav": "SAV", "savannah hilton head international airport": "SAV",
    # South Bend
    "south bend": "SBN", "sbn": "SBN", "south bend international airport": "SBN",
    # Louisville
    "louisville": "SDF", "sdf": "SDF", "louisville muhammad ali international airport": "SDF",
    # Seattle
    "seattle": "SEA", "sea": "SEA", "seattle-tacoma international airport": "SEA",
    # San Francisco
    "san francisco": "SFO", "sfo": "SFO", "san francisco international airport": "SFO",
    # San Jose
    "san jose": "SJC", "sjc": "SJC", "norman y. mineta san jose international airport": "SJC",
    # San Juan
    "san juan": "SJU", "sju": "SJU", "luis muñoz marín international airport": "SJU",
    # Salt Lake City
    "salt lake city": "SLC", "slc": "SLC", "salt lake city international airport": "SLC",
    # Sacramento
    "sacramento": "SMF", "smf": "SMF", "sacramento international airport": "SMF",
    # Orange County
    "orange county": "SNA", "sna": "SNA", "john wayne airport": "SNA",
    # Sarasota
    "sarasota": "SRQ", "srq": "SRQ", "sarasota-bradenton international airport": "SRQ",
    # St. Louis
    "st louis": "STL", "st. louis": "STL", "stl": "STL", "st. louis lambert international airport": "STL",
    # St. Thomas (USVI)
    "st thomas": "STT", "stt": "STT", "cyril e. king airport": "STT",
    # Syracuse
    "syracuse": "SYR", "syr": "SYR", "syracuse hancock international airport": "SYR",
    # Tampa
    "tampa": "TPA", "tpa": "TPA", "tampa international airport": "TPA",
    # Tulsa
    "tulsa": "TUL", "tul": "TUL", "tulsa international airport": "TUL",
    # Knoxville
    "knoxville": "TYS", "tys": "TYS", "mcghee tyson airport": "TYS",
    # Northwest Arkansas
    "arkansas": "XNA", "xna": "XNA", "northwest arkansas national airport": "XNA",
}

# Add a new action to capture flight details from metadata
class ActionSetFlightDetails(Action):
    def name(self) -> str:
        return "action_set_flight_details"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:

        # Get flight info from metadata
        metadata = tracker.latest_message.get("metadata", {})
        flight_details = metadata.get("flight_info")
        
        print(f"[DEBUG] Setting flight details from metadata: {flight_details}")
        
        if flight_details:
            # Store the flight details in the slot
            return [
                SlotSet("flight_info", flight_details),
                FollowupAction("booking_form")
            ]
        else:
            dispatcher.utter_message(text="Sorry, I couldn't find the flight details. Please try selecting the flight again.")
            return []


class ValidateBookingForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_booking_form"

    def validate_username(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        username = slot_value.strip()

        # Get flight_info from the slot that was set by action_set_flight_details
        flight_details = tracker.get_slot("flight_info")
        print(f"[DEBUG] Flight details in validate_username: {flight_details}")
        
        if not flight_details:
            # Try to get it from metadata as fallback
            metadata = tracker.latest_message.get("metadata", {})
            flight_details = metadata.get("flight_info")
            print(f"[DEBUG] Flight details from metadata fallback: {flight_details}")
            
            if not flight_details:
                dispatcher.utter_message(text="Sorry, I couldn't find the flight details to start the booking. Please try selecting the flight again.")
                return {"username": None, "flight_info": None}
            else:
                # If we got it from metadata, set it in the slot
                return {"flight_info": flight_details, "username": username}

        if not username:
            dispatcher.utter_message(text="Please provide a valid username.")
            return {"username": None}

        try:
            res = requests.get(f"http://localhost:8003/api/users/check_existence?username={username}")
            data = res.json()
            if data.get("exists"):
                dispatcher.utter_message(text=f"Hello, {username}! Please enter your F-PIN.")
                return {"username": username}
            else:
                dispatcher.utter_message(text="Sorry, that username does not exist. Please try again.")
                return {"username": None}
        except Exception as e:
            print(f"[DEBUG] Error checking username: {e}")
            dispatcher.utter_message(text=f"I'm sorry, I encountered an error checking your username. Please try again.")
            return {"username": None}

    def validate_mpin(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        username = tracker.get_slot("username")
        mpin = slot_value.strip()

        if not username:
            dispatcher.utter_message(text="Please provide your username first.")
            return {"mpin": None}

        payload = {"username": username, "mpin": mpin}
        try:
            res = requests.post("http://localhost:8003/api/users/authenticate", json=payload)
            data = res.json()
            if data.get("success"):
                dispatcher.utter_message(text="Authentication successful!")
                return {"mpin": mpin}
            else:
                dispatcher.utter_message(text="Authentication failed. Please check your username and F-PIN. Let's try again.")
                return {"username": None, "mpin": None}
        except Exception as e:
            print(f"[DEBUG] Authentication error: {e}")
            dispatcher.utter_message(text=f"Authentication error: {str(e)}. Please try again.")
            return {"username": None, "mpin": None}


class ActionFindFlight(Action):
    def name(self) -> str:
        return "action_find_flight"

    def run(self, 
            dispatcher: CollectingDispatcher, 
            tracker: Tracker, 
            domain: DomainDict) -> List[Dict[Text, Any]]:
        
        source = tracker.get_slot("source")
        destination = tracker.get_slot("destination")
        day = tracker.get_slot("day")
        month = tracker.get_slot("month")
        year = tracker.get_slot("year")
        date_slot = tracker.get_slot("date")
        priority = tracker.get_slot("priority") or "cost"
        print([source, destination, day, month, year, date_slot, priority])

        if not source:
            dispatcher.utter_message(text="Sorry I am not able to process your request currently. Please check our website meTTa-Flights for booking http://localhost:3000")
            return []
        if not destination:
            dispatcher.utter_message(text="Sorry I am not able to process your request currently. Please check our website meTTa-Flights for booking http://localhost:3000")
            return []
        
        if day and month and year:
            try:
                day = int(day)
                month = int(month)
                year = int(year)
            except ValueError:
                dispatcher.utter_message(text="Please provide valid numeric values for day, month, and year.")
                return []
        elif date_slot:
            try:
                date_str = date_slot.replace("/", "-").strip()
                dt = datetime.strptime(date_str, "%Y-%m-%d")
                year, month, day = dt.year, dt.month, dt.day
            except Exception:
                dispatcher.utter_message(text="I couldn't understand the date format. Please provide it as YYYY-MM-DD or specify day, month, and year separately.")
                return []
        else:
            dispatcher.utter_message(text="Please provide the travel date (day, month, year) or in YYYY-MM-DD format.")
            return []

        source = iata_map.get(source.strip().lower(), source.strip().upper())
        destination = iata_map.get(destination.strip().lower(), destination.strip().upper())

        payload = {
            "source": source,
            "destination": destination,
            "year": int(year),
            "month": int(month),
            "day": int(day),
            "priority": priority,
        }
        print(f"[DEBUG] Payload: {payload}")

        try:
            res = requests.get("http://localhost:8003/api/flights/search", params=payload)
            data = res.json()
            rum = data.get("flights", [])

            flights=[rum[0]]
            print(f"[DEBUG] Found flights: {len(flights)}")

            if not flights:
                dispatcher.utter_message(text="Sorry, no flights found for that query.")
            else:
                dispatcher.utter_message(json_message={"flights": flights})
                if flights:
                    return [
                        SlotSet("flight_info", flights[0]),
                        SlotSet("source", None),
                        SlotSet("destination", None),
                        SlotSet("date", None),
                        SlotSet("day", None),
                        SlotSet("month", None),
                        SlotSet("year", None),
                        SlotSet("priority", None)
                    ]

        except Exception as e:
            print(f"[DEBUG] Error fetching flights: {e}")
            dispatcher.utter_message(text=f"Sorry no best flights found according to you choice. Please check our website meTTa-Flights for booking http://localhost:3000 ")

        return [
            SlotSet("source", None),
            SlotSet("destination", None),
            SlotSet("date", None),
            SlotSet("day", None),
            SlotSet("month", None),
            SlotSet("year", None),
            SlotSet("priority", None)
        ]


class ActionBookFlight(Action):
    def name(self) -> str:
        return "action_book_flight"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:

        username = tracker.get_slot("username")
        mpin = tracker.get_slot("mpin")
        flight_details = tracker.get_slot("flight_info")
        
        print(f"[DEBUG] Booking flight for user: {username}")
        print(f"[DEBUG] Flight details in action_book_flight: {flight_details}")

        if not flight_details:
            dispatcher.utter_message(text="Sorry, I couldn't find the flight details. Please try selecting the flight again.")
            return [SlotSet("username", None), SlotSet("mpin", None)]

        if not username or not mpin:
            dispatcher.utter_message(text="Please provide both username and F-PIN for booking.")
            return [SlotSet("username", None), SlotSet("mpin", None)]

        payload = {
            "username": username,
            "flight_details": flight_details
        }

        try:
            print(f"[DEBUG] Sending booking request: {payload}")
            res = requests.post("http://localhost:8003/api/bookings/create", json=payload)
            data = res.json()
            
            print(f"[DEBUG] Booking response: {data}")
            
            if data.get("success"):
                booking_id = data.get("booking_id", "N/A")
                dispatcher.utter_message(
                    text=f"🎉 Booking confirmed! Your booking ID is {booking_id}. You can check your booking details in the bookings section."
                )
                return [
                    SlotSet("username", None), 
                    SlotSet("mpin", None), 
                    SlotSet("flight_info", None)
                ]
            else:
                error_msg = data.get("error", "Unknown error occurred")
                dispatcher.utter_message(text=f"Sorry, there was an issue with the booking: {error_msg}. Please try again.")
                return [SlotSet("username", None), SlotSet("mpin", None)]
                
        except Exception as e:
            print(f"[DEBUG] Booking error: {e}")
            dispatcher.utter_message(text=f"Booking error: {str(e)}")
            return [SlotSet("username", None), SlotSet("mpin", None)]


class ActionGeminiFallback(Action):
    def name(self) -> Text:
        return "action_gemini_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_message = tracker.latest_message.get('text')
        
        genai_api_key = os.environ.get("GEMINI_API_KEY")
        if not genai_api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set!")
        genai.configure(api_key=genai_api_key)
        gemini_model = genai.GenerativeModel('gemini-2.5-flash-lite')
        
        prompt = f"""
        You are an AI assistant for a flight search and booking platform named "meTTa-Flights". Your name is "meTTa-AI". Your purpose is to be a friendly, polite, and helpful conversational partner. You should answer all user queries, no matter how general, and try to keep the user engaged on the website.

        You are a cutting-edge AI chatbot that seamlessly integrates with SingularityNET's MeTTa knowledge representation system. Your backend is built with FastAPI and Python, and your frontend uses Next.js, Tailwind CSS, and other modern technologies.

        You have access to a knowledge base of over 75,000 flights from 103 US airports. The system uses three specialized APIs for cheapest, fastest, and optimized flight searches.

        When answering a query, use the following guidelines:
        - **Project-Specific Queries:** If the user asks about the project, its tech stack, or the underlying technology (like Rasa, MeTTa, or SingularityNET), provide a detailed and enthusiastic answer using the information below.
        - **General Queries:** For questions unrelated to the project (e.g., "what is the weather," "tell me a joke"), provide a brief, direct, and polite answer.
        - **Keep it Conversational:** Be friendly and use a helpful tone.
        - **Final Statement:** You **must** conclude every single response by telling the user how to provide flight booking information. Do not ask for specific details like source or destination. Instead, provide a clear, full example to help the user. For example: "I would be happy to help you with your next flight booking. You can provide me with the details like 'find me a flight from SOURCE to DESTINATION on YYYY-MM-DD'."
        - **General Knowledge:** You can answer general knowledge questions, for example about places to visit in certain places ,but always steer the conversation back to flight bookings.
        **Project Knowledge Base:**(only tell this info if user asks about the project or related tech)
        - **Name:** meTTa-AI, part of the "meTTa-Flights" project.
        - **Purpose:** A comprehensive flight search and booking platform.
        - **Core Technology:** Uses SingularityNET's MeTTa knowledge representation system to store flight data as "knowledge atoms". This allows for intelligent reasoning and optimization.
        - **Key Features:** Multi-API search (cheapest, fastest, optimized), unified booking, user authentication with JWT tokens, and a modern Next.js frontend.
        - **APIs:** The system has multiple APIs running on different ports, including a Backend on port 8000, Cheapest on 8001, Fastest on 8003, Optimized on 8002, and Unified Booking on 8005.
        - **Error Rate:** The system has a low error rate of <0.1% with graceful fallback.
        - **Tech Stack:** Frontend: Next.js 14, TypeScript, Tailwind CSS, Shadcn/ui. Backend: FastAPI, Python, JWT, SQLite, SQLAlchemy.

        User's question: {user_message}
        """

        try:
            response = gemini_model.generate_content(prompt)
            gemini_response = response.text
            dispatcher.utter_message(text=gemini_response)
        except Exception as e:
            print(f"[DEBUG] Gemini API error: {e}")
            dispatcher.utter_message(text=f"I'm sorry, I'm having trouble with that right now. Error: {e}")

        return []