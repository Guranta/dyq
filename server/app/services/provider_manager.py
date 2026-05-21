from functools import lru_cache

from app.config import get_settings
from app.models.generate import GenerationMode, GenerationType, GenerateRequest, TaskRecord, TaskStatus
from app.providers import BaseProvider, MockProvider, OpenAICompatibleProvider


class ProviderManager:
    def __init__(self, providers: list[BaseProvider]):
        self.providers = sorted(providers, key=lambda provider: provider.priority)

    def select_provider(self, generation_type: GenerationType, mode: GenerationMode) -> BaseProvider | None:
        for provider in self.providers:
            if provider.supports(generation_type, mode):
                return provider
        return None

    def estimate_cost(self, generation_type: GenerationType, count: int = 1, duration: int = 5) -> int:
        if generation_type == GenerationType.image:
            return max(1, count)
        return max(5, duration * 4)

    async def generate_image(self, request: GenerateRequest) -> TaskRecord:
        return await self._generate(GenerationType.image, request)

    async def generate_video(self, request: GenerateRequest) -> TaskRecord:
        return await self._generate(GenerationType.video, request)

    async def _generate(self, generation_type: GenerationType, request: GenerateRequest) -> TaskRecord:
        provider = self.select_provider(generation_type, request.mode)
        if provider is None:
            return TaskRecord(
                id="task_unavailable",
                status=TaskStatus.failed,
                type=generation_type,
                mode=request.mode,
                prompt=request.prompt,
                provider="none",
                model="none",
                cost=0,
                progress=100,
                error="No provider supports this generation type",
            )
        cost = self.estimate_cost(generation_type, request.count, request.duration)
        if generation_type == GenerationType.image:
            return await provider.generate_image(request, cost)
        return await provider.generate_video(request, cost)


@lru_cache
def get_provider_manager() -> ProviderManager:
    settings = get_settings()
    providers: list[BaseProvider] = []
    if settings.ai_provider == "openai_compatible":
        providers.append(OpenAICompatibleProvider(settings))
    providers.append(MockProvider(settings))
    return ProviderManager(providers)
