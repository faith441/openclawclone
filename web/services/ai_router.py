"""
AI Router - Model-Agnostic AI Layer
Supports multiple AI providers: OpenAI, Anthropic, Google, Ollama, and more
"""
import os
import json
import httpx
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod


class AIProvider(Enum):
    """Supported AI Providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    OLLAMA = "ollama"
    GROQ = "groq"
    TOGETHER = "together"
    OPENROUTER = "openrouter"


@dataclass
class AIModel:
    """AI Model Configuration"""
    provider: AIProvider
    model_id: str
    name: str
    context_window: int
    cost_per_1k_input: float
    cost_per_1k_output: float
    supports_vision: bool = False
    supports_tools: bool = False
    is_local: bool = False


# Available Models Registry
MODELS = {
    # OpenAI Models
    "gpt-4o": AIModel(
        provider=AIProvider.OPENAI,
        model_id="gpt-4o",
        name="GPT-4o",
        context_window=128000,
        cost_per_1k_input=0.005,
        cost_per_1k_output=0.015,
        supports_vision=True,
        supports_tools=True
    ),
    "gpt-4o-mini": AIModel(
        provider=AIProvider.OPENAI,
        model_id="gpt-4o-mini",
        name="GPT-4o Mini",
        context_window=128000,
        cost_per_1k_input=0.00015,
        cost_per_1k_output=0.0006,
        supports_vision=True,
        supports_tools=True
    ),
    "gpt-4-turbo": AIModel(
        provider=AIProvider.OPENAI,
        model_id="gpt-4-turbo",
        name="GPT-4 Turbo",
        context_window=128000,
        cost_per_1k_input=0.01,
        cost_per_1k_output=0.03,
        supports_vision=True,
        supports_tools=True
    ),
    "gpt-3.5-turbo": AIModel(
        provider=AIProvider.OPENAI,
        model_id="gpt-3.5-turbo",
        name="GPT-3.5 Turbo",
        context_window=16385,
        cost_per_1k_input=0.0005,
        cost_per_1k_output=0.0015,
        supports_tools=True
    ),

    # Anthropic Models
    "claude-3-opus": AIModel(
        provider=AIProvider.ANTHROPIC,
        model_id="claude-3-opus-20240229",
        name="Claude 3 Opus",
        context_window=200000,
        cost_per_1k_input=0.015,
        cost_per_1k_output=0.075,
        supports_vision=True,
        supports_tools=True
    ),
    "claude-3-sonnet": AIModel(
        provider=AIProvider.ANTHROPIC,
        model_id="claude-3-5-sonnet-20241022",
        name="Claude 3.5 Sonnet",
        context_window=200000,
        cost_per_1k_input=0.003,
        cost_per_1k_output=0.015,
        supports_vision=True,
        supports_tools=True
    ),
    "claude-3-haiku": AIModel(
        provider=AIProvider.ANTHROPIC,
        model_id="claude-3-haiku-20240307",
        name="Claude 3 Haiku",
        context_window=200000,
        cost_per_1k_input=0.00025,
        cost_per_1k_output=0.00125,
        supports_vision=True,
        supports_tools=True
    ),

    # Google Models
    "gemini-1.5-pro": AIModel(
        provider=AIProvider.GOOGLE,
        model_id="gemini-1.5-pro",
        name="Gemini 1.5 Pro",
        context_window=1000000,
        cost_per_1k_input=0.00125,
        cost_per_1k_output=0.005,
        supports_vision=True,
        supports_tools=True
    ),
    "gemini-1.5-flash": AIModel(
        provider=AIProvider.GOOGLE,
        model_id="gemini-1.5-flash",
        name="Gemini 1.5 Flash",
        context_window=1000000,
        cost_per_1k_input=0.000075,
        cost_per_1k_output=0.0003,
        supports_vision=True,
        supports_tools=True
    ),

    # Groq Models (Fast inference)
    "llama-3.1-70b": AIModel(
        provider=AIProvider.GROQ,
        model_id="llama-3.1-70b-versatile",
        name="Llama 3.1 70B",
        context_window=131072,
        cost_per_1k_input=0.00059,
        cost_per_1k_output=0.00079,
        supports_tools=True
    ),
    "mixtral-8x7b": AIModel(
        provider=AIProvider.GROQ,
        model_id="mixtral-8x7b-32768",
        name="Mixtral 8x7B",
        context_window=32768,
        cost_per_1k_input=0.00024,
        cost_per_1k_output=0.00024,
        supports_tools=True
    ),

    # Ollama (Local)
    "ollama-llama3": AIModel(
        provider=AIProvider.OLLAMA,
        model_id="llama3",
        name="Llama 3 (Local)",
        context_window=8192,
        cost_per_1k_input=0,
        cost_per_1k_output=0,
        is_local=True
    ),
    "ollama-mistral": AIModel(
        provider=AIProvider.OLLAMA,
        model_id="mistral",
        name="Mistral (Local)",
        context_window=8192,
        cost_per_1k_input=0,
        cost_per_1k_output=0,
        is_local=True
    ),
}


class BaseProvider(ABC):
    """Base class for AI providers"""

    @abstractmethod
    async def chat(
        self,
        messages: List[Dict],
        model: str,
        api_key: str,
        **kwargs
    ) -> Tuple[str, Dict]:
        """Send chat completion request"""
        pass

    @abstractmethod
    async def stream_chat(
        self,
        messages: List[Dict],
        model: str,
        api_key: str,
        **kwargs
    ):
        """Stream chat completion"""
        pass


class OpenAIProvider(BaseProvider):
    """OpenAI API Provider"""

    BASE_URL = "https://api.openai.com/v1"

    async def chat(
        self,
        messages: List[Dict],
        model: str,
        api_key: str,
        **kwargs
    ) -> Tuple[str, Dict]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "messages": messages,
                    **kwargs
                },
                timeout=120.0
            )
            data = response.json()

            if "error" in data:
                raise Exception(data["error"]["message"])

            content = data["choices"][0]["message"]["content"]
            usage = {
                "input_tokens": data["usage"]["prompt_tokens"],
                "output_tokens": data["usage"]["completion_tokens"],
                "total_tokens": data["usage"]["total_tokens"]
            }
            return content, usage

    async def stream_chat(self, messages, model, api_key, **kwargs):
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                f"{self.BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "messages": messages,
                    "stream": True,
                    **kwargs
                },
                timeout=120.0
            ) as response:
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = line[6:]
                        if data == "[DONE]":
                            break
                        chunk = json.loads(data)
                        if chunk["choices"][0]["delta"].get("content"):
                            yield chunk["choices"][0]["delta"]["content"]


class AnthropicProvider(BaseProvider):
    """Anthropic (Claude) API Provider"""

    BASE_URL = "https://api.anthropic.com/v1"

    async def chat(
        self,
        messages: List[Dict],
        model: str,
        api_key: str,
        **kwargs
    ) -> Tuple[str, Dict]:
        # Convert messages to Anthropic format
        system = ""
        anthropic_messages = []
        for msg in messages:
            if msg["role"] == "system":
                system = msg["content"]
            else:
                anthropic_messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.BASE_URL}/messages",
                headers={
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "max_tokens": kwargs.get("max_tokens", 4096),
                    "system": system,
                    "messages": anthropic_messages
                },
                timeout=120.0
            )
            data = response.json()

            if "error" in data:
                raise Exception(data["error"]["message"])

            content = data["content"][0]["text"]
            usage = {
                "input_tokens": data["usage"]["input_tokens"],
                "output_tokens": data["usage"]["output_tokens"],
                "total_tokens": data["usage"]["input_tokens"] + data["usage"]["output_tokens"]
            }
            return content, usage

    async def stream_chat(self, messages, model, api_key, **kwargs):
        system = ""
        anthropic_messages = []
        for msg in messages:
            if msg["role"] == "system":
                system = msg["content"]
            else:
                anthropic_messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })

        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                f"{self.BASE_URL}/messages",
                headers={
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "max_tokens": kwargs.get("max_tokens", 4096),
                    "system": system,
                    "messages": anthropic_messages,
                    "stream": True
                },
                timeout=120.0
            ) as response:
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = json.loads(line[6:])
                        if data["type"] == "content_block_delta":
                            yield data["delta"]["text"]


class GoogleProvider(BaseProvider):
    """Google (Gemini) API Provider"""

    BASE_URL = "https://generativelanguage.googleapis.com/v1beta"

    async def chat(
        self,
        messages: List[Dict],
        model: str,
        api_key: str,
        **kwargs
    ) -> Tuple[str, Dict]:
        # Convert to Gemini format
        gemini_contents = []
        for msg in messages:
            role = "user" if msg["role"] in ["user", "system"] else "model"
            gemini_contents.append({
                "role": role,
                "parts": [{"text": msg["content"]}]
            })

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.BASE_URL}/models/{model}:generateContent",
                params={"key": api_key},
                json={"contents": gemini_contents},
                timeout=120.0
            )
            data = response.json()

            if "error" in data:
                raise Exception(data["error"]["message"])

            content = data["candidates"][0]["content"]["parts"][0]["text"]
            usage = {
                "input_tokens": data.get("usageMetadata", {}).get("promptTokenCount", 0),
                "output_tokens": data.get("usageMetadata", {}).get("candidatesTokenCount", 0),
                "total_tokens": data.get("usageMetadata", {}).get("totalTokenCount", 0)
            }
            return content, usage

    async def stream_chat(self, messages, model, api_key, **kwargs):
        gemini_contents = []
        for msg in messages:
            role = "user" if msg["role"] in ["user", "system"] else "model"
            gemini_contents.append({
                "role": role,
                "parts": [{"text": msg["content"]}]
            })

        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                f"{self.BASE_URL}/models/{model}:streamGenerateContent",
                params={"key": api_key, "alt": "sse"},
                json={"contents": gemini_contents},
                timeout=120.0
            ) as response:
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = json.loads(line[6:])
                        if "candidates" in data:
                            text = data["candidates"][0]["content"]["parts"][0].get("text", "")
                            if text:
                                yield text


class OllamaProvider(BaseProvider):
    """Ollama (Local) Provider"""

    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url

    async def chat(
        self,
        messages: List[Dict],
        model: str,
        api_key: str = None,  # Not needed for local
        **kwargs
    ) -> Tuple[str, Dict]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": model,
                    "messages": messages,
                    "stream": False
                },
                timeout=300.0
            )
            data = response.json()

            content = data["message"]["content"]
            usage = {
                "input_tokens": data.get("prompt_eval_count", 0),
                "output_tokens": data.get("eval_count", 0),
                "total_tokens": data.get("prompt_eval_count", 0) + data.get("eval_count", 0)
            }
            return content, usage

    async def stream_chat(self, messages, model, api_key=None, **kwargs):
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                f"{self.base_url}/api/chat",
                json={
                    "model": model,
                    "messages": messages,
                    "stream": True
                },
                timeout=300.0
            ) as response:
                async for line in response.aiter_lines():
                    if line:
                        data = json.loads(line)
                        if data.get("message", {}).get("content"):
                            yield data["message"]["content"]


class GroqProvider(BaseProvider):
    """Groq (Fast inference) Provider"""

    BASE_URL = "https://api.groq.com/openai/v1"

    async def chat(
        self,
        messages: List[Dict],
        model: str,
        api_key: str,
        **kwargs
    ) -> Tuple[str, Dict]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "messages": messages,
                    **kwargs
                },
                timeout=60.0
            )
            data = response.json()

            if "error" in data:
                raise Exception(data["error"]["message"])

            content = data["choices"][0]["message"]["content"]
            usage = {
                "input_tokens": data["usage"]["prompt_tokens"],
                "output_tokens": data["usage"]["completion_tokens"],
                "total_tokens": data["usage"]["total_tokens"]
            }
            return content, usage

    async def stream_chat(self, messages, model, api_key, **kwargs):
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                f"{self.BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "messages": messages,
                    "stream": True,
                    **kwargs
                },
                timeout=60.0
            ) as response:
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = line[6:]
                        if data == "[DONE]":
                            break
                        chunk = json.loads(data)
                        if chunk["choices"][0]["delta"].get("content"):
                            yield chunk["choices"][0]["delta"]["content"]


class AIRouter:
    """
    Model-Agnostic AI Router
    Routes requests to the appropriate provider based on model selection
    """

    def __init__(self):
        self.providers = {
            AIProvider.OPENAI: OpenAIProvider(),
            AIProvider.ANTHROPIC: AnthropicProvider(),
            AIProvider.GOOGLE: GoogleProvider(),
            AIProvider.OLLAMA: OllamaProvider(),
            AIProvider.GROQ: GroqProvider(),
        }

    def get_models(self) -> List[Dict]:
        """Get list of available models"""
        return [
            {
                "id": model_id,
                "name": model.name,
                "provider": model.provider.value,
                "context_window": model.context_window,
                "cost_per_1k_input": model.cost_per_1k_input,
                "cost_per_1k_output": model.cost_per_1k_output,
                "supports_vision": model.supports_vision,
                "supports_tools": model.supports_tools,
                "is_local": model.is_local
            }
            for model_id, model in MODELS.items()
        ]

    def get_model(self, model_id: str) -> Optional[AIModel]:
        """Get model by ID"""
        return MODELS.get(model_id)

    async def chat(
        self,
        messages: List[Dict],
        model_id: str,
        api_keys: Dict[str, str],
        **kwargs
    ) -> Tuple[str, Dict, float]:
        """
        Send chat completion to the appropriate provider

        Args:
            messages: List of message dicts with 'role' and 'content'
            model_id: Model identifier (e.g., 'gpt-4o', 'claude-3-sonnet')
            api_keys: Dict of provider -> API key mappings

        Returns:
            Tuple of (response_content, usage_dict, cost)
        """
        model = MODELS.get(model_id)
        if not model:
            raise ValueError(f"Unknown model: {model_id}")

        provider = self.providers.get(model.provider)
        if not provider:
            raise ValueError(f"Unsupported provider: {model.provider}")

        # Get API key for provider
        api_key = api_keys.get(model.provider.value)
        if not api_key and not model.is_local:
            raise ValueError(f"No API key provided for {model.provider.value}")

        # Make request
        content, usage = await provider.chat(
            messages=messages,
            model=model.model_id,
            api_key=api_key,
            **kwargs
        )

        # Calculate cost
        cost = (
            (usage["input_tokens"] / 1000) * model.cost_per_1k_input +
            (usage["output_tokens"] / 1000) * model.cost_per_1k_output
        )

        return content, usage, cost

    async def stream_chat(
        self,
        messages: List[Dict],
        model_id: str,
        api_keys: Dict[str, str],
        **kwargs
    ):
        """Stream chat completion"""
        model = MODELS.get(model_id)
        if not model:
            raise ValueError(f"Unknown model: {model_id}")

        provider = self.providers.get(model.provider)
        if not provider:
            raise ValueError(f"Unsupported provider: {model.provider}")

        api_key = api_keys.get(model.provider.value)
        if not api_key and not model.is_local:
            raise ValueError(f"No API key provided for {model.provider.value}")

        async for chunk in provider.stream_chat(
            messages=messages,
            model=model.model_id,
            api_key=api_key,
            **kwargs
        ):
            yield chunk

    def select_best_model(
        self,
        task_type: str,
        api_keys: Dict[str, str],
        prefer_local: bool = False
    ) -> str:
        """
        Auto-select the best model based on task type and available API keys

        Args:
            task_type: 'simple', 'complex', 'creative', 'coding', 'vision'
            api_keys: Available API keys
            prefer_local: Prefer local models if available

        Returns:
            Model ID
        """
        available_providers = set(api_keys.keys())

        # Check for local models first if preferred
        if prefer_local:
            if AIProvider.OLLAMA.value in available_providers:
                return "ollama-llama3"

        # Task-based selection
        if task_type == "simple":
            # Cheap, fast models
            if AIProvider.GROQ.value in available_providers:
                return "mixtral-8x7b"
            if AIProvider.OPENAI.value in available_providers:
                return "gpt-4o-mini"
            if AIProvider.ANTHROPIC.value in available_providers:
                return "claude-3-haiku"

        elif task_type == "complex":
            # Most capable models
            if AIProvider.ANTHROPIC.value in available_providers:
                return "claude-3-sonnet"
            if AIProvider.OPENAI.value in available_providers:
                return "gpt-4o"
            if AIProvider.GOOGLE.value in available_providers:
                return "gemini-1.5-pro"

        elif task_type == "coding":
            # Best for code
            if AIProvider.ANTHROPIC.value in available_providers:
                return "claude-3-sonnet"
            if AIProvider.OPENAI.value in available_providers:
                return "gpt-4o"

        elif task_type == "vision":
            # Vision-capable models
            if AIProvider.OPENAI.value in available_providers:
                return "gpt-4o"
            if AIProvider.ANTHROPIC.value in available_providers:
                return "claude-3-sonnet"
            if AIProvider.GOOGLE.value in available_providers:
                return "gemini-1.5-pro"

        # Default fallback
        if AIProvider.OPENAI.value in available_providers:
            return "gpt-4o-mini"
        if AIProvider.ANTHROPIC.value in available_providers:
            return "claude-3-haiku"
        if AIProvider.GOOGLE.value in available_providers:
            return "gemini-1.5-flash"

        raise ValueError("No API keys available for any provider")


# Global router instance
router = AIRouter()


# Convenience functions
def get_available_models():
    """Get all available models"""
    return router.get_models()


async def chat(messages, model_id, api_keys, **kwargs):
    """Send chat completion"""
    return await router.chat(messages, model_id, api_keys, **kwargs)


async def stream_chat(messages, model_id, api_keys, **kwargs):
    """Stream chat completion"""
    async for chunk in router.stream_chat(messages, model_id, api_keys, **kwargs):
        yield chunk


def select_best_model(task_type, api_keys, prefer_local=False):
    """Auto-select best model for task"""
    return router.select_best_model(task_type, api_keys, prefer_local)
