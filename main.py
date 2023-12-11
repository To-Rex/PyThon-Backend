import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True, port=8000)
    # uvicorn.run(
    #     app="app.main:app",
    #     host="localhost",
    #     port=8000,
    #     reload=True
    # )
