import httpx
from typing import Optional, Dict, Any
from schemas.flight_schemas import PassengerInfo

class UserService:
    def __init__(self):
        self.auth_api_url = "http://localhost:8001"
    
    async def get_current_user_details(self, token: str) -> Optional[Dict[str, Any]]:
        """Get current user details from auth API"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.auth_api_url}/api/auth/me",
                    headers={"Authorization": f"Bearer {token}"},
                    timeout=10.0
                )
                if response.status_code == 200:
                    return response.json()
                else:
                    print(f"Failed to get user details: {response.status_code}")
                    return None
        except Exception as e:
            print(f"Error fetching user details: {str(e)}")
            return None
    
    async def get_user_saved_passengers(self, token: str) -> Optional[Dict[str, Any]]:
        """Get user's saved passengers from auth API"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.auth_api_url}/api/user/saved-passengers",
                    headers={"Authorization": f"Bearer {token}"},
                    timeout=10.0
                )
                if response.status_code == 200:
                    return response.json()
                else:
                    print(f"Failed to get saved passengers: {response.status_code}")
                    return None
        except Exception as e:
            print(f"Error fetching saved passengers: {str(e)}")
            return None
    
    async def get_user_passenger_info(self, user_id: str, token: str) -> PassengerInfo:
        """Get passenger information for the current user"""
        try:
            # Get user details
            user_details = await self.get_current_user_details(token)
            
            # Get saved passengers
            saved_passengers = await self.get_user_saved_passengers(token)
            
            if user_details:
                # Use primary saved passenger if available, otherwise use user details
                primary_passenger = None
                if saved_passengers:
                    for passenger in saved_passengers:
                        if passenger.get('is_primary', False):
                            primary_passenger = passenger
                            break
                
                if primary_passenger:
                    # Use saved passenger details
                    return PassengerInfo(
                        first_name=primary_passenger.get('first_name', ''),
                        last_name=primary_passenger.get('last_name', ''),
                        email=primary_passenger.get('email', user_details.get('email', '')),
                        date_of_birth=primary_passenger.get('date_of_birth', ''),
                        passport_number=primary_passenger.get('passport_number', ''),
                        nationality=primary_passenger.get('nationality', 'US'),
                        seat_preference=primary_passenger.get('seat_preference', 'window'),
                        meal_preference=primary_passenger.get('special_requests', 'standard')
                    )
                else:
                    # Use user details as fallback
                    return PassengerInfo(
                        first_name=user_details.get('name', '').split()[0] if user_details.get('name') else 'User',
                        last_name=user_details.get('name', '').split()[-1] if user_details.get('name') and len(user_details.get('name', '').split()) > 1 else 'Name',
                        email=user_details.get('email', ''),
                        date_of_birth=user_details.get('date_of_birth', '1990-01-01'),
                        passport_number=None,
                        nationality=user_details.get('nationality', 'US'),
                        seat_preference='window',
                        meal_preference='standard'
                    )
            else:
                # Fallback to default passenger info
                return PassengerInfo(
                    first_name="User",
                    last_name="Name",
                    email="user@example.com",
                    date_of_birth="1990-01-01",
                    passport_number=None,
                    nationality="US",
                    seat_preference="window",
                    meal_preference="standard"
                )
                
        except Exception as e:
            print(f"Error getting passenger info: {str(e)}")
            # Return default passenger info on error
            return PassengerInfo(
                first_name="User",
                last_name="Name",
                email="user@example.com",
                date_of_birth="1990-01-01",
                passport_number=None,
                nationality="US",
                seat_preference="window",
                meal_preference="standard"
            )

# Initialize user service
user_service = UserService() 