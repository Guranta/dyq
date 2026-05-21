"use client";

import { useEffect, useState } from "react";
import {
  estimateGeneration,
  generateImage,
  generateVideo,
  getTask,
  type EstimateResponse,
  type GeneratedAsset,
  type GenerationMode,
  type GenerationType,
  type TaskStatus,
} from "@/lib/api";
import { GenerationResult } from "./GenerationResult";

type Props = {
  type: GenerationType;
  defaultPrompt: string;
};

export function GenerationForm({ type, defaultPrompt }: Props) {
  const mode: GenerationMode = type === "image" ? "text_to_image" : "text_to_video";
  const [prompt, setPrompt] = useState(defaultPrompt);
  const [duration, setDuration] = useState(5);
  const [estimate, setEstimate] = useState<EstimateResponse | null>(null);
  const [taskId, setTaskId] = useState<string | null>(null);
  const [status, setStatus] = useState<TaskStatus | null>(null);
  const [progress, setProgress] = useState(0);
  const [results, setResults] = useState<GeneratedAsset[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    let ignore = false;
    estimateGeneration({ type, mode, count: 1, duration })
      .then((data) => {
        if (!ignore) setEstimate(data);
      })
      .catch((err: Error) => {
        if (!ignore) setError(err.message);
      });
    return () => {
      ignore = true;
    };
  }, [duration, mode, type]);

  useEffect(() => {
    if (!taskId || status === "completed" || status === "failed") return;
    const timer = window.setInterval(async () => {
      try {
        const task = await getTask(taskId);
        setStatus(task.status);
        setProgress(task.progress);
        setResults(task.results);
        setError(task.error ?? null);
      } catch (err) {
        setError(err instanceof Error ? err.message : "任务查询失败");
      }
    }, 1500);
    return () => window.clearInterval(timer);
  }, [status, taskId]);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitting(true);
    setError(null);
    setResults([]);
    setTaskId(null);
    try {
      const response =
        type === "image"
          ? await generateImage({ prompt, mode, count: 1, ratio: "1:1", resolution: "1024x1024" })
          : await generateVideo({ prompt, mode, duration, ratio: "9:16", resolution: "720p" });
      setTaskId(response.task_id);
      setStatus(response.status);
      setProgress(response.status === "completed" ? 100 : 10);
      setResults(response.results);
      setError(response.error ?? null);
    } catch (err) {
      setStatus("failed");
      setError(err instanceof Error ? err.message : "生成失败");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_0.9fr]">
      <form onSubmit={handleSubmit} className="rounded-3xl border border-white/10 bg-white/[0.05] p-6 shadow-2xl shadow-black/20">
        <label className="block text-sm font-medium text-slate-200" htmlFor="prompt">
          描述你的创意
        </label>
        <textarea
          id="prompt"
          className="mt-3 min-h-44 w-full rounded-2xl border border-white/10 bg-black/30 p-4 text-base text-white outline-none ring-0 placeholder:text-slate-500 focus:border-indigo-300"
          value={prompt}
          onChange={(event) => setPrompt(event.target.value)}
          placeholder="例如：一只橘猫在雨夜东京街头慢慢行走，电影感，霓虹灯反射"
        />
        {type === "video" ? (
          <div className="mt-5">
            <label className="text-sm text-slate-300" htmlFor="duration">
              视频时长：{duration}s
            </label>
            <input
              id="duration"
              className="mt-2 w-full accent-indigo-400"
              max={10}
              min={3}
              onChange={(event) => setDuration(Number(event.target.value))}
              type="range"
              value={duration}
            />
          </div>
        ) : null}
        <div className="mt-5 rounded-2xl border border-white/10 bg-black/20 p-4 text-sm text-slate-300">
          {estimate ? (
            <div className="grid gap-2 sm:grid-cols-2">
              <span>预计消耗：{estimate.cost} 积分</span>
              <span>预计时间：{estimate.estimated_time_seconds}s</span>
              <span>供应商：{estimate.selected_provider}</span>
              <span>模型：{estimate.selected_model}</span>
            </div>
          ) : (
            "正在估算成本..."
          )}
        </div>
        <button
          className="mt-5 w-full rounded-2xl bg-indigo-400 px-5 py-3 font-semibold text-slate-950 transition hover:bg-indigo-300 disabled:cursor-not-allowed disabled:opacity-60"
          disabled={submitting || prompt.trim().length === 0}
          type="submit"
        >
          {submitting ? "正在提交..." : type === "image" ? "生成图片" : "生成视频"}
        </button>
      </form>
      <GenerationResult error={error} progress={progress} results={results} status={status} />
    </div>
  );
}
