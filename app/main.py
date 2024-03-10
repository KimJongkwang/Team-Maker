from pathlib import Path
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from app.team_maker import TeamMaker


app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("./index.html", context={"request": request})


class InputModel(BaseModel):
    players: str


@app.post("/data")
async def submit_data(request: Request, text_data: str = Form(...)):
    player_list = text_data.split("/")

    pstat, game = make_team(player_list)

    context = {"request": request, "game": game, "pstat": pstat}
    response = templates.TemplateResponse("./index.html", context=context)
    response.set_cookie("players", text_data)
    return response


@app.get("/data")
async def submit_data(request: Request):
    text_data = request.cookies["players"]
    player_list = text_data.split("/")

    pstat, game = make_team(player_list)

    context = {"request": request, "game": game, "pstat": pstat}
    response = templates.TemplateResponse("./index.html", context=context)
    response.set_cookie("players", text_data)
    return response


@app.get("/redirect-index")
async def submit_data():
    return RedirectResponse("/")


# 1/2/3/4/5/6/7/8/9/10/11/12/13/14/15/16/17/18/19/20/21/22/23/24/25/26/27/28/29/30/31/32/33


def make_team(players):
    players_match = {i: p for i, p in enumerate(players)}
    players_number = list(players_match.keys())
    tm = TeamMaker(players_number, players_match=players_match)
    teams = tm.choice_team()

    all_game = {}
    for i in range(len(teams)):
        all_game[i] = tm.allocate_position_per_game(teams[i])

    result = {
        "Team01": all_game[0],
        "Team02": all_game[1],
        "Team03": all_game[2],
    }

    player_stats = tm.player_stats
    for plist in player_stats:
        plist[0] = players_match[plist[0]]
    return player_stats, result
