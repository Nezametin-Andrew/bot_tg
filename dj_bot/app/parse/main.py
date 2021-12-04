import requests
from bs4 import BeautifulSoup


class DataGame:

    def __init__(self):
        self.session = requests.Session()
        self.user_agent = [
            "Mozilla/5.0", "(Windows NT 10.0; Win64; x64)", "AppleWebKit/537.36",
            "(KHTML, like Gecko)", "Chrome/96.0.4664.45 Safari/537.36"
        ]
        self.headers = {"user-agent": " ".join(self.user_agent)}
        self.default_link = "https://randomus.ru/"
        self.data = data = {
            "from": 1,
            "to": 100,
            "count": 1,
            "action": "generate",
            "max_count": 100,
            "max_count": 300,
            "check": None,
            }

    def get_obj_bs4(self, text):
        return BeautifulSoup(text, 'html.parser')

    def request(self, **kwargs):
        if kwargs.get('first') is not None:
            return self.session.get(url=self.default_link + "number", headers=self.headers)
        else:
            return self.session.post(url=self.default_link + "number", data=self.data)

    def secret_key(self, text):
        return str(self.get_obj_bs4(text).find_all('input')[-2]).split()[-1].split('"')[-2]

    def random_num(self, text):
        return str(self.get_obj_bs4(text).textarea).split()[-1].split("<")[-2].split(">")[-1]

    def serial_key(self, text):
        return "".join(str(self.get_obj_bs4(text).h1).split()[6:-2])

    def get_data_for_game(self):
        try:
            f_r = self.request(first=True)
            if f_r.status_code == 200:
                self.data['check'] = self.secret_key(text=f_r.text)
            if self.data['check'] is not None:
                s_r = self.request()
                serial_key, random_num = self.serial_key(text=s_r.text), self.random_num(text=s_r.text)

                return {
                    "random_num": random_num,
                    "img": self.default_link + f"num_{serial_key}.png",
                    "link": self.default_link + f"num{serial_key}"
                }
        except Exception as e:
            return {"error": str(e)}
