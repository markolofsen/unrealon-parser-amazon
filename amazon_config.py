"""
Amazon Config - EXTENDS Driver AutoConfig

Proper extension of driver configuration with Amazon-specific settings.
"""

import os
from pathlib import Path
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from unrealon_driver.src.config.auto_config import AutoConfig
from unrealon_driver.src.dto.services import DriverBrowserConfig
from unrealon_driver.src.dto.execution import DaemonModeConfig
from unrealon_driver.src.dto.cli import ParserInstanceConfig


# Paths
THIS_DIR = Path(__file__).resolve().parent
SYSTEM_DIR = THIS_DIR / "system"


parser_instance_config = ParserInstanceConfig(
    parser_id="amazon_parser",
    parser_name="Amazon Catalog Parser",
    description="Amazon parser with automatic scheduling and live countdown",
)


class ParserSettings(BaseSettings):
    """🔥 Amazon environment settings from config.env"""

    model_config = SettingsConfigDict(
        env_file=THIS_DIR / "config.env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="UNREALON_",
        case_sensitive=False,
    )

    # System Paths
    SYSTEM_DIR: str = Field(default="system")
    BROWSER_PROFILE_DIR: str = Field(default="system/browser_profiles")

    # API Keys - THE MAIN ISSUE!
    OPENROUTER_API_KEY: str
    SERVER_URL: str
    API_KEY: str

    # Runtime Limits
    LLM_DAILY_LIMIT: float = Field(default=1.0)
    MAX_PAGES: int = Field(default=2)

    # Browser Settings
    BROWSER_HEADLESS: bool = Field(default=False)
    BROWSER_TIMEOUT: int = Field(default=30)
    SAVE_SCREENSHOTS: bool = Field(default=False)

    # Logging Settings
    LOG_LEVEL: str = Field(default="INFO")
    LOG_TO_FILE: bool = Field(default=True)


# 🔥 Load Amazon settings globally
parser_settings = ParserSettings()


class AmazonAutoConfig(AutoConfig):
    """Amazon-specific AutoConfig that extends driver config."""

    def __init__(self):
        # Initialize with custom system_dir and Amazon settings
        super().__init__()
        self.parser_id = parser_instance_config.parser_id

        # 🔥 FORCE Amazon system directory
        self.system_dir = SYSTEM_DIR
        self.project_root = THIS_DIR.parent

        # Ensure Amazon directories exist
        SYSTEM_DIR.mkdir(exist_ok=True)

        for dir in ["logs", "results", "browser_profiles"]:
            (SYSTEM_DIR / dir).mkdir(exist_ok=True)

        # Reinitialize configs with Amazon paths
        self._initialize_configs()

    def _create_browser_config(self):
        """Override browser config with Amazon + STEALTH settings."""
        # 🔥 CREATE FRESH CONFIG with Amazon settings from config.env
        return DriverBrowserConfig(
            parser_id=self.parser_id,
            headless=parser_settings.BROWSER_HEADLESS,  # From config.env!
            timeout=parser_settings.BROWSER_TIMEOUT,  # From config.env!
            user_data_dir=str(SYSTEM_DIR),
            page_load_strategy="normal",
            wait_for_selector_timeout=10,
            network_idle_timeout=3,
            enable_javascript=True,
            enable_images=True,
            enable_css=True,
            debug_mode=False,
            save_screenshots=parser_settings.SAVE_SCREENSHOTS,  # From config.env!
        )

    def _create_llm_config(self):
        """Override LLM config with Amazon settings from config.env."""
        config = super()._create_llm_config()

        # 🔥 FORCE Amazon LLM settings from config.env
        config.provider = "openrouter"
        config.model = "anthropic/claude-3.5-sonnet"
        config.api_key = parser_settings.OPENROUTER_API_KEY  # From config.env!
        config.enable_caching = True

        return config

    def _create_daemon_config(self):
        """Override daemon config with Amazon-specific settings."""

        return DaemonModeConfig(
            server_url=parser_settings.SERVER_URL,
            api_key=parser_settings.API_KEY,
            auto_reconnect=True,
            connection_timeout=30,
            heartbeat_interval=30,  # Heartbeat every 30 seconds
            max_reconnect_attempts=3,  # Max reconnect attempts
            health_check_interval=60,
            enable_metrics=True,
        )


# Global Amazon config instance
amazon_config = AmazonAutoConfig()
