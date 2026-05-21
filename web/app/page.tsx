import Link from "next/link";
import { getHealth } from "@/lib/api";

export default async function Home() {
  let health = "unknown";
  try {
    const response = await getHealth();
    health = response.status;
  } catch {
    health = "offline";
  }

  return (
    <main className="mx-auto max-w-6xl px-6 pb-16 pt-10">
      <section className="rounded-[2rem] border border-white/10 bg-white/[0.04] p-8 shadow-2xl shadow-black/20 md:p-12">
        <div className="mb-6 inline-flex rounded-full border border-white/10 bg-black/20 px-4 py-2 text-sm text-slate-300">
          后端状态：<span className="ml-1 text-indigo-200">{health}</span>
        </div>
        <h1 className="max-w-3xl text-4xl font-semibold tracking-tight md:text-6xl">
          今天想创作什么？
        </h1>
        <p className="mt-5 max-w-2xl text-lg leading-8 text-slate-300">
          先跑通最基础的 AI 生成闭环：输入一句话，调用后端 Provider，生成图片或视频任务，并查看结果。
        </p>
        <div className="mt-8 flex flex-col gap-3 sm:flex-row">
          <Link className="rounded-2xl bg-indigo-400 px-6 py-3 text-center font-semibold text-slate-950 hover:bg-indigo-300" href="/create/image">
            生成图片
          </Link>
          <Link className="rounded-2xl border border-white/10 bg-white/10 px-6 py-3 text-center font-semibold text-white hover:bg-white/15" href="/create/video">
            生成视频
          </Link>
        </div>
      </section>
      <section className="mt-8 grid gap-4 md:grid-cols-3">
        {["成本预估", "任务轮询", "Provider 适配"].map((title) => (
          <div key={title} className="rounded-3xl border border-white/10 bg-white/[0.04] p-5">
            <h2 className="font-semibold">{title}</h2>
            <p className="mt-2 text-sm leading-6 text-slate-400">MVP 已接入基础接口，后续会叠加登录、配额、项目保存和真实供应商配置。</p>
          </div>
        ))}
      </section>
    </main>
  );
}
