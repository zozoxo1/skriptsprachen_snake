from typing import Optional

from fastapi import FastAPI, Cookie, status, Response
from enums.Direction import Direction

app = FastAPI()


@app.get("/move/{direction}", status_code=status.HTTP_202_ACCEPTED)
def movePlayer(direction: str, response: Response, userId: Optional[str] = Cookie(None)):
    if not userId:
        print("userId not set")
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"message": "userId is not set as cookie"}

    # TODO: check if userId is currently playing

    print("userId: %s" % userId)

    directionValues = [member.value for member in Direction]
    direction = direction.upper()

    if direction not in directionValues:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "direction is not valid"}

    # TODO: set moving direction

    return {"message": "direction is %s" % direction}
