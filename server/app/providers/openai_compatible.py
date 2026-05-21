from uuid import uuid4

import httpx

from app.config import Settings
from app.models.generate import GeneratedAsset, GenerationMode, GenerationType, GenerateRequest, TaskRecord, TaskStatus
from app.providers.base import BaseProvider


class OpenAICompatibleProvider(BaseProvider):
    name = "openai_compatible"
    display_name = "OpenAI-compatible Provider"
    priority = 10
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
        return await self._post_generation(GenerationType.image, request, cost, self.settings.ai_image_path)

    async def generate_video(self, request: GenerateRequest, cost: int) -> TaskRecord:
        return await self._post_generation(GenerationType.video, request, cost, self.settings.ai_video_path)

    async def _post_generation(
        self,
        generation_type: GenerationType,
        request: GenerateRequest,
        cost: int,
        path: str,
    ) -> TaskRecord:
        if not self.settings.ai_base_url or not self.settings.ai_api_key:
            return self._failed_task(generation_type, request, cost, "AI_BASE_URL and AI_API_KEY are required")

        url = self.settings.ai_base_url.rstrip("/") + "/" + path.lstrip("/")
        payload = {
            "model": self.model_for(generation_type),
            "prompt": request.prompt,
            "n": request.count,
            "size": request.resolution,
            "duration": request.duration,
            "ratio": request.ratio,
        }
        headers = {"Authorization": f"Bearer {self.settings.ai_api_key}"}

        try:
            async with httpx.AsyncClient(timeout=120) as client:
                response = await client.post(url, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
        except Exception as exc:
            return self._failed_task(generation_type, request, cost, str(exc))

        task_id = f"task_{uuid4().hex}"
        urls = self._extract_urls(data)
        status = TaskStatus.completed if urls else TaskStatus.pending
        results = [
            GeneratedAsset(
                id=f"asset_{uuid4().hex}",
                type=generation_type,
                url=url,
                mime_type="image/*" if generation_type == GenerationType.image else "video/*",
            )
            for url in urls
        ]
        return TaskRecord(
            id=task_id,
            status=status,
            type=generation_type,
            mode=request.mode,
            prompt=request.prompt,
            provider=self.name,
            model=self.model_for(generation_type),
            cost=cost,
            progress=100 if status == TaskStatus.completed else 10,
            results=results,
            raw_response=data,
        )

    def _failed_task(self, generation_type: GenerationType, request: GenerateRequest, cost: int, error: str) -> TaskRecord:
        return TaskRecord(
            id=f"task_{uuid4().hex}",
            status=TaskStatus.failed,
            type=generation_type,
            mode=request.mode,
            prompt=request.prompt,
            provider=self.name,
            model=self.model_for(generation_type),
            cost=cost,
            progress=100,
            error=error,
        )

    def _extract_urls(self, data: dict) -> list[str]:
        if isinstance(data.get("url"), str):
            return [data["url"]]
        if isinstance(data.get("urls"), list):
            return [url for url in data["urls"] if isinstance(url, str)]
        items = data.get("data")
        if isinstance(items, list):
            urls: list[str] = []
            for item in items:
                if isinstance(item, dict) and isinstance(item.get("url"), str):
                    urls.append(item["url"])
            return urls
        return []
