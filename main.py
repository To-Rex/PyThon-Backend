import uvicorn

if __name__ == "__main__":
    #uvicorn.run("app.main:app", reload=True)
    #port 8081
    uvicorn.run("app.main:app", port=8081, reload=True)
