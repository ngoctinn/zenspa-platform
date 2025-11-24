"use client";

import { AdminUserProfile, Role } from "@/apiRequests/adminUser";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Loader2 } from "lucide-react";
import { useEffect, useState } from "react";

interface RoleAssignmentDialogProps {
  user: AdminUserProfile | null;
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onSubmit: (userId: string, roleIds: string[]) => Promise<void>;
  availableRoles: Role[];
}

export function RoleAssignmentDialog({
  user,
  open,
  onOpenChange,
  onSubmit,
  availableRoles,
}: RoleAssignmentDialogProps) {
  const [selectedRoles, setSelectedRoles] = useState<string[]>([]);
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    if (user) {
      setSelectedRoles(user.roles.map((r) => r.id));
    }
  }, [user]);

  const handleRoleToggle = (roleId: string) => {
    setSelectedRoles((prev) =>
      prev.includes(roleId)
        ? prev.filter((id) => id !== roleId)
        : [...prev, roleId]
    );
  };

  const handleSubmit = async () => {
    if (!user) return;

    setIsSubmitting(true);
    try {
      await onSubmit(user.id, selectedRoles);
      onOpenChange(false);
    } catch (error) {
      console.error(error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Phân Quyền Người Dùng</DialogTitle>
          <DialogDescription>
            Gán vai trò cho tài khoản {user?.email}
          </DialogDescription>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          {availableRoles.map((role) => (
            <div key={role.id} className="flex items-center space-x-2">
              <Checkbox
                id={`role-${role.id}`}
                checked={selectedRoles.includes(role.id)}
                onCheckedChange={() => handleRoleToggle(role.id)}
              />
              <div className="grid gap-1.5 leading-none">
                <Label
                  htmlFor={`role-${role.id}`}
                  className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                >
                  {role.name}
                </Label>
                <p className="text-sm text-muted-foreground">
                  {role.description}
                </p>
              </div>
            </div>
          ))}
        </div>
        <DialogFooter>
          <Button onClick={handleSubmit} disabled={isSubmitting}>
            {isSubmitting && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
            Lưu phân quyền
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
