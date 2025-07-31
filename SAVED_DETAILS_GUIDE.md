# Saved Passenger & Payment Details Guide

## 🎯 **Overview**

The saved details feature allows users to store passenger and payment information for quick reuse during future bookings. This saves time and reduces the need to re-enter the same information repeatedly.

## 📍 **Where to Save Details**

### **1. Automatic Saving (Primary Method)**
- **Location**: After successful booking completion
- **Process**: When you complete a booking, the system automatically saves:
  - First passenger as "Primary Passenger"
  - Payment method as "Default Payment"
- **No Action Required**: This happens automatically after your first booking

### **2. Manual Management (Profile Page)**
- **Location**: Profile Page → "Saved Details" Tab
- **Access**: Go to your profile and click the "Saved Details" tab
- **Features**:
  - View all saved passengers and payment methods
  - Add new passengers/payment methods manually
  - Edit existing details
  - Delete saved details
  - Set primary passengers and default payment methods

## 🚀 **How to Use Saved Details During Booking**

### **Step 1: Start Booking Process**
1. Search for flights on the Flights page
2. Select your desired flight
3. Click "Book Now" to proceed to booking

### **Step 2: Use Saved Passenger Details**
- **Location**: Each passenger form in the booking page
- **How to Use**:
  1. Look for the "Use saved:" dropdown next to each passenger form
  2. Click the dropdown to see your saved passengers
  3. Select a saved passenger to auto-fill the form
  4. The form will be populated with all saved details
  5. You can still edit any fields after loading

### **Step 3: Use Saved Payment Details**
- **Location**: Payment Information section in the booking page
- **How to Use**:
  1. Look for the "Use saved:" dropdown in the payment section
  2. Click the dropdown to see your saved payment methods
  3. Select a saved payment method to auto-fill the form
  4. The payment form will be populated with saved details
  5. You can still edit any fields after loading

## 🔧 **Managing Saved Details**

### **Profile Page Management**
1. **Navigate to Profile**: Click your profile icon → "Profile"
2. **Open Saved Details Tab**: Click the "Saved Details" tab
3. **View Saved Information**:
   - See all saved passengers with their details
   - See all saved payment methods (last 4 digits only for security)
   - Primary passengers and default payments are clearly marked

### **Available Actions**
- **Add New**: Click "Add Passenger" or "Add Payment Method" buttons
- **Edit**: Click the edit icon next to any saved detail
- **Delete**: Click the trash icon to remove saved details
- **Set Primary/Default**: Use the interface to mark primary passengers and default payments

## 🔒 **Security Features**

### **Payment Security**
- Only last 4 digits of card numbers are stored
- Full card details are never saved in the database
- CVV is never stored (must be entered for each booking)
- Secure encryption for all stored data

### **User Isolation**
- Each user can only see their own saved details
- No cross-user data access
- Secure authentication required for all operations

## 📱 **User Experience Flow**

### **First-Time User**
1. **Book First Flight**: Enter all passenger and payment details manually
2. **Automatic Saving**: After successful booking, details are automatically saved
3. **Future Bookings**: Use saved details via dropdown menus

### **Returning User**
1. **Quick Booking**: Use saved details to auto-fill forms
2. **Edit if Needed**: Modify any auto-filled information
3. **Complete Booking**: Proceed with booking as usual
4. **Updated Saving**: New details are saved for future use

## 🎨 **Visual Indicators**

### **In Booking Forms**
- **Dropdown Menus**: "Use saved:" dropdowns appear when saved details exist
- **Auto-fill**: Forms are populated instantly when selecting saved details
- **Success Messages**: Toast notifications confirm when details are loaded

### **In Profile Page**
- **Primary Badge**: "Primary" badge on main passenger
- **Default Badge**: "Default" badge on main payment method
- **Loading States**: Spinner animations while loading saved details
- **Empty States**: Helpful messages when no saved details exist

## 🔄 **Data Flow**

### **Saving Process**
1. User completes booking
2. System extracts passenger and payment data
3. Data is saved to database with user association
4. First passenger marked as primary
5. Payment method marked as default

### **Loading Process**
1. User starts new booking
2. System fetches saved details for the user
3. Dropdown menus are populated with saved options
4. User selects desired saved details
5. Forms are auto-filled with selected data

## 🛠 **Technical Implementation**

### **Backend**
- **Database Models**: `SavedPassenger` and `SavedPayment` tables
- **API Endpoints**: Full CRUD operations for saved details
- **Security**: JWT authentication and user isolation
- **Validation**: Data validation and sanitization

### **Frontend**
- **API Service**: `savedDetailsApiService` for backend communication
- **State Management**: React state for saved details
- **UI Components**: Dropdown menus and management interface
- **Error Handling**: Graceful error handling and user feedback

## 📋 **Best Practices**

### **For Users**
- Keep saved details up to date
- Use primary passenger for yourself
- Set your most-used payment method as default
- Review saved details periodically

### **For Security**
- Never share your login credentials
- Use strong passwords
- Log out when using shared devices
- Report any suspicious activity

## 🆘 **Troubleshooting**

### **Common Issues**
- **No Saved Details**: Complete your first booking to start saving details
- **Dropdown Not Appearing**: Ensure you're logged in and have saved details
- **Auto-fill Not Working**: Try refreshing the page and selecting again
- **Can't Edit Details**: Use the profile page to manage saved details

### **Getting Help**
- Check the profile page for saved details management
- Ensure you're logged in with the correct account
- Contact support if issues persist

---

**Note**: This feature is designed to make your booking experience faster and more convenient while maintaining the highest security standards for your personal information. 