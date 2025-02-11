# Game Leaderboard

This is a FastAPI-based backend with PostgreSQL and React for managing a game leaderboard. It allows players to join games, track scores, and view leaderboards.

---

## 🚀 **Setup Instructions**

### **1️⃣ Prerequisites**

Ensure you have the following installed:

-   **Docker & Docker Compose**
-   **Python 3.9+**
-   **Node.js & Yarn** (for frontend development)

### **2️⃣ Clone the Repository**

```bash
# Clone this repository
git clone https://github.com/your-repo/game-leaderboard.git
cd game-leaderboard
```

### **3️⃣ Set Up Environment Variables**

#### **Backend (`backend/.env`)**

```env
DATABASE_URL=postgresql://postgres:secret@db:5432/gamebase
SECRET_KEY=mysecretkey
DEBUG=True
```

#### **Frontend (`frontend/.env`)**

```env
REACT_APP_API_URL=http://localhost:8000
```

### **4️⃣ Start the Application**

Run the following command to build and start the services:

```bash
docker-compose up --build
```

### **5️⃣ Apply Database Migrations**

```bash
# Inside the backend container
docker-compose exec backend alembic upgrade head
```

---

## 🌍 **Ports**

| Service           | Port   |
| ----------------- | ------ |
| Backend (FastAPI) | `8000` |
| Frontend (React)  | `3000` |
| PostgreSQL        | `5433` |

---

## 📌 **API Endpoints**

### **🔹 Game APIs**

| Method | Endpoint                   | Description                                   |
| ------ | -------------------------- | --------------------------------------------- |
| `GET`  | `/games/{game_id}/details` | Get game details (players, upvotes, sessions) |
| `POST` | `/games/{game_id}/join`    | Join a game                                   |

### **🔹 Leaderboard APIs**

| Method | Endpoint           | Description                           |
| ------ | ------------------ | ------------------------------------- |
| `GET`  | `/games/{game_id}` | Get leaderboard (only active players) |

### **🔹 Contestant APIs**

| Method   | Endpoint                       | Description                        |
| -------- | ------------------------------ | ---------------------------------- |
| `DELETE` | `/contestants/{contestant_id}` | Remove a player (deletes sessions) |

---

## 🔧 **Development & Debugging**

### **Running Backend Locally (Without Docker)**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Mac/Linux
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### **Running Frontend Locally**

```bash
cd frontend
yarn install
yarn start
```

### **Check API Docs**

Open **Swagger UI**:

```
http://localhost:8000/docs
```

---

## 🛠️ **Troubleshooting**

-   **Database Issues?** Restart PostgreSQL:
    ```bash
    docker-compose restart db
    ```
-   **Migrations Not Working?** Recreate them:
    ```bash
    alembic revision --autogenerate -m "Fix migrations"
    alembic upgrade head
    ```
-   **Frontend Not Updating?** Ensure React hot reload is working:
    ```bash
    docker-compose restart frontend
    ```

---

## 📜 **License**

This project is licensed under the MIT License.

---

🚀 **Now your game leaderboard is ready to run!** Let me know if you need any modifications.
