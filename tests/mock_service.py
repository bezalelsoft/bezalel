from fastapi import FastAPI
import uvicorn


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


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000, log_level="info")
