from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel


app = FastAPI()


def generate_pages(n_pages=4, records_per_page=3):
    pages = []
    for page_idx in range(0, n_pages):
        page = []
        for record_idx in range(0, records_per_page):
            page.append({
                "key1": "val",
                "r": record_idx + page_idx * records_per_page,
                "rInPage": record_idx
            })
        pages.append(page)
    return pages


pages = generate_pages()


@app.get("/page-api")
async def root(pageNumber: int):
    pageIndex = pageNumber-1
    assert pageIndex < len(pages)
    assert pageIndex >= 0

    return {
        "pageCount": len(pages),
        "pageNumber": pageNumber,
        "entities": pages[pageIndex],
        }


@app.post("/page-api-post")
async def paginate_api_post(pageNumber: int):
    pageIndex = pageNumber-1
    assert pageIndex < len(pages)
    assert pageIndex >= 0

    return {
        "pageCount": len(pages),
        "pageNumber": pageNumber,
        "entities": pages[pageIndex],
        }


class Paging(BaseModel):
    pageNumber: int


class ComplexRequest(BaseModel):
    paging: Paging


@app.post("/page-api-post-2")
async def paginate_api_post_2(request: ComplexRequest):
    pageIndex = request.paging.pageNumber - 1
    assert pageIndex < len(pages)
    assert pageIndex >= 0

    return {
        "paging": {
            "pageCount": len(pages),
            "pageNumber": request.paging.pageNumber,
        },
        "entities": pages[pageIndex],
        }

@app.post("/page-api-post-total-records")
async def paginate_api_post_total_records(request: ComplexRequest):
    pageIndex = request.paging.pageNumber - 1
    assert pageIndex < len(pages)
    assert pageIndex >= 0

    totalRecords = sum([len(p) for p in pages])

    return {
        "paging": {
            "totalRecords": totalRecords
        },
        "entities": pages[pageIndex],
        }


def run_uvicorn_server():
    uvicorn.run(app, host="localhost", port=5000, log_level="info")


if __name__ == "__main__":
    run_uvicorn_server()
