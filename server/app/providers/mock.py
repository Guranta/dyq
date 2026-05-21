from html import escape
from pathlib import Path
from uuid import uuid4

from app.config import Settings
from app.models.generate import GeneratedAsset, GenerationMode, GenerationType, GenerateRequest, TaskRecord, TaskStatus
from app.providers.base import BaseProvider


class MockProvider(BaseProvider):
    name = "mock"
    display_name = "Mock Provider"
    priority = 999
    capabilities = {
        GenerationMode.text_to_image,
        GenerationMode.image_to_image,
        GenerationMode.text_to_video,
        GenerationMode.image_to_video,
    }

    def __init__(self, settings: Settings):
        self.settings = settings

    def model_for(self, generation_type: GenerationType) -> str:
        return self.settings.ai_image_model if generation_type == GenerationType.image else self.settings.ai_video_model

    async def generate_image(self, request: GenerateRequest, cost: int) -> TaskRecord:
        task_id = f"task_{uuid4().hex}"
        file_path = self.settings.output_dir / f"{task_id}.svg"
        self._write_svg(file_path, request.prompt)
        return TaskRecord(
            id=task_id,
            status=TaskStatus.completed,
            type=GenerationType.image,
            mode=request.mode,
            prompt=request.prompt,
            provider=self.name,
            model=self.model_for(GenerationType.image),
            cost=cost,
            progress=100,
            results=[
                GeneratedAsset(
                    id=f"asset_{uuid4().hex}",
                    type=GenerationType.image,
                    url=f"/outputs/{file_path.name}",
                    mime_type="image/svg+xml",
                )
            ],
        )

    async def generate_video(self, request: GenerateRequest, cost: int) -> TaskRecord:
        task_id = f"task_{uuid4().hex}"
        file_path = self.settings.output_dir / f"{task_id}.txt"
        file_path.write_text(
            f"Mock video generation\nPrompt: {request.prompt}\nDuration: {request.duration}s\nRatio: {request.ratio}\n",
            encoding="utf-8",
        )
        return TaskRecord(
            id=task_id,
            status=TaskStatus.completed,
            type=GenerationType.video,
            mode=request.mode,
            prompt=request.prompt,
            provider=self.name,
            model=self.model_for(GenerationType.video),
            cost=cost,
            progress=100,
            results=[
                GeneratedAsset(
                    id=f"asset_{uuid4().hex}",
                    type=GenerationType.video,
                    url=f"/outputs/{file_path.name}",
                    mime_type="text/plain",
                )
            ],
        )

    def _write_svg(self, file_path: Path, prompt: str) -> None:
        safe_prompt = escape(prompt[:180])
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024">
  <defs>
    <linearGradient id="g" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0%" stop-color="#111827"/>
      <stop offset="55%" stop-color="#4f46e5"/>
      <stop offset="100%" stop-color="#ec4899"/>
    </linearGradient>
  </defs>
  <rect width="1024" height="1024" rx="64" fill="url(#g)"/>
  <text x="72" y="140" font-size="54" fill="white" font-family="Arial, sans-serif" font-weight="700">大云雀 Mock Image</text>
  <foreignObject x="72" y="220" width="880" height="620">
    <div xmlns="http://www.w3.org/1999/xhtml" style="font-family: Arial, sans-serif; color: white; font-size: 42px; line-height: 1.35; word-break: break-word;">
      {safe_prompt}
    </div>
  </foreignObject>
</svg>
"""
        file_path.write_text(svg, encoding="utf-8")
