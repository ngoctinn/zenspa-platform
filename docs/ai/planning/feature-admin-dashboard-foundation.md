```markdown
---
phase: planning
title: Lập Kế Hoạch Dự Án & Phân Tích Nhiệm Vụ
description: Phân tích công việc thành các nhiệm vụ có thể thực hiện và ước tính thời gian
---

# Lập Kế Hoạch Dự Án & Phân Tích Nhiệm Vụ - Nền tảng Dashboard Admin

## Mốc Quan Trọng

- [ ] **Mốc 1:** Xây dựng xong bộ components giao diện cơ bản cho layout admin.
- [ ] **Mốc 2:** Tích hợp layout vào Next.js App Router và tạo trang dashboard mẫu.
- [ ] **Mốc 3:** Hoàn thiện responsive và logic phân quyền cho menu.

## Phân Tích Nhiệm Vụ

**Công việc cụ thể nào cần thực hiện?**

### Giai Đoạn 1: Xây Dựng Components Giao Diện (UI)

- [ ] **Nhiệm vụ 1.1:** Tạo file và viết code JSX/TSX cơ bản cho các components giao diện dựa trên `#file:admin-panel`:
  - `components/admin/AdminPanelLayout.tsx`
  - `components/admin/Sidebar.tsx`
  - `components/admin/Navbar.tsx`
  - `components/admin/ContentLayout.tsx`
  - `components/admin/Menu.tsx`
  - `components/admin/UserNav.tsx`
  - `components/admin/SheetMenu.tsx`
  - `components/admin/CollapseMenuButton.tsx`
  - `components/admin/SidebarToggle.tsx`
- [ ] **Nhiệm vụ 1.2:** Style các components bằng Tailwind CSS và sử dụng các primitives từ Shadcn/UI (`Sheet`, `DropdownMenu`, `Button`, v.v.).

### Giai Đoạn 2: Tích Hợp Vào Next.js & Tạo Trang Mẫu

- [ ] **Nhiệm vụ 2.1:** Tạo file layout `app/admin/layout.tsx`.
- [ ] **Nhiệm vụ 2.2:** Import và sử dụng component `AdminPanelLayout` trong `app/admin/layout.tsx` để bao bọc `children`.
- [ ] **Nhiệm vụ 2.3:** Tạo trang dashboard mẫu tại `app/admin/dashboard/page.tsx`. Trang này sẽ sử dụng `ContentLayout` và hiển thị một vài nội dung giả lập.
- [ ] **Nhiệm vụ 2.4:** Tạo file cấu hình menu (ví dụ: `config/menu.ts`) để định nghĩa các `NavLink` tĩnh ban đầu.

### Giai Đoạn 3: Hoàn Thiện Logic & Responsive

- [ ] **Nhiệm vụ 3.1:** Thêm logic state (`useState`) vào `AdminPanelLayout.tsx` để quản lý trạng thái đóng/mở của `Sidebar`.
- [ ] **Nhiệm vụ 3.2:** Kết nối các nút `SidebarToggle` và `CollapseMenuButton` để cập nhật trạng thái của sidebar.
- [ ] **Nhiệm vụ 3.3:** Tích hợp API `getUserProfile` vào `UserNav` để hiển thị thông tin người dùng thật.
- [ ] **Nhiệm vụ 3.4:** Lọc danh sách menu trong `Menu.tsx` dựa trên vai trò của người dùng lấy được từ `getUserProfile`.
- [ ] **Nhiệm vụ 3.5:** Kiểm tra và tinh chỉnh responsive trên các kích thước màn hình khác nhau.

## Phụ Thuộc

- **API:** Phụ thuộc vào API `/api/v1/users/me` đã có để lấy thông tin và vai trò người dùng.
- **UI Components:** Phụ thuộc vào thư viện Shadcn/UI đã được cài đặt.

## Thời Gian & Ước Tính

- **Giai Đoạn 1:** ~2-3 giờ
- **Giai Đoạn 2:** ~1-2 giờ
- **Giai Đoạn 3:** ~2-3 giờ
- **Tổng cộng:** ~5-8 giờ

## Rủi Ro & Giảm Thiểu

- **Rủi ro:** Logic quản lý trạng thái sidebar giữa các component có thể phức tạp.
- **Giảm thiểu:** Sử dụng React Context hoặc một state manager đơn giản (như Zustand) nếu `useState` và props drilling trở nên quá phức tạp. Tuy nhiên, với quy mô hiện tại, `useState` là đủ.

## Tài Nguyên Cần Thiết

- **Nhà phát triển:** 1
- **Thiết kế:** Dựa trên các components mẫu trong `#file:admin-panel`.
- **Tài liệu:** `docs/ai/design/feature-admin-dashboard-foundation.md`.
```
