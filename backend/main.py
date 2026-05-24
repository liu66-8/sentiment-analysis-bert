from contextlib import asynccontextmanager
import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse

from backend.settings import STATIC_DIR
from backend.models.database import init_db
from backend.api.analyze import router as analyze_router
from backend.api.history import router as history_router
from backend.api.status import router as status_router
from backend.api.auth import router as auth_router
from backend.api.stats import router as stats_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    try:
        from backend.services.predictor import predictor
    except Exception as e:
        print(f"[WARNING] 模型加载失败: {e}")
        print("[INFO] 请确保 models/BEST_checkpoint.tar 存在")
    yield


app = FastAPI(
    title="细粒度餐饮评论情感分析系统",
    description="基于 BERT 的 20 维度情感分析 API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze_router)
app.include_router(history_router)
app.include_router(status_router)
app.include_router(auth_router)
app.include_router(stats_router)

js_dir = os.path.join(STATIC_DIR, "js")
css_dir = os.path.join(STATIC_DIR, "css")
if os.path.isdir(js_dir):
    app.mount("/js", StaticFiles(directory=js_dir), name="js")
if os.path.isdir(css_dir):
    app.mount("/css", StaticFiles(directory=css_dir), name="css")


@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.isfile(index_path):
        return FileResponse(index_path, media_type="text/html")
    return {"message": "前端文件未找到，请检查 frontend 目录"}
