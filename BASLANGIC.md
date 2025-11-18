# Temizlik Takip Sistemi - Başlangıç Kılavuzu

## 🚀 Hızlı Başlangıç

Projeyi çalıştırmak için **2 seçenek** var:

### Seçenek 1: Docker Compose ile (ÖNERİLEN)

```bash
./start-docker.sh
```

**Avantajları:**
- Tek komutla her şey hazır
- PostgreSQL otomatik başlar
- Production ortamına benzer
- Kolay yönetim

**Gereksinimler:**
- Docker
- docker-compose

---

### Seçenek 2: Manuel Geliştirme Ortamı

```bash
./start-dev.sh
```

**Avantajları:**
- Yerel geliştirme için uygun
- Daha hızlı reload
- Debug kolay

**Gereksinimler:**
- PostgreSQL kurulu olmalı
- Python 3.11+
- Node.js 18+

---

## 📝 Giriş Bilgileri

Sistem başlatıldıktan sonra:

```
Email: admin@kku.com
Şifre: admin123
```

---

## 🌐 Erişim URL'leri

### Docker Compose ile:
- **Frontend:** http://localhost:8080
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

### Manuel çalıştırma ile:
- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

---

## 🛠️ Manuel Kurulum (İsteğe Bağlı)

### 1. PostgreSQL Kurulumu

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
```

**macOS:**
```bash
brew install postgresql
brew services start postgresql
```

**Windows:**
- PostgreSQL indirin: https://www.postgresql.org/download/windows/

### 2. Database Oluşturma

```bash
sudo -u postgres psql
```

```sql
CREATE DATABASE appdb;
CREATE USER app WITH PASSWORD 'app';
GRANT ALL PRIVILEGES ON DATABASE appdb TO app;
\q
```

### 3. Backend Kurulumu

```bash
cd backend
pip install -r requirements.txt
alembic upgrade head
```

### 4. Admin User Oluşturma

```bash
cd backend
python -c "
from app.db.base import SessionLocal, Base, engine
from app.db.models.user import User, UserRole
from app.security.auth import get_password_hash

Base.metadata.create_all(bind=engine)
db = SessionLocal()

admin = User(
    email='admin@kku.com',
    hashed_password=get_password_hash('admin123'),
    full_name='Sistem Admin',
    role=UserRole.ADMIN,
    is_active=True
)
db.add(admin)
db.commit()
print('Admin oluşturuldu!')
db.close()
"
```

### 5. Frontend Kurulumu

```bash
cd frontend
npm install
```

### 6. Servisleri Başlatma

**Backend (Terminal 1):**
```bash
cd backend
uvicorn app.main:app --reload
```

**Frontend (Terminal 2):**
```bash
cd frontend
npm run dev
```

---

## 🐛 Sorun Giderme

### "Database bağlanamıyor" hatası

```bash
# PostgreSQL çalışıyor mu?
sudo systemctl status postgresql

# Başlatmak için:
sudo systemctl start postgresql
```

### "Email validator hatası"

```bash
cd backend
pip install email-validator
```

### "Migration hatası"

```bash
cd backend
# Mevcut migration'ları sil
rm -rf alembic/versions/*.py
# Yeniden oluştur
alembic revision --autogenerate -m "Initial"
alembic upgrade head
```

### Frontend build hatası

```bash
cd frontend
rm -rf node_modules
npm install
npm run build
```

---

## 📚 Sistem Kullanımı

### Admin İşlemleri (Dashboard)

1. **Login** olun (admin@kku.com / admin123)
2. **Quick Start Guide** takip edin:
   - Buildings (Binalar) ekleyin
   - Departments (Bölümler) ekleyin
   - Periods (Dönemler) oluşturun
   - Locations (Konumlar) tanımlayın
   - Users (Kullanıcılar - staff/supervisor) ekleyin
   - Assignments (Görevler) atayın

### Staff İşlemleri

- Atanan görevleri görüntüleme
- Temizlik tamamlama
- Not ekleme

### Supervisor İşlemleri

- Tamamlanan görevleri inceleme
- Onaylama/Reddetme
- Puan verme

---

## 🔧 Geliştirme

### Backend API Test

```bash
# Swagger UI
http://localhost:8000/docs

# ReDoc
http://localhost:8000/redoc
```

### Database Şeması

```bash
cd backend
alembic revision --autogenerate -m "Açıklama"
alembic upgrade head
```

### Kod Kalitesi

```bash
# Backend
cd backend
black app/
flake8 app/

# Frontend
cd frontend
npm run lint
```

---

## 📦 Production Build

### Frontend

```bash
cd frontend
npm run build
# dist/ klasörü oluşur
```

### Docker

```bash
docker-compose up -d
```

---

## ❓ Yardım

Sorun yaşıyorsanız:

1. Log'ları kontrol edin:
   ```bash
   # Docker
   docker-compose logs -f

   # Manuel
   # Backend terminal'inde hata mesajları görünür
   ```

2. Database bağlantısını test edin:
   ```bash
   psql -h localhost -U app -d appdb
   ```

3. API endpoint'lerini test edin:
   ```bash
   curl http://localhost:8000/docs
   ```

---

## 📄 Lisans

Bu proje KKÜ Bitirme Projesi kapsamında geliştirilmiştir.
