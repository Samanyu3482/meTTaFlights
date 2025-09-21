from rasa_sdk import Action, FormValidationAction
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk import Tracker
from datetime import datetime
import requests
from typing import Any, Text, Dict, List

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

# Replace BookingForm with FormValidationAction
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
        """Validate username value."""
        if slot_value and len(slot_value.strip()) > 0:
            return {"username": slot_value.strip()}
        else:
            dispatcher.utter_message(text="Please provide a valid username.")
            return {"username": None}

    def validate_mpin(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate mpin value and authenticate the user."""
        username = tracker.get_slot("username")
        mpin = slot_value

        if not username:
            dispatcher.utter_message(text="Please provide your username first.")
            return {"mpin": None}

        payload = {"username": username, "mpin": mpin}
        try:
            # Call your API to authenticate
            res = requests.post("http://localhost:8003/api/users/authenticate", json=payload)
            data = res.json()

            if data.get("success"):
                dispatcher.utter_message(text="Authentication successful!")
                return {"mpin": mpin}
            else:
                dispatcher.utter_message(text="Authentication failed. Please check your username and MPIN. Let's try again.")
                # Reset slots to restart the form
                return {"username": None, "mpin": None}
        except Exception as e:
            dispatcher.utter_message(text=f"Authentication error: {str(e)}. Please try again.")
            return {"username": None, "mpin": None}

# actions.py

class ActionBookFlight(Action):
    def name(self) -> str:
        return "action_book_flight"

    def run(self, 
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:
        
        username = tracker.get_slot("username")
        mpin = tracker.get_slot("mpin")
        
        # Check if user is authenticated
        if not username or not mpin:
            dispatcher.utter_message(text="To book this flight, I need to authenticate you first. Please provide your username and MPIN.")
            return [SlotSet("requested_slot", "username")]
        
        # Retrieve flight details from the slot instead of the latest message
        flight_details = tracker.get_slot("flight_info")
        
        if not flight_details:
            dispatcher.utter_message(text="Sorry, I couldn't find the flight details. Please try selecting the flight again.")
            return []

        payload = {
            "username": username,
            "flight_details": flight_details
        }

        try:
            res = requests.post("http://localhost:8003/api/bookings/create", json=payload)
            data = res.json()
            if data.get("success"):
                dispatcher.utter_message(text=f"Booking confirmed! Your booking ID is {data.get('booking_id')}. You can check your booking details in bookings section.")
                # Clear authentication slots after successful booking
                return [SlotSet("username", None), SlotSet("mpin", None)]
            else:
                dispatcher.utter_message(text="Sorry, there was an issue with the booking. Please try again.")
        except Exception as e:
            dispatcher.utter_message(text=f"Booking error: {str(e)}")

        return []
    
    # You can remove the _extract_flight_details method from this class
    # as you are now getting the information from a slot.

class ActionFindFlight(Action):
    def name(self) -> str:
        return "action_find_flight"

    def run(self, 
            dispatcher: CollectingDispatcher, 
            tracker: Tracker, 
            domain: DomainDict) -> List[Dict[Text, Any]]:
        
        source = tracker.get_slot("source")
        destination = tracker.get_slot("destination")
        
        # Get separate date components
        day = tracker.get_slot("day")
        month = tracker.get_slot("month")
        year = tracker.get_slot("year")
        
        # Fallback: try to parse from combined date slot if separate components not available
        date_slot = tracker.get_slot("date")
        
        priority = tracker.get_slot("priority") or "cost"

        if not source:
            dispatcher.utter_message(text="Please provide the source airport or city.")
            return []
        if not destination:
            dispatcher.utter_message(text="Please provide the destination airport or city.")
            return []
        
        # Handle date components
        if day and month and year:
            # Use separate components if available
            try:
                day = int(day)
                month = int(month)
                year = int(year)
            except ValueError:
                dispatcher.utter_message(text="Please provide valid numeric values for day, month, and year.")
                return []
        elif date_slot:
            # Parse combined date as fallback
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

        # Convert city names to IATA codes using the iata_map
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
            flights = data.get("flights", [])
            print(flights)

            if not flights:
                dispatcher.utter_message(text="Sorry, no flights found for that query.")
            else:
                dispatcher.utter_message(json_message={"flights": flights})

        except Exception as e:
            dispatcher.utter_message(text=f"Error fetching flights: {str(e)}")

        return [
            SlotSet("source", None),
            SlotSet("destination", None),
            SlotSet("date", None),
            SlotSet("day", None),
            SlotSet("month", None),
            SlotSet("year", None),
            SlotSet("priority", None)
        ]
    
class ActionSetFlightDetails(Action):
    def name(self) -> Text:
        return "action_set_flight_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Extract flight details from the message metadata
        flight_details = tracker.latest_message.get("metadata", {}).get("flight_info")

        if flight_details:
            return [SlotSet("flight_info", flight_details)]
        else:
            dispatcher.utter_message(text="Sorry, I couldn't find the flight details to start the booking. Please try again.")
            return []