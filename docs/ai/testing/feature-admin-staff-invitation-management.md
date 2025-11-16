---
phase: testing
title: Chiến Lược Kiểm Tra
description: Xác định cách tiếp cận kiểm tra, trường hợp kiểm tra và đảm bảo chất lượng
---

# Chiến Lược Kiểm Tra

## Mục Tiêu Bao Phủ Kiểm Tra

**Chúng ta nhắm đến mức kiểm tra nào?**

- 100% cho logic backend xử lý các trường hợp.
- Tích hợp với Supabase API.
- End-to-end cho luồng mời và chấp nhận.

## Kiểm Tra Đơn Vị

**Thành phần riêng lẻ nào cần kiểm tra?**

### Admin Service

- [ ] Test kiểm tra user tồn tại
- [ ] Test gọi Supabase invite
- [ ] Test gán role cho user hiện tại
- [ ] Test xử lý trùng role

### Admin Routes

- [ ] Test auth middleware
- [ ] Test input validation

## Kiểm Tra Tích Hợp

**Chúng ta kiểm tra tương tác thành phần như thế nào?**

- [ ] Test API với DB changes
- [ ] Test với Supabase mock

## Kiểm Tra End-to-End

**Luồng người dùng nào cần xác thực?**

- [ ] Luồng mời user mới
- [ ] Luồng gán role cho user hiện tại

## Dữ Liệu Kiểm Tra

**Chúng ta sử dụng dữ liệu nào để kiểm tra?**

- Mock users trong test DB.

## Báo Cáo & Bao Phủ Kiểm Tra

**Chúng ta xác minh và giao tiếp kết quả kiểm tra như thế nào?**

- Chạy pytest với coverage.

## Kiểm Tra Hiệu Suất

**Chúng ta xác thực hiệu suất như thế nào?**

- Kịch bản load: 100 invites đồng thời, measure response time.
- Baseline: <2s average, <5s p95.
- Tools: Locust hoặc Artillery for load testing.
