# Alembic Database Migrations

Thư mục này chứa database migration scripts cho ZenSpa Backend.

## Cấu hình

Alembic được cấu hình để:

- Load database URL từ environment variable `DATABASE_URL`
- Sử dụng SQLModel metadata cho autogenerate
- Chạy migrations trong async mode
- Convert async database URL sang sync URL cho Alembic

## Sử dụng

### Tạo migration mới

```bash
# Autogenerate migration từ model changes
alembic revision --autogenerate -m "description of changes"

# Tạo empty migration
alembic revision -m "description of changes"
```

### Apply migrations

```bash
# Upgrade to latest version
alembic upgrade head

# Upgrade to specific version
alembic upgrade <revision_id>

# Upgrade by one version
alembic upgrade +1
```

### Rollback migrations

```bash
# Downgrade by one version
alembic downgrade -1

# Downgrade to specific version
alembic downgrade <revision_id>

# Downgrade all
alembic downgrade base
```

### Xem migration history

```bash
# Show current version
alembic current

# Show migration history
alembic history

# Show migration history with details
alembic history --verbose
```

## Lưu ý quan trọng

1. **Import models**: Đảm bảo import tất cả SQLModel models trong `env.py` để autogenerate hoạt động đúng
2. **Review migrations**: Luôn review generated migrations trước khi apply
3. **Test migrations**: Test migrations trên development database trước
4. **Backup**: Backup production database trước khi chạy migrations
5. **Environment**: Đảm bảo `DATABASE_URL` được set trong environment

## Cấu trúc

- `alembic.ini` - Alembic configuration
- `env.py` - Migration environment setup (async support)
- `script.py.mako` - Template cho migration scripts
- `versions/` - Migration scripts directory

## Ví dụ migration workflow

```bash
# 1. Tạo hoặc update SQLModel models
# 2. Generate migration
alembic revision --autogenerate -m "add user table"

# 3. Review generated migration in versions/
# 4. Apply migration
alembic upgrade head

# 5. Verify in database
```

## Troubleshooting

**Error: "Can't locate revision identified by"**

- Kiểm tra database có bảng `alembic_version` chưa
- Run `alembic stamp head` để sync version

**Error: "No changes in schema detected"**

- Đảm bảo models được import trong `env.py`
- Kiểm tra SQLModel metadata có chứa model không

**Error: "Database URL not set"**

- Đảm bảo `DATABASE_URL` trong `.env` file
- Load `.env` trước khi run alembic
