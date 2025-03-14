import importlib
import logging
from pathlib import Path

from fastapi import APIRouter

logger = logging.getLogger(__name__)


def get_global_router():
    router = APIRouter()

    # Discover all modules inside "modules/"
    package_path = Path(__file__).resolve().parent.parent / "modules"
    package_name = "modules"

    logger.info(f"Scanning modules in: {package_path}")

    for module_path in package_path.iterdir():
        if module_path.is_dir() and (module_path / "routes.py").exists():
            module_name = module_path.name
            try:
                logger.info(f"Loading routes from module: {module_name}")
                module = importlib.import_module(f"{package_name}.{module_name}.routes")
                if hasattr(module, "router"):
                    router.include_router(module.router)
            except ModuleNotFoundError:
                continue  # Skip modules without a `routes.py`

    return router
