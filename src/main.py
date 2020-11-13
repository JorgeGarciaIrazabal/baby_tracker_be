import json
import shutil
from pathlib import Path

import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
import tarfile

from src.controllers import *
from src.app import app

DIST_PATH = Path("/home/jirazabal/code/baby_tracker_be/dist")
DIST_TAR_PATH = DIST_PATH.parent / "dist.tar.gz"


def get_ip():
    import socket

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping", response_model=str, tags=["api"])
def ping():
    return f"hello {datetime.now().isoformat()}"


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
@app.get("/login", response_class=HTMLResponse, include_in_schema=False)
def read_root():
    return (DIST_PATH / "index.html").read_text()


if DIST_TAR_PATH.exists():
    tar = tarfile.open(DIST_TAR_PATH)
    shutil.rmtree(DIST_PATH, ignore_errors=True)
    tar.extractall(str(DIST_PATH.parent))


app.mount("/", StaticFiles(directory=str(DIST_PATH)))


if __name__ == "__main__":
    # token =
    # "eyJhbGciOiJSUzI1NiIsImtpZCI6ImQwNWVmMjBjNDUxOTFlZmY2NGIyNWQzODBkNDZmZGU1NWFjMjI5ZDEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJuYmYiOjE2MDQyOTQxMDMsImF1ZCI6IjY1NDM5NzcxNzMtcG83NmNibjVyNDV0aTBtYTRudGE0MXZqNjg2YnJtbmYuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMTE5NTIyMDg3NTc1NTc4NzA3ODgiLCJlbWFpbCI6ImpvcmdlLmdpcmF6YWJhbEBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwibmFtZSI6IkpvcmdlIEdhcmPDrWEgSXJhesOhYmFsIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hLS9BT2gxNEdqdFhFSmxxVGhjMngxNmtvb01nRl9nRmppV0J3S0k4Z0s3T3llS1hnPXM5Ni1jIiwiZ2l2ZW5fbmFtZSI6IkpvcmdlIiwiZmFtaWx5X25hbWUiOiJHYXJjw61hIElyYXrDoWJhbCIsImlhdCI6MTYwNDI5NDQwMywiZXhwIjoxNjA0Mjk4MDAzLCJqdGkiOiJiZTYwM2Q0OTdmOGVjYTIzMmVhMWI0YmEzMDU1ZmUzZDJmNDUxOWEwIn0.HIePCJIEQqfKThip4wVVzCE2BrByO61A_KJXouKbYAD82q0l_h8dzQxKTkkeNl21t5ZeEQKrySQzSf38IPzglZnkujlJIVKiydp_VvXTYLPIsiyBMjPhjgT2tCYwsuxvHRznkmZhm9E1mDXXsRVehnrNfvkk49N5rsl6p8OBQomFhZ7wZusTvjvYzNwg1kkwVxcPhuApHZ8ZMDYPUjnMOnhQiUW5_vd2XJeXeihn2pU4n0YrxhVt8gP0nx32t4WJOebhyFC-lXaG7rcRMW-6hS-nafPMzTCEhCkG5g32pMAVp165kkk4ZoLm4A7E2tExkcosyMTq1Gp2bsP7Xw9JfA"
    # jwt.decode(token, SECRET, algorithms=["RS256"])
    # secrets_path = Path(__file__).parent.parent / "secrets"
    # print(secrets_path)
    with (Path(__file__).parent / "openapi.json").open(mode="w") as f:
        json.dump(app.openapi(), f)
    print(f"local_id: http://{get_ip()}:9001")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=9001,
    )
else:
    tar = tarfile.open(str(DIST_PATH.parent / "dist.tar.gz"))
    tar.extractall(str(DIST_PATH.parent))
