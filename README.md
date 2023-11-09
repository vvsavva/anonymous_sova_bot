# anonymous_sova_bot
[Anonymous telegram bot](https://t.me/anonymous_sova_bot) for communication by vsavva

[Анонимный телеграмм бот](https://t.me/anonymous_sova_bot) для общения
![image](https://github.com/vsavva/anonymous_sova_bot/assets/67558876/f1491d7c-9227-46b6-8082-245c2019cf00)
# Settings Настройка 
Setting up the bot to work correctly

Настройка правильной работы бота

First of all we need to receive an access token.

Прежде всего нам необходимо получить токен доступа.

```

pip install yoomoney --upgrade

```

Installing the yoomoney library

Устанавливаем библиотеку yoomoney



Log in to your YooMoney wallet with your username. If you do not have a wallet, [create it](https://yoomoney.ru/reg).

Войдите в свой кошелек YooMoney под своим именем пользователя. Если у вас нет кошелька, [создайте его](https://yoomoney.ru/reg).

Go to the App [registration page](https://yoomoney.ru/myservices/new).

Перейдите на страницу [регистрации приложения](https://yoomoney.ru/myservices/new).

Click the Confirm button.

Нажмите кнопку «Подтвердить».

Follow all steps from the program.

Выполните все шаги программы.
```

from yoomoney import Authorize
Authorize(
      client_id="YOUR_CLIENT_ID",
      redirect_uri="YOUR_REDIRECT_URI",
      scope=["account-info",
             "operation-history",
             "operation-details",
             "incoming-transfers",
             "payment-p2p",
             "payment-shop",
             ]
      )

```
Next, fill in the payment token, database name name.bd, wallet number
yoomoney, channel name from the link where the bot must be located

Далее заполнить платежный токен, название базы данных название.bd, номер кошелька
yoomoney, название канала из  ссылки где обязательно должен состоять бот

![image](https://github.com/vsavva/anonymous_sova_bot/assets/67558876/0528a1d2-8983-4046-b180-73940726a8b7)

