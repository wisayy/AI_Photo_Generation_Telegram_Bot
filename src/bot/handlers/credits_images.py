

# Список изображений для покупки кредитов
credits_list = [
    {"credits": 10, "image_link": "https://sun9-59.userapi.com/c909328/u253345731/docs/d23/56789c6a22c4/10_credits.jpg?extra=U4bS1tN9R_gAAeSmlzDuf6HHU7InUYbltxZhS_M3ptjjso-EmeZp9BSEK8D1reExDp5apSL9SoA9c7O1YL1FiOW0NXy9G_ttAxi1U9eYVq5g284W4IqvTSWkDwB8J6fMxxPvntZ98dMjgab3oP06Fzfu"},
    {"credits": 20, "image_link": "https://psv4.userapi.com/c909618/u253345731/docs/d7/6b59a8529308/20_credits.jpg?extra=6MrASeqXuYlkHjoZViltnSh0sNlfD-h0QN81EaxXpvbjrtE1QODLg-M2t1cRU63XHAYtNvRD1NEj2ZmTiFG6RyLBu_mFC_1Hndhv87dQwHn1cOJc7FqzZqmDmYGcRf6UcxKlvdRKmL45AphNiLK8xqAQ"},
    {"credits": 50, "image_link": "https://psv4.userapi.com/c909628/u253345731/docs/d13/c1fac84aa782/50_credits.jpg?extra=KR-Gt7CVvgI7lRzpjevhkB9UGKcCOW3g7qcuclis2qcCGCdSjg-qA_5XWT9RF-gfmPdK9_nRj-MdKcJK8AjCZXwvDz2ZwGq0qrv7FcB1yAys9IgawwmdyiTDDICoSaAYhuHj9W6c4jAMwlRK5nJwmyC5"},
    {"credits": 100, "image_link": "https://psv4.userapi.com/c237331/u253345731/docs/d49/d41fc338d75d/100_credits.jpg?extra=LjggRt__4YafM4WK5j8cuHoiI9ScLKI0hl4u3ZSgp0KQKrAd_x0QuFeH_aJD-aORyTQCfAGxfxpUKFrFW6UMHiJRmHSL6LJ8B3VQhYAGCsM05DoMDzGQKYkYBVUShsvGhhEODl-xlTaaCwfv2hsqGr9u"},
    {"credits": 500, "image_link": "https://psv4.userapi.com/c909628/u253345731/docs/d46/0b55a25e8e41/500_credits.jpg?extra=mrHFfJ-gAGSJwOGC9dkn92VMtKb6trQSDZmuFaZK_RUJCESgDYdGk_TX8VHCtInyBshp7Jk4LfeI8QCEbm9FAKDMtLOJI2IEH1fAoEPL16C6YJxqyjk6VmZ4uFaUQMy5QeepBisbMJG77Yufvmtmuo5P"},
    {"credits": 1000, "image_link": "https://psv4.userapi.com/c909518/u253345731/docs/d49/b6f0bdcd36ca/1000_credits.jpg?extra=fSgz0cM10WPlIcU1XuEe_gU1CsQfwCCcLgZUL_MEce5SFYyqWd-lEhPoktWgd-3a10XCGiqW3Y996CwTKEKCFSETT8Ne5qx5dC8B6DEnafypFZvNjxlaBysQ-xAuga9fwVObwv-iuVEsDKA96etKAjvr"},
    {"credits": 3000, "image_link": "https://psv4.userapi.com/c236331/u253345731/docs/d5/15d908ddc0c8/3000_credits.jpg?extra=XUHrb4mhkL7Ckw_wLktyHng-N7KptpzZQFkc9yWS9Vgqz7vvynZgOmDsnuqQKprSeN4ciL3PYFUy6iSJo0KgkdKFfNUkX1zxkl8IiiI8KSds3hAFC1iGFxBYjGExRCMgewtpjErBYAp6k4oqOd69D8fn"}
]

async def get_image_link(selected_credit_option):
    # Поиск ссылки на изображение по выбранному количеству кредитов
    for credit_option in credits_list:
        if credit_option["credits"] == selected_credit_option:
            return credit_option["image_link"]
