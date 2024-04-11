import flet as ft
# from stateful_flet import StatefulUC
import requests
import random



class App(ft.UserControl):
    def __init__(self, page : ft.Page):
        super().__init__()
        self.page = page
        self.params = {
            "random": True,
            "special_chars": True,
            "caps": True,
            "nums": True,
            "num_words": 4,
            "num_chars": 16,
            "camel": True,
            'delimiter': "words",
        }

    def flip_random(self):
        is_random = self.params["random"]
        self.params["random"] = not self.params["random"]
        if is_random:
            pass
        else:
            pass



    def build(self):
        

        tb3 = ft.TextField(label="Generated Password", read_only=True, value='hello')
        btn_refresh = ft.TextButton(icon=ft.icons.REFRESH)
        simple_toggle = ft.Switch(label="Memorable Password" if not get_random(self.app_state) else "Random Password", value=False, on_change=toggle_random(self.app_state))
        num_words = ft.Slider(value=4, min=2, max=8, label="")
        caps = ft.Switch(label="Capital Letters")


        generate_password(self.params)

        self._content = ft.SafeArea(
            content=ft.ListView([
                ft.Text("Hello World"),
                ft.Row([
                    tb3,
                    btn_refresh
                ]),
                ft.Row([
                    simple_toggle,
                    num_words if get_random(self.page) else ft.Text("")
                ])
            ]),
        )
        return self._content



def camel_case(word):
    res = []
    res[:] = word
    res[0] = res[0].upper()

    return ''.join(res)

def get_random_words(num_words):
    url = f"https://random-word-api.herokuapp.com/word?number={num_words}"
    response = requests.get(url)
    if response.status_code == 200:
        words = response.json()
        # print(words)
        return words
    else:
        print(f"Error: Unable to fetch random words. Status code: {response.status_code}")
        return None

def generate_password(params):
    import re

    random_ = params["random"]
    num_chars = params["num_chars"]
    use_special = params["special_chars"]
    delimiter = params["delimiter"]
    caps = params["caps"]
    nums = params["nums"]
    num_words = params["num_words"]
    words = get_random_words(num_words)
    special_chars = '[@_!#$%^&*()<>?/\\|}{~:]'
    a_low = 'abcdefghijklmnopqrstuvwxyz'
    a_up = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    alphabet = a_low + a_up
    numbers = '0123456789'

    password = ""

    if random_:
        for i in range(num_chars):
            if use_special:
                if caps:
                    if nums:
                        coin_flip = random.randint(0,2)
                        match coin_flip:
                            case 0:
                                password += alphabet[random.randint(0, len(alphabet)-1)]
                            case 1:
                                password += special_chars[random.randint(0, len(special_chars)-1)]
                            case 2:
                                password += numbers[random.randint(0, len(numbers)-1)]
                    else:
                        coin_flip = random.randint(0,1)
                        match coin_flip:
                            case 0:
                                password += alphabet[random.randint(0, len(alphabet)-1)]
                            case 1:
                                password += special_chars[random.randint(0, len(special_chars)-1)] 
                else:
                    if nums:
                        coin_flip = random.randint(0,2)
                        match coin_flip:
                            case 0:
                                password += a_low[random.randint(0, len(a_low)-1)]
                            case 1:
                                password += special_chars[random.randint(0, len(special_chars)-1)]
                            case 2:
                                password += numbers[random.randint(0, len(numbers)-1)]
                    else:
                        coin_flip = random.randint(0,1)
                        match coin_flip:
                            case 0:
                                password += a_low[random.randint(0, len(a_low)-1)]
                            case 1:
                                password += special_chars[random.randint(0, len(special_chars)-1)]

            else:
                if caps:
                    if nums:
                        coin_flip = random.randint(0,1)
                        match coin_flip:
                            case 0:
                                password += alphabet[random.randint(0, len(alphabet)-1)]
                            case 1:
                                password += numbers[random.randint(0, len(numbers)-1)]
                    else:
                        password += alphabet[random.randint(0, len(alphabet)-1)]
                           
                else:
                    if nums:
                        coin_flip = random.randint(0,1)
                        match coin_flip:
                            case 0:
                                password += a_low[random.randint(0, len(a_low)-1)]
                            case 1:
                                password += numbers[random.randint(0, len(numbers)-1)]
                    else:
                        password += a_low[random.randint(0, len(a_low)-1)]

    else:
        delims = special_chars
        if delimiter == "numbers":
            delims = numbers

        for word in words:
            if not params["lower"]:
                if caps:
                    coin_flip = bool(random.randint(0,1))
                    if coin_flip:
                        word = word.upper()
                else:
                    word = camel_case(word)

            
            
            if words[-1].lower() == word.lower():
                password += word
            else:
                password += word + delims[random.randint(0, len(delims)-1)]

    print(password)



def toggle_random(page):
    random = page.client_storage.get("random")
    if random:
        page.client_storage.set("random", False)
    else: 
        page.client_storage.set("random", True)

    page.update()

def get_random(page):
    return page.client_storage.get("random")



def main(page: ft.Page):
    page.title = "Password Generator"
    page.vertical_alignment   = 'center'
    page.horizontal_alignment = 'center'


    page.add(App(page))
    params = {
        "random": False,

        "special_chars": True,
        "caps": False,
        "nums": True,
        "num_chars": 12,

        "num_words": 8,
        "lower": False,
        "delimiter": "special"
    }

    generate_password(params)

if __name__ == '__main__':   
    ft.app(main)