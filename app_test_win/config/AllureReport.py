import allure


def show_pic(path, case_name):
    """
    report show images
    """
    with open(path, "rb") as file:
        file = file.read()
        allure.attach(file, case_name, attachment_type=allure.attachment_type.JPG)


def show_url(url):
    with allure.step("url:"):
        allure.attach(url, "URL地址")


def show_headers(headers):
    with allure.step("headers"):
        allure.attach(str(headers), "headers")
        print(f'header: \n {headers}')


def show_step(name, ste_data):
    with allure.step(name):
        allure.attach(ste_data, name)
        print(f'{name}：\n {ste_data}')


def show_response(response):
    with allure.step("response"):
        allure.attach(response, "response")
        print(f'response：\n {response}')


def show_except_response(response):
    with allure.step("预期结果"):
        allure.attach(response, "预期结果")
        print(f'预期结果：\n {response}')








