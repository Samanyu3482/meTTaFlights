# MeTTa Flight Search System

A modern flight booking application that combines a beautiful Next.js frontend with a powerful MeTTa knowledge base backend for intelligent flight search.

## 🚀 Features

- **Real MeTTa Integration**: Search flights using the MeTTa knowledge base with 50,000+ flight records
- **Modern UI**: Beautiful, responsive frontend built with Next.js, Tailwind CSS, and shadcn/ui
- **Smart Search**: Advanced filtering by source, destination, date, and price
- **Real-time Results**: Instant search results from the MeTTa knowledge base
- **RESTful API**: FastAPI backend with comprehensive flight search endpoints

## 🏗️ Architecture

```
Frontend (Next.js) ←→ FastAPI Backend ←→ MeTTa Knowledge Base
     Port 3000           Port 8000         flights.metta (50K+ records)
```

## 📋 Prerequisites

- Python 3.8+
- Node.js 18+
- npm or yarn

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd metta
   ```

2. **Install Python dependencies**
   ```bash
   cd project
   pip install -r requirements.txt
   cd ..
   ```

3. **Install Node.js dependencies**
   ```bash
   cd me-tt-a-flights
   npm install
   cd ..
   ```

## 🚀 Quick Start

### Option 1: Use the startup script (Recommended)
```bash
./start.sh
```

This will start both the backend and frontend automatically.

### Option 2: Manual startup

1. **Start the MeTTa backend**
   ```bash
   cd project
   python api.py
   ```
   The backend will be available at http://localhost:8000

2. **Start the Next.js frontend** (in a new terminal)
   ```bash
   cd me-tt-a-flights
   npm run dev
   ```
   The frontend will be available at http://localhost:3000

## 📡 API Endpoints

The FastAPI backend provides the following endpoints:

- `GET /` - API status
- `GET /health` - Health check
- `POST /api/flights/search` - Search flights with parameters
- `GET /api/flights/all` - Get all flights
- `GET /api/flights/source/{source}` - Search by source airport
- `GET /api/flights/destination/{destination}` - Search by destination airport
- `GET /api/flights/route/{source}/{destination}` - Search by route

### API Documentation
Visit http://localhost:8000/docs for interactive API documentation.

## 🔍 How to Use

1. **Open the application** at http://localhost:3000
2. **Search for flights** using the search form:
   - Enter source and destination airports (e.g., JFK, LAX, SFO)
   - Select departure date
   - Choose number of passengers and travel class
3. **View results** from the MeTTa knowledge base
4. **Filter and sort** results using the sidebar filters
5. **Select a flight** to proceed to booking

## 📊 Sample Data

The system includes a comprehensive flight dataset with:
- **50,000+ flight records** in MeTTa format
- **Data structure**: `(flight year month day source destination cost)`
- **Sample airports**: JFK, LAX, SFO, ORD, ATL, MIA, and many more
- **Date range**: 2013 flights with various routes and prices

## 🧠 MeTTa Knowledge Base

The flight data is stored in `project/Data/flights.metta` and contains:
- Flight records in MeTTa syntax
- Airport codes and routes
- Pricing information
- Date-based search capabilities

### Sample MeTTa Query
```metta
!(match &space (flight 2013 1 1 JFK LAX $cost) (flight 2013 1 1 JFK LAX $cost))
```

## 🎨 Frontend Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Dark/Light Mode**: Toggle between themes
- **Real-time Search**: Instant results from MeTTa backend
- **Advanced Filtering**: Filter by price, source, destination
- **Sorting Options**: Sort by price, date, source, destination
- **Loading States**: Beautiful loading animations
- **Error Handling**: User-friendly error messages

## 🔧 Development

### Backend Development
```bash
cd project
# Install dependencies
pip install -r requirements.txt

# Run the API
python api.py

# Run tests (if available)
python -m pytest
```

### Frontend Development
```bash
cd me-tt-a-flights
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Run tests
npm test
```

## 📁 Project Structure

```
metta/
├── project/                 # MeTTa Backend
│   ├── api.py              # FastAPI application
│   ├── main.py             # MeTTa integration
│   ├── search_logic.metta  # MeTTa search functions
│   ├── Data/
│   │   └── flights.metta   # Flight knowledge base
│   └── requirements.txt    # Python dependencies
├── me-tt-a-flights/        # Next.js Frontend
│   ├── app/                # App router pages
│   ├── components/         # React components
│   ├── hooks/              # Custom hooks
│   ├── lib/                # Utilities and API service
│   └── package.json        # Node.js dependencies
├── start.sh               # Startup script
└── README.md              # This file
```

## 🐛 Troubleshooting

### Backend Issues
- **Port 8000 already in use**: Kill the process or change the port in `api.py`
- **MeTTa loading errors**: Check that `flights.metta` exists in `project/Data/`
- **Import errors**: Ensure all Python dependencies are installed

### Frontend Issues
- **Port 3000 already in use**: Kill the process or change the port
- **API connection errors**: Ensure the backend is running on port 8000
- **Build errors**: Clear `.next` folder and reinstall dependencies

### General Issues
- **CORS errors**: Check that the backend CORS settings include `http://localhost:3000`
- **Data not loading**: Verify the MeTTa knowledge base is properly loaded

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- **MeTTa**: For the powerful knowledge representation system
- **Next.js**: For the excellent React framework
- **FastAPI**: For the high-performance Python web framework
- **shadcn/ui**: For the beautiful UI components 