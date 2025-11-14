---
phase: design
title: Thiết Kế - feature-customer-services
description: Kiến trúc và quyết định thiết kế cho trang gói dịch vụ
---

# Thiết Kế

## Kiến Trúc Hệ Thống

- Component: ServicesPage với list of ServiceCard
- Data: Fetch từ Supabase 'services'
- UI: Card với progress bar cho remaining sessions

## Quyết Định Thiết Kế

- Progress bar từ Shadcn/UI cho visual remaining
- Button "Mua thêm" redirect to booking

## Sơ Đồ

```mermaid
graph TD
    A[ServicesPage] --> B[ServiceCard]
    B --> C[Name, Description]
    B --> D[Progress: Used/Total]
    B --> E[Button: Mua thêm]
```
