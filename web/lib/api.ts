export type GenerationType = "image" | "video";
export type GenerationMode = "text_to_image" | "image_to_image" | "text_to_video" | "image_to_video";
export type TaskStatus = "pending" | "processing" | "completed" | "failed";

export type EstimateResponse = {
  cost: number;
  estimated_time_seconds: number;
  selected_provider: string;
  selected_model: string;
};

export type GeneratedAsset = {
  id: string;
  type: GenerationType;
  url: string;
  mime_type: string;
};

export type GenerateResponse = {
  task_id: string;
  status: TaskStatus;
  cost: number;
  provider: string;
  model: string;
  poll_url: string;
  results: GeneratedAsset[];
  error?: string | null;
};

export type TaskResponse = {
  id: string;
  status: TaskStatus;
  type: GenerationType;
  mode: GenerationMode;
  progress: number;
  provider: string;
  model: string;
  results: GeneratedAsset[];
  cost: number;
  error?: string | null;
};

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...init?.headers,
    },
  });

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || `Request failed with ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export function assetUrl(path: string): string {
  if (path.startsWith("http://") || path.startsWith("https://")) return path;
  return `${API_BASE_URL}${path}`;
}

export function getHealth(): Promise<{ status: string }> {
  return apiFetch("/api/v1/health", { cache: "no-store" });
}

export function estimateGeneration(input: {
  type: GenerationType;
  mode: GenerationMode;
  count?: number;
  duration?: number;
}): Promise<EstimateResponse> {
  return apiFetch("/api/v1/generate/estimate", {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export function generateImage(input: { prompt: string; mode: GenerationMode; count?: number; ratio?: string; resolution?: string }) {
  return apiFetch<GenerateResponse>("/api/v1/generate/image", {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export function generateVideo(input: { prompt: string; mode: GenerationMode; duration?: number; ratio?: string; resolution?: string }) {
  return apiFetch<GenerateResponse>("/api/v1/generate/video", {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export function getTask(taskId: string): Promise<TaskResponse> {
  return apiFetch(`/api/v1/tasks/${taskId}`, { cache: "no-store" });
}
