# meTTaFlights Authentication API

This is the authentication backend API for the meTTaFlights application, providing user authentication and profile management functionality.

## Features

- **Authentication System**
  - User registration and login
  - JWT token-based authentication
  - Password hashing with bcrypt
  - Session management
  - Profile management

- **User Features**
  - Search history tracking
  - Favorite routes management
  - Profile updates

## Prerequisites

- Python 3.8+
- pip (Python package manager)

## Installation

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in the backend directory with the following content:
   ```
   SECRET_KEY=your-super-secret-key-change-this-in-production
   DATABASE_URL=sqlite:///./auth_database.db
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   REFRESH_TOKEN_EXPIRE_DAYS=7
   ```

## Running the Server

### Option 1: Using the start script
```bash
python start_server.py
```

### Option 2: Using uvicorn directly
```bash
uvicorn api:app --host 0.0.0.0 --port 8001 --reload
```

### Option 3: Using the main API file
```bash
python api.py
```

The server will start on `http://localhost:8001`

## API Documentation

Once the server is running, you can access:

- **Interactive API Documentation (Swagger UI):** http://localhost:8001/docs
- **Alternative API Documentation (ReDoc):** http://localhost:8001/redoc
- **Health Check:** http://localhost:8001/health

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user
- `POST /api/auth/refresh` - Refresh access token
- `GET /api/auth/me` - Get current user info
- `PUT /api/auth/profile` - Update user profile

### User Features
- `GET /api/user/search-history` - Get user's search history
- `POST /api/user/search-history` - Add search history entry
- `POST /api/user/favorite-routes` - Add favorite route
- `GET /api/user/favorite-routes` - Get user's favorite routes
- `DELETE /api/user/favorite-routes/{id}` - Delete favorite route

## Database

The application uses SQLite as the database. The database file (`auth_database.db`) will be created automatically when you first run the application.

### Database Schema

- **users** - User accounts and profiles
- **user_sessions** - User session management
- **search_history** - User search history
- **favorite_routes** - User's favorite routes

## Development

### Project Structure
```
backend/
├── api.py                 # Main FastAPI application
├── requirements.txt       # Python dependencies
├── start_server.py       # Server start script
├── .env                  # Environment variables
├── database/
│   └── database.py       # Database configuration
├── models/
│   └── user.py          # Database models
├── schemas/
│   └── auth_schemas.py  # Pydantic schemas
└── services/
    ├── auth_service.py  # Authentication logic
    └── dependencies.py  # FastAPI dependencies
```

### Adding New Endpoints

1. Define the endpoint in `api.py`
2. Add corresponding schemas in `schemas/` if needed
3. Add business logic in `services/` if needed
4. Update this README with the new endpoint

## Security

- Passwords are hashed using bcrypt
- JWT tokens are used for authentication
- CORS is configured for frontend integration
- Input validation using Pydantic schemas

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure you're running from the backend directory
2. **Database errors**: Delete `auth_database.db` and restart the server
3. **Port already in use**: Change the port in the start command or kill the process using port 8001

### Logs

The server logs will show:
- API requests and responses
- Database operations
- Authentication events
- Error messages

## Production Deployment

For production deployment:

1. Change the `SECRET_KEY` to a strong, unique value
2. Use a production database (PostgreSQL, MySQL)
3. Set up proper CORS origins
4. Use HTTPS
5. Set up proper logging
6. Use a production WSGI server like Gunicorn

## License

This project is part of the meTTaFlights application.