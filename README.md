# Hafif Temizlik Takip Sistemi

Bu proje, okul/kampüs ölçeğinde temizlik operasyonlarını dijitalleştiren hafif bir takip sistemidir. PWA (Progressive Web App) + Modüler Monolit API + PostgreSQL mimarisi ile geliştirilmiştir.

## Özellikler

- **RBAC (Role-Based Access Control)**: Admin, Staff, Supervisor rolleri
- **PWA**: Offline app shell cache, mobil uyumlu
- **Erişilebilirlik**: 18px font, 56px buton, yüksek kontrast
- **Hiyerarşik Mekan Yönetimi**: Bina > Departman > Lokasyon yapısı
- **Görev Yaşam Döngüsü**: Atama → Temizleme → Onay/Red
- **Docker Deploy**: Tek komutla çalıştırma

## Teknoloji Stack

### Backend
- **FastAPI** (Python 3.11+)
- **SQLAlchemy** + **Alembic** (ORM & Migrations)
- **PostgreSQL 15** (Database)
- **JWT** + **bcrypt** (Authentication)
- **Pydantic** (Validation)

### Frontend
- **Vue 3** + **Composition API**
- **Vite** (Build Tool)
- **Pinia** (State Management)
- **Vue Router** (Routing)
- **Tailwind CSS** (Styling)
- **Axios** (HTTP Client)

### Infrastructure
- **Docker** + **Docker Compose**
- **Nginx** (Reverse Proxy)
- **PostgreSQL** (Database)

## Kurulum ve Çalıştırma

### Gereksinimler
- Docker & Docker Compose
- Git

### 1. Projeyi Klonlayın
```bash
git clone <repository-url>
cd temizlik-takip-sistemi
```

### 2. Environment Variables
```bash
cp .env.example .env
# .env dosyasını ihtiyacınıza göre düzenleyin
```

### 3. Uygulamayı Başlatın
```bash
docker-compose up -d
```

### 4. Database Migration
```bash
docker-compose exec api alembic upgrade head
```

### 5. Uygulamaya Erişim
- **Frontend**: http://localhost:8080
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Kullanım

### İlk Kurulum
1. Admin hesabı oluşturun (veritabanında manuel)
2. Binalar, bölümler ve mekanları ekleyin
3. Periyot oluşturun ve aktifleştirin
4. Kullanıcıları oluşturun (staff, supervisor)
5. Görev atamaları yapın

### Roller ve Yetkiler

#### Admin
- Tüm CRUD işlemleri
- Dashboard istatistikleri
- Görev atamaları
- Periyot yönetimi

#### Staff (Hizmetli)
- Kendi görevlerini görme
- "Temizledim" işaretleme
- Not ekleme

#### Supervisor (Denetçi)
- Onay bekleyen görevleri görme
- Görev onaylama/reddetme
- Puan verme (1-5)
- Not ekleme

## API Endpoints

### Authentication
- `POST /api/v1/auth/login` - Giriş
- `GET /api/v1/auth/me` - Kullanıcı bilgileri

### Admin Endpoints
- `GET|POST /api/v1/users` - Kullanıcı yönetimi
- `GET|POST /api/v1/buildings` - Bina yönetimi
- `GET|POST /api/v1/departments` - Bölüm yönetimi
- `GET|POST /api/v1/locations` - Mekan yönetimi
- `GET|POST /api/v1/periods` - Periyot yönetimi
- `GET|POST /api/v1/assignments` - Atama yönetimi
- `GET /api/v1/dashboard/active-period-stats` - Dashboard

### Staff Endpoints
- `GET /api/v1/my/assignments` - Kendi görevleri
- `POST /api/v1/my/assignments/{id}/clean` - Temizledim

### Supervisor Endpoints
- `GET /api/v1/my/reviews` - Onay bekleyenler
- `POST /api/v1/my/reviews/{id}/approve` - Onayla
- `POST /api/v1/my/reviews/{id}/reject` - Reddet

## Veri Modeli

### User
- id, email, hashed_password, full_name
- role (admin|staff|supervisor)
- is_active, created_at, updated_at

### Building
- id, name, code, is_active
- created_at, updated_at

### Department
- id, name, code, is_active
- created_at, updated_at

### Location
- id, name, location_type, location_subtype
- building_id, department_id, parent_location_id
- is_leaf, floor_label, area_sqm, special_instructions
- is_active, created_at, updated_at

### Period
- id, name, start_date, end_date
- status (planned|active|completed)
- created_at, updated_at

### Assignment
- id, location_id, period_id
- staff_user_id, supervisor_user_id
- status (pending|cleaned|approved|rejected)
- staff_notes, supervisor_notes, rejection_reason
- rating (1-5), staff_completed_at, supervisor_reviewed_at
- created_at, updated_at

## Geliştirme

### Backend Geliştirme
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Geliştirme
```bash
cd frontend
npm install
npm run dev
```

### Database Migration
```bash
# Yeni migration oluştur
alembic revision --autogenerate -m "description"

# Migration uygula
alembic upgrade head
```

## PWA Özellikleri

- **App Shell Caching**: Statik dosyalar cache'lenir
- **Offline Support**: Temel UI offline çalışır
- **Install Prompt**: Ana ekrana ekleme
- **Responsive Design**: Mobil uyumlu

## Güvenlik

- **JWT Authentication**: Bearer token
- **Password Hashing**: bcrypt
- **CORS Protection**: Kontrollü origin
- **SQL Injection Protection**: SQLAlchemy ORM
- **Input Validation**: Pydantic schemas

## Performans

- **Database Indexing**: Kritik alanlar index'li
- **Pagination**: Tüm liste endpoint'leri
- **Connection Pooling**: SQLAlchemy
- **Static Asset Optimization**: Vite build

## Troubleshooting

### Database Bağlantı Sorunu
```bash
docker-compose logs db
docker-compose restart db
```

### API Bağlantı Sorunu
```bash
docker-compose logs api
docker-compose restart api
```

### Frontend Build Sorunu
```bash
docker-compose logs web
docker-compose restart web
```

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## İletişim

Sorularınız için issue açabilir veya iletişime geçebilirsiniz.
