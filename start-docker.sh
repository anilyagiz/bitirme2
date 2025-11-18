#!/bin/bash

# Temizlik Takip Sistemi - Docker Compose ile Başlatma

echo "🐳 Docker Compose ile başlatılıyor..."

# Docker kontrol
if ! command -v docker &> /dev/null; then
    echo "❌ Docker kurulu değil!"
    echo ""
    echo "Docker kurulumu:"
    echo "  Ubuntu: curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh"
    echo "  macOS: brew install docker"
    echo "  Windows: Docker Desktop indir (docker.com)"
    echo ""
    exit 1
fi

# docker-compose veya docker compose kontrol
if command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE="docker-compose"
elif docker compose version &> /dev/null; then
    DOCKER_COMPOSE="docker compose"
else
    echo "❌ docker-compose kurulu değil!"
    exit 1
fi

# Eski container'ları temizle
echo "🧹 Eski container'lar temizleniyor..."
$DOCKER_COMPOSE down -v 2>/dev/null || true

# Container'ları başlat
echo "📦 Container'lar başlatılıyor..."
$DOCKER_COMPOSE up -d

echo ""
echo "⏳ PostgreSQL hazırlanıyor (10 saniye bekleniyor)..."
sleep 10

# Migration çalıştır
echo "📋 Database migration çalıştırılıyor..."
$DOCKER_COMPOSE exec -T api alembic upgrade head || {
    echo "⚠️  Migration başarısız oldu, tekrar deneniyor..."
    sleep 5
    $DOCKER_COMPOSE exec -T api alembic upgrade head
}

# Admin user oluştur
echo "👤 Admin user oluşturuluyor..."
$DOCKER_COMPOSE exec -T api python -c "
from app.db.base import SessionLocal, Base, engine
from app.db.models.user import User, UserRole
from app.security.auth import get_password_hash

Base.metadata.create_all(bind=engine)
db = SessionLocal()

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
    print('✅ Admin oluşturuldu')
else:
    print('✅ Admin mevcut')

db.close()
"

echo ""
echo "✅ Sistem başarıyla başlatıldı!"
echo ""
echo "📝 Giriş bilgileri:"
echo "   Email: admin@kku.com"
echo "   Şifre: admin123"
echo ""
echo "🌐 Uygulamaya erişim:"
echo "   Frontend: http://localhost:8080"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "📊 Log'ları görmek için:"
echo "   $DOCKER_COMPOSE logs -f"
echo ""
echo "🛑 Durdurmak için:"
echo "   $DOCKER_COMPOSE down"
echo ""
