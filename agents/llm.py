from dataclasses import dataclass
from typing import Optional, Dict, Any
from openai import AsyncOpenAI
from openai import AsyncAzureOpenAI
from google import genai
from anthropic import AsyncAnthropic
from ollama import AsyncClient
from enum import Enum
try:
    import openai
except ImportError:
    openai = None

try:
    import google.generativeai as genai
except ImportError:
    genai = None

try:
    import anthropic
except ImportError:
    anthropic = None

try:
    import ollama
except ImportError:
    ollama = None

class LLMProvider(Enum):
    """Supported LLM providers"""
    OPENAI = "openai"
    GEMINI = "gemini"
    CLAUDE = "claude"
    OLLAMA = "ollama"
    AZURE_OPENAI = "azure_openai"

@dataclass
class LLMConfig:
    """Configuration for LLM providers"""
    provider: LLMProvider
    model: str
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    timeout: int = 30
    extra_params: Optional[Dict[str, Any]] = None

@dataclass
class LLMConfig:
    """Configuration for LLM providers"""
    provider: LLMProvider
    model: str
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    timeout: int = 30
    extra_params: Optional[Dict[str, Any]] = None

class LLMClient:
    """Unified LLM client supporting multiple providers"""
    
    def __init__(self, config: LLMConfig):
        self.config = config
        self._client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the appropriate LLM client based on provider"""
        if self.config.provider == LLMProvider.OPENAI:
            if not openai:
                raise ImportError("OpenAI library not installed. Run: pip install openai")
            self._client = openai.AsyncOpenAI(
                api_key=self.config.api_key,
                base_url=self.config.base_url,
                timeout=self.config.timeout
            )
        
        elif self.config.provider == LLMProvider.AZURE_OPENAI:
            if not openai:
                raise ImportError("OpenAI library not installed. Run: pip install openai")
            self._client = openai.AsyncAzureOpenAI(
                api_key=self.config.api_key,
                azure_endpoint=self.config.base_url,
                api_version="2024-02-01",
                timeout=self.config.timeout
            )
        
        elif self.config.provider == LLMProvider.GEMINI:
            if not genai:
                raise ImportError("Google AI library not installed. Run: pip install google-generativeai")
            genai.configure(api_key=self.config.api_key)
            self._client = genai.GenerativeModel(self.config.model)
        
        elif self.config.provider == LLMProvider.CLAUDE:
            if not anthropic:
                raise ImportError("Anthropic library not installed. Run: pip install anthropic")
            self._client = anthropic.AsyncAnthropic(
                api_key=self.config.api_key,
                timeout=self.config.timeout
            )
        
        elif self.config.provider == LLMProvider.OLLAMA:
            if not ollama:
                raise ImportError("Ollama library not installed. Run: pip install ollama")
            self._client = ollama.AsyncClient(
                host=self.config.base_url or "http://localhost:11434"
            )
    
    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate response from LLM"""
        try:
            if self.config.provider == LLMProvider.OPENAI:
                return await self._generate_openai(prompt, system_prompt)
            elif self.config.provider == LLMProvider.AZURE_OPENAI:
                return await self._generate_azure_openai(prompt, system_prompt)
            elif self.config.provider == LLMProvider.GEMINI:
                return await self._generate_gemini(prompt, system_prompt)
            elif self.config.provider == LLMProvider.CLAUDE:
                return await self._generate_claude(prompt, system_prompt)
            elif self.config.provider == LLMProvider.OLLAMA:
                return await self._generate_ollama(prompt, system_prompt)
            else:
                raise ValueError(f"Unsupported provider: {self.config.provider}")
        
        except Exception as e:
            raise Exception(f"LLM generation failed for {self.config.provider}: {str(e)}")
    
    async def _generate_openai(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = await self._client.chat.completions.create(
            model=self.config.model,
            messages=messages,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            **(self.config.extra_params or {})
        )
        return response.choices[0].message.content
    
    async def _generate_azure_openai(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        return await self._generate_openai(prompt, system_prompt)  # Same API
    
    async def _generate_gemini(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\nUser: {prompt}"
        
        # Gemini async generation
        response = await self._client.generate_content_async(
            full_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=self.config.temperature,
                max_output_tokens=self.config.max_tokens,
                **(self.config.extra_params or {})
            )
        )
        return response.text
    
    async def _generate_claude(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        kwargs = {
            "model": self.config.model,
            "max_tokens": self.config.max_tokens or 1024,
            "temperature": self.config.temperature,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        if system_prompt:
            kwargs["system"] = system_prompt
        
        if self.config.extra_params:
            kwargs.update(self.config.extra_params)
        
        response = await self._client.messages.create(**kwargs)
        return response.content[0].text
    
    async def _generate_ollama(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\nUser: {prompt}"
        
        response = await self._client.generate(
            model=self.config.model,
            prompt=full_prompt,
            options={
                "temperature": self.config.temperature,
                "num_predict": self.config.max_tokens,
                **(self.config.extra_params or {})
            }
        )
        return response['response']


# Example usage configurations for different LLM providers
def create_openai_config(api_key: str, model: str = "gpt-4") -> LLMConfig:
    return LLMConfig(
        provider=LLMProvider.OPENAI,
        model=model,
        api_key=api_key,
        temperature=0.7,
        max_tokens=1000
    )

def create_gemini_config(api_key: str, model: str = "gemini-pro") -> LLMConfig:
    return LLMConfig(
        provider=LLMProvider.GEMINI,
        model=model,
        api_key=api_key,
        temperature=0.7,
        max_tokens=1000
    )

def create_claude_config(api_key: str, model: str = "claude-3-sonnet-20240229") -> LLMConfig:
    return LLMConfig(
        provider=LLMProvider.CLAUDE,
        model=model,
        api_key=api_key,
        temperature=0.7,
        max_tokens=1000
    )

def create_ollama_config(model: str = "llama2", base_url: str = "http://localhost:11434") -> LLMConfig:
    return LLMConfig(
        provider=LLMProvider.OLLAMA,
        model=model,
        base_url=base_url,
        temperature=0.7,
        max_tokens=1000
    )

def create_azure_openai_config(api_key: str, azure_endpoint: str, model: str = "gpt-4") -> LLMConfig:
    return LLMConfig(
        provider=LLMProvider.AZURE_OPENAI,
        model=model,
        api_key=api_key,
        base_url=azure_endpoint,
        temperature=0.7,
        max_tokens=1000
    )