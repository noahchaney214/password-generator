import flet as ft
# from stateful_flet import StatefulUC
import requests
import random


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
                password += word + delimiter[random.randint(0, len(delimiter)-1)]

    return password



class SwitchOption(ft.Row):
    def __init__(self, text_options, page):
        super().__init__()
        self.text = text_options
        self.page = page

        

        self.controls = [
            ft.Container(
                content = self.txt,
                alignment=ft.alignment.center_left,
                width = 200,
                height = 50
            ),
            ft.Container(
                content = self.switch,
                width = 200,
                alignment=ft.alignment.center_right
            )
        ]

    



def main(page: ft.Page):
    page.title = "Password Generator"
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.window_width = 400        
    page.window_height = 400       
    page.window_resizable = False

    
    isRandom = False
    # random toggle change state
    def change_state():
        if random_switch.value:
            txt.value = "Random Password"
        else: 
            txt.value = "Memorable Password"

        isRandom = random_switch.value

        page.update()

    # generate the password 
    def get_pass(e):
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
        password = generate_password(params)
        pass_field.value = password
        page.update()

    # where the generated password will be
    pass_field = ft.TextField(adaptive=True, label="Generated Password", read_only=True)
    
    # Manage Random/Memorable Password Toggle
    txt = ft.Text("Memorable Password")
    random_switch = ft.Switch(width=150, on_change=lambda a: change_state())
    random_switch_row = ft.Row([
        ft.Container(
            content = txt,
            alignment=ft.alignment.center_left,
            width = 200,
            height = 50
        ),
        ft.Container(
            content = random_switch,
            width = 200,
            alignment=ft.alignment.center_right
        )
    ])

    # special character toggle 
    on_off = "off"
    

    def toggle_special():
        global on_off
        if special_switch.value:
            on_text.value = f"Special Characters: On"
        else:
            on_text.value = f"Special Characters: Off"
        page.update()

    on_text = ft.Text("Special Characters: Off")
    special_switch = ft.Switch(on_change=lambda a: toggle_special())
    special_chars = ft.Row([
        ft.Container(
            content=on_text,
            width = 154,
            alignment=ft.alignment.center_left
        ),
        ft.Container(
            content = special_switch,
            width = 200,
            alignment=ft.alignment.center_right
        )
    ])

    def dropdown_change(e):
        print(e.control.value)

    opts = ["Numbers", "Spaces", "Hyphens", "Colons", "Special Characters", "Numbers and Special Characters", "Commas", "Underscores"]
    opts = [ft.dropdown.Option(x) for x in opts]
    delimiter = ft.Row([
        ft.Container(
            content=ft.Text("Delimiter: "),
            width = 200
        ),
        ft.Container(
            
            content = ft.Dropdown(
                on_change=dropdown_change,
                options=opts,
                value=opts[0],
                width=150,
                alignment=ft.alignment.top_left
            ),
            width= 150,
        )
    ])

    

    page.add(
        ft.SafeArea(
            content=ft.ListView([
                ft.Container(
                    content=ft.Row(controls=[
                        pass_field,
                        ft.FloatingActionButton(icon=ft.icons.REFRESH)
                    ]),
                    height = 100
                ),
                random_switch_row,
                ft.Divider(height=9, thickness=3),
                
                delimiter,
                special_chars,

            ]),
        )
    )


if __name__ == '__main__':   
    ft.app(main)