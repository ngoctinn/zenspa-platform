"use client";

import { toast } from "sonner";

type ToastVariant = "info" | "success" | "warning" | "error";

interface ToastProps {
  message: string;
  variant?: ToastVariant;
}

// Utility function for showing toast
export const showToast = ({ message, variant = "info" }: ToastProps) => {
  const getToastStyle = (variant: ToastVariant) => {
    switch (variant) {
      case "success":
        return {
          "--normal-bg":
            "color-mix(in oklab, light-dark(var(--color-green-600), var(--color-green-400)) 10%, var(--background))",
          "--normal-text":
            "light-dark(var(--color-green-600), var(--color-green-400))",
          "--normal-border":
            "light-dark(var(--color-green-600), var(--color-green-400))",
        } as React.CSSProperties;
      case "warning":
        return {
          "--normal-bg":
            "color-mix(in oklab, light-dark(var(--color-amber-600), var(--color-amber-400)) 10%, var(--background))",
          "--normal-text":
            "light-dark(var(--color-amber-600), var(--color-amber-400))",
          "--normal-border":
            "light-dark(var(--color-amber-600), var(--color-amber-400))",
        } as React.CSSProperties;
      case "error":
        return {
          "--normal-bg":
            "color-mix(in oklab, var(--destructive) 10%, var(--background))",
          "--normal-text": "var(--destructive)",
          "--normal-border": "var(--destructive)",
        } as React.CSSProperties;
      case "info":
      default:
        return {
          "--normal-bg":
            "color-mix(in oklab, light-dark(var(--color-sky-600), var(--color-sky-400)) 10%, var(--background))",
          "--normal-text":
            "light-dark(var(--color-sky-600), var(--color-sky-400))",
          "--normal-border":
            "light-dark(var(--color-sky-600), var(--color-sky-400))",
        } as React.CSSProperties;
    }
  };

  const style = getToastStyle(variant);

  switch (variant) {
    case "success":
      toast.success(message, { style });
      break;
    case "warning":
      toast.warning(message, { style });
      break;
    case "error":
      toast.error(message, { style });
      break;
    case "info":
    default:
      toast.info(message, { style });
      break;
  }
};
