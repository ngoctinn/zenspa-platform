---
phase: planning
title: Lập Kế Hoạch Dự Án & Phân Tích Nhiệm Vụ
description: Phân tích công việc thành các nhiệm vụ có thể thực hiện và ước tính thời gian
---

# Lập Kế Hoạch Dự Án & Phân Tích Nhiệm Vụ

## Mốc Quan Trọng

**Các điểm kiểm tra chính là gì?**

- [ ] Mốc 1: Hoàn thành thiết kế DB và models
- [ ] Mốc 2: Triển khai backend API
- [ ] Mốc 3: Triển khai frontend và tích hợp

## Phân Tích Nhiệm Vụ

**Công việc cụ thể nào cần thực hiện?**

### Giai Đoạn 1: Nền Tảng

- [ ] Nhiệm vụ 1.1: Tạo enum Role và bảng UserRoleLink trong SQLModel (admin_models.py)
- [ ] Nhiệm vụ 1.2: Tạo migration Alembic cho bảng UserRoleLink mới
- [ ] Nhiệm vụ 1.3: Cập nhật logic để sử dụng UserRoleLink thay vì Profile.role (để hỗ trợ nhiều-nhiều)

### Giai Đoạn 2: Tính Năng Cốt Lõi

- [x] Nhiệm vụ 2.1: Module admin đã tồn tại với schemas, service, routes cơ bản
- [ ] Nhiệm vụ 2.2: Cập nhật admin_service.py để xử lý invite và assign role qua UserRoleLink
- [ ] Nhiệm vụ 2.3: Tạo API endpoint POST /api/v1/admin/invite-staff (thêm vào admin_routes.py)
- [ ] Nhiệm vụ 2.4: Cập nhật admin_schemas.py với InviteStaffRequest schema

### Giai Đoạn 3: Tích Hợp & Hoàn Chỉnh

- [ ] Nhiệm vụ 3.1: Tạo component InviteStaffForm trên frontend
- [ ] Nhiệm vụ 3.2: Tạo API request và tích hợp với backend
- [ ] Nhiệm vụ 3.3: Thêm trang admin/staff và bảo vệ route

## Phụ Thuộc

**Điều gì cần xảy ra theo thứ tự nào?**

- Phụ thuộc nhiệm vụ: Tạo UserRoleLink trước, sau đó cập nhật logic service, API trước frontend.
- Phụ thuộc bên ngoài: Supabase service_role key, email templates (đã có sẵn).

## Thời Gian & Ước Tính

**Khi nào mọi thứ sẽ hoàn thành?**

- Nỗ lực ước tính: 2-3 ngày cho backend (tạo models, migration, cập nhật logic), 1-2 ngày cho frontend.
- Ngày mục tiêu: Hoàn thành trong tuần này.

## Rủi Ro & Giảm Thiểu

**Điều gì có thể sai sót?**

- Rủi ro: Migration conflict với data hiện tại (Profile.role), Supabase invite API thay đổi, email không gửi được, logic nhiều-nhiều phức tạp hơn.
- Giảm thiểu: Backup data trước migration, test với email thật, có fallback manual, migrate data từ Profile.role sang UserRoleLink.

## Tài Nguyên Cần Thiết

**Chúng ta cần gì để thành công?**

- Thành viên: Developer backend và frontend.
- Công cụ: VS Code, Supabase dashboard.
