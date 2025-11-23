```markdown
---
phase: testing
title: Chiến Lược Kiểm Tra
description: Xác định cách tiếp cận kiểm tra, trường hợp kiểm tra và đảm bảo chất lượng
---

# Chiến Lược Kiểm Tra - Nền tảng Dashboard Admin

## Mục Tiêu Bao Phủ Kiểm Tra

- **Phạm vi kiểm tra:** Tập trung vào kiểm tra giao diện (UI) và tương tác người dùng trên layout admin.
- **Mục tiêu:** Đảm bảo layout hiển thị đúng trên các thiết bị, các nút hoạt động và logic phân quyền menu hoạt động chính xác.

## Kiểm Tra Đơn Vị

**Thành phần riêng lẻ nào cần kiểm tra?**

- **`Menu.tsx`:**
  - [ ] **Trường hợp kiểm tra 1:** Render đúng số lượng mục menu khi được cung cấp một mảng `NavLink` tĩnh.
  - [ ] **Trường hợp kiểm tra 2:** Lọc và chỉ hiển thị các mục menu mà người dùng có quyền truy cập dựa trên vai trò.
  - [ ] **Trường hợp kiểm tra 3:** Không hiển thị mục menu nào nếu vai trò người dùng không khớp với bất kỳ `NavLink` nào.
- **`UserNav.tsx`:**
  - [ ] **Trường hợp kiểm tra 1:** Hiển thị tên và email của người dùng khi dữ liệu được cung cấp.
  - [ ] **Trường hợp kiểm tra 2:** Hiển thị trạng thái loading khi đang fetch dữ liệu.
  - [ ] **Trường hợp kiểm tra 3:** Gọi hàm `onSignOut` khi người dùng nhấp vào nút "Đăng xuất".

## Kiểm Tra Tích Hợp

**Chúng ta kiểm tra tương tác thành phần như thế nào?**

- **`AdminPanelLayout.tsx` và các component con:**
  - [ ] **Kịch bản tích hợp 1:** Khi nhấp vào `SidebarToggle` trong `Navbar`, trạng thái `isCollapsed` của `Sidebar` thay đổi tương ứng.
  - [ ] **Kịch bản tích hợp 2:** Khi nhấp vào `CollapseMenuButton` trong `Sidebar`, trạng thái `isCollapsed` cũng thay đổi.
  - [ ] **Kịch bản tích hợp 3:** Trên màn hình di động, `Sidebar` ẩn và `SheetMenu` trong `Navbar` được hiển thị.

## Kiểm Tra End-to-End

**Luồng người dùng nào cần xác thực?**

- [ ] **Luồng người dùng 1 (Admin):**
  1. Đăng nhập với tài khoản admin.
  2. Điều hướng đến `/admin/dashboard`.
  3. Xác nhận layout admin được hiển thị đúng (Sidebar, Navbar).
  4. Xác nhận Sidebar hiển thị đầy đủ các mục menu dành cho admin.
  5. Nhấp vào một mục menu và xác nhận đã điều hướng đến đúng trang.
  6. Thu gọn và mở rộng sidebar, xác nhận layout thay đổi chính xác.
  7. Mở dropdown người dùng và đăng xuất thành công.
- [ ] **Luồng người dùng 2 (Responsive):**
  1. Mở trang `/admin/dashboard` trên trình duyệt có kích thước di động.
  2. Xác nhận `Sidebar` đã bị ẩn.
  3. Nhấp vào nút menu trên `Navbar` để mở `SheetMenu`.
  4. Xác nhận các mục menu hiển thị trong `SheetMenu`.
  5. Nhấp vào một mục và xác nhận điều hướng đúng.

## Kiểm Tra Thủ Công

**Điều gì cần xác thực của con người?**

- [ ] **Danh sách kiểm tra UI/UX:**
  - Giao diện có khớp với thiết kế mẫu không?
  - Khoảng cách, màu sắc, font chữ có nhất quán không?
  - Các hiệu ứng (hover, focus, transition) có mượt mà không?
  - Icon có hiển thị đúng không?
- [ ] **Tương thích trình duyệt:** Kiểm tra trên Chrome, Firefox, Safari phiên bản mới nhất.
- [ ] **Tương thích thiết bị:** Kiểm tra trên Desktop, Tablet (dọc và ngang), Mobile.
```
