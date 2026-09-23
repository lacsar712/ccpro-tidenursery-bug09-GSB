from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routers import auth, hatcheries, ponds, water_samples, feed_events, dashboard

app = FastAPI(title="TideNursery API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


FIELD_LABELS = {
    "pondId": "塘口",
    "sampledAt": "采样时间",
    "tempC": "水温",
    "salinityPpt": "盐度",
    "doMgL": "溶解氧",
    "ph": "pH",
    "fedAt": "投喂时间",
    "feedType": "饵料类型",
    "amountKg": "投喂量",
    "operatorName": "操作人",
}

ERROR_TYPE_MESSAGES = {
    "float_parsing": "必须是有效数字",
    "int_parsing": "必须是整数",
    "float_type": "必须是数字",
    "int_type": "必须是整数",
    "string_type": "必须是字符串",
    "datetime_parsing": "时间格式不正确",
    "finite_number": "必须是有限数值",
    "missing": "缺少必填字段",
}


def _translate_error(err: dict) -> str:
    loc = [str(x) for x in err.get("loc", []) if x != "body"]
    field = loc[-1] if loc else ""
    label = FIELD_LABELS.get(field, field)
    err_type = err.get("type", "")
    if err_type == "missing":
        return f"缺少必填字段：{label}" if label else "缺少必填字段"
    msg = err.get("msg", "校验失败")
    if msg.startswith("Value error, "):
        # 自定义校验器抛出的已是完整中文信息
        return msg[len("Value error, "):]
    translated = ERROR_TYPE_MESSAGES.get(err_type)
    if translated:
        return f"{label}{translated}" if label else translated
    return f"{label}：{msg}" if label else msg


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    messages = [_translate_error(err) for err in exc.errors()]
    detail = "；".join(m for m in messages if m) or "请求参数校验失败"
    return JSONResponse(status_code=400, content={"detail": detail})


app.include_router(auth.router)
app.include_router(hatcheries.router)
app.include_router(ponds.router)
app.include_router(water_samples.router)
app.include_router(feed_events.router)
app.include_router(dashboard.router)


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "TideNursery"}
