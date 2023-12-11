import uvicorn

if __name__ == "__main__":
    #uvicorn.run("app.main:app", reload=True, host='0.0.0.0')
    uvicorn.run("app.main:app", reload=True)

    # uvicorn.run(
    #     app="app.main:app",
    #     host="localhost",
    #     port=8000,
    #     reload=True
    # )
