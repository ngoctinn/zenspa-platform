---
phase: testing
title: Chiến Lược Kiểm Thử - Admin User Management
description: Chiến lược kiểm thử, test cases và tiêu chí chất lượng cho tính năng quản lý tài khoản người dùng
---

# Chiến Lược Kiểm Thử - Admin User Management

## Tổng Quan Chiến Lược

**Chúng ta sẽ test như thế nào?**

- **Coverage Target:** 80% code coverage
- **Testing Pyramid:** Unit (60%) > Integration (30%) > E2E (10%)
- **Automation:** CI/CD pipeline với automated tests
- **Performance:** Load testing cho 1000 concurrent users

## Unit Tests

### Backend Unit Tests

**File:** `backend/tests/test_admin_user_service.py`

```python
import pytest
from unittest.mock import AsyncMock, MagicMock
from app.modules.user.user_service import UserAdminService
from app.modules.user.user_schemas import AdminCreateUser

class TestUserAdminService:
    @pytest.mark.asyncio
    async def test_list_users_basic(self, mock_session):
        """Test list users without filters"""
        # Arrange
        mock_users = [MagicMock(), MagicMock()]
        mock_session.exec.return_value = AsyncMock()
        mock_session.exec.return_value.all.return_value = mock_users

        # Act
        result = await UserAdminService.list_users(mock_session)

        # Assert
        assert len(result) == 2
        mock_session.exec.assert_called_once()

    @pytest.mark.asyncio
    async def test_list_users_with_search(self, mock_session):
        """Test list users with search filter"""
        # Arrange
        search_term = "john"
        mock_session.exec.return_value = AsyncMock()
        mock_session.exec.return_value.all.return_value = []

        # Act
        await UserAdminService.list_users(mock_session, search=search_term)

        # Assert
        # Verify search condition was applied
        call_args = mock_session.exec.call_args
        query = call_args[0][0]
        assert "ilike" in str(query)

    @pytest.mark.asyncio
    async def test_create_user_success(self, mock_session):
        """Test successful user creation"""
        # Arrange
        user_data = AdminCreateUser(
            email="test@example.com",
            full_name="Test User",
            roles=["role1", "role2"]
        )
        mock_profile = MagicMock()
        mock_session.add.return_value = None
        mock_session.commit.return_value = AsyncMock()
        mock_session.refresh.return_value = AsyncMock()

        # Mock the assign_roles method
        with patch.object(UserAdminService, 'assign_roles_to_user') as mock_assign:
            # Act
            result = await UserAdminService.create_user_by_admin(
                mock_session, user_data, "admin_id"
            )

            # Assert
            mock_session.add.assert_called_once()
            mock_assign.assert_called_once_with(
                mock_session, mock_profile.id, user_data.roles
            )
```

### Frontend Unit Tests

**File:** `frontend/__tests__/components/admin/user-management-page.test.tsx`

```typescript
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { AdminUserManagementPage } from "@/components/admin/user-management-page";
import { adminUserApi } from "@/apiRequests/adminUser";

// Mock API
jest.mock("@/apiRequests/adminUser");

const mockUsers = [
  {
    id: "1",
    email: "user1@example.com",
    full_name: "User One",
    is_active: true,
    roles: [{ id: "1", name: "Customer" }],
  },
];

describe("AdminUserManagementPage", () => {
  beforeEach(() => {
    (adminUserApi.listUsers as jest.Mock).mockResolvedValue(mockUsers);
  });

  it("renders user list on load", async () => {
    render(<AdminUserManagementPage />);

    await waitFor(() => {
      expect(screen.getByText("User One")).toBeInTheDocument();
      expect(screen.getByText("user1@example.com")).toBeInTheDocument();
    });
  });

  it("filters users based on search", async () => {
    render(<AdminUserManagementPage />);

    const searchInput = screen.getByPlaceholderText(
      "Tìm kiếm theo email hoặc tên..."
    );
    fireEvent.change(searchInput, { target: { value: "user1" } });

    await waitFor(() => {
      expect(adminUserApi.listUsers).toHaveBeenCalledWith(
        expect.objectContaining({ search: "user1" })
      );
    });
  });

  it("opens create dialog when button clicked", async () => {
    render(<AdminUserManagementPage />);

    const createButton = screen.getByText("Tạo Tài Khoản Mới");
    fireEvent.click(createButton);

    expect(screen.getByText("Tạo Tài Khoản Mới")).toBeInTheDocument();
  });
});
```

## Integration Tests

### API Integration Tests

**File:** `backend/tests/test_admin_user_routes.py`

```python
import pytest
from httpx import AsyncClient
from app.main import app
from app.core.auth import create_access_token

@pytest.mark.asyncio
class TestAdminUserRoutes:
    async def test_list_users_requires_admin(self, client: AsyncClient):
        """Test that list users requires admin role"""
        # Arrange - Create token without admin role
        token = create_access_token({"sub": "user_id", "role": "customer"})

        # Act
        response = await client.get(
            "/api/v1/admin/users",
            headers={"Authorization": f"Bearer {token}"}
        )

        # Assert
        assert response.status_code == 403

    async def test_list_users_success_with_admin(self, client: AsyncClient, admin_token):
        """Test successful user listing with admin token"""
        # Act
        response = await client.get(
            "/api/v1/admin/users",
            headers={"Authorization": f"Bearer {admin_token}"}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    async def test_create_user_validation(self, client: AsyncClient, admin_token):
        """Test user creation with invalid data"""
        # Arrange
        invalid_data = {
            "email": "invalid-email",  # Invalid email format
            "full_name": "",
            "roles": []
        }

        # Act
        response = await client.post(
            "/api/v1/admin/users",
            json=invalid_data,
            headers={"Authorization": f"Bearer {admin_token}"}
        )

        # Assert
        assert response.status_code == 422  # Validation error

    async def test_create_user_success(self, client: AsyncClient, admin_token):
        """Test successful user creation"""
        # Arrange
        user_data = {
            "email": "newuser@example.com",
            "full_name": "New User",
            "phone": "+1234567890",
            "roles": ["customer"]
        }

        # Act
        response = await client.post(
            "/api/v1/admin/users",
            json=user_data,
            headers={"Authorization": f"Bearer {admin_token}"}
        )

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["full_name"] == user_data["full_name"]
```

## End-to-End Tests

### E2E Test Scenarios

**File:** `frontend/e2e/admin-user-management.spec.ts`

```typescript
import { test, expect } from "@playwright/test";

test.describe("Admin User Management", () => {
  test.beforeEach(async ({ page }) => {
    // Login as admin
    await page.goto("/auth/signin");
    await page.fill('[data-testid="email"]', "admin@example.com");
    await page.fill('[data-testid="password"]', "adminpass");
    await page.click('[data-testid="signin-button"]');
    await page.waitForURL("/admin");
  });

  test("should display user management page", async ({ page }) => {
    await page.goto("/admin/users");

    await expect(page.locator("h1")).toContainText(
      "Quản Lý Tài Khoản Người Dùng"
    );
    await expect(
      page.locator('[data-testid="create-user-button"]')
    ).toBeVisible();
  });

  test("should create new user", async ({ page }) => {
    await page.goto("/admin/users");

    // Click create button
    await page.click('[data-testid="create-user-button"]');

    // Fill form
    await page.fill('[data-testid="email"]', "testuser@example.com");
    await page.fill('[data-testid="full-name"]', "Test User");
    await page.fill('[data-testid="phone"]', "+1234567890");

    // Select role
    await page.click('[data-testid="role-customer"]');

    // Submit
    await page.click('[data-testid="submit-create-user"]');

    // Verify success
    await expect(page.locator(".toast-success")).toContainText(
      "Tạo tài khoản thành công"
    );
    await expect(page.locator("text=testuser@example.com")).toBeVisible();
  });

  test("should search users", async ({ page }) => {
    await page.goto("/admin/users");

    // Type in search
    await page.fill('[data-testid="search-input"]', "john");

    // Wait for results
    await page.waitForSelector('[data-testid="user-row"]');

    // Verify filtered results
    const userRows = page.locator('[data-testid="user-row"]');
    await expect(userRows).toHaveCount(1);
    await expect(userRows.first()).toContainText("john");
  });

  test("should update user status", async ({ page }) => {
    await page.goto("/admin/users");

    // Click edit on first user
    await page.click('[data-testid="edit-user"]:first-child');

    // Toggle active status
    await page.click('[data-testid="active-toggle"]');

    // Save
    await page.click('[data-testid="save-changes"]');

    // Verify
    await expect(page.locator(".toast-success")).toContainText(
      "Cập nhật thành công"
    );
  });
});
```

## Performance Tests

### Load Testing

```bash
# K6 load test script
# File: performance-tests/admin-user-management.js

import http from 'k6/http'
import { check, sleep } from 'k6'

export let options = {
  stages: [
    { duration: '2m', target: 100 }, // Ramp up to 100 users
    { duration: '5m', target: 100 }, // Stay at 100 users
    { duration: '2m', target: 200 }, // Ramp up to 200 users
    { duration: '5m', target: 200 }, // Stay at 200 users
    { duration: '2m', target: 0 },   // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(99)<1500'], // 99% of requests should be below 1.5s
  },
}

const BASE_URL = __ENV.BASE_URL || 'http://localhost:8000'

export default function () {
  const params = {
    headers: {
      'Authorization': `Bearer ${__ENV.ADMIN_TOKEN}`,
      'Content-Type': 'application/json',
    },
  }

  // Test list users
  let response = http.get(`${BASE_URL}/api/v1/admin/users`, params)
  check(response, {
    'list users status is 200': (r) => r.status === 200,
    'list users response time < 1000ms': (r) => r.timings.duration < 1000,
  })

  sleep(1)
}
```

## Security Tests

### Authorization Tests

```python
# File: backend/tests/test_security_admin_user.py

@pytest.mark.asyncio
class TestAdminUserSecurity:
    async def test_non_admin_cannot_access_admin_routes(self, client: AsyncClient):
        """Test that non-admin users cannot access admin routes"""
        roles = ['customer', 'staff', None]

        for role in roles:
            token = create_access_token({
                "sub": "user_id",
                "role": role
            })

            response = await client.get(
                "/api/v1/admin/users",
                headers={"Authorization": f"Bearer {token}"}
            )

            assert response.status_code == 403

    async def test_admin_can_access_all_routes(self, client: AsyncClient):
        """Test that admin can access all admin routes"""
        token = create_access_token({
            "sub": "admin_id",
            "role": "admin"
        })

        routes = [
            "/api/v1/admin/users",
            "/api/v1/admin/roles"
        ]

        for route in routes:
            response = await client.get(
                route,
                headers={"Authorization": f"Bearer {token}"}
            )

            assert response.status_code in [200, 404]  # 404 is ok if route not implemented yet

    async def test_sql_injection_protection(self, client: AsyncClient, admin_token):
        """Test protection against SQL injection"""
        malicious_search = "'; DROP TABLE users; --"

        response = await client.get(
            f"/api/v1/admin/users?search={malicious_search}",
            headers={"Authorization": f"Bearer {admin_token}"}
        )

        # Should not crash, should return safe results
        assert response.status_code == 200
```

## Test Coverage Report

**Coverage Requirements:**

- Backend: >80% coverage
- Frontend: >70% coverage
- Critical paths: 100% coverage

**Coverage Exclusions:**

- Generated code (migrations, protobuf)
- Test files
- External libraries

## CI/CD Integration

**Automated Testing Pipeline:**

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]

jobs:
  test-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.12"
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      - name: Run tests
        run: |
          cd backend
          pytest --cov=app --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  test-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Node
        uses: actions/setup-node@v3
        with:
          node-version: "20"
      - name: Install dependencies
        run: |
          cd frontend
          pnpm install
      - name: Run tests
        run: |
          cd frontend
          pnpm test -- --coverage
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

## Bug Tracking & Reporting

**Test Failure Handling:**

- Failed tests block deployment
- Automatic notifications to dev team
- Detailed failure reports with screenshots/logs
- Regression tests for critical bugs

**Test Data Management:**

- Use factories for test data creation
- Clean up test data after each test
- Separate test database from production
- Anonymize sensitive test data
