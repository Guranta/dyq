import { GenerationForm } from "@/components/GenerationForm";

export default function VideoCreatePage() {
  return (
    <main className="mx-auto max-w-6xl px-6 pb-16 pt-8">
      <div className="mb-8">
        <p className="text-sm text-pink-200">视频创作</p>
        <h1 className="mt-2 text-3xl font-semibold tracking-tight md:text-5xl">一句话生成视频</h1>
        <p className="mt-4 max-w-2xl text-slate-300">当前默认使用 Mock Provider 生成视频占位文件，真实供应商接入后会返回视频预览。</p>
      </div>
      <GenerationForm defaultPrompt="一只橘猫在雨夜东京街头慢慢行走，电影感，霓虹灯倒映在水洼里" type="video" />
    </main>
  );
}
