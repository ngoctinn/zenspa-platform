---
phase: design
title: Thiết Kế - feature-customer-notifications
description: Kiến trúc và quyết định thiết kế cho trang thông báo
---

# Thiết Kế

## Kiến Trúc Hệ Thống

- Component: NotificationsPage với filter tabs
- Data: Supabase 'notifications'
- UI: List với unread indicators

## Quyết Định Thiết Kế

- Badge cho unread count
- Actions: Mark read, Delete

## Sơ Đồ

```mermaid
graph TD
    A[NotificationsPage] --> B[Tabs: All/Unread]
    B --> C[NotificationItem]
    C --> D[Title, Message, Date]
    C --> E[Badge: Unread]
    C --> F[Actions: Mark Read/Delete]
```
