# Hướng Dẫn Thiết Lập Auth Hook Tự Động Tạo Profile

## Tổng Quan

Hướng dẫn này sẽ giúp bạn thiết lập **Auth Hook** trong Supabase để tự động tạo profile khách hàng khi người dùng đăng ký tài khoản. Điều này đảm bảo rằng mỗi user trong `auth.users` sẽ có một bản ghi tương ứng trong bảng `profiles`.

## Mục Tiêu

- Tự động đồng bộ dữ liệu giữa `auth.users` và `profiles`
- Đảm bảo tính nhất quán dữ liệu
- Giảm tải cho backend API

## Điều Kiện Tiên Quyết

- Tài khoản Supabase với quyền admin
- Database đã có bảng `profiles` (đã tạo qua Alembic migration)
- Truy cập Supabase Dashboard

## Các Bước Thiết Lập

### Bước 1: Truy Cập Supabase Dashboard

1. Mở [Supabase Dashboard](https://supabase.com/dashboard)
2. Chọn project ZenSpa của bạn
3. Điều hướng đến **Database > Functions**

### Bước 2: Tạo Postgres Function

1. Nhấn **Create a new function**
2. Điền thông tin:

   - **Name**: `create_profile_on_signup`
   - **Schema**: `public`
   - **Return type**: `trigger`

3. Trong phần **Definition**, paste đoạn code sau:

```sql
CREATE OR REPLACE FUNCTION public.create_profile_on_signup()
RETURNS trigger
LANGUAGE plpgsql
SECURITY DEFINER SET search_path = public
AS $$
BEGIN
  INSERT INTO public.profiles (id, email, full_name, role, created_at, updated_at)
  VALUES (
    NEW.id,
    NEW.email,
    COALESCE(NEW.raw_user_meta_data->>'full_name', NEW.email),
    COALESCE(NEW.raw_user_meta_data->>'role', 'customer'),
    NOW(),
    NOW()
  );
  RETURN NEW;
END;
$$;
```

### Bước 3: Tạo Trigger

Sau khi tạo function, tạo trigger để gọi function khi có user mới:

```sql
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.create_profile_on_signup();
```

### Bước 4: Cấp Quyền Cho Function

Đảm bảo function có quyền insert vào bảng profiles:

```sql
GRANT USAGE ON SCHEMA public TO postgres, anon, authenticated, service_role;
GRANT ALL ON public.profiles TO postgres, anon, authenticated, service_role;
```

## Xác Minh Thiết Lập

### Kiểm Tra Function

1. Trong Supabase Dashboard > Database > Functions
2. Xem function `create_profile_on_signup` đã được tạo

### Kiểm Tra Trigger

1. Chạy query trong SQL Editor:

```sql
SELECT * FROM pg_trigger WHERE tgname = 'on_auth_user_created';
```

### Test Tạo User

1. Đăng ký user mới qua Supabase Auth
2. Kiểm tra bảng `profiles`:

```sql
SELECT * FROM public.profiles WHERE email = 'test@example.com';
```

## Xử Lý Sự Cố

### Lỗi "Permission Denied"

- Đảm bảo đã cấp quyền đúng cho function
- Kiểm tra RLS policies trên bảng profiles

### Trigger Không Kích Hoạt

- Kiểm tra trigger đã được tạo: `SELECT * FROM pg_trigger;`
- Xem logs trong Supabase Dashboard > Database > Logs

### Dữ Liệu Không Đồng Bộ

- Nếu có user cũ chưa có profile, chạy script migration:

```sql
INSERT INTO public.profiles (id, email, full_name, role, created_at, updated_at)
SELECT
  id,
  email,
  COALESCE(raw_user_meta_data->>'full_name', email),
  COALESCE(raw_user_meta_data->>'role', 'customer'),
  created_at,
  updated_at
FROM auth.users
WHERE id NOT IN (SELECT id FROM public.profiles);
```

## Lưu Ý Quan Trọng

- Function này chỉ tạo profile cơ bản với thông tin từ auth.users
- Thông tin chi tiết (phone, birth_date, avatar) sẽ được cập nhật qua API
- Đảm bảo RLS được cấu hình đúng để bảo mật dữ liệu

## Tài Liệu Tham Khảo

- [Supabase Auth Hooks Documentation](https://supabase.com/docs/guides/auth/auth-hooks)
- [PostgreSQL Triggers](https://www.postgresql.org/docs/current/sql-createtrigger.html)
- ZenSpa Design: `docs/ai/design/feature-backend-user-profile-api.md`
