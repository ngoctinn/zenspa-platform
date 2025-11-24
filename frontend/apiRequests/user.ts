import { UpdateUserProfileData, UserProfile } from "@/lib/types";

export const getUserProfile = async (): Promise<UserProfile> => {
  const response = await fetch("http://localhost:8000/api/v1/users/me", {
    credentials: "include", // Send cookies with request
  });

  if (!response.ok) {
    throw new Error("Failed to fetch user profile");
  }

  return response.json();
};

export const updateUserProfile = async (
  data: UpdateUserProfileData
): Promise<UserProfile> => {
  const response = await fetch("http://localhost:8000/api/v1/users/me", {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include", // Send cookies with request
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error("Failed to update user profile");
  }

  return response.json();
};
