# Blank Social Network API 

A modern, feature-rich social media platform built with Django REST Framework. This API provides comprehensive functionality for user management, content creation, and social interactions with robust authentication and permission systems.

![Django](https://img.shields.io/badge/Django-5.2.4-green)
![DRF](https://img.shields.io/badge/Django%20REST%20Framework-3.16.0-blue)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🚀 Features

### User Management
- **Custom User Model** with role-based access control (Admin, Moderator, User)
- **JWT Authentication** with token refresh functionality
- **User Profiles** with bio, GitHub links, and avatar support
- **Follow/Unfollow System** with relationship tracking
- **Advanced User Validation** including password strength requirements

### Content Management
- **Post Creation** with text content and image support (max 280 characters)
- **Hashtag Validation** - all posts must contain at least one hashtag (#)
- **Privacy Controls** - Public, Followers-only, or Private post visibility
- **Like System** with toggle functionality (like/unlike)
- **Content Filtering** by author and advanced search capabilities

### Security & Permissions
- **Role-based Access Control** with granular permissions
- **Owner-based Permissions** - users can only edit their own content
- **Input Validation** at multiple levels (model, serializer, view)
- **Age Verification** - minimum 16 years old requirement
- **File Size Validation** - avatar upload limits

## 🏗️ Architecture

### Project Structure
```
social-network/
├── apps/
│   ├── users/           # User management & authentication
│   │   ├── models.py    # User, Profile, Relationship models
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── permissions.py
│   └── posts/           # Content management
│       ├── models.py    # Post, Like models
│       ├── serializers.py
│       └── views.py
├── config/              # Django configuration
├── requirements.txt
└── manage.py
```

### Key Models

#### User Model
- Extended Django's AbstractUser
- Custom fields: role, avatar
- Comprehensive validation methods
- Property methods for full name handling

#### Profile Model
- One-to-one relationship with User
- Bio, GitHub URL, birth date
- Age calculation property
- Age validation (16+ years)

#### Post Model
- Author relationship with User
- Content with hashtag requirement
- Image upload support
- Visibility controls (public/followers/private)
- Timestamp tracking

#### Relationship Model
- Follow/follower system
- Self-follow prevention
- Unique constraint on user pairs

## 🔧 API Endpoints

### Authentication
```
POST   /api/auth/login/     # JWT token generation
POST   /api/auth/refresh/   # Token refresh
```

### Users
```
GET    /api/users/          # List users (Admin only)
POST   /api/users/          # User registration
GET    /api/users/{id}/     # User profile details
PUT    /api/users/{id}/     # Update user (Owner only)
DELETE /api/users/{id}/     # Delete user (Admin only)
GET    /api/users/me/       # Current user profile
POST   /api/users/{id}/change-password/  # Password change
POST   /api/users/{id}/follow/           # Follow user
DELETE /api/users/{id}/unfollow/         # Unfollow user
```

### Profiles
```
GET    /api/profiles/       # Current user's profile
PUT    /api/profiles/       # Update profile
```

### Posts
```
GET    /api/posts/          # List posts (with filtering)
POST   /api/posts/          # Create post (Auth required)
GET    /api/posts/{id}/     # Post details
PUT    /api/posts/{id}/     # Update post (Owner only)
DELETE /api/posts/{id}/     # Delete post (Owner only)
POST   /api/posts/{id}/like/ # Toggle like on post
```

### Query Parameters
- `?author={user_id}` - Filter posts by author
- Standard pagination support

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### Quick Start
```bash
# Clone the repository
git clone https://www.github.com/angelchiav/blank-social-network.git
cd blank-social-network

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### Environment Variables
Create a `.env` file in the project root:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

## 🔐 Authentication & Security

### JWT Token Authentication
The API uses JWT tokens for authentication with the following flow:
1. **Login** with username/password to receive access & refresh token
2. **Refresh** tokens when they expire using the refresh endpoint

### Permission System
- **Public Access**: User registration, post listing (public posts)
- **Authenticated Users**: Create posts, follow users, like content
- **Owner Permissions**: Edit own posts and profile
- **Admin Permissions**: User management, content moderation

### Input Validation
Multi-layer validation ensures data integrity:
- **Model Level**: Database constraints and custom clean methods
- **Serializer Level**: Field validation and business logic
- **View Level**: Permission checks and additional validation

## 📝 Usage Examples

### User Registration
```python
POST /api/users/
{
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "password": "SecurePass123!",
    "password2": "SecurePass123!"
}
```

### Create a Post
```python
POST /api/posts/
Headers: Authorization: Bearer <access_token>
{
    "content": "Just built an amazing Django API! #coding #django",
    "visibility": "public"
}
```

### Follow a User
```python
POST /api/users/5/follow/
Headers: Authorization: Bearer <access_token>
```

## 🧪 Testing

### Running Tests
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test apps.users
python manage.py test apps.posts

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

### Test Coverage
- Model validation testing
- API endpoint testing
- Permission system testing
- Authentication flow testing

## 🚀 Deployment

### Production Considerations
1. **Environment Variables**: Use production-ready secret keys
2. **Database**: Replace SQLite with PostgreSQL/MySQL
3. **Static Files**: Configure proper static file serving
4. **Security**: Enable HTTPS, set proper CORS headers
5. **Monitoring**: Add logging and error tracking

### Deployment Platforms
- **Heroku**: Ready for deployment with Procfile
- **Render**: Supports automatic deployments
- **Railway**: Simple deployment with GitHub integration
- **DigitalOcean**: VPS deployment with Docker

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes with proper tests
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

### Code Standards
- Follow PEP 8 style guidelines
- Write comprehensive docstrings
- Add tests for new features
- Use meaningful commit messages

## 📋 Roadmap

### Planned Features
- [ ] **Comments System** - Threaded comments on posts
- [ ] **Notifications** - Real-time notifications for interactions
- [ ] **Media Management** - Video and audio post support
- [ ] **Search & Discovery** - Advanced search with hashtags and mentions
- [ ] **Direct Messaging** - Private messaging between users
- [ ] **Content Moderation** - Automated content filtering
- [ ] **Analytics Dashboard** - User engagement metrics
- [ ] **Mobile App Integration** - React Native/Flutter app

### Technical Improvements
- [ ] **Redis Caching** - Performance optimization
- [ ] **Celery Tasks** - Background job processing
- [ ] **ElasticSearch** - Advanced search capabilities
- [ ] **Docker Support** - Containerized deployment
- [ ] **API Documentation** - Swagger/OpenAPI integration
- [ ] **Rate Limiting** - API throttling implementation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

- **Developer**: [angelchiav](https://github.com/angelchiav)

## 📞 Support

For support, please open an issue on GitHub or contact the development team.
