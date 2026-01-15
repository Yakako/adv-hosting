# 🗄️ Database Explanation & How to Check

## Your Database Setup

### ✅ What You Have:

**PostgreSQL Database in Docker**
```
Container Name: car-classification-db
Image: postgres:13
Status: ✅ Running (Up 4 hours)
Port Mapping: 5433 (your computer) → 5432 (container)
```

**Database Credentials:**
```
Database: car_classification
User: car_user
Password: car_password
Host: localhost
Port: 5433
```

**Connection String:**
```
postgresql://car_user:car_password@localhost:5433/car_classification
```

---

## 📊 Your Current Data

**Table: `predictions`**

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Auto-incrementing ID |
| image_path | VARCHAR | Path to uploaded image |
| predicted_class | VARCHAR | Car class (Toyota, BMW, etc.) |
| confidence | FLOAT | Prediction confidence (0-1) |
| created_at | TIMESTAMP | When prediction was made |

**Current Stats:**
- Total Predictions: **7**
- Average Confidence: **92.85%**
- Classes: Toyota (2), Nissan (1), Hyundai (1), Chevrolet (1), Ford (1), Mercedes-Benz (1)

---

## 🔍 Ways to Check Your Database

### 1. Using Python Script (Easiest)
```bash
cd "/Users/rong/Desktop/I5/Advanced Programming for DS/Project /backend"
python check_database.py
```

### 2. Using Docker CLI
```bash
# Connect to PostgreSQL inside container
docker exec -it car-classification-db psql -U car_user -d car_classification

# Once inside, run SQL commands:
\dt                          # List tables
SELECT * FROM predictions;   # View all predictions
SELECT COUNT(*) FROM predictions;  # Count total
\q                           # Quit
```

### 3. View Container Logs
```bash
docker logs car-classification-db
```

### 4. Check Container Status
```bash
docker ps | grep car-classification
```

### 5. Using a Database Tool (Optional)
Install a GUI tool like:
- **pgAdmin** (https://www.pgadmin.org/)
- **DBeaver** (https://dbeaver.io/)
- **Postico** (Mac only)

Connection details:
- Host: localhost
- Port: 5433
- Database: car_classification
- User: car_user
- Password: car_password

---

## 🐳 Docker Database Commands

### Start Database
```bash
cd "/Users/rong/Desktop/I5/Advanced Programming for DS/Project /backend"
docker-compose up -d
```

### Stop Database
```bash
docker-compose down
```

### Restart Database
```bash
docker-compose restart
```

### View Database Logs
```bash
docker logs -f car-classification-db  # -f for follow (live logs)
```

### Check Database Status
```bash
docker-compose ps
```

### Access Database Shell
```bash
docker exec -it car-classification-db bash
```

---

## 💡 How It Works

```
Your FastAPI App (port 8001)
        ↓
   SQLAlchemy ORM
        ↓
PostgreSQL in Docker (port 5433)
        ↓
   Stores predictions data
```

**Data Flow:**
1. User uploads image via API
2. API saves image to `uploads/` folder
3. Mock model makes prediction
4. **Prediction saved to PostgreSQL database**
5. API returns result to user

**Why Docker?**
- Easy to install and run PostgreSQL
- Isolated environment
- No need to install PostgreSQL on your Mac
- Easy to delete/recreate if needed

---

## 🔧 Database Maintenance

### Clear All Predictions
```python
# Run in Python
from database.connection import SessionLocal
from database.models import Prediction

db = SessionLocal()
db.query(Prediction).delete()
db.commit()
print("All predictions deleted!")
```

### Backup Database
```bash
docker exec car-classification-db pg_dump -U car_user car_classification > backup.sql
```

### Restore Database
```bash
cat backup.sql | docker exec -i car-classification-db psql -U car_user -d car_classification
```

---

## ✅ Your Database is Working Perfectly!

**Summary:**
- ✅ PostgreSQL container running in Docker
- ✅ Database connected successfully
- ✅ Table `predictions` created
- ✅ 7 predictions stored
- ✅ API can read/write data

Run `python check_database.py` anytime to inspect your data!
