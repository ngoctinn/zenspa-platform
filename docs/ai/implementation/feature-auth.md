---
phase: implementation
title: Hướng Dẫn Triển Khai
description: Ghi chú triển khai kỹ thuật, mẫu và hướng dẫn mã
---

# Hướng Dẫn Triển Khai

## Thiết Lập Phát Triển

**Chúng ta bắt đầu như thế nào?**

**Điều kiện tiên quyết:**

- Node.js 18+ và pnpm installed
- Supabase account và project created
- Python 3.12+ cho backend testing
- Git repository initialized

**Các bước setup môi trường:**

1. Clone repository: `git clone <repo-url>`
2. Install frontend deps: `cd frontend && pnpm install`
3. Setup environment variables (xem `.env.example`)
4. Start dev server: `pnpm dev`

**Cấu hình cần thiết:**

```bash
# .env.local
NEXT_PUBLIC_SUPABASE_URL=your-supabase-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-key
```

## Cấu Trúc Mã

**Mã được tổ chức như thế nào?**

```
frontend/
├── app/
│   ├── auth/                    # Auth pages
│   │   ├── login/
│   │   │   └── page.tsx
│   │   ├── register/
│   │   │   └── page.tsx
│   │   ├── forgot-password/
│   │   │   └── page.tsx
│   │   └── reset-password/
│   │       └── page.tsx
│   ├── globals.css
│   ├── layout.tsx
│   └── page.tsx
├── components/
│   ├── auth/                    # Auth components
│   │   ├── AuthLayout.tsx
│   │   ├── LoginForm.tsx
│   │   ├── RegisterForm.tsx
│   │   ├── ForgotPasswordForm.tsx
│   │   └── ResetPasswordForm.tsx
│   ├── common/                  # Shared components
│   └── ui/                      # Shadcn components
├── lib/
│   ├── auth/                    # Auth utilities
│   │   ├── supabase.ts
│   │   ├── auth-context.tsx
│   │   └── middleware.ts
│   └── utils.ts
└── middleware.ts                # Next.js middleware
```

**Quy ước đặt tên:**

- Components: PascalCase (LoginForm.tsx)
- Files: kebab-case (forgot-password.tsx)
- Functions: camelCase (handleSubmit)
- Constants: UPPER_SNAKE_CASE (SUPABASE_URL)

## Ghi Chú Triển Khai

**Chi tiết kỹ thuật chính cần nhớ:**

### Tính Năng Cốt Lõi

**Supabase Client Setup:**

```typescript
// lib/auth/supabase.ts
import { createBrowserClient, createServerClient } from "@supabase/ssr";
import { cookies } from "next/headers";

export function createClient() {
  const cookieStore = cookies();

  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll();
        },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value, options }) =>
            cookieStore.set(name, value, options)
          );
        },
      },
    }
  );
}
```

**Auth Context Implementation:**

```typescript
// lib/auth/auth-context.tsx
"use client";

import { createContext, useContext, useEffect, useState } from "react";
import { User } from "@supabase/supabase-js";
import { createBrowserClient } from "@supabase/ssr";

type AuthContextType = {
  user: User | null;
  loading: boolean;
  signOut: () => Promise<void>;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const supabase = createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  );

  useEffect(() => {
    const getUser = async () => {
      const {
        data: { user },
      } = await supabase.auth.getUser();
      setUser(user);
      setLoading(false);
    };

    getUser();

    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((event, session) => {
      setUser(session?.user ?? null);
      setLoading(false);
    });

    return () => subscription.unsubscribe();
  }, []);

  const signOut = async () => {
    await supabase.auth.signOut();
  };

  return (
    <AuthContext.Provider value={{ user, loading, signOut }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
```

**Form Validation với Zod:**

```typescript
// lib/auth/schemas.ts
import { z } from "zod";

export const loginSchema = z.object({
  email: z.string().email("Email không hợp lệ"),
  password: z.string().min(6, "Mật khẩu phải có ít nhất 6 ký tự"),
});

export const registerSchema = z
  .object({
    email: z.string().email("Email không hợp lệ"),
    password: z
      .string()
      .min(8, "Mật khẩu phải có ít nhất 8 ký tự")
      .regex(
        /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/,
        "Mật khẩu phải chứa chữ hoa, chữ thường và số"
      ),
    confirmPassword: z.string(),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: "Mật khẩu xác nhận không khớp",
    path: ["confirmPassword"],
  });

export const forgotPasswordSchema = z.object({
  email: z.string().email("Email không hợp lệ"),
});
```

**Login Form Component:**

```typescript
// components/auth/LoginForm.tsx
"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { createBrowserClient } from "@supabase/ssr";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { showToast } from "@/components/common/Toast";
import { loginSchema, type LoginFormData } from "@/lib/auth/schemas";

export function LoginForm() {
  const [loading, setLoading] = useState(false);
  const supabase = createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  );

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = async (data: LoginFormData) => {
    setLoading(true);
    try {
      const { error } = await supabase.auth.signInWithPassword({
        email: data.email,
        password: data.password,
      });

      if (error) {
        showToast({
          message: "Email hoặc mật khẩu không đúng",
          variant: "error",
        });
      } else {
        showToast({
          message: "Đăng nhập thành công!",
          variant: "success",
        });
        // Redirect sẽ được handle bởi middleware
      }
    } catch (error) {
      showToast({
        message: "Có lỗi xảy ra, vui lòng thử lại",
        variant: "error",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <Label htmlFor="email">Email</Label>
        <Input
          id="email"
          type="email"
          {...register("email")}
          placeholder="your@email.com"
        />
        {errors.email && (
          <p className="text-sm text-destructive mt-1">
            {errors.email.message}
          </p>
        )}
      </div>

      <div>
        <Label htmlFor="password">Mật khẩu</Label>
        <InputPassword
          id="password"
          {...register("password")}
          placeholder="••••••••"
        />
        {errors.password && (
          <p className="text-sm text-destructive mt-1">
            {errors.password.message}
          </p>
        )}
      </div>

      <Button type="submit" className="w-full" disabled={loading}>
        {loading ? "Đang đăng nhập..." : "Đăng nhập"}
      </Button>
    </form>
  );
}
```

### Mẫu & Thực Tiễn Tốt Nhất

**Error Handling Pattern:**

```typescript
// Centralized error handling
export function handleAuthError(error: AuthError) {
  switch (error.message) {
    case "Invalid login credentials":
      return "Email hoặc mật khẩu không đúng";
    case "Email not confirmed":
      return "Vui lòng xác nhận email trước khi đăng nhập";
    case "Too many requests":
      return "Quá nhiều lần thử, vui lòng đợi 1 phút";
    default:
      return "Có lỗi xảy ra, vui lòng thử lại";
  }
}
```

**Loading States:**

```typescript
// Consistent loading UI
{
  loading ? (
    <div className="flex items-center justify-center">
      <Loader2 className="h-4 w-4 animate-spin" />
      <span className="ml-2">Đang xử lý...</span>
    </div>
  ) : (
    <Button>Submit</Button>
  );
}
```

**Responsive Design:**

```typescript
// Mobile-first approach
<div className="max-w-md mx-auto px-4 sm:px-6 lg:px-8">
  <div className="bg-card p-6 rounded-lg shadow-sm">{/* Form content */}</div>
</div>
```

## Điểm Tích Hợp

**Các phần kết nối như thế nào?**

**Frontend ↔ Supabase:**

- Sử dụng @supabase/ssr cho server/client consistency
- Auth state được sync qua cookies
- Automatic token refresh

**Auth Context ↔ Components:**

- useAuth hook để access user state
- Components subscribe to auth changes
- Automatic re-renders khi auth state thay đổi

**Middleware ↔ Routing:**

```typescript
// middleware.ts
import { createServerClient } from "@supabase/ssr";
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export async function middleware(request: NextRequest) {
  const { supabase, response } = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return request.cookies.getAll();
        },
        setAll() {
          /* handle in response */
        },
      },
    }
  );

  const {
    data: { user },
  } = await supabase.auth.getUser();

  // Protected routes
  if (request.nextUrl.pathname.startsWith("/dashboard") && !user) {
    return NextResponse.redirect(new URL("/auth/login", request.url));
  }

  // Auth routes - redirect if already logged in
  if (request.nextUrl.pathname.startsWith("/auth") && user) {
    return NextResponse.redirect(new URL("/dashboard", request.url));
  }

  return response;
}

export const config = {
  matcher: ["/dashboard/:path*", "/auth/:path*"],
};
```

**Backend JWT Verification:**

```python
# app/core/auth.py
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer
import jwt
import httpx
import json

security = HTTPBearer()

async def get_current_user(token: str = Depends(security)):
    try:
        # Fetch Supabase public key (cache this in production)
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.supabase_url}/rest/v1/",
                headers={"apikey": settings.supabase_anon_key}
            )
            jwks = response.json()

        # Decode JWT
        header = jwt.get_unverified_header(token.credentials)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }

        payload = jwt.decode(
            token.credentials,
            rsa_key,
            algorithms=["RS256"],
            audience="authenticated"
        )

        return payload["sub"]  # user_id

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

## Xử Lý Lỗi

**Chúng ta xử lý thất bại như thế nào?**

**Network Errors:**

```typescript
try {
  const { data, error } = await supabase.auth.signUp(userData);
  if (error) throw error;
} catch (error) {
  if (error instanceof Error) {
    if (error.message.includes("network")) {
      showToast({
        message: "Lỗi kết nối, vui lòng kiểm tra internet",
        variant: "error",
      });
    } else {
      showToast({ message: handleAuthError(error), variant: "error" });
    }
  }
}
```

**Validation Errors:**

- Client-side: Zod validation với real-time feedback
- Server-side: Supabase error messages được translate sang tiếng Việt
- UI: Error states với clear messaging và focus management

**Auth State Errors:**

- Token expired: Auto refresh hoặc redirect to login
- Invalid session: Clear local state và redirect
- Concurrent login: Handle gracefully với user notification

## Cân Nhắc Hiệu Suất

**Chúng ta giữ tốc độ như thế nào?**

**Frontend Optimizations:**

- Lazy load auth components
- Debounce form validation (300ms)
- Optimistic UI updates
- Minimize re-renders với React.memo

**Auth Performance:**

- JWT cached in memory (no localStorage thrashing)
- Supabase CDN for global performance
- Minimal auth checks (only when needed)

**Bundle Size:**

- Tree shake unused Supabase features
- Dynamic imports cho auth pages
- Minimize dependencies

## Ghi Chú Bảo Mật

**Các biện pháp bảo mật nào đang được áp dụng?**

**Authentication:**

- JWT với RS256 signing (asymmetric encryption)
- Token expiration (1 hour default)
- Refresh token rotation
- Secure cookie settings (httpOnly, secure, sameSite)

**Input Validation:**

- Client-side validation với Zod
- Server-side validation trong Supabase
- Sanitize user inputs
- Rate limiting (Supabase built-in)

**Data Protection:**

- Passwords hashed với bcrypt
- Sensitive data encrypted at rest
- HTTPS only
- CORS properly configured

**Session Management:**

- Stateless JWT (no server-side sessions)
- Automatic logout on token expiry
- Secure logout (revoke refresh tokens)
- CSRF protection với sameSite cookies
