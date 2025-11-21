---
phase: implementation
title: Hướng Dẫn Triển Khai - Backend Async Migration
description: Hướng dẫn chi tiết code async cho database
---

# Hướng Dẫn Triển Khai - Backend Async Migration

## Thiết Lập Phát Triển

**Chúng ta bắt đầu như thế nào?**

- Cài đặt driver: `pip install asyncpg`
- Cài đặt hỗ trợ test: `pip install pytest-asyncio`

## Cấu Trúc Mã

**Mã được tổ chức như thế nào?**

### `app/core/database.py`

```python
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

# URL ví dụ: postgresql+asyncpg://user:pass@localhost/db
engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
```

### Service Pattern

```python
# Cũ (Sync)
def get_user(session: Session, user_id: str):
    return session.query(User).get(user_id)

# Mới (Async)
async def get_user(session: AsyncSession, user_id: str):
    result = await session.exec(select(User).where(User.id == user_id))
    return result.first()
```

## Ghi Chú Triển Khai

**Chi tiết kỹ thuật chính cần nhớ:**

### Thay đổi Query

- Không dùng `session.query(...)` nữa (đây là style cũ của SQLAlchemy sync).
- Dùng `await session.exec(select(...))` là chuẩn của SQLModel.
- Với `create`, `update`, `delete`:
  - `session.add(obj)` (không cần await)
  - `await session.commit()`
  - `await session.refresh(obj)`

### Xử lý Relationship

- Nếu truy cập `user.roles` mà roles chưa được load, sẽ lỗi trong async.
- Giải pháp: Eager load.
  ```python
  from sqlalchemy.orm import selectinload
  statement = select(User).options(selectinload(User.roles)).where(...)
  ```

## Xử Lý Lỗi

**Chúng ta xử lý thất bại như thế nào?**

- Sử dụng `try...except` bao quanh các block `await session.commit()` để rollback nếu cần.
- `await session.rollback()`

## Cân Nhắc Hiệu Suất

**Chúng ta giữ tốc độ như thế nào?**

- Tận dụng `asyncio.gather` nếu cần thực hiện nhiều query độc lập (tuy nhiên với cùng 1 session thì thường phải tuần tự, cẩn thận race condition nếu dùng chung session). Thường trong 1 request scope, các query DB vẫn tuần tự nhưng không block CPU cho việc khác.
