from app.routers.zones import router as zones_router
from app.routers.donors import router as donors_router
from app.routers.inventory import router as inventory_router
from app.routers.alerts import router as alerts_router

__all__ = [
    "zones_router",
    "donors_router",
    "inventory_router",
    "alerts_router",
]
