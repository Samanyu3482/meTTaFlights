# MeTTa Flight Search & Booking System

A comprehensive flight search and booking platform featuring a modern Next.js frontend, multiple specialized search APIs, authentication system, and unified booking capabilities.

##  Features

- **Multi-API Search System**: Three specialized APIs for cheapest, fastest, and optimized flight searches
- **Unified Booking System**: Seamless integration between search APIs and booking backend
- **User Authentication**: Complete login/signup system with JWT tokens
- **Modern UI**: Beautiful, responsive frontend built with Next.js, Tailwind CSS, and shadcn/ui
- **Real MeTTa Integration**: Search flights using the MeTTa knowledge base with 50,000+ flight records
- **Smart Search**: Advanced filtering by source, destination, date, price, and travel preferences
- **Real-time Results**: Instant search results from multiple search algorithms
- **Booking Management**: Complete booking workflow with user trip management

##  System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Cheapest API  │    │   Fastest API   │    │ Optimized API   │
│   (Port 8001)   │    │   (Port 8003)   │    │   (Port 8002)   │
│                 │    │                 │    │                 │
│ • Price Focus   │    │ • Time Focus    │    │ • Balanced      │
│ • Cost Sorting  │    │ • Duration Opt  │    │ • Multi-Factor  │
│ • Budget Travel │    │ • Speed First   │    │ • Smart Scoring │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌─────────────▼─────────────┐
                    │   Unified Booking API     │
                    │      (Port 8005)          │
                    │                           │
                    │ • Integration Layer       │
                    │ • Data Transformation     │
                    │ • Booking Orchestration   │
                    │ • User Management         │
                    └─────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │   Backend Auth & Booking  │
                    │      (Port 8000)          │
                    │                           │
                    │ • User Authentication     │
                    │ • Booking Management      │
                    │ • Database Operations     │
                    │ • Session Management      │
                    └─────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │   Next.js Frontend        │
                    │      (Port 3000)          │
                    │                           │
                    │ • User Interface          │
                    │ • Search & Booking        │
                    │ • Trip Management         │
                    │ • Profile Management      │
                    └───────────────────────────┘
```

##  Prerequisites

Before setting up the project, ensure you have the following installed:

### Required Software
- **Python 3.12+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 18+** - [Download Node.js](https://nodejs.org/)
- **Git** - [Download Git](https://git-scm.com/)
- **pip** (Python package manager - usually comes with Python)

### Verify Installation
```bash
# Check Python version
python --version  # Should be 3.12 or higher

# Check Node.js version
node --version    # Should be 18 or higher

# Check npm version
npm --version     # Should be 9 or higher

# Check Git version
git --version     # Should be installed
```

##  Complete Setup Guide

### Step 1: Clone the Repository
```bash
# Clone the repository
git clone <your-repository-url>
cd metta

# Verify the project structure
ls -la
```

### Step 2: Set Up Python Virtual Environment
```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Verify activation (you should see (venv) in your terminal)
which python  # Should point to venv/bin/python
```

### Step 3: Install Python Dependencies

#### Backend Dependencies
```bash
# Install backend dependencies
cd backend
pip install -r requirements.txt
cd ..
```

#### Search APIs Dependencies
```bash
# Install cheapest API dependencies
cd chatbot-api/cheapest-api
pip install -r requirements.txt
cd ../..

# Install fastest API dependencies
cd chatbot-api/fastest-api
pip install -r requirements.txt
cd ../..

# Install optimized API dependencies
cd chatbot-api/optimized-api
pip install -r requirements.txt
cd ../..

# Install unified booking API dependencies
cd chatbot-api/unified-booking-api
pip install -r requirements.txt
cd ../..
```

### Step 4: Set Up Database
```bash
# Navigate to backend directory
cd backend

# Initialize the database (this will create auth_database.db)
python -c "
from database.database import engine
from models import user, booking
user.Base.metadata.create_all(bind=engine)
booking.Base.metadata.create_all(bind=engine)
print('Database initialized successfully!')
"

cd ..
```

### Step 5: Install Node.js Dependencies
```bash
# Install frontend dependencies
cd me-tt-a-flights
npm install
cd ..
```

### Step 6: Environment Configuration

#### Backend Environment
```bash
# Create backend environment file
cd backend
cat > .env << EOF
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
DATABASE_URL=sqlite:///./auth_database.db
EOF
cd ..
```

#### Frontend Environment
```bash
# Create frontend environment file
cd me-tt-a-flights
cat > .env.local << EOF
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_CHEAPEST_API_URL=http://localhost:8001
NEXT_PUBLIC_FASTEST_API_URL=http://localhost:8003
NEXT_PUBLIC_OPTIMIZED_API_URL=http://localhost:8002
NEXT_PUBLIC_UNIFIED_BOOKING_API_URL=http://localhost:8005
EOF
cd ..
```

##  Starting the Application

### Option 1: Automated Startup (Recommended)
```bash
# Make the startup script executable
chmod +x start_all_services.sh

# Start all services
./start_all_services.sh
```

### Option 2: Manual Startup

#### Terminal 1: Backend Authentication & Booking API
```bash
# Activate virtual environment
source venv/bin/activate

# Start backend API
cd backend
python api.py
```
**Backend will be running on:** http://localhost:8000

#### Terminal 2: Cheapest Search API
```bash
# Activate virtual environment
source venv/bin/activate

# Start cheapest API
cd chatbot-api/cheapest-api
python main.py
```
**Cheapest API will be running on:** http://localhost:8001

#### Terminal 3: Fastest Search API
```bash
# Activate virtual environment
source venv/bin/activate

# Start fastest API
cd chatbot-api/fastest-api
python main.py
```
**Fastest API will be running on:** http://localhost:8003

#### Terminal 4: Optimized Search API
```bash
# Activate virtual environment
source venv/bin/activate

# Start optimized API
cd chatbot-api/optimized-api
python main.py
```
**Optimized API will be running on:** http://localhost:8002

#### Terminal 5: Unified Booking API
```bash
# Activate virtual environment
source venv/bin/activate

# Start unified booking API
cd chatbot-api/unified-booking-api
python main.py
```
**Unified Booking API will be running on:** http://localhost:8005

#### Terminal 6: Frontend Application
```bash
# Start frontend
cd me-tt-a-flights
npm run dev
```
**Frontend will be running on:** http://localhost:3000

##  Verifying the Setup

### 1. Check All Services Are Running
```bash
# Check if all ports are active
curl http://localhost:8000/health  # Backend
curl http://localhost:8001/api/cheapest/health  # Cheapest API
curl http://localhost:8003/api/fastest/health   # Fastest API
curl http://localhost:8002/api/optimized/health # Optimized API
curl http://localhost:8005/api/unified-booking/health # Unified Booking API
```

### 2. Test User Registration
```bash
# Register a test user
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpassword123",
    "first_name": "Test",
    "last_name": "User"
  }'
```

### 3. Test Authentication
```bash
# Login to get JWT token
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpassword123"
  }'
```

## API Documentation

### Backend API (Port 8000)
- **Authentication**: `/api/auth/register`, `/api/auth/login`, `/api/auth/profile`
- **Bookings**: `/api/bookings`, `/api/bookings/{booking_id}`
- **Documentation**: http://localhost:8000/docs

### Search APIs
- **Cheapest API**: http://localhost:8001/docs
- **Fastest API**: http://localhost:8003/docs
- **Optimized API**: http://localhost:8002/docs
- **Unified Booking API**: http://localhost:8005/docs

##  How to Use the Application

### 1. User Registration & Login
1. Open http://localhost:3000
2. Click "Sign Up" to create a new account
3. Fill in your details and create account
4. Login with your credentials

### 2. Flight Search
1. Navigate to the "Flights" page
2. Enter source and destination airports (e.g., JFK, LAX)
3. Select departure date
4. Choose search priority:
   - **Cheapest**: Lowest price flights
   - **Fastest**: Shortest duration flights
   - **Optimized**: Balanced cost and time

### 3. Flight Booking
1. Select a flight from search results
2. Click "Book Flight"
3. Enter passenger details
4. Provide payment information
5. Confirm booking

### 4. Trip Management
1. View your bookings in "My Trips"
2. Manage existing bookings
3. View booking history

##  Project Structure

```
metta/
├── backend/                    # Authentication & Booking Backend
│   ├── api.py                 # Main FastAPI application
│   ├── auth_database.db       # SQLite database
│   ├── models/                # Database models
│   ├── schemas/               # Pydantic schemas
│   ├── services/              # Business logic
│   └── requirements.txt       # Python dependencies
├── chatbot-api/               # Search & Booking APIs
│   ├── cheapest-api/          # Cheapest flight search (Port 8001)
│   ├── fastest-api/           # Fastest flight search (Port 8003)
│   ├── optimized-api/         # Optimized flight search (Port 8002)
│   └── unified-booking-api/   # Unified booking system (Port 8005)
├── me-tt-a-flights/           # Next.js Frontend
│   ├── app/                   # App router pages
│   ├── components/            # React components
│   ├── hooks/                 # Custom hooks
│   ├── lib/                   # Utilities and API service
│   └── package.json           # Node.js dependencies
├── details/                   # Documentation & Data
│   ├── airports.csv           # Airport codes and names
│   ├── metta_sample_flights.csv # Sample flight data
│   ├── chatbot_apis_documentation.md # API documentation
│   └── api_descriptions.md    # API descriptions
├── project/                   # Original MeTTa data
│   └── Data/                  # Flight data files
├── venv/                      # Python virtual environment
├── start_all_services.sh      # Startup script
└── README.md                  # This file
```

##  Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Find process using the port
lsof -i :8000  # Replace with your port number

# Kill the process
kill -9 <PID>
```

#### 2. Virtual Environment Issues
```bash
# Deactivate current environment
deactivate

# Remove and recreate virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate
```

#### 3. Database Issues
```bash
# Remove and recreate database
cd backend
rm auth_database.db
python -c "
from database.database import engine
from models import user, booking
user.Base.metadata.create_all(bind=engine)
booking.Base.metadata.create_all(bind=engine)
"
```

#### 4. Node.js Dependencies Issues
```bash
# Clear npm cache and reinstall
cd me-tt-a-flights
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

#### 5. API Connection Issues
```bash
# Check if all APIs are running
curl http://localhost:8000/health
curl http://localhost:8001/api/cheapest/health
curl http://localhost:8003/api/fastest/health
curl http://localhost:8002/api/optimized/health
curl http://localhost:8005/api/unified-booking/health
```

### Performance Issues
- **Slow API responses**: Check if virtual environment is activated
- **Frontend not loading**: Ensure all APIs are running
- **Database errors**: Verify database file permissions

##  Development

### Adding New Features
1. Create a feature branch: `git checkout -b feature/new-feature`
2. Make your changes
3. Test thoroughly
4. Commit with descriptive messages
5. Push and create a pull request

### Code Style
- **Python**: Follow PEP 8 guidelines
- **JavaScript/TypeScript**: Use ESLint and Prettier
- **API Design**: Follow RESTful principles

### Testing
```bash
# Backend tests
cd backend
python -m pytest

# Frontend tests
cd me-tt-a-flights
npm test
```

## Data Sources

### Flight Data
- **Format**: MeTTa knowledge base format
- **Location**: `project/Data/flights.metta`
- **Records**: 50,000+ flight records
- **Structure**: `(flight year month day source dest cost takeoff landing)`

### Airport Data
- **Source**: Extracted from flight dataset
- **Location**: `details/airports.csv`
- **Format**: CSV with airport codes, names, cities, states, countries

##  Deployment

### Production Setup
1. **Environment Variables**: Set production environment variables
2. **Database**: Use PostgreSQL instead of SQLite
3. **Caching**: Implement Redis for performance
4. **Load Balancing**: Use nginx or similar
5. **Monitoring**: Set up logging and monitoring

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d
```

##  Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Ensure all tests pass
6. Submit a pull request

##  License

This project is licensed under the MIT License.

##  Acknowledgments

- **MeTTa**: For the powerful knowledge representation system
- **Next.js**: For the excellent React framework
- **FastAPI**: For the high-performance Python web framework
- **shadcn/ui**: For the beautiful UI components
- **JWT**: For secure authentication
- **SQLAlchemy**: For database operations

##  Support

For support and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review the API documentation in `details/` folder
- Contact No: +91 9816898181
- Email : gautamsamanyu3482@gmail.com , samanyu3393.beai24@chitkara.edu.in
