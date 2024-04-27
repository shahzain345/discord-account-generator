from curl_cffi import requests
from typing import Union
from .proofs.hsw import get_hsw
from .recognition._solver import solve
from ._motiondata import get_data
from PIL import Image
from io import BytesIO
import json, random, string, httpx
import urllib.parse
import datetime
import base64


def image_url_to_base64(url):
    # Send a GET request to the image URL
    response = httpx.get(url)
    # Raise an exception if the request was unsuccessful
    response.raise_for_status()

    # Convert the image (response.content) to a Base64 string
    image_buffer = BytesIO(response.content)
    base64_bytes = base64.b64encode(image_buffer.getvalue())

    # Convert bytes to string
    base64_string = base64_bytes.decode("utf-8")

    return base64_string


class hCaptchaSolver(requests.Session):
    """
    A solver for hCaptcha
    basicallly a try to solve this "unsolvable captcha"
    by Shahzain345 2024
    `site_key`: str
    `site_url`: str
    `proxies(Optional)`: str | None
    """

    def __init__(self, site_key: str, site_url: str, proxies: Union[str, None] = None):
        self.site_key = site_key
        self.site_url = site_url
        self.version = "b1c589a"
        super().__init__(proxy=proxies, impersonate="safari17_0")
        self.answers = {}

    def _get_challenge_data(self):
        resp = self.post(
            "https://api.hcaptcha.com/getcaptcha/4c672d35-0701-42b2-88c3-78380b0db560",
            data=get_data(),
            headers={
                "Host": "api.hcaptcha.com",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:124.0) Gecko/20100101 Firefox/124.0",
                "Accept": "application/json",
                "Accept-Language": "en-GB,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "Content-Type": "application/x-www-form-urlencoded",
                "Origin": "https://newassets.hcaptcha.com",
                "DNT": "1",
                "Sec-GPC": "1",
                "Connection": "keep-alive",
                "Referer": "https://newassets.hcaptcha.com/",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-site",
            },
        ).json()
        self.c = resp["c"]
        self.tasklist = resp["tasklist"]
        self.key = resp["key"]
        self.question = resp["requester_question"]["en"]
        self._proof_data = resp["c"]["req"]
        # self.requester_example = resp["requester_question_example"][0]

    def _submit(self):
        st = str(round(datetime.datetime.now().timestamp()))
        payload = {
            "v": self.version,
            "job_mode": "image_label_binary",
            "answers": self.answers,
            "serverdomain": "discord.com",
            "sitekey": "4c672d35-0701-42b2-88c3-78380b0db560",
            "motionData": '{"st":1714134220833,"dct":1714134220833,"mm":[[23,273,1714134222053],[36,270,1714134222071],[58,268,1714134222087],[62,268,1714134222103],[67,268,1714134222120],[71,269,1714134222137],[72,269,1714134222153],[73,269,1714134222170],[73,227,1714134222319],[73,166,1714134222620],[73,166,1714134222637],[73,166,1714134222653],[73,166,1714134222670],[72,167,1714134222686],[72,167,1714134222703],[72,220,1714134223070],[72,223,1714134223138],[71,226,1714134223154],[70,228,1714134223170],[70,229,1714134223186],[71,278,1714134223404],[71,280,1714134223421],[73,283,1714134223437],[74,284,1714134223454],[75,285,1714134223471],[75,285,1714134223487],[75,432,1714134223853],[74,432,1714134223870],[73,440,1714134223886],[72,446,1714134223920],[71,446,1714134223936],[71,453,1714134223953],[69,455,1714134223986],[68,453,1714134224003],[67,453,1714134224019],[66,443,1714134224037],[66,439,1714134224053],[67,431,1714134224070],[67,428,1714134224086],[67,426,1714134224104],[68,420,1714134224121],[68,413,1714134224137],[68,409,1714134224154],[68,400,1714134224170],[67,397,1714134224187],[67,393,1714134224203],[67,393,1714134224220],[67,392,1714134224237],[67,392,1714134224253],[67,392,1714134224287],[67,390,1714134224303],[67,389,1714134224320],[68,386,1714134224336],[69,384,1714134224354],[70,380,1714134224370],[71,377,1714134224387],[72,372,1714134224403],[73,371,1714134224420],[74,368,1714134224436],[77,363,1714134224454],[79,361,1714134224470],[82,358,1714134224486],[83,357,1714134224503],[84,356,1714134224521],[84,356,1714134224537],[84,356,1714134224554],[84,356,1714134224570],[84,356,1714134224587],[84,356,1714134224603],[84,356,1714134224621],[84,356,1714134224637],[84,356,1714134224736],[84,356,1714134224754],[84,356,1714134224771],[83,356,1714134224787],[83,357,1714134224803],[85,363,1714134224819],[86,366,1714134224837],[87,373,1714134224854],[85,380,1714134224887],[85,381,1714134224904],[85,382,1714134224920],[84,384,1714134224937],[82,390,1714134224969],[81,392,1714134224987],[80,395,1714134225004],[79,396,1714134225021],[78,399,1714134225052],[78,400,1714134225070],[78,404,1714134225086],[78,408,1714134225102],[78,409,1714134225119],[78,409,1714134225136],[78,409,1714134225303],[79,410,1714134225319],[81,412,1714134225337],[81,413,1714134225354],[82,414,1714134225370],[83,416,1714134225386],[86,418,1714134225403],[98,424,1714134225420],[108,426,1714134225436],[138,434,1714134225454],[161,440,1714134225470],[201,451,1714134225486],[224,459,1714134225503],[239,465,1714134225519],[270,474,1714134225537],[282,477,1714134225554],[286,478,1714134225571],[294,482,1714134225603],[295,483,1714134225620],[296,485,1714134225637],[296,485,1714134225654],[296,486,1714134225671],[297,490,1714134225703],[300,492,1714134225719],[301,493,1714134225736],[302,493,1714134225753],[302,493,1714134225770],[304,494,1714134225787],[304,494,1714134225803],[304,494,1714134225820],[304,494,1714134225836],[305,494,1714134225852],[306,496,1714134225869],[307,498,1714134225887],[311,503,1714134225903],[313,506,1714134225920],[321,513,1714134225937],[326,516,1714134225953],[332,520,1714134225971],[333,523,1714134226004],[334,530,1714134226037],[335,531,1714134226054],[339,531,1714134226070],[341,530,1714134226087],[345,525,1714134226104],[347,522,1714134226121],[349,515,1714134226137],[347,500,1714134226169],[344,495,1714134226187],[343,491,1714134226203],[345,487,1714134226237],[345,487,1714134226253],[345,486,1714134226287],[345,486,1714134226320],[345,487,1714134226403],[345,494,1714134226419],[345,498,1714134226437],[343,505,1714134226453],[342,506,1714134226471],[342,509,1714134226487],[342,511,1714134226503],[341,516,1714134226520],[341,520,1714134226536],[341,530,1714134226554],[342,534,1714134226570],[344,539,1714134226586],[345,541,1714134226604],[347,544,1714134226620],[347,545,1714134226637],[347,545,1714134226653],[347,545,1714134226744],[347,545,1714134226769],[347,546,1714134226786],[347,546,1714134226804],[347,547,1714134226836],[347,547,1714134226853],[346,549,1714134226871],[346,549,1714134226887],[346,550,1714134226903],[346,550,1714134226919],[345,550,1714134226936],[345,550,1714134226970],[345,550,1714134226987],[345,550,1714134227004],[345,550,1714134227021],[345,551,1714134227153],[345,551,1714134227170],[344,552,1714134227187],[344,553,1714134227204],[343,554,1714134227236],[342,555,1714134227253],[342,556,1714134227271],[342,556,1714134227304],[342,556,1714134227353],[342,556,1714134227370],[340,557,1714134227594],[340,557,1714134227627]],"mm-mp":27.058252427184467,"md":[[84,356,1714134224653],[78,409,1714134225194],[345,486,1714134226304],[342,556,1714134227344]],"md-mp":897,"mu":[[84,356,1714134224761],[78,409,1714134225314],[345,487,1714134226418],[342,556,1714134227425]],"mu-mp":888,"topLevel":{"st":1714132054046,"sc":{"availWidth":1440,"availHeight":815,"width":1440,"height":900,"colorDepth":30,"pixelDepth":30,"top":0,"left":0,"availTop":25,"availLeft":0,"mozOrientation":"landscape-primary","onmozorientationchange":null},"nv":{"permissions":{},"pdfViewerEnabled":true,"doNotTrack":"1","maxTouchPoints":0,"mediaCapabilities":{},"oscpu":"Intel Mac OS X 10.15","vendor":"","vendorSub":"","productSub":"20100101","cookieEnabled":true,"buildID":"20181001000000","mediaDevices":{},"credentials":{},"clipboard":{},"mediaSession":{},"userActivation":{},"globalPrivacyControl":true,"webdriver":false,"hardwareConcurrency":4,"geolocation":{},"appCodeName":"Mozilla","appName":"Netscape","appVersion":"5.0 (Macintosh)","platform":"MacIntel","userAgent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:125.0) Gecko/20100101 Firefox/125.0","product":"Gecko","language":"en-GB","languages":["en-GB","en"],"locks":{},"onLine":true,"storage":{},"plugins":["internal-pdf-viewer","internal-pdf-viewer","internal-pdf-viewer","internal-pdf-viewer","internal-pdf-viewer"]},"dr":"","inv":false,"exec":false,"wn":[],"wn-mp":0,"xy":[[0,278,1,1714134212432],[0,257,1,1714134212449],[0,241,1,1714134212472],[0,237,1,1714134212504],[0,235,1,1714134212520],[0,234,1,1714134212536],[0,233,1,1714134212553],[0,232,1,1714134212753],[0,231,1,1714134212770],[0,230,1,1714134212786],[0,227,1,1714134212804],[0,213,1,1714134212836],[0,203,1,1714134212869],[0,198,1,1714134212895],[0,195,1,1714134212913],[0,187,1,1714134212936],[0,184,1,1714134212953],[0,182,1,1714134212969],[0,180,1,1714134212986],[0,179,1,1714134213002],[0,177,1,1714134213019],[0,176,1,1714134213036],[0,175,1,1714134213053],[0,174,1,1714134213070],[0,173,1,1714134213087],[0,174,1,1714134214370],[0,179,1,1714134214387],[0,189,1,1714134214404],[0,204,1,1714134214420],[0,215,1,1714134214436],[0,229,1,1714134214453],[0,275,1,1714134214470],[0,300,1,1714134214487],[0,325,1,1714134214503],[0,349,1,1714134214521],[0,373,1,1714134214537],[0,395,1,1714134214553],[0,418,1,1714134214570],[0,440,1,1714134214587],[0,461,1,1714134214606],[0,497,1,1714134214637],[0,513,1,1714134214653],[0,528,1,1714134214670],[0,542,1,1714134214687],[0,554,1,1714134214703],[0,566,1,1714134214720],[0,577,1,1714134214736],[0,587,1,1714134214753],[0,596,1,1714134214769],[0,605,1,1714134214786],[0,613,1,1714134214803],[0,620,1,1714134214820],[0,627,1,1714134214838],[0,633,1,1714134214920],[0,627,1,1714134214937],[0,618,1,1714134214953],[0,610,1,1714134214970],[0,600,1,1714134214987],[0,591,1,1714134215003],[0,581,1,1714134215021],[0,559,1,1714134215053],[0,550,1,1714134215070],[0,542,1,1714134215086],[0,534,1,1714134215103],[0,526,1,1714134215119],[0,519,1,1714134215136],[0,511,1,1714134215155],[0,501,1,1714134215503],[0,490,1,1714134215520],[0,481,1,1714134215537],[0,471,1,1714134215553],[0,463,1,1714134215570],[0,456,1,1714134215586],[0,451,1,1714134215604],[0,448,1,1714134215620],[0,442,1,1714134215637],[0,436,1,1714134215654],[0,430,1,1714134215670],[0,424,1,1714134215687],[0,419,1,1714134215704],[0,409,1,1714134215736],[0,404,1,1714134215753],[0,399,1,1714134215770],[0,395,1,1714134215787],[0,391,1,1714134215804],[0,387,1,1714134215820],[0,383,1,1714134215837],[0,379,1,1714134215853],[0,376,1,1714134215870],[0,373,1,1714134215887],[0,370,1,1714134215903],[0,369,1,1714134216004],[0,349,1,1714134216020],[0,337,1,1714134216038],[0,329,1,1714134216054],[0,321,1,1714134216070],[0,315,1,1714134216087],[0,312,1,1714134216103],[0,310,1,1714134216120],[0,309,1,1714134216137],[0,310,1,1714134216587],[0,312,1,1714134216604],[0,315,1,1714134216620],[0,317,1,1714134216636],[0,321,1,1714134216653],[0,325,1,1714134216670],[0,332,1,1714134216687],[0,340,1,1714134216703],[0,347,1,1714134216720],[0,353,1,1714134216736],[0,357,1,1714134216754],[0,360,1,1714134216770],[0,362,1,1714134216787],[0,366,1,1714134216804],[0,370,1,1714134216820],[0,373,1,1714134216837],[0,374,1,1714134217404],[0,379,1,1714134217436],[0,383,1,1714134217454],[0,386,1,1714134217471],[0,391,1,1714134217487],[0,397,1,1714134217503],[0,401,1,1714134217520],[0,405,1,1714134217537],[0,408,1,1714134217553],[0,409,1,1714134217570],[0,404,1,1714134220886],[0,175,1,1714134220920],[0,172,1,1714134222237],[0,159,1,1714134222254],[0,148,1,1714134222271],[0,138,1,1714134222287],[0,133,1,1714134222303],[0,126,1,1714134222320],[0,108,1,1714134222338],[0,85,1,1714134222387],[0,79,1,1714134222403],[0,75,1,1714134222420],[0,72,1,1714134222470],[0,73,1,1714134222703],[0,75,1,1714134222720],[0,79,1,1714134222736],[0,86,1,1714134222753],[0,89,1,1714134222770],[0,97,1,1714134222787],[0,104,1,1714134222803],[0,111,1,1714134222820],[0,116,1,1714134222839],[0,122,1,1714134222870],[0,123,1,1714134222886],[0,124,1,1714134222903],[0,125,1,1714134223020],[0,127,1,1714134223120],[0,128,1,1714134223137],[0,130,1,1714134223154],[0,132,1,1714134223171],[0,135,1,1714134223204],[0,139,1,1714134223221],[0,144,1,1714134223237],[0,149,1,1714134223254],[0,155,1,1714134223270],[0,160,1,1714134223287],[0,166,1,1714134223304],[0,170,1,1714134223321],[0,175,1,1714134223354],[0,179,1,1714134223387],[0,181,1,1714134223406],[0,186,1,1714134223570],[0,191,1,1714134223587],[0,201,1,1714134223604],[0,210,1,1714134223621],[0,216,1,1714134223637],[0,250,1,1714134223654],[0,258,1,1714134223670],[0,277,1,1714134223687],[0,280,1,1714134223703],[0,285,1,1714134223721],[0,297,1,1714134223754],[0,309,1,1714134223787],[0,314,1,1714134223803],[0,320,1,1714134223820],[0,325,1,1714134223837],[0,330,1,1714134223853],[0,339,1,1714134223886],[0,347,1,1714134223920],[0,351,1,1714134223936],[0,355,1,1714134223954],[0,361,1,1714134223986],[0,364,1,1714134224002],[0,366,1,1714134224020],[0,368,1,1714134224036],[0,370,1,1714134224053],[0,372,1,1714134224070],[0,374,1,1714134224086],[0,376,1,1714134224120],[0,377,1,1714134224137],[0,378,1,1714134224154],[0,380,1,1714134224187]],"xy-mp":58.937743190661486,"mm":[[589,503,1714134212504],[589,499,1714134212586],[589,439,1714134213154],[589,439,1714134213303],[593,438,1714134213320],[743,793,1714134214720],[744,804,1714134214736],[745,814,1714134214753],[746,823,1714134214769],[748,832,1714134214786],[750,840,1714134214803],[752,846,1714134214820],[753,853,1714134214838],[753,807,1714134215021],[753,776,1714134215070],[752,769,1714134215086],[752,761,1714134215103],[752,753,1714134215119],[583,730,1714134219804],[558,732,1714134219821],[502,738,1714134219854],[489,741,1714134219870],[487,742,1714134219887],[485,743,1714134219903],[481,744,1714134219920],[479,744,1714134219936],[474,748,1714134219953],[469,752,1714134219969],[460,759,1714134219987],[456,762,1714134220003],[481,530,1714134221371],[491,526,1714134221388],[503,522,1714134221405],[509,520,1714134221437],[510,519,1714134221454],[512,517,1714134221470],[515,515,1714134221487],[523,509,1714134221504],[525,507,1714134221520],[526,505,1714134221536],[526,505,1714134221554],[526,505,1714134221587],[530,499,1714134221620],[535,493,1714134221636],[537,490,1714134221654],[540,485,1714134221687],[543,481,1714134221704],[547,476,1714134221736],[550,472,1714134221753],[550,471,1714134221770],[550,470,1714134221787],[549,470,1714134221803],[549,470,1714134221820],[548,470,1714134221836],[548,470,1714134221869],[545,468,1714134221887],[541,466,1714134221904],[533,462,1714134221920],[529,461,1714134221937],[527,461,1714134221954],[530,460,1714134221986],[540,457,1714134222003],[573,450,1714134222020],[593,445,1714134222037]],"mm-mp":82.48844884488453},"v":1}',
            "n": get_hsw(self._proof_data),
            "c": json.dumps(self.c),
        }
        self.headers["content-type"] = "application/json;charset=UTF-8"
        data = self.post(
            f"https://api.hcaptcha.com/checkcaptcha/4c672d35-0701-42b2-88c3-78380b0db560/{self.key}",
            json=payload,
            headers={
                "Host": "api.hcaptcha.com",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:124.0) Gecko/20100101 Firefox/124.0",
                "Accept": "application/json",
                "Accept-Language": "en-GB,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "Content-Type": "application/json",
                "Origin": "https://newassets.hcaptcha.com",
                "DNT": "1",
                "Sec-GPC": "1",
                "Connection": "keep-alive",
                "Referer": "https://newassets.hcaptcha.com/",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-site",
            },
        ).json()
        if not data.get("pass"):
            raise Exception(f"Submit rejected, {data}")
        self.token = data["generated_pass_UUID"]
        return self.token

    def _recognize(self):
        images = {}
        for index, task in enumerate(self.tasklist):
            images[str(index)] = image_url_to_base64(task["datapoint_uri"])
        resp = solve(images, None, self.question)
        for index, task in enumerate(self.tasklist):
            if index in resp["solution"]:
                self.answers[task["task_key"]] = "true"
            else:
                self.answers[task["task_key"]] = "false"

    def solve(self):
        self._get_challenge_data()
        self._recognize()
        res = self._submit()
        return res


if __name__ == "__main__":
    solver = hCaptchaSolver("4c672d35-0701-42b2-88c3-78380b0db560", "discord.com")
    solver.solve()