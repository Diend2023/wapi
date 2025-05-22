import os
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html, get_swagger_ui_oauth2_redirect_html
from app.api.endpoints import test, delta_force, minecraft
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(docs_url=None, redoc_url=None, openapi_url="/openapi.json")
static_dir = os.path.join(os.path.dirname(__file__), "static")

app.include_router(test.router)
app.include_router(delta_force.router)
app.include_router(minecraft.router)
app.mount("/static", StaticFiles(directory=static_dir), name="static")



@app.get("/", tags=["Test"])
def read_root():
    return {"message": "Welcome to the wapi Server!"}

@app.get("/favicon.ico", tags=["Static"])
async def get_favicon():
    return FileResponse("app/static/wapi/favicon.ico")

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title="Wapi Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="static/swagger-ui/swagger-ui-bundle.js",
        swagger_css_url="static/swagger-ui/swagger-ui.css",
        swagger_favicon_url="static/swagger-ui/favicon.ico"
    )


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title="Wapi ReDoc",
        redoc_js_url="static/redoc/redoc.standalone.js",
        redoc_favicon_url="static/redoc/favicon.ico",
        with_google_fonts=False
    )


@app.get("/openapi.json", include_in_schema=False)
async def openapi():
    return app.openapi()