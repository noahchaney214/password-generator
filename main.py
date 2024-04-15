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
    
def get_delim(delimiter) -> str:
    special_chars = '[@_!#$%^&*()<>?/\\|}{~:]'
    match delimiter:
        case "Numbers":
            return str(random.randint(1, 9))
        case "Spaces":
            return ' '
        case "Hyphens":
            return '-'
        case "Colons":
            return ':'
        case "Special Characters":
            return special_chars[random.randint(0, len(special_chars)-1)]
        case "Numbers and Special Characters":
            coin_flip = random.randint(0, 1)
            return special_chars[random.randint(0, len(special_chars)-1)] if bool(coin_flip) else str(random.randint(1, 9))
        case "Commas":
            return ','
        case "Underscores":
            return '_'
        case None:
            return ''


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
                if caps == "Capitalise":
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
                if caps == "Capitalise":
                    coin_flip = bool(random.randint(0,1))
                    if coin_flip:
                        word = word.upper()
                elif caps == "Camel Case":
                    word = camel_case(word)
            
            if words[-1].lower() == word.lower():
                password += word + (str(random.randint(0, 9)) if params["include_nums"] else '')
            else:
                password += word + (str(random.randint(0, 9)) if params["include_nums"] else '') + get_delim(delimiter)

    return password

isRandom = False
def main(page: ft.Page):
    page.title = "Password Generator"
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.window_width = 400        
    page.window_height = 400       
    page.window_resizable = False

    params = {
        "random": False,

        "special_chars": True,
        "caps": "Lower",
        "nums": True,
        "num_chars": 12,

        "num_words": 4,
        "include_nums": False,
        "lower": False,
        "delimiter": "Numbers"
    }

    # generate the password 
    def get_pass(e):
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
    
    def toggle_special():
        global on_off
        if special_switch.value:
            on_text.value = f"Special Characters"
        else:
            on_text.value = f"Special Characters"
        params["special_characters"] = special_switch.value
        page.update()

    on_text = ft.Text("Special Characters")
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
        params["delimiter"] = e.control.value

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
                value="Numbers",
                width=150,
                alignment=ft.alignment.top_left
            ),
            width= 150,
        )
    ])

 
    # random toggle change state
    def change_state():
        global isRandom
    
        if random_switch.value:
            txt.value = "Random Password"
        else: 
            txt.value = "Memorable Password"

        isRandom = random_switch.value
        
        params["random"] = random_switch.value

        change_options()

        page.update()

    
    def change_count(e):
        if isRandom:
            e.control.min = 4
            e.control.max = 64
            e.control.divisions = 60
            count_txt.value = f"{int(e.control.value)} characters"
            params["num_chars"] = int(e.control.value)
        else:
            e.control.min = 2
            e.control.max = 8
            e.control.divisions = 6
            count_txt.value = f"{int(e.control.value)} words"
            params["num_words"] = int(e.control.value)
        page.update()

    count_txt = ft.Text("4 words")

    count = ft.Row([
        ft.Container(
            content=count_txt,
            width=100
        ),
        ft.Container(
            content = ft.Slider(
                value=4,
                min=2, 
                max=8, 
                divisions=6, 
                label="{value}",
                on_change=change_count
            ),
            width=275
        )
    ])

    # capitalize switch for memorable password
    def capitalise(e):
        value = ""
        if e.control.value == 0:
            value = "Lower"
        elif e.control.value == 1:
            value = "Capitalise"
        else:
            value = "Camel Case"
        e.control.label = value
        capitalize_txt.value = value
        params["caps"] = value
        page.update()

    capitalize_txt = ft.Text("Capitalise")
    capitalize = ft.Row([
        ft.Container(
            content=capitalize_txt,
            width=154
        ),
        ft.Container(
            content=ft.Slider(
                min=0,
                max=2,
                divisions=2,
                value=1,
                label=capitalize_txt.value,
                on_change=capitalise
            ),
            width=200,
            alignment=ft.alignment.center_right
        )
    ])


    # capitals switch for random password
    def capitals_change(e):
        params["caps"] = e.control.value
        page.update()

    capitals = ft.Row([
        ft.Container(
            content=ft.Text("Capital Letters"),
            width=154
        ),
        ft.Container(
            content=ft.Switch(
                on_change=capitals_change
            ),
            width=200,
            alignment=ft.alignment.center_right
        )
    ])


    # include numbers switch for both password types
    def include_nums(e):
        params["include_nums"] = e.control.value
        params["nums"] = e.control.value
        page.update()

    include = ft.Row([
        ft.Container(
            content=ft.Text("Include Numbers"),
            width=154
        ),
        ft.Container(
            content=ft.Switch(
                on_change=include_nums
            ),
            width=200,
            alignment=ft.alignment.center_right
        )
    ])

    
    memorable = ft.ListView([
        count,
        delimiter,
        capitalize,
        include
    ])

    random_pass = ft.ListView([
        count,
        special_chars,
        capitals,
        include
    ])
    global options
    options = memorable

    def change_options():
        
        global options
        if isRandom:  # Check if the random switch is toggled
            options = random_pass
        else:
            options = memorable
        page.update()


    page.add(
        ft.SafeArea(
            content=ft.ListView([
                ft.Container(
                    content=ft.Row(controls=[
                        pass_field,
                        ft.FloatingActionButton(icon=ft.icons.REFRESH, on_click=get_pass)
                    ]),
                    height = 100
                ),
                random_switch_row,
                ft.Divider(height=9, thickness=3),
                options
            ]),
        )
    )


if __name__ == '__main__':   
    ft.app(main)