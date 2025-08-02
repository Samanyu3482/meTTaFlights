# API Descriptions

## Overview

This document provides detailed descriptions of all 4 APIs in the chatbot-api folder, explaining their purpose, functionality, technical implementation, and business logic.

---

## 1. Cheapest API (Port 8001)

### Purpose
The Cheapest API is designed to find flights with the lowest possible cost from the available flight dataset. It prioritizes price over other factors like travel time or convenience.

### Core Functionality
- **Price Optimization**: Analyzes all available flights and returns the one with the minimum cost
- **Cost Calculation**: Considers base fare, taxes, and any additional fees
- **Multi-Stop Support**: Can find cheapest options including connecting flights
- **Real-time Pricing**: Provides current pricing information

### Technical Implementation
- **Algorithm**: Uses sorting algorithms to find minimum cost flights
- **Data Source**: Processes MeTTa format flight data from `project copy/Data_new/flights.metta`
- **Caching**: Implements response caching for frequently searched routes
- **Validation**: Validates input parameters and airport codes

### Business Logic
1. **Input Validation**: Checks source/destination airports, dates, and passenger count
2. **Flight Filtering**: Filters flights by date and route
3. **Cost Sorting**: Sorts flights by total cost (base fare + taxes)
4. **Connection Analysis**: Evaluates multi-stop options for better pricing
5. **Result Enhancement**: Adds airline details, duration calculations, and metadata

### Use Cases
- Budget-conscious travelers
- Price comparison analysis
- Cost optimization for business travel
- Backpacker and economy travel planning

### Performance Characteristics
- **Response Time**: Typically 50-200ms for direct flights
- **Scalability**: Handles multiple concurrent requests
- **Memory Usage**: Efficient data structures for large datasets
- **Accuracy**: 100% accurate cost calculations from source data

---

## 2. Fastest API (Port 8003)

### Purpose
The Fastest API focuses on finding flights with the shortest travel duration, prioritizing time efficiency over cost considerations.

### Core Functionality
- **Duration Optimization**: Analyzes flight durations and returns the fastest option
- **Time Calculation**: Considers actual flight time, layovers, and connections
- **Route Analysis**: Evaluates different routing options for speed
- **Real-time Availability**: Checks current flight schedules

### Technical Implementation
- **Algorithm**: Uses graph algorithms to find shortest path in time
- **Data Processing**: Converts MeTTa data to time-based calculations
- **Time Zone Handling**: Manages different time zones for accurate duration
- **Connection Optimization**: Finds optimal layover times

### Business Logic
1. **Duration Calculation**: Computes total travel time including layovers
2. **Route Optimization**: Finds fastest routing through available connections
3. **Time Zone Conversion**: Handles departure/arrival time zones
4. **Connection Analysis**: Evaluates layover efficiency
5. **Speed Prioritization**: Ranks flights by total duration

### Use Cases
- Business travelers with tight schedules
- Emergency travel arrangements
- Time-sensitive business meetings
- Quick weekend getaways
- Connecting flight optimization

### Performance Characteristics
- **Response Time**: 30-150ms for direct flights
- **Complexity**: O(n log n) for route optimization
- **Memory Efficiency**: Optimized for time-based queries
- **Accuracy**: Precise duration calculations with time zone handling

---

## 3. Optimized API (Port 8002)

### Purpose
The Optimized API provides a balanced approach, considering both cost and time factors to find the most efficient flight option overall.

### Core Functionality
- **Multi-Criteria Optimization**: Balances cost, time, and convenience
- **Scoring Algorithm**: Uses weighted scoring for different factors
- **Smart Recommendations**: Provides the best overall value
- **User Preference Learning**: Adapts to user behavior patterns

### Technical Implementation
- **Scoring System**: Implements weighted scoring algorithm
- **Factor Analysis**: Considers cost, time, convenience, and reliability
- **Machine Learning**: Basic pattern recognition for optimization
- **Dynamic Weighting**: Adjusts factors based on route characteristics

### Business Logic
1. **Factor Weighting**: Assigns weights to cost (40%), time (35%), convenience (25%)
2. **Normalization**: Normalizes different metrics to comparable scales
3. **Scoring Calculation**: Computes overall efficiency score
4. **Ranking**: Ranks flights by composite score
5. **Recommendation**: Returns the highest-scoring option

### Use Cases
- General travel planning
- Family vacations
- Business travel with moderate constraints
- First-time travelers
- Balanced travel optimization

### Performance Characteristics
- **Response Time**: 100-300ms due to complex calculations
- **Algorithm Complexity**: O(n log n) for scoring and ranking
- **Memory Usage**: Higher due to multi-factor analysis
- **Accuracy**: Balanced optimization with user preference consideration

---

## 4. Unified Booking API (Port 8005)

### Purpose
The Unified Booking API serves as an integration layer between the three search APIs and the existing backend booking system, providing a seamless booking experience.

### Core Functionality
- **API Integration**: Connects search APIs with booking system
- **Data Transformation**: Converts between different data formats
- **User Management**: Handles user authentication and session management
- **Booking Orchestration**: Manages the complete booking workflow

### Technical Implementation
- **Microservices Architecture**: Acts as an API gateway
- **Data Mapping**: Converts search API output to booking system input
- **Authentication Proxy**: Forwards JWT tokens to backend services
- **Error Handling**: Comprehensive error management and rollback
- **Transaction Management**: Ensures booking consistency

### Business Logic
1. **Flight Selection**: Receives selected flight from search APIs
2. **Data Validation**: Validates flight details and user information
3. **Format Conversion**: Transforms data between API formats
4. **Booking Creation**: Creates booking in backend system
5. **Confirmation**: Returns booking confirmation with reference

### Integration Points
- **Input**: Receives flight details from any of the three search APIs
- **Output**: Creates bookings in the main backend system
- **Authentication**: Uses JWT tokens for user identification
- **Database**: Integrates with existing booking database

### Use Cases
- Complete flight booking workflow
- Integration with existing booking systems
- Multi-API search result booking
- User trip management
- Booking history and management

### Performance Characteristics
- **Response Time**: 200-500ms including backend integration
- **Reliability**: High availability with error recovery
- **Scalability**: Handles multiple concurrent bookings
- **Data Consistency**: Ensures booking data integrity

---

## System Architecture

### Microservices Design
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
                    └───────────────────────────┘
```

### Data Flow
1. **User Request**: Frontend sends search request to any search API
2. **Flight Search**: Search API processes request and returns results
3. **Flight Selection**: User selects a flight from search results
4. **Booking Request**: Frontend sends booking request to Unified API
5. **Data Transformation**: Unified API converts data formats
6. **Backend Integration**: Unified API creates booking in backend
7. **Confirmation**: Booking confirmation returned to user

### Technology Stack
- **Framework**: FastAPI (Python)
- **Authentication**: JWT (JSON Web Tokens)
- **Data Format**: JSON for API communication
- **Database**: SQLite (backend booking system)
- **HTTP Client**: httpx for inter-service communication
- **Validation**: Pydantic for data validation

### Security Features
- **JWT Authentication**: Secure token-based authentication
- **CORS Support**: Cross-origin resource sharing
- **Input Validation**: Comprehensive parameter validation
- **Error Handling**: Secure error responses
- **User Isolation**: Proper data separation between users

### Scalability Considerations
- **Horizontal Scaling**: Each API can be scaled independently
- **Load Balancing**: Can distribute load across multiple instances
- **Caching**: Response caching for improved performance
- **Database Optimization**: Efficient queries and indexing
- **Microservices**: Independent deployment and scaling

### Monitoring and Observability
- **Health Checks**: All APIs provide health endpoints
- **Logging**: Comprehensive request/response logging
- **Metrics**: Performance and usage metrics
- **Error Tracking**: Detailed error reporting
- **API Documentation**: Auto-generated API documentation

---

## Development and Deployment

### Development Environment
- **Python 3.12**: Runtime environment
- **Virtual Environment**: Isolated dependency management
- **Hot Reload**: Development server with auto-reload
- **Debug Mode**: Detailed error messages and logging

### Deployment Strategy
- **Containerization**: Docker support for easy deployment
- **Environment Variables**: Configuration management
- **Port Management**: Dedicated ports for each service
- **Service Discovery**: API endpoint discovery

### Testing Strategy
- **Unit Tests**: Individual component testing
- **Integration Tests**: API interaction testing
- **End-to-End Tests**: Complete workflow testing
- **Performance Tests**: Load and stress testing

### Maintenance and Updates
- **Version Control**: Git-based version management
- **API Versioning**: Backward compatibility support
- **Rollback Strategy**: Quick rollback capabilities
- **Documentation**: Comprehensive API documentation

---

## Future Enhancements

### Planned Features
- **Real-time Pricing**: Live price updates from airlines
- **Advanced Search**: More sophisticated search algorithms
- **User Preferences**: Personalized search results
- **Mobile Optimization**: Enhanced mobile experience
- **Analytics Dashboard**: Usage and performance analytics

### Technical Improvements
- **Database Migration**: PostgreSQL for production
- **Caching Layer**: Redis for improved performance
- **Message Queue**: Asynchronous processing
- **API Gateway**: Centralized API management
- **Monitoring**: Advanced observability tools

### Business Features
- **Loyalty Program**: User rewards and points
- **Group Bookings**: Multi-passenger optimization
- **Corporate Accounts**: Business travel management
- **Travel Insurance**: Integrated insurance options
- **Multi-language**: Internationalization support 