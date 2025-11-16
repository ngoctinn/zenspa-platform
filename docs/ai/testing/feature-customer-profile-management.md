---
phase: testing
title: Chiến Lược Kiểm Tra
description: Xác định cách tiếp cận kiểm tra, trường hợp kiểm tra và đảm bảo chất lượng
---

# Chiến Lược Kiểm Tra

## Mục Tiêu Bao Phủ Kiểm Tra

**Chúng ta nhắm đến mức kiểm tra nào?**

- Unit: 100% models, service.
- Integration: API endpoints.
- E2E: Signup → view/update profile.

## Kiểm Tra Đơn Vị

**Thành phần riêng lẻ nào cần kiểm tra?**

### Backend Service

- [ ] Test get_profile_by_id (found/not found).
- [ ] Test update_profile (validation).

### Frontend Component

- [ ] Test ProfileForm submit.

## Kiểm Tra Tích Hợp

**Chúng ta kiểm tra tương tác thành phần như thế nào?**

- [ ] GET /me returns profile.
- [ ] PUT /me updates DB.

## Kiểm Tra End-to-End

**Luồng người dùng nào cần xác thực?**

- [ ] Signup → profile created.
- [ ] Login → view profile.
- [ ] Update profile → saved.

## Kiểm Tra Thủ Công

**Điều gì cần xác thực của con người?**

- UI form validation, avatar upload.
