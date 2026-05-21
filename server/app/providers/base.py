from abc import ABC, abstractmethod

from app.models.generate import GenerationMode, GenerationType, GenerateRequest, TaskRecord


class BaseProvider(ABC):
    name: str
    display_name: str
    priority: int = 100
    capabilities: set[GenerationMode] = set()

    def supports(self, generation_type: GenerationType, mode: GenerationMode) -> bool:
        if generation_type == GenerationType.image:
            return mode in {GenerationMode.text_to_image, GenerationMode.image_to_image} and mode in self.capabilities
        if generation_type == GenerationType.video:
            return mode in {GenerationMode.text_to_video, GenerationMode.image_to_video} and mode in self.capabilities
        return False

    def public_info(self) -> dict[str, object]:
        return {
            "name": self.name,
            "display_name": self.display_name,
            "priority": self.priority,
            "capabilities": sorted(self.capabilities),
        }

    def model_for(self, generation_type: GenerationType) -> str:
        return generation_type.value

    def estimated_time_seconds(self, generation_type: GenerationType) -> int:
        return 5 if generation_type == GenerationType.image else 60

    @abstractmethod
    async def generate_image(self, request: GenerateRequest, cost: int) -> TaskRecord:
        raise NotImplementedError

    @abstractmethod
    async def generate_video(self, request: GenerateRequest, cost: int) -> TaskRecord:
        raise NotImplementedError
