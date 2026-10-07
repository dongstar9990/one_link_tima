from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse

app = FastAPI()

ANDROID_URL = "https://play.google.com/store/apps/details?id=com.mytima"
IOS_URL = "https://sahabanking.page.link/saha15"
DEFAULT_URL = ANDROID_URL


async def detect_platform(request: Request) -> str:
    # Ưu tiên header do client tự gửi (đáng tin cậy hơn)
    custom_platform = request.headers.get('x-platform', '').lower()
    if custom_platform in ('ios', 'android'):
        return custom_platform

    # Fallback: parse User-Agent
    ua = request.headers.get('user-agent', '').lower()

    if 'android' in ua:
        return 'android'
    elif any(kw in ua for kw in ('iphone', 'ipad', 'ipod')):
        return 'ios'
    else:
        return 'unknown'


@app.get('/api/download')
async def download_redirect(request: Request):
    platform = await detect_platform(request)

    if platform == 'android':
        return RedirectResponse(url=ANDROID_URL, status_code=302)
    elif platform == 'ios':
        return RedirectResponse(url=IOS_URL, status_code=302)
    else:
        return RedirectResponse(url=DEFAULT_URL, status_code=302)


from urllib.parse import quote

ADJUST_URL = (
    "https://app.adjust.com/25uy7b61"
    "?campaign=0610-tinchap-inbox"
    "&adgroup=0610-tinchap-inbox-page-hành+vi+sở+thích"
    "&creative=Hành+vi+sở+thích+1"
)
# Mã hóa tiếng Việt trong link (hành -> h%C3%A0nh), giữ nguyên : / ? = & + %
ADJUST_URL_ENCODED = quote(ADJUST_URL, safe=":/?=&+%")


@app.get("/api/download_simp")
async def download_simp():
    return RedirectResponse(url=ADJUST_URL_ENCODED, status_code=302)
