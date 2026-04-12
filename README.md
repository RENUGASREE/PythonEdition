# Python Edition: Adaptive & Interactive Learning Assistant 🐍

A premium, AI-enhanced adaptive learning platform designed to take users from Python basics to professional mastery. The platform features a sophisticated recommendation engine, real-time code execution, and high-fidelity analytics.

**🌐 Live Demo:** [https://python-edition-adaptive-learning.vercel.app](https://python-edition-adaptive-learning.vercel.app)

---

## 🚀 Key Features

### 🧠 Adaptive Learning Engine
- **Diagnostic Placement**: A comprehensive 15-question quiz to assess baseline knowledge across 6 core modules.
- **Mastery-Based Progression**: Intelligent backend logic that tracks proficiency (0.0 – 1.0) and unlocks content dynamically.
- **Personalized Recommendations**: Automatic difficulty adjustment (Beginner, Intermediate, Pro) for every module based on user performance.

### 📚 Professional Curriculum
- **60 Deep-Dive Topics**: Covering everything from Variable Scope to Decorators and Context Managers.
- **180+ Lessons**: Each topic contains progressive lessons (Objective, Concept, Example, Takeaway).
- **Interactive Challenges**: 60 integrated coding challenges with an auto-grading sandbox.

### 📊 Performance Analytics
- **Topic Proficiency Radar**: Visual mastery breakdown across the curriculum.
- **Real-time Progress Tracking**: Granular tracking of lesson completion and quiz scores.
- **Mastery Vector Visualization**: Deep insights into the learner's knowledge profile.

### 🛠️ Developer Suite
- **Interactive IDE**: Integrated code editor with instant feedback and error diagnostics.
- **RAG-Powered Chatbot**: AI assistant trained on the curriculum for context-aware help.

---

## 🛠️ Tech Stack

| Layer | Technologies |
|-------|-------------|
| **Frontend** | React 18, Vite, Tailwind CSS, Framer Motion, Recharts |
| **Backend** | Django 5.0, Django REST Framework, PostgreSQL |
| **AI / ML** | OpenAI GPT-4o (via RAG) for intelligent tutoring |
| **Execution** | Isolated sandbox for secure Python code evaluation |

---

## 📦 Project Structure

```
Python_Edition/
├── backend/            # Django core, adaptive logic, and curriculum data
│   ├── ai_engine/      # RAG-powered AI tutoring engine
│   ├── analytics/      # Performance tracking and analytics
│   ├── assessments/    # Quizzes, placement tests, and challenges
│   ├── core/           # Shared models and utilities
│   ├── evaluation/     # Adaptive recommendation engine
│   ├── gamification/   # Badges, streaks, and rewards
│   ├── lessons/        # Lesson content management
│   ├── recommendation/ # Personalized learning path suggestions
│   └── users/          # User authentication and profiles
├── client/             # React frontend application
│   ├── public/         # Static assets
│   └── src/            # Components, pages, hooks, and state management
```

---

## 🏁 Prerequisites

- **Node.js** 18+
- **Python** 3.12+
- **PostgreSQL**

---

## � Deployment Guide

### Architecture
- **Frontend**: Vercel (React + Vite)
- **Backend**: Render (Django + PostgreSQL)
- **Database**: PostgreSQL (Render Managed Database)

### Quick Deploy (One-Click Setup)

#### 1. Fork & Clone Repository
```bash
git clone https://github.com/RENUGASREE/PythonEdition.git
cd PythonEdition
```

#### 2. Backend Deployment (Render)
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `python-edition-backend`
   - **Runtime**: Python 3
   - **Build Command**: `cd backend && pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - **Start Command**: `cd backend && gunicorn python_edition_django.wsgi:application`
5. Add Environment Variables (see `DEPLOYMENT_ENV_VARIABLES.md`)
6. Deploy!

#### 3. Frontend Deployment (Vercel)
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "Add New..." → "Project"
3. Connect your GitHub repository
4. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: `./`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
5. Add Environment Variable:
   - `VITE_API_BASE_URL`: `https://your-backend-url.onrender.com/api`
6. Deploy!

### Environment Variables Setup

#### Backend (Render)
Required variables - see `DEPLOYMENT_ENV_VARIABLES.md` for complete list:
```bash
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=false
ALLOWED_HOSTS=your-app.onrender.com,localhost
DATABASE_URL=postgresql://user:pass@host:port/dbname
CORS_ALLOWED_ORIGINS=https://your-app.vercel.app
OPENAI_API_KEY=your-openai-key
```

#### Frontend (Vercel)
```bash
VITE_API_BASE_URL=https://your-backend.onrender.com/api
```

### Post-Deployment Steps
1. **Create Superuser** (Render Console):
   ```bash
   cd backend && python manage.py createsuperuser
   ```
2. **Load Initial Data**:
   ```bash
   cd backend && python manage.py loaddata curriculum_data.json
   ```
3. **Test API Endpoints**:
   - Health Check: `https://your-backend.onrender.com/api/health/`
   - Admin Panel: `https://your-backend.onrender.com/admin/`

### Monitoring & Maintenance
- **Backend Logs**: Check Render dashboard for application logs
- **Frontend Logs**: Check Vercel dashboard for build/function logs
- **Database**: Use Render's pgAdmin for database management
- **API Usage**: Monitor OpenAI API usage and costs

### Troubleshooting
- **CORS Issues**: Verify `CORS_ALLOWED_ORIGINS` matches your frontend URL
- **Database Connection**: Ensure `DATABASE_URL` is correct and accessible
- **Static Files**: Run `collectstatic` command if assets are missing
- **API Errors**: Check OpenAI API key and model configuration

---

## �📄 License

This project is licensed under the MIT License.
