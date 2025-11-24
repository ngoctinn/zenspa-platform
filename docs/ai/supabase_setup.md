# Hướng Dẫn Cấu Hình Supabase

Tài liệu này hướng dẫn cấu hình Supabase để hỗ trợ các tính năng bảo mật và tự động hóa đã được cập nhật trong Backend.

## 1. Tự Động Tạo Profile (Database Trigger)

Để tránh việc tạo Profile giả trong code backend, chúng ta sử dụng Database Trigger để tự động tạo row trong bảng `public.profiles` ngay khi một user mới được tạo trong `auth.users`.

Chạy đoạn SQL sau trong **SQL Editor** của Supabase:

```sql
-- 1. Tạo function xử lý user mới
create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer set search_path = public
as $$
begin
  insert into public.profiles (id, full_name, avatar_url)
  values (
    new.id,
    new.raw_user_meta_data ->> 'full_name',
    new.raw_user_meta_data ->> 'avatar_url'
  );
  return new;
end;
$$;

-- 2. Tạo trigger kích hoạt khi có insert vào auth.users
create or replace trigger on_auth_user_created
  after insert on auth.users
  for each row execute procedure public.handle_new_user();
```

## 2. Custom Claims cho Phân Quyền (Auth Hook)

Để tối ưu hóa hiệu năng, chúng ta sẽ inject thông tin `roles` vào JWT Token (Custom Claims) để Backend không cần query database mỗi khi check quyền.

### Bước 1: Tạo Function Hook

Chạy đoạn SQL sau trong **SQL Editor**:

```sql
-- Tạo function hook để inject claims
create or replace function public.custom_access_token_hook(event jsonb)
returns jsonb
language plpgsql
stable
as $$
declare
  claims jsonb;
  user_roles text[];
begin
  -- Lấy danh sách roles của user từ bảng user_role_links và roles
  select array_agg(r.name)
  into user_roles
  from public.user_role_links url
  join public.roles r on url.role_id = r.id
  where url.user_id = (event->>'user_id')::uuid;

  -- Nếu không có role nào, mặc định là customer (hoặc rỗng)
  if user_roles is null then
    user_roles := array[]::text[];
  end if;

  claims := event->'claims';

  -- Inject roles vào app_metadata
  if jsonb_typeof(claims->'app_metadata') is null then
    claims := jsonb_set(claims, '{app_metadata}', '{}');
  end if;

  claims := jsonb_set(claims, '{app_metadata, roles}', to_jsonb(user_roles));

  -- Trả về claims đã update
  event := jsonb_set(event, '{claims}', claims);
  return event;
end;
$$;

-- Cấp quyền cho supabase_auth_admin để chạy function này
grant execute on function public.custom_access_token_hook to supabase_auth_admin;
grant usage on schema public to supabase_auth_admin;
grant select on table public.user_role_links to supabase_auth_admin;
grant select on table public.roles to supabase_auth_admin;
```

### Bước 2: Kích Hoạt Hook trong Dashboard

1.  Truy cập **Supabase Dashboard** -> **Authentication** -> **Hooks**.
2.  Tìm mục **"Custom Access Token"** (hoặc `MFA & Captcha` -> `Hooks` tùy phiên bản giao diện, hiện tại thường nằm trong `Auth Settings` -> `Hooks`).
3.  Chọn **"Enable Hook"**.
4.  Chọn function `custom_access_token_hook` vừa tạo.
5.  Lưu lại.

## 3. Kiểm Tra

Sau khi cấu hình xong:

1.  Đăng nhập lại user.
2.  Decode JWT Token (dùng jwt.io) để kiểm tra xem có field `app_metadata.roles` hay không.
3.  Backend sẽ tự động đọc field này để phân quyền.
