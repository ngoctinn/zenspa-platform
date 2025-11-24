import { createSupabaseBrowserClient } from "@/utils/supabaseClient";

const BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

type CustomOptions = Omit<RequestInit, "method" | "body"> & {
  baseUrl?: string | undefined;
  body?: unknown;
};

export const http = {
  request: async <T>(
    method: "GET" | "POST" | "PUT" | "DELETE" | "PATCH",
    url: string,
    options?: CustomOptions
  ): Promise<T> => {
    const body = options?.body ? JSON.stringify(options.body) : undefined;
    const baseHeaders: HeadersInit = {
      "Content-Type": "application/json",
    };

    // Get token from Supabase
    const supabase = createSupabaseBrowserClient();
    const { data } = await supabase.auth.getSession();
    if (data.session?.access_token) {
      baseHeaders["Authorization"] = `Bearer ${data.session.access_token}`;
    }

    const baseUrl = options?.baseUrl === undefined ? BASE_URL : options.baseUrl;
    const fullUrl = url.startsWith("/")
      ? `${baseUrl}${url}`
      : `${baseUrl}/${url}`;

    const res = await fetch(fullUrl, {
      ...options,
      headers: {
        ...baseHeaders,
        ...options?.headers,
      },
      body,
      method,
    });

    if (!res.ok) {
      // Handle errors
      const error = await res.json().catch(() => ({}));
      throw new Error(error.detail || error.message || "API request failed");
    }

    return res.json() as Promise<T>;
  },

  get: <T>(url: string, options?: CustomOptions) =>
    http.request<T>("GET", url, options),

  post: <T>(url: string, body: unknown, options?: CustomOptions) =>
    http.request<T>("POST", url, { ...options, body }),

  put: <T>(url: string, body: unknown, options?: CustomOptions) =>
    http.request<T>("PUT", url, { ...options, body }),

  delete: <T>(url: string, options?: CustomOptions) =>
    http.request<T>("DELETE", url, options),
};
