from fastapi import APIRouter

from app.api.v1.endpoints.auth_router import router as auth_router
from app.api.v1.endpoints.user_router import router as user_router
from app.api.v1.endpoints.product_router import router as product_router
from app.api.v1.endpoints.category_router import router as category_router
from app.api.v1.endpoints.productImage_router import router as product_image_router
from app.api.v1.endpoints.session_router import router as session_router


router = APIRouter()

router.include_router(auth_router)
router.include_router(user_router)
router.include_router(product_router)
router.include_router(category_router)
router.include_router(product_image_router)
router.include_router(session_router)