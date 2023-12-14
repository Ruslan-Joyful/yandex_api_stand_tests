import data
import requests
import sender_stand_request


# Получение токена
def get_new_user_token():
    response = sender_stand_request.post_new_user(data.user_body)
    return response.json()["authToken"]


# Функция для изменения значения в параметре name в теле запроса
def get_kit_body(new_name):
    # Копируется словарь с телом запроса из файла data
    current_body = data.kit_body.copy()
    # Изменение значения в поле name
    current_body["name"] = new_name
    # Возвращается новый словарь с нужным значением name
    return current_body


# Функция для позитивной проверки
def positive_assert(new_name):
    # В переменную auth_token сохраняется полученный токен
    auth_token = get_new_user_token()
    # В переменную kit_body сохраняется обновлённое тело запроса
    kit_body = get_kit_body(new_name)
    # В переменную kit_response сохраняется результат запроса на создание набора:
    kit_response = sender_stand_request.post_new_client_kit(kit_body, auth_token)
    # Проверяется, что код ответа равен 201

    assert kit_response.status_code == 201
    assert kit_response.json()['name'] == new_name
    print(kit_response.json())


# Функция негативной проверки, когда в ответе ошибка про символы
def negative_assert_code_400_symbol(new_name):
    # В переменную auth_token сохраняется полученный токен
    auth_token = get_new_user_token()
    # В переменную kit_body сохраняется обновлённое тело запроса
    kit_body = get_kit_body(new_name)
    # В переменную kit_response сохраняется результат запроса на создание набора:
    kit_response = sender_stand_request.post_new_client_kit(kit_body, auth_token)
    # Проверяется, что код ответа равен 400

    assert kit_response.status_code == 400
    assert kit_response.json()['name'] == new_name


# Функция для негативной проверки, когда в ответе ошибка: "Не все необходимые параметры были переданы"
def negative_assert_code_400_no_name(kit_body):
    # В переменную auth_token сохраняется полученный токен
    auth_token = get_new_user_token()
    # В переменную kit_response сохраняется результат запроса на создание набора:
    kit_response = sender_stand_request.post_new_client_kit(kit_body, auth_token)
    # Проверяется, что код ответа равен 400

    assert kit_response.status_code == 400


# Тест 1. Успешное создание набора. Параметр name состоит из 1 символа
def test_positive_assert():
    positive_assert("a")

# Тест 2. Успешное создание набора. Параметр name состоит из 511 символов
def test_positive_assert():
    positive_assert("AbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabC")

# Тест 3. Ошибка. Количество символов меньше допустимого. Параметр name состоит из 0
def test_negative_assert_code_400_symbol():
    negative_assert_code_400_symbol("")

# Тест 4. Ошибка. Количество символов больше допустимого. Параметр name состоит из 512 символов
def test_negative_assert_code_400_symbol():
    negative_assert_code_400_symbol("AbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcD")

# Тест 5. Успешное создание набора. Параметр name состоит из английских букв
def test_positive_assert():
    positive_assert("QWErty")

# Тест 6. Успешное создание набора. Параметр name состоит из русских букв
def test_positive_assert():
    positive_assert("Мария")

# Тест 7. Успешное создание набора. Параметр name состоит из спецсимволов
def test_positive_assert():
    positive_assert("№""%@,")
    
# Тест 8. Успешное создание набора. Параметр name включает в себя пробелы
def test_positive_assert():
    positive_assert("Человек и КО")

# Тест 9. Успешное создание набора. Параметр name состоит из цифр
def test_positive_assert():
    positive_assert("123")

# Тест 10. Ошибка. Параметр name не передан в запросе
def test_negative_assert_code_400_no_name():
    # Копируется словарь с телом запроса из файла data в переменную kit_body
    kit_body = data.kit_body.copy()
    # Удаление параметра name из запроса
    kit_body.pop("name")
    # Проверка полученного ответа
    negative_assert_code_400_no_name(kit_body)

# Тест 11. Ошибка. Передан другой тип параметра. Тип параметра name: число
def test_negative_assert_code_400_number_type():
    # В переменную kit_body сохраняется обновлённое тело запроса
    kit_body = get_kit_body(12)
    # В переменную user_response сохраняется результат запроса на создание пользователя:
    response = sender_stand_request.post_new_user(kit_body)
    # Проверка кода ответа
    assert response.status_code == 400