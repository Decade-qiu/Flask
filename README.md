# Online Live Teaching Platform

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)  [![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)  [![Flask](https://img.shields.io/badge/flask-2.0%2B-green)](https://flask.palletsprojects.com/)  [![Vue.js](https://img.shields.io/badge/vue.js-3.0%2B-green)](https://vuejs.org/)  [![PyQt5](https://img.shields.io/badge/pyqt5-5.15%2B-green)](https://www.riverbankcomputing.com/software/pyqt/)  

Online Live Teaching Platform is a comprehensive educational software designed to facilitate online teaching and learning. Built with Flask, Vue.js, and PyQt5, this platform enables live streaming, interactive features, course management, and community discussions for teachers, students, administrators, and regulators.

---

## 🚀 Features

### Core Functionality
- **Live Streaming and Interaction**  
  - Video and audio live streaming  
  - Screen sharing and whiteboard tools  
  - Real-time chat and "raise hand" feature for student-teacher interaction  

- **Course and Recording Management**  
  - Course creation and enrollment  
  - Live session recording (view, download, delete)  
  - Upload and manage course materials  

- **Student Engagement**  
  - Attendance check-in system  
  - Community discussion forum with Markdown support  
  - Personalized course recommendations  

- **Administrative Tools**  
  - User and role management  
  - Platform data maintenance  
  - Content monitoring and complaint handling  

### Non-Functional Features
- **High Availability**: Accessible anytime, anywhere  
- **Security**: Encrypted data transmission and user authentication  
- **Scalability**: Supports multiple devices and growing user bases  
- **Performance**: Low latency, high concurrency, and fast response times  
- **Usability**: Intuitive UI with clear workflows  

---

## 🛠 Technical Architecture

### Backend Components
- Flask web framework  
- REST API for client-server communication  
- WebSocket for real-time features  
- Nginx with HTTP-FLV for video streaming  

### Frontend Components
- Vue.js for the student web interface  
- PyQt5 for the teacher desktop client  
- HTML/CSS templates for rendering  

### Database and Storage
- Relational database (e.g., MySQL or SQLite) for user and course data  
- Object storage (OBS) for media files  
- File system for static assets  

### UI/UX Design
- Prototyping with Mockplus (墨刀)  
- Modular UI components for consistency  

---


## 👓 Project Structure

The project is organized into the following directories and files:

```
FLASK/
├── __pycache__/          # Compiled Python bytecode files
├── .git/                 # Git repository metadata
├── blueprints/           # Flask blueprints for modular routing
├── migration/            # Database migration scripts
├── model/                # Database models and schemas
├── OBS/                  # Object storage for media files
├── static/               # Static files (CSS, JS, images)
├── templates/            # HTML templates for rendering
├── Test/                 # Test scripts and resources
├── tools/                # Utility scripts and tools
├── ui/                   # UI design files and prototypes
├── app.py                # Main Flask application file
└── config.py             # Configuration settings
```

---

## 🔧 Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Decade-qiu/online-live-teaching-platform.git
   cd online-live-teaching-platform
   ```

2. **Install Backend Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**:
   ```bash
   # Create .env file
   cp .env.example .env

   # Edit .env with your configurations
   DATABASE_URI=your_database_uri
   SECRET_KEY=your_secret_key
   NGINX_STREAMING_URL=your_nginx_streaming_url
   ```

4. **Set Up the Frontend (Vue.js)**:
   ```bash
   cd frontend
   npm install
   npm run serve
   ```

5. **Set Up the Streaming Server**:
   - Install Nginx with the HTTP-FLV module.
   - Configure Nginx for streaming:
     ```bash
     sudo cp tools/nginx.conf /etc/nginx/nginx.conf
     sudo nginx -s reload
     ```

6. **Initialize the Database**:
   ```bash
   flask db upgrade
   ```

7. **Run the Application**:
   ```bash
   python app.py
   ```

8. **Run the Teacher Client**:
   ```bash
   python teacher_client.py
   ```

---

## 📚 API Documentation

### User Management
- `POST /auth/register` - Register a new user  
- `POST /auth/login` - Log in and get a token  
- `GET /user/profile` - Retrieve user profile  
- `PUT /user/profile` - Update user profile  

### Course and Live Session Management
- `POST /course/create` - Create a new course  
- `GET /course/list` - List all available courses  
- `POST /live/start` - Start a live session  
- `GET /live/recordings` - List session recordings  

### Community Features
- `POST /discussion/post` - Create a new discussion post  
- `GET /discussion/list` - List discussion posts  
- `POST /discussion/comment` - Comment on a post  

---

## 🔒 Security

- JWT-based authentication for secure access  
- Role-based access control for different user types  
- Encrypted data transmission for privacy  
- Content monitoring to ensure compliance  
- Regular backups for data integrity  

---

## 🤝 Contributing

1. Fork the repository.  
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).  
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).  
4. Push to the branch (`git push origin feature/AmazingFeature`).  
5. Open a Pull Request.  

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Flask team for the lightweight web framework  
- Vue.js team for the frontend framework  
- PyQt5 for the teacher client interface  
- Nginx for reliable streaming support  
- Mockplus (墨刀) for UI/UX prototyping  


## 🗺 Roadmap

### Phase 1 (Completed)
- Core platform development  
- Live streaming and interaction features  
- Course and user management  

### Phase 2 (Planned)
- Enhanced community features  
- Mobile application support  
- Advanced analytics for learning progress  

### Phase 3 (Future)
- AI-driven personalized learning paths  
- Integration with third-party educational tools  
- Global scalability improvements  

---
