---
phase: design
title: Thiết Kế - feature-customer-appointments
description: Kiến trúc và quyết định thiết kế cho trang lịch hẹn
---

# Thiết Kế

## Kiến Trúc Hệ Thống

- Component: AppointmentsPage với Tabs (All, Upcoming, Past)
- Data: Fetch từ Supabase table 'appointments'
- UI: Card list với details (date, service, status)

## Quyết Định Thiết Kế

- Sử dụng Tabs từ Shadcn/UI cho filter
- Card cho mỗi appointment với actions (cancel for upcoming)
- Responsive grid

## Sơ Đồ

```mermaid
graph TD
    A[AppointmentsPage] --> B[Tabs: All/Upcoming/Past]
    B --> C[AppointmentCard]
    C --> D[Details: Date, Service, Status]
    C --> E[Actions: Cancel if upcoming]
```
