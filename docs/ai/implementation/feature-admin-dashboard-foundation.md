```markdown
---
phase: implementation
title: Hướng Dẫn Triển Khai
description: Ghi chú triển khai kỹ thuật, mẫu và hướng dẫn mã
---

# Hướng Dẫn Triển Khai - Nền tảng Dashboard Admin

## Thiết Lập Phát Triển

- **Điều kiện tiên quyết:** Dự án frontend Next.js đã được cài đặt và chạy (`pnpm dev`).
- **Thư viện:** Đảm bảo `lucide-react` đã được cài đặt để sử dụng icon.

## Cấu Trúc Mã

**Mã được tổ chức như thế nào?**

- **Components Layout:** Toàn bộ code cho layout sẽ nằm trong `frontend/components/admin/`.
- **Cấu hình Menu:** File định nghĩa các mục menu sẽ nằm ở `frontend/config/menu.ts`.
- **Routing:** Các trang quản trị sẽ được đặt trong `frontend/app/admin/`. Layout chính là `frontend/app/admin/layout.tsx`.

## Ghi Chú Triển Khai

**Chi tiết kỹ thuật chính cần nhớ:**

- **Quản lý trạng thái Sidebar:**
  - Sử dụng `useState` trong `AdminPanelLayout` để lưu trạng thái `isCollapsed`.
  - Truyền trạng thái và hàm cập nhật xuống các component con (`Sidebar`, `Navbar`) qua props.
  - Lưu trạng thái sidebar vào `localStorage` để duy trì sở thích của người dùng giữa các lần tải lại trang.
- **Responsive:**
  - Sử dụng các breakpoint của Tailwind CSS (`md:`, `lg:`) để thay đổi giao diện.
  - `Sidebar` sẽ bị ẩn hoàn toàn trên màn hình nhỏ (`md:` và nhỏ hơn).
  - `SheetMenu` trong `Navbar` sẽ chỉ hiển thị trên màn hình nhỏ để cung cấp điều hướng thay thế.
- **Phân quyền Menu:**
  - Trong `Menu.tsx`, trước khi render danh sách, hãy lọc mảng menu dựa trên thuộc tính `roles` của mỗi `NavLink` và vai trò của người dùng hiện tại.
  - Nếu một `NavLink` không có thuộc tính `roles`, nó sẽ được hiển thị cho tất cả mọi người.

## Điểm Tích Hợp

- **API Người dùng:** Component `UserNav` sẽ gọi hàm `getUserProfile` từ `apiRequests/user.ts` để lấy dữ liệu. Cần xử lý trạng thái loading và error.
- **Supabase Auth:** Logic đăng xuất trong `UserNav` sẽ gọi `supabase.auth.signOut()`.

## Xử Lý Lỗi

- **Lỗi API:** Khi gọi `getUserProfile` thất bại, `UserNav` nên hiển thị một trạng thái mặc định hoặc thông báo lỗi nhỏ, không làm sập toàn bộ layout.
- **Không có vai trò:** Xử lý trường hợp người dùng không có vai trò hoặc vai trò không hợp lệ, có thể hiển thị một bộ menu mặc định hoặc không hiển thị menu nào.
```
