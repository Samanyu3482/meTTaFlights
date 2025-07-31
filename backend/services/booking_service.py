import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from models.booking import Booking, Passenger, Payment
from models.user import User
from schemas.booking_schemas import CreateBookingRequest, UpdateBookingStatusRequest

class BookingService:
    def __init__(self):
        pass
    
    def generate_booking_ref(self) -> str:
        """Generate a unique booking reference"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_suffix = str(uuid.uuid4())[:8].upper()
        return f"BK{timestamp}{random_suffix}"
    
    def create_booking(self, db: Session, user_id: int, booking_data: CreateBookingRequest) -> Optional[Booking]:
        """Create a new booking with passengers and payment"""
        try:
            # Create the main booking
            booking = Booking(
                booking_ref=self.generate_booking_ref(),
                user_id=user_id,
                status="confirmed",
                
                # Flight details
                flight_year=booking_data.flight.year,
                flight_month=booking_data.flight.month,
                flight_day=booking_data.flight.day,
                source=booking_data.flight.source,
                destination=booking_data.flight.destination,
                cost=booking_data.flight.cost,
                takeoff=booking_data.flight.takeoff,
                landing=booking_data.flight.landing,
                duration=booking_data.flight.duration,
                
                # Airline details
                airline_code=booking_data.flight.airline.get('code') if booking_data.flight.airline else None,
                airline_name=booking_data.flight.airline.get('name') if booking_data.flight.airline else None,
                airline_logo=booking_data.flight.airline.get('logo') if booking_data.flight.airline else None,
                airline_description=booking_data.flight.airline.get('description') if booking_data.flight.airline else None,
                
                # Flight type
                is_connecting=booking_data.flight.is_connecting or False,
                connection_airport=booking_data.flight.connection_airport,
                layover_hours=booking_data.flight.layover_hours,
                
                # Booking details
                total_cost=float(booking_data.flight.cost.replace('$', '').replace(',', '')) * booking_data.passenger_count,
                passenger_count=booking_data.passenger_count
            )
            
            db.add(booking)
            db.flush()  # Get the booking ID
            
            # Create passengers
            for passenger_data in booking_data.passengers:
                passenger = Passenger(
                    booking_id=booking.id,
                    first_name=passenger_data.first_name,
                    last_name=passenger_data.last_name,
                    date_of_birth=passenger_data.date_of_birth,
                    passport_number=passenger_data.passport_number,
                    email=passenger_data.email,
                    phone=passenger_data.phone,
                    seat_preference=passenger_data.seat_preference,
                    special_requests=passenger_data.special_requests
                )
                db.add(passenger)
            
            # Create payment (store only last 4 digits for security)
            card_number = booking_data.payment.card_number
            last_four = card_number[-4:] if len(card_number) >= 4 else card_number
            
            payment = Payment(
                booking_id=booking.id,
                card_number=last_four,  # Only last 4 digits
                card_holder_name=booking_data.payment.card_holder_name,
                expiry_month=booking_data.payment.expiry_month,
                expiry_year=booking_data.payment.expiry_year,
                cvv=booking_data.payment.cvv,
                billing_address=booking_data.payment.billing_address,
                city=booking_data.payment.city,
                state=booking_data.payment.state,
                zip_code=booking_data.payment.zip_code,
                country=booking_data.payment.country
            )
            db.add(payment)
            
            db.commit()
            db.refresh(booking)
            return booking
            
        except Exception as e:
            db.rollback()
            print(f"Error creating booking: {str(e)}")
            return None
    
    def get_user_bookings(self, db: Session, user_id: int) -> List[Booking]:
        """Get all bookings for a user"""
        try:
            bookings = db.query(Booking).filter(
                Booking.user_id == user_id
            ).order_by(Booking.created_at.desc()).all()
            return bookings
        except Exception as e:
            print(f"Error getting user bookings: {str(e)}")
            return []
    
    def get_booking_by_id(self, db: Session, booking_id: int, user_id: int) -> Optional[Booking]:
        """Get a specific booking by ID (user can only see their own bookings)"""
        try:
            booking = db.query(Booking).filter(
                Booking.id == booking_id,
                Booking.user_id == user_id
            ).first()
            return booking
        except Exception as e:
            print(f"Error getting booking: {str(e)}")
            return None
    
    def get_booking_by_ref(self, db: Session, booking_ref: str, user_id: int) -> Optional[Booking]:
        """Get a booking by reference number (user can only see their own bookings)"""
        try:
            booking = db.query(Booking).filter(
                Booking.booking_ref == booking_ref,
                Booking.user_id == user_id
            ).first()
            return booking
        except Exception as e:
            print(f"Error getting booking by ref: {str(e)}")
            return None
    
    def update_booking_status(self, db: Session, booking_id: int, user_id: int, status_data: UpdateBookingStatusRequest) -> Optional[Booking]:
        """Update booking status"""
        try:
            booking = self.get_booking_by_id(db, booking_id, user_id)
            if not booking:
                return None
            
            booking.status = status_data.status
            booking.updated_at = datetime.utcnow()
            
            db.commit()
            db.refresh(booking)
            return booking
        except Exception as e:
            db.rollback()
            print(f"Error updating booking status: {str(e)}")
            return None
    
    def delete_booking(self, db: Session, booking_id: int, user_id: int) -> bool:
        """Delete a booking (user can only delete their own bookings)"""
        try:
            booking = self.get_booking_by_id(db, booking_id, user_id)
            if not booking:
                return False
            
            db.delete(booking)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print(f"Error deleting booking: {str(e)}")
            return False
    
    def get_bookings_by_status(self, db: Session, user_id: int, status: str) -> List[Booking]:
        """Get bookings by status"""
        try:
            bookings = db.query(Booking).filter(
                Booking.user_id == user_id,
                Booking.status == status
            ).order_by(Booking.created_at.desc()).all()
            return bookings
        except Exception as e:
            print(f"Error getting bookings by status: {str(e)}")
            return []
    
    def get_upcoming_bookings(self, db: Session, user_id: int) -> List[Booking]:
        """Get upcoming bookings (confirmed and future date)"""
        try:
            from datetime import date
            today = date.today()
            
            bookings = db.query(Booking).filter(
                Booking.user_id == user_id,
                Booking.status == "confirmed"
            ).all()
            
            # Filter for future dates
            upcoming_bookings = []
            for booking in bookings:
                try:
                    flight_date = date(
                        int(booking.flight_year),
                        int(booking.flight_month),
                        int(booking.flight_day)
                    )
                    if flight_date >= today:
                        upcoming_bookings.append(booking)
                except (ValueError, TypeError):
                    continue
            
            return sorted(upcoming_bookings, key=lambda x: x.created_at, reverse=True)
        except Exception as e:
            print(f"Error getting upcoming bookings: {str(e)}")
            return []
    
    def get_completed_bookings(self, db: Session, user_id: int) -> List[Booking]:
        """Get completed bookings (past date)"""
        try:
            from datetime import date
            today = date.today()
            
            bookings = db.query(Booking).filter(
                Booking.user_id == user_id
            ).all()
            
            # Filter for past dates
            completed_bookings = []
            for booking in bookings:
                try:
                    flight_date = date(
                        int(booking.flight_year),
                        int(booking.flight_month),
                        int(booking.flight_day)
                    )
                    if flight_date < today:
                        completed_bookings.append(booking)
                except (ValueError, TypeError):
                    continue
            
            return sorted(completed_bookings, key=lambda x: x.created_at, reverse=True)
        except Exception as e:
            print(f"Error getting completed bookings: {str(e)}")
            return []

# Create global instance
booking_service = BookingService() 