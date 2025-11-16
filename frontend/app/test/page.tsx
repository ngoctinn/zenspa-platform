"use client";

import { getUserProfile } from "@/apiRequests/user";
import { Button } from "@/components/ui/button";
import { useState } from "react";

export default function TestPage() {
  const [result, setResult] = useState<string>("");
  const [loading, setLoading] = useState(false);

  const handleTest = async () => {
    setLoading(true);
    setResult("");
    try {
      const profile = await getUserProfile();
      setResult(`Thành công: ${JSON.stringify(profile, null, 2)}`);
    } catch (error) {
      setResult(
        `Lỗi: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Test API getUserProfile</h1>
      <Button onClick={handleTest} disabled={loading}>
        {loading ? "Đang test..." : "Test API"}
      </Button>
      {result && (
        <pre className="mt-4 p-4 bg-gray-100 rounded border overflow-auto">
          {result}
        </pre>
      )}
    </div>
  );
}
