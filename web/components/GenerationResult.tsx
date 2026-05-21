import { assetUrl, type GeneratedAsset, type TaskStatus } from "@/lib/api";

type Props = {
  status: TaskStatus | null;
  progress?: number;
  results: GeneratedAsset[];
  error?: string | null;
};

export function GenerationResult({ status, progress = 0, results, error }: Props) {
  if (!status) return null;

  return (
    <section className="rounded-3xl border border-white/10 bg-white/[0.04] p-5 shadow-2xl shadow-black/20">
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-lg font-semibold">生成结果</h2>
        <span className="rounded-full bg-white/10 px-3 py-1 text-xs text-slate-200">{status}</span>
      </div>
      {status !== "completed" ? (
        <div className="h-2 overflow-hidden rounded-full bg-white/10">
          <div className="h-full rounded-full bg-indigo-400 transition-all" style={{ width: `${progress}%` }} />
        </div>
      ) : null}
      {error ? <p className="mt-4 rounded-2xl bg-red-500/10 p-3 text-sm text-red-200">{error}</p> : null}
      <div className="mt-5 grid gap-4">
        {results.map((asset) => (
          <article key={asset.id} className="overflow-hidden rounded-2xl border border-white/10 bg-black/20">
            {asset.type === "image" ? (
              <img alt="生成图片" className="w-full" src={assetUrl(asset.url)} />
            ) : asset.mime_type.startsWith("video/") ? (
              <video className="w-full" controls src={assetUrl(asset.url)} />
            ) : (
              <div className="p-4 text-sm text-slate-300">
                Mock 视频结果已生成：
                <a className="ml-2 text-indigo-300 underline" href={assetUrl(asset.url)} target="_blank">
                  打开占位文件
                </a>
              </div>
            )}
          </article>
        ))}
      </div>
    </section>
  );
}
