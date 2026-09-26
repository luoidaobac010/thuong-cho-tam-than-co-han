"""
config.py
Cấu hình LLM cho CoThuong-AI.
Mặc định gọi qua Antigravity CLI (`agy`), fallback Google Gemini API.

Cấu hình qua biến môi trường hoặc file config.json:
    COTHUONG_PROVIDER=agy|gemini      (mặc định: agy)
    COTHUONG_MODEL=<model slug>       (agy: xem `agy models`)
    GEMINI_API_KEY=<your_key>         (chỉ cần cho provider gemini)
"""

from __future__ import annotations

import json
import os
import shutil
from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_MODELS = {
    "agy": "gemini-3.8-flash-medium",
    "gemini": "gemini-2.0-flash",
}


@dataclass
class LLMConfig:
    """Cấu hình cho LLM provider."""
    
    # Provider: "agy" (Antigravity CLI) hoặc "gemini" (API key)
    provider: str = "agy"
    
    # Model name, rỗng = default theo provider
    model: str = ""
    
    # API key (from env or config)
    api_key: str = ""
    
    # Generation parameters (agy không hỗ trợ temperature/top_p/max tokens)
    temperature: float = 0.3  # Thấp để output ổn định, nhất quán
    max_output_tokens: int = 8192
    top_p: float = 0.95
    
    # agy: thời gian chờ tối đa (--print-timeout)
    agy_timeout: str = "5m"
    
    # Safety settings — cho phép nội dung học thuật
    safety_settings: dict = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.model:
            self.model = DEFAULT_MODELS.get(self.provider, "")
        # Try to load API key from environment
        if not self.api_key:
            if self.provider == "gemini":
                self.api_key = os.environ.get("GEMINI_API_KEY", "")
    
    @classmethod
    def from_file(cls, config_path: Path) -> "LLMConfig":
        """Load config from JSON file."""
        with open(config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls(**data)
    
    def to_file(self, config_path: Path) -> None:
        """Save config to JSON file."""
        data = {
            "provider": self.provider,
            "model": self.model,
            "api_key": self.api_key,
            "temperature": self.temperature,
            "max_output_tokens": self.max_output_tokens,
            "top_p": self.top_p,
            "agy_timeout": self.agy_timeout,
        }
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def validate(self) -> None:
        """Kiểm tra config hợp lệ trước khi chạy."""
        if self.provider == "agy":
            if not shutil.which("agy"):
                raise ValueError(
                    "❌ Không tìm thấy lệnh `agy`!\n"
                    "   Cài: brew install --cask antigravity-cli\n"
                    "   Sau đó chạy `agy` 1 lần để đăng nhập Google."
                )
            return
        if self.provider != "gemini":
            raise ValueError(f"❌ Provider '{self.provider}' không hỗ trợ (dùng 'agy' hoặc 'gemini').")
        if not self.api_key:
            raise ValueError(
                f"❌ API key chưa được cấu hình!\n"
                f"   Cách 1: Set biến môi trường GEMINI_API_KEY\n"
                f"   Cách 2: Chạy: python solve.py --setup\n"
                f"   Cách 3: Sửa file config.json"
            )


def get_default_config_path() -> Path:
    """Trả về đường dẫn config.json mặc định."""
    return Path(__file__).resolve().parent.parent / "config.json"


def load_config(config_path: Path | None = None) -> LLMConfig:
    """
    Load config theo thứ tự ưu tiên:
    1. File config_path (nếu có)
    2. File config.json trong project
    3. Biến môi trường
    4. Giá trị mặc định
    """
    if config_path and config_path.exists():
        config = LLMConfig.from_file(config_path)
    elif get_default_config_path().exists():
        config = LLMConfig.from_file(get_default_config_path())
    else:
        config = LLMConfig()
    
    # Override with env vars if present.
    # Đổi provider thì reset model về default của provider mới.
    env_provider = os.environ.get("COTHUONG_PROVIDER", "")
    if env_provider and env_provider != config.provider:
        config.provider = env_provider
        config.model = DEFAULT_MODELS.get(env_provider, "")
    
    env_key = os.environ.get("GEMINI_API_KEY", "")
    if env_key:
        config.api_key = env_key
    
    env_model = os.environ.get("COTHUONG_MODEL", "")
    if env_model:
        config.model = env_model
    
    return config
