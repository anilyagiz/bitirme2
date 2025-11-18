# Production Deployment Guide - Temizlik Takip Sistemi

Bu rehber, Temizlik Takip Sistemi'ni production ortamında güvenli ve performanslı bir şekilde çalıştırmak için gerekli adımları içerir.

## 📋 İçindekiler

1. [Gereksinimler](#gereksinimler)
2. [Güvenlik Yapılandırması](#güvenlik-yapılandırması)
3. [Deployment Adımları](#deployment-adımları)
4. [SSL/HTTPS Kurulumu](#sslhttps-kurulumu)
5. [Monitoring ve Logging](#monitoring-ve-logging)
6. [Backup ve Restore](#backup-ve-restore)
7. [Performans Optimizasyonu](#performans-optimizasyonu)
8. [Sorun Giderme](#sorun-giderme)

---

## Gereksinimler

### Sistem Gereksinimleri

- **CPU**: Minimum 2 core (4 core önerilir)
- **RAM**: Minimum 4GB (8GB önerilir)
- **Disk**: Minimum 20GB SSD
- **OS**: Ubuntu 20.04+ / Debian 11+ / RHEL 8+

### Yazılım Gereksinimleri

- Docker Engine 20.10+
- Docker Compose 2.0+
- Git
- (Opsiyonel) Nginx reverse proxy için ayrı sunucu

---

## Güvenlik Yapılandırması

### 1. Environment Variables Oluşturma

```bash
# .env dosyası oluştur
cp .env.example .env
```

**.env dosyasını düzenleyin:**

```bash
# MUTLAKA DEĞİŞTİRİN!
JWT_SECRET=$(openssl rand -hex 32)

# Database şifresi
DB_USER=app
DB_PASSWORD=$(openssl rand -base64 32)
DB_NAME=appdb

# Domain ve CORS
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Email ayarları (opsiyonel)
# SMTP_HOST=smtp.gmail.com
# SMTP_PORT=587
# SMTP_USER=your-email@gmail.com
# SMTP_PASSWORD=your-app-password
```

### 2. Güvenlik Duvarı (Firewall)

```bash
# UFW kullanıyorsanız
sudo ufw allow 22/tcp     # SSH
sudo ufw allow 80/tcp     # HTTP
sudo ufw allow 443/tcp    # HTTPS
sudo ufw enable

# Firewalld kullanıyorsanız
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

### 3. Dosya İzinleri

```bash
# Script'leri executable yap
chmod +x scripts/*.sh
chmod +x start-docker.sh

# Hassas dosyaları koru
chmod 600 .env
```

---

## Deployment Adımları

### 1. Sunucuya Bağlanma ve Proje İndirme

```bash
# SSH ile sunucuya bağlan
ssh user@your-server-ip

# Proje dizini oluştur
mkdir -p /opt/temizlik-takip
cd /opt/temizlik-takip

# Git'ten çek (private repo ise SSH key ekleyin)
git clone https://github.com/yourusername/bitirme2.git .
```

### 2. Environment Yapılandırması

```bash
# .env dosyasını oluştur ve düzenle
cp .env.example .env
nano .env

# JWT secret oluştur ve ekle
openssl rand -hex 32
```

### 3. Docker Build ve Başlatma

```bash
# Production build
docker-compose -f docker-compose.prod.yml build

# Container'ları başlat
docker-compose -f docker-compose.prod.yml up -d

# Log'ları kontrol et
docker-compose -f docker-compose.prod.yml logs -f
```

### 4. Database Migration ve Admin Oluşturma

```bash
# Migration'ları çalıştır (otomatik olur ama kontrol için)
docker-compose -f docker-compose.prod.yml exec api alembic upgrade head

# Admin user oluştur
docker-compose -f docker-compose.prod.yml exec api python -c "
from app.db.base import SessionLocal, Base, engine
from app.db.models.user import User, UserRole
from app.security.auth import get_password_hash

Base.metadata.create_all(bind=engine)
db = SessionLocal()

admin = db.query(User).filter(User.email == 'admin@kku.com').first()

if not admin:
    admin = User(
        email='admin@kku.com',
        hashed_password=get_password_hash('CHANGE_THIS_PASSWORD'),
        full_name='Sistem Admin',
        role=UserRole.ADMIN,
        is_active=True
    )
    db.add(admin)
    db.commit()
    print('Admin oluşturuldu')
else:
    print('Admin zaten mevcut')

db.close()
"
```

### 5. Health Check

```bash
# API health check
curl http://localhost:8000/health

# Frontend health check
curl http://localhost/health
```

---

## SSL/HTTPS Kurulumu

### Let's Encrypt ile Ücretsiz SSL

```bash
# Certbot kur
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx

# SSL sertifikası al
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# Sertifikaları Docker volume'a kopyala
sudo mkdir -p nginx/ssl
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem nginx/ssl/key.pem
```

### Nginx HTTPS Konfigürasyonu

`frontend/nginx.prod.conf` dosyasındaki HTTPS bölümünü aktif edin:

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # HSTS
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # ... rest of config ...
}

# HTTP to HTTPS redirect
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}
```

Container'ı yeniden başlat:

```bash
docker-compose -f docker-compose.prod.yml restart web
```

### SSL Sertifikası Otomatik Yenileme

```bash
# Crontab'a ekle
sudo crontab -e

# Her ayın 1'inde saat 03:00'te yenile
0 3 1 * * certbot renew --quiet && cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem /opt/temizlik-takip/nginx/ssl/cert.pem && cp /etc/letsencrypt/live/yourdomain.com/privkey.pem /opt/temizlik-takip/nginx/ssl/key.pem && docker-compose -f /opt/temizlik-takip/docker-compose.prod.yml restart web
```

---

## Monitoring ve Logging

### Log'ları İzleme

```bash
# Tüm servislerin log'ları
docker-compose -f docker-compose.prod.yml logs -f

# Sadece API log'ları
docker-compose -f docker-compose.prod.yml logs -f api

# Sadece database log'ları
docker-compose -f docker-compose.prod.yml logs -f db

# Son 100 satır
docker-compose -f docker-compose.prod.yml logs --tail=100
```

### Container Status İzleme

```bash
# Container durumları
docker-compose -f docker-compose.prod.yml ps

# Resource kullanımı
docker stats

# Disk kullanımı
docker system df
```

### Prometheus + Grafana (Opsiyonel - Gelişmiş)

```bash
# docker-compose.prod.yml'e ekleyin:
#   prometheus:
#     image: prom/prometheus
#     volumes:
#       - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
#     ports:
#       - "9090:9090"
#
#   grafana:
#     image: grafana/grafana
#     ports:
#       - "3000:3000"
#     environment:
#       - GF_SECURITY_ADMIN_PASSWORD=admin
```

---

## Backup ve Restore

### Otomatik Backup

Backup service docker-compose.prod.yml içinde tanımlı ve her gün otomatik çalışır.

**Manuel backup:**

```bash
docker-compose -f docker-compose.prod.yml exec backup /scripts/backup.sh
```

**Backup'ları listeleme:**

```bash
ls -lh backups/
```

### Restore İşlemi

```bash
# Restore script'ini çalıştır
docker-compose -f docker-compose.prod.yml exec backup /scripts/restore.sh /backups/backup_20250118_020000.sql.gz
```

**Manuel restore:**

```bash
gunzip -c backups/backup_20250118_020000.sql.gz | docker-compose -f docker-compose.prod.yml exec -T db psql -U app -d appdb
```

### Remote Backup (ÖNERİLİR)

```bash
# S3'e backup gönderme (AWS CLI kurulu olmalı)
aws s3 cp backups/ s3://your-bucket/temizlik-takip-backups/ --recursive

# Rsync ile remote sunucuya
rsync -avz backups/ user@backup-server:/backups/temizlik-takip/
```

---

## Performans Optimizasyonu

### 1. Database Optimizasyonu

```sql
-- PostgreSQL'de connection pool ayarları
-- /etc/postgresql/15/main/postgresql.conf

max_connections = 100
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 4MB
maintenance_work_mem = 64MB
```

### 2. API Worker Sayısı

`docker-compose.prod.yml` içinde worker sayısını artırın:

```yaml
command: >
  gunicorn app.main:app 
    --workers 8 
    --worker-class uvicorn.workers.UvicornWorker 
    --bind 0.0.0.0:8000
```

**Worker sayısı formülü:** `(2 x CPU_CORES) + 1`

### 3. Redis Cache (Opsiyonel)

```yaml
# docker-compose.prod.yml'e ekle
redis:
  image: redis:7-alpine
  restart: always
  command: redis-server --appendonly yes
  volumes:
    - redis_data:/data
  networks:
    - app-network
```

### 4. CDN Kullanımı

Static dosyalar için CloudFlare veya AWS CloudFront kullanın.

---

## Sorun Giderme

### API Başlamıyor

```bash
# Log'ları kontrol et
docker-compose -f docker-compose.prod.yml logs api

# Container'ın durumunu kontrol et
docker-compose -f docker-compose.prod.yml ps

# Restart
docker-compose -f docker-compose.prod.yml restart api
```

### Database Bağlantı Hatası

```bash
# Database container'ı çalışıyor mu?
docker-compose -f docker-compose.prod.yml ps db

# Database log'ları
docker-compose -f docker-compose.prod.yml logs db

# Manuel bağlantı testi
docker-compose -f docker-compose.prod.yml exec db psql -U app -d appdb -c "SELECT 1;"
```

### Frontend 502 Bad Gateway

```bash
# Backend çalışıyor mu kontrol et
curl http://localhost:8000/health

# Nginx config test
docker-compose -f docker-compose.prod.yml exec web nginx -t

# Nginx reload
docker-compose -f docker-compose.prod.yml exec web nginx -s reload
```

### Disk Dolu

```bash
# Docker temizliği
docker system prune -a --volumes

# Log rotasyonu
docker-compose -f docker-compose.prod.yml logs --tail=1000 > logs_backup.txt
```

### Memory Leak

```bash
# Container'ı restart et
docker-compose -f docker-compose.prod.yml restart api

# Resource limit ekle (docker-compose.prod.yml)
api:
  deploy:
    resources:
      limits:
        memory: 2G
      reservations:
        memory: 1G
```

---

## Güncelleme ve Maintenance

### Uygulama Güncellemesi

```bash
# Yeni kodu çek
git pull origin main

# Rebuild ve restart (zero-downtime için)
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d

# Migration'ları çalıştır
docker-compose -f docker-compose.prod.yml exec api alembic upgrade head
```

### Zero-Downtime Deployment

```bash
# Blue-green deployment için script
./scripts/deploy.sh
```

---

## Production Checklist

### Pre-Launch

- [ ] `.env` dosyasında JWT_SECRET değiştirildi
- [ ] `.env` dosyasında DEBUG=false ayarlandı
- [ ] Database şifresi güçlü ve benzersiz
- [ ] CORS_ORIGINS production domain'e ayarlandı
- [ ] SSL sertifikası kuruldu
- [ ] Firewall kuralları yapılandırıldı
- [ ] Admin şifresi değiştirildi
- [ ] Backup script'i test edildi

### Post-Launch

- [ ] Health check endpoint çalışıyor
- [ ] SSL sertifikası doğrulandı (A+ rating)
- [ ] Monitoring kuruldu
- [ ] Log rotation yapılandırıldı
- [ ] Backup'lar otomatik alınıyor
- [ ] Performance test yapıldı
- [ ] Security scan yapıldı

---

## Destek ve İletişim

**Sorun bildirmek için:**
- GitHub Issues: https://github.com/yourusername/bitirme2/issues

**Dokümantasyon:**
- Development: [BASLANGIC.md](./BASLANGIC.md)
- Production: [PRODUCTION.md](./PRODUCTION.md)

---

## Lisans

Bu proje KKÜ Bitirme Projesi kapsamında geliştirilmiştir.
