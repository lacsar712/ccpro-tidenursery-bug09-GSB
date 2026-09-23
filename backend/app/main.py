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


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    field_names = {
        "pond_id": "塘口",
        "pondId": "塘口",
        "sampled_at": "采样时间",
        "sampledAt": "采样时间",
        "fed_at": "投喂时间",
        "fedAt": "投喂时间",
        "temp_c": "水温",
        "tempC": "水温",
        "salinity_ppt": "盐度",
        "salinityPpt": "盐度",
        "do_mg_l": "溶解氧",
        "doMgL": "溶解氧",
        "ph": "pH",
        "feed_type": "饵料类型",
        "feedType": "饵料类型",
        "amount_kg": "投喂量",
        "amountKg": "投喂量",
        "operator_name": "操作人",
        "operatorName": "操作人",
        "notes": "备注",
    }
    messages = []
    for err in exc.errors():
        loc = [x for x in err.get("loc", []) if x not in ("body",)]
        field = loc[-1] if loc else None
        label = field_names.get(str(field), str(field)) if field else None
        err_type = err.get("type", "")
        if err_type == "missing":
            messages.append(f"{label}不能为空")
            continue
        if err_type.endswith("_type") or err_type.endswith("_parsing"):
            numeric_fields = {
                "temp_c", "tempC", "salinity_ppt", "salinityPpt", "do_mg_l", "doMgL",
                "ph", "amount_kg", "amountKg", "pond_id", "pondId",
            }
            if field and str(field) in numeric_fields:
                messages.append(f"{label}必须为有效数字")
            elif label:
                messages.append(f"{label}格式无效")
            else:
                messages.append("请求参数格式无效")
            continue
        # pydantic 业务校验器抛出的 ValueError：直接使用其中文消息
        ctx_error = err.get("ctx", {}).get("error")
        if ctx_error is not None and str(ctx_error):
            messages.append(str(ctx_error))
            continue
        msg = err.get("msg", "校验失败")
        messages.append(f"{label}: {msg}" if label else msg)
    detail = "; ".join(messages) if messages else "请求参数校验失败"
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
