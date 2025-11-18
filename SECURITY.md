# Security Policy

## Supported Versions

Sadece en son production sürümü güvenlik güncellemeleri alır.

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

Güvenlik açığı bildirmek için:

1. **ASLA** public issue açmayın
2. Email: security@yourdomain.com
3. Detaylı açıklama ve reproduction steps ekleyin
4. 48 saat içinde yanıt alacaksınız

## Security Features

### Implemented

- ✅ JWT Authentication
- ✅ Bcrypt password hashing
- ✅ HTTPS/TLS support
- ✅ CORS configuration
- ✅ Rate limiting
- ✅ SQL injection protection (SQLAlchemy ORM)
- ✅ XSS protection headers
- ✅ CSRF protection
- ✅ Security headers (X-Frame-Options, X-Content-Type-Options, etc.)
- ✅ Input validation (Pydantic)
- ✅ Database connection pooling
- ✅ Error message sanitization in production

### Best Practices

1. **Environment Variables**: Asla .env dosyasını commit etmeyin
2. **Secrets**: JWT_SECRET her ortam için farklı ve güçlü olmalı
3. **Database**: Production'da güçlü şifre kullanın
4. **SSL**: Let's Encrypt veya valid sertifika kullanın
5. **Updates**: Dependency'leri düzenli güncelleyin
6. **Backups**: Günlük otomatik backup alın
7. **Monitoring**: Log'ları düzenli kontrol edin
8. **Access**: Sadece gerekli portları açık tutun

## Known Issues

Bilinen güvenlik açığı bulunmamaktadır.

## Updates

Güvenlik güncellemeleri için GitHub Releases sayfasını takip edin.
