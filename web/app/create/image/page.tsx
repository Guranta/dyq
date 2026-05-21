import { GenerationForm } from "@/components/GenerationForm";

export default function ImageCreatePage() {
  return (
    <main className="mx-auto max-w-6xl px-6 pb-16 pt-8">
      <div className="mb-8">
        <p className="text-sm text-indigo-200">图片创作</p>
        <h1 className="mt-2 text-3xl font-semibold tracking-tight md:text-5xl">一句话生成图片</h1>
        <p className="mt-4 max-w-2xl text-slate-300">当前默认使用 Mock Provider 生成 SVG 占位图，真实供应商接入后会返回实际图片。</p>
      </div>
      <GenerationForm defaultPrompt="国风少女站在雨夜街头，霓虹灯反射在水面，电影感，细节丰富" type="image" />
    </main>
  );
}
