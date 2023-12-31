storage_options = {
    "YM": {
        "YM:A": "Софьино",
        "YM:B": "Томилино",
        "YM:C": "Бережковская набережная",
        "YM:D": "Царицыно",
        "YM:other" : "Другое"
    },
    "WB": {
        "WB:A": "Коледино",
        "WB:B": "Электросталь",
        "WB:C": "Подольск",
        "WB:D": "Алексин",
        "WB:E": "Обухово",
        "WB:F": "Внуково",
        "WB:G": "Вешки",
        "WB:other" : "Другое"
    },
    "OZ": {
        "OZ:A": "Пушкино 1",
        "OZ:B": "Пушкино 2",
        "OZ:C": "Хоругвино",
        "OZ:D": "Саларьево",
        "OZ:E": "Истра",
        "OZ:F": "Щербинка",
        "OZ:G": "Львовский",
        "OZ:H": "Жуковский",
        "OZ:I": "Химки",
        "OZ:other" : "Другое"
    }
}
storage_names = {
    "YM":"Яндекс Маркет",
    "OZ":"Ozon",
    "WB":"Wildberries"
}

package_names = {
    "BOX":"Коробки",
    "PAL":"Паллеты"
}
price_list = '''Склады вайлдберис :
Коледино 
Электросталь
Подольск
Алексин 
Обухово 
Внуково
Вешки

Склады Озон:
Хоругвино
Пушкино 1
Пушкино 2
Саларьево
Истра
Щербинка
Львовский
Жуковский
Химки

Склады Яндекс Маркет:
Софьино
Томилино
Бережковская набережная
Царицыно 

1-3 коробки-2000р
4-7коробок-2500
До 10 коробок-3000
До 20 коробок-4000
20-30 коробок-4500
30-45к-5000
45-60к-6500

1-2 паллета-5000
3-5 паллет-5500
6-7 паллет-6500
8-10 паллет-8500
11-13 паллет-12000
До 15 паллет-14500

Хоругвино озон цены:
1-6 коробок -3000
7-10 коробок-4000
По палетам так же как и остальные склады

Паллет -300р
Палетирование-300р

Другие склады - другие цены'''

support_contacts = "Для технической поддержки пишите разработчику в ЛС (@EgorRy)Для поддержки по поводу заказа пишите (@AlenaKoroleva088)"
operator = 1202939724
package_options ={
    
    "BOX": {
        "BOX:1": "1-3 коробки-2000р",
        "BOX:2": "4-7коробок-2500",
        "BOX:3": "До 10 коробок-3000",
        "BOX:4": "До 20 коробок-4000",
        "BOX:5": "20-30 коробок-4500",
        "BOX:6": "30-45 коробок-5000",
        "BOX:7": "45-60 коробок-6500"
    },
    "PAL": {
        "PAL:1": "1-2 паллета-5000",
        "PAL:2": "3-5 паллет-5500",
        "PAL:3": "6-7 паллет-6500",
        "PAL:4": "8-10 паллет-8500",
        "PAL:5": "11-13 паллет-12000",
        "PAL:6": "До 15 паллет-14500",
    }
}

database_path = "MAIN.sql"
database_user_name = "root"
database_user_password = "root"
force_new_database = False
delay = 3

admins = []