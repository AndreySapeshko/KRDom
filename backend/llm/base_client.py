from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseLLMClient(ABC):
    client_id: str

    @abstractmethod
    async def llm_complete_json(self, prompt: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError
