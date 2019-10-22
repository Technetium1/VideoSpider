# https://github.com/Technetium1
import configparser
import certifi
import sys
import urllib3
import webbrowser
from os import system
from dataclasses import dataclass

version = "1.0"

# Set title
system("title Tech's VS Tool " + version)

# Read VideoSpiderKeys.ini
config = configparser.ConfigParser()
config.read("VideoSpiderKeys.ini")
http = urllib3.PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=certifi.where())


@dataclass
class Nympho:
    api: str = config["SECRETS"]["API_KEY"]
    secret: str = config["SECRETS"]["SECRET_KEY"]
    ip: str = None
    vid: str = None
    ticket: str = None
    sid: int = 0

    def __post_init__(self):
        if len(self.api) > 0 or len(self.secret) > 0:
            pass
        else:
            print("API or SECRET_KEY not found!")
            sys.exit()
        _ = http.request("GET", "https://icanhazip.com")
        if _.status != 200:
            sys.exit()
        else:
            self.ip = _.data.decode("utf-8").strip("\n")


def openbrowser(is_imdb=False, infos=None):
    baseurl = "https://videospider.stream/getvideo?key={api}&video_id={vid}&ticket={ticket}".format(
        api=infos.api, vid=infos.vid, ticket=infos.ticket
    )
    if is_imdb is False:
        print("Opening TMDB URL: " + baseurl + "&tmdb=1")
        input("Enter to exit and open URL!")
        webbrowser.open_new_tab(baseurl + "&tmdb=1")
    else:
        print("Opening IMDB URL: " + baseurl)
        input("Enter to exit and open URL!")
        webbrowser.open_new_tab(baseurl)


def mkreq(url: str) -> str:  # not sure what type, maybe str
    # print(url)
    req = http.request("GET", url)
    if req.status != 200:
        print(
            "Couldn't make the request for\n{}\n got {} in mkreq()".format(
                url, req.status
            )
        )
        return None
    else:
        return req.data.decode("utf-8")


def getticket(infos: Nympho) -> str:
    if infos.vid is None:
        print("No video id for some reason for getticket()\nexiting...")
        sys.exit()
    baseurl = "https://videospider.in/getticket.php?key={api}&secret_key={secret}&video_id={vid}".format(
        api=infos.api, secret=infos.secret, vid=infos.vid
    )
    if infos.sid is None:
        req = mkreq(baseurl + "&ip={}".format(infos.ip))
    else:
        req = mkreq(baseurl + "&s={}&ip={}".format(infos.sid, infos.ip))
    return req


def is_sane(a: str):
    a = a.strip().lower()
    if "y" or "Y" in a or "n" or "N" in a:
        if a == "y" or a == "Y":
            return True
        else:
            return False
    else:
        return None


def prompt(y: str, n: str) -> str:
    method = input(f"{y}? ENTER Y/N (N= {n}):\n")
    if is_sane(method) is True:
        return y
    elif is_sane(method) is False:
        return n
    else:
        prompt(y, n)


if __name__ == "__main__":
    method = prompt("IMDB", "TMDB")
    seasonornah = input("Season ID (optional): ").strip()
    episodeid = input("ID from Movie DB to search: ").strip()
    if len(seasonornah) > 0:
        nympho = Nympho(sid=seasonornah, vid=episodeid)
    else:
        nympho = Nympho(vid=episodeid)
    # print(nympho)
    nympho.ticket = getticket(nympho)
    if method == "IMDB":
        # TMDB
        openbrowser(True, nympho)
    else:
        openbrowser(False, nympho)
