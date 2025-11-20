"use client";

import { toast } from "sonner";

type ToastVariant = "info" | "success" | "warning" | "error";

interface ToastProps {
  message: string;
  description?: string;
  variant?: ToastVariant;
}

// Utility function for showing toast
export const showToast = ({
  message,
  description,
  variant = "info",
}: ToastProps) => {
  switch (variant) {
    case "success":
      toast.success(message, { description });
      break;
    case "warning":
      toast.warning(message, { description });
      break;
    case "error":
      toast.error(message, { description });
      break;
    case "info":
    default:
      toast.info(message, { description });
      break;
  }
};

export { toast };
