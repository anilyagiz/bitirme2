#!/bin/bash

# Temizlik Takip Sistemi - Development Başlatma Scripti

echo "🚀 Temizlik Takip Sistemi başlatılıyor..."

# PostgreSQL kontrol et
if ! command -v postgres &> /dev/null; then
    echo "⚠️  PostgreSQL bulunamadı!"
    echo ""
    echo "Çözüm 1: Docker Compose kullan (ÖNERİLEN)"
    echo "  docker-compose up -d"
    echo ""
    echo "Çözüm 2: PostgreSQL kur"
    echo "  Ubuntu/Debian: sudo apt-get install postgresql postgresql-contrib"
    echo "  macOS: brew install postgresql"
    echo ""
    exit 1
fi

# PostgreSQL başlat
echo "📦 PostgreSQL başlatılıyor..."
if command -v systemctl &> /dev/null; then
    sudo systemctl start postgresql
elif command -v service &> /dev/null; then
    sudo service postgresql start
else
    pg_ctl -D /usr/local/var/postgres start
fi

sleep 2

# Database oluştur (varsa hata vermez)
echo "🗄️  Database oluşturuluyor..."
psql -U postgres -c "CREATE DATABASE appdb;" 2>/dev/null || true
psql -U postgres -c "CREATE USER app WITH PASSWORD 'app';" 2>/dev/null || true
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE appdb TO app;" 2>/dev/null || true

# Backend migration
echo "📋 Database migration çalıştırılıyor..."
cd backend
alembic upgrade head

# Admin user oluştur
echo "👤 Admin user oluşturuluyor..."
python -c "
from app.db.base import SessionLocal, Base, engine
from app.db.models.user import User, UserRole
from app.security.auth import get_password_hash
import uuid

# Tables oluştur
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Admin var mı kontrol et
admin = db.query(User).filter(User.email == 'admin@kku.com').first()

if not admin:
    admin = User(
        email='admin@kku.com',
        hashed_password=get_password_hash('admin123'),
        full_name='Sistem Admin',
        role=UserRole.ADMIN,
        is_active=True
    )
    db.add(admin)
    db.commit()
    print('✅ Admin user oluşturuldu: admin@kku.com / admin123')
else:
    print('✅ Admin user zaten mevcut: admin@kku.com / admin123')

db.close()
" || echo "⚠️  Admin user oluşturulamadı (normal olabilir)"

# Backend başlat
echo "🌐 Backend başlatılıyor (http://localhost:8000)..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

cd ../frontend

# Frontend başlat
echo "💻 Frontend başlatılıyor (http://localhost:5173)..."
npm run dev &
FRONTEND_PID=$!

echo ""
echo "✅ Sistem başarıyla başlatıldı!"
echo ""
echo "📝 Giriş bilgileri:"
echo "   Email: admin@kku.com"
echo "   Şifre: admin123"
echo ""
echo "🌐 Uygulamaya erişim:"
echo "   Frontend: http://localhost:5173"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "🛑 Durdurmak için: Ctrl+C"
echo ""

# Trap Ctrl+C to cleanup
trap "echo '🛑 Sistem durduruluyor...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT

# Wait for processes
wait
