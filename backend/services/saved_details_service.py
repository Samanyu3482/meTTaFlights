from typing import List, Optional
from sqlalchemy.orm import Session
from models.user import SavedPassenger, SavedPayment
from schemas.auth_schemas import SavedPassengerRequest, SavedPaymentRequest

class SavedDetailsService:
    def __init__(self):
        pass
    
    # Saved Passengers methods
    def get_user_saved_passengers(self, db: Session, user_id: int) -> List[SavedPassenger]:
        """Get all saved passengers for a user"""
        try:
            passengers = db.query(SavedPassenger).filter(
                SavedPassenger.user_id == user_id
            ).order_by(SavedPassenger.created_at.desc()).all()
            return passengers
        except Exception as e:
            print(f"Error getting saved passengers: {str(e)}")
            return []
    
    def save_passenger(self, db: Session, user_id: int, passenger_data: SavedPassengerRequest) -> Optional[SavedPassenger]:
        """Save a new passenger for a user"""
        try:
            # If this is marked as primary, unmark other primary passengers
            if passenger_data.is_primary:
                db.query(SavedPassenger).filter(
                    SavedPassenger.user_id == user_id,
                    SavedPassenger.is_primary == True
                ).update({"is_primary": False})
            
            passenger = SavedPassenger(
                user_id=user_id,
                first_name=passenger_data.first_name,
                last_name=passenger_data.last_name,
                date_of_birth=passenger_data.date_of_birth,
                passport_number=passenger_data.passport_number,
                email=passenger_data.email,
                phone=passenger_data.phone,
                seat_preference=passenger_data.seat_preference,
                special_requests=passenger_data.special_requests,
                is_primary=passenger_data.is_primary
            )
            
            db.add(passenger)
            db.commit()
            db.refresh(passenger)
            return passenger
        except Exception as e:
            db.rollback()
            print(f"Error saving passenger: {str(e)}")
            return None
    
    def update_saved_passenger(self, db: Session, passenger_id: int, user_id: int, passenger_data: SavedPassengerRequest) -> Optional[SavedPassenger]:
        """Update a saved passenger"""
        try:
            passenger = db.query(SavedPassenger).filter(
                SavedPassenger.id == passenger_id,
                SavedPassenger.user_id == user_id
            ).first()
            
            if not passenger:
                return None
            
            # If this is marked as primary, unmark other primary passengers
            if passenger_data.is_primary:
                db.query(SavedPassenger).filter(
                    SavedPassenger.user_id == user_id,
                    SavedPassenger.id != passenger_id,
                    SavedPassenger.is_primary == True
                ).update({"is_primary": False})
            
            # Update passenger data
            for field, value in passenger_data.dict().items():
                setattr(passenger, field, value)
            
            db.commit()
            db.refresh(passenger)
            return passenger
        except Exception as e:
            db.rollback()
            print(f"Error updating saved passenger: {str(e)}")
            return None
    
    def delete_saved_passenger(self, db: Session, passenger_id: int, user_id: int) -> bool:
        """Delete a saved passenger"""
        try:
            passenger = db.query(SavedPassenger).filter(
                SavedPassenger.id == passenger_id,
                SavedPassenger.user_id == user_id
            ).first()
            
            if not passenger:
                return False
            
            db.delete(passenger)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print(f"Error deleting saved passenger: {str(e)}")
            return False
    
    # Saved Payments methods
    def get_user_saved_payments(self, db: Session, user_id: int) -> List[SavedPayment]:
        """Get all saved payments for a user"""
        try:
            payments = db.query(SavedPayment).filter(
                SavedPayment.user_id == user_id
            ).order_by(SavedPayment.created_at.desc()).all()
            return payments
        except Exception as e:
            print(f"Error getting saved payments: {str(e)}")
            return []
    
    def save_payment(self, db: Session, user_id: int, payment_data: SavedPaymentRequest) -> Optional[SavedPayment]:
        """Save a new payment method for a user"""
        try:
            # If this is marked as default, unmark other default payments
            if payment_data.is_default:
                db.query(SavedPayment).filter(
                    SavedPayment.user_id == user_id,
                    SavedPayment.is_default == True
                ).update({"is_default": False})
            
            # Store only last 4 digits for security
            card_number = payment_data.card_number
            last_four = card_number[-4:] if len(card_number) >= 4 else card_number
            
            payment = SavedPayment(
                user_id=user_id,
                card_number=last_four,
                card_holder_name=payment_data.card_holder_name,
                expiry_month=payment_data.expiry_month,
                expiry_year=payment_data.expiry_year,
                billing_address=payment_data.billing_address,
                city=payment_data.city,
                state=payment_data.state,
                zip_code=payment_data.zip_code,
                country=payment_data.country,
                is_default=payment_data.is_default
            )
            
            db.add(payment)
            db.commit()
            db.refresh(payment)
            return payment
        except Exception as e:
            db.rollback()
            print(f"Error saving payment: {str(e)}")
            return None
    
    def update_saved_payment(self, db: Session, payment_id: int, user_id: int, payment_data: SavedPaymentRequest) -> Optional[SavedPayment]:
        """Update a saved payment method"""
        try:
            payment = db.query(SavedPayment).filter(
                SavedPayment.id == payment_id,
                SavedPayment.user_id == user_id
            ).first()
            
            if not payment:
                return None
            
            # If this is marked as default, unmark other default payments
            if payment_data.is_default:
                db.query(SavedPayment).filter(
                    SavedPayment.user_id == user_id,
                    SavedPayment.id != payment_id,
                    SavedPayment.is_default == True
                ).update({"is_default": False})
            
            # Store only last 4 digits for security
            card_number = payment_data.card_number
            last_four = card_number[-4:] if len(card_number) >= 4 else card_number
            
            # Update payment data
            payment.card_number = last_four
            payment.card_holder_name = payment_data.card_holder_name
            payment.expiry_month = payment_data.expiry_month
            payment.expiry_year = payment_data.expiry_year
            payment.billing_address = payment_data.billing_address
            payment.city = payment_data.city
            payment.state = payment_data.state
            payment.zip_code = payment_data.zip_code
            payment.country = payment_data.country
            payment.is_default = payment_data.is_default
            
            db.commit()
            db.refresh(payment)
            return payment
        except Exception as e:
            db.rollback()
            print(f"Error updating saved payment: {str(e)}")
            return None
    
    def delete_saved_payment(self, db: Session, payment_id: int, user_id: int) -> bool:
        """Delete a saved payment method"""
        try:
            payment = db.query(SavedPayment).filter(
                SavedPayment.id == payment_id,
                SavedPayment.user_id == user_id
            ).first()
            
            if not payment:
                return False
            
            db.delete(payment)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print(f"Error deleting saved payment: {str(e)}")
            return False

# Create global instance
saved_details_service = SavedDetailsService() 