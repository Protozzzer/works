# works

                                              Python Chat
                                       Что это и для чего делалось?
    Это Python - приложение, созданное в качестве тестового задания, а также для ознакомления с такими темами: socket (сокеты), 
    GUI на PyQt5, Threads(потоки), работа с базами данных на основе библиотеки MySQLdb с СУБД MySql, и, конечно же, 
    оттачивание навыков работы непосредственно с Python3.5+. Основные функции приложения: 
    
                          1) Возможность вести диалог двум и более клиентам посредством интерфейса чата, 
                             подключенных к одной локальной сети. 
                          2) Регистрация/авторизация пользователя.
                          3) Сохранение истории сообщений пользователей в чате независимо от перезагрузки 
                             сервера или выхода участников чата.
                            
                                                Установка
     Для того, чтобы инсталлировать приложение на Ваш Пк, понадобится средствами различных программ 
     (создать .exe файл можно при помощи pyinstaller, инсталлер можно создать средствами Inno Script Studio) создать инсталлер,
     в котором будут включены необходимые библиотеки для работы программы, а также дополнительно инсталлер установит необходимое 
     сопровождение для корректной работы: MySql Server, готовую к работе базу данных с таблицами(файл из проэкта), Python3.5+. 
     
                                    Что необходимо для того, чтобы запустить чат? 
                                    
     1) Создать .exe файл, и с ним отдельно закинуть в архив установщик MySql http://www.mysql.ru/download/, установкщик Python 
     https://www.python.org/downloads, также файл бд с таблицами, а также файл readme.txt с инструкцией по установке. 
     2) Создать инсталлер, куда поместить все вышеперечисленное ПО, настроив установку данного ПО автоматически.
     
                                      Какие технологии были использованы, причины. 
     1) Чат изначально был задуман на локальную работу между подключенными ПК. Соответственно, для реализации нужно было изучить
     socket. Это базовая библиотека Python для организации работы сервера и клиента, прослушки и передачи сообщений. На данный момент
     существуют и другие библиотеки, с улучшенными возможностями, также фреймворки, организующие более удобную работу, однако взор был 
     остановлен на socket, поскольку это необходимая база для тех людей, кто хочет познакомится с технологиями сетей, понять процессы взаимодействия
     сервера и клиента. Выбор пал на технологию сети UDP - протокол датаграммной передачи данных, поскольку он более легок в реализации, 
     хорошо подходит для начального освоения. Также можно было применить протокол TCP/IP. В чем различие? TCP/IP всегда делает запрос на установку соединения
     перед отправкой сообщения, соответственно гарантирует доставку данных, надежность.  UDP не использует такой механизм "рукопожатия" - 
     соответственно сообщения будут отправляться без установки предварительного соединения, что сказывается на надежности. Сообщения могут не дойти, 
     либо же прийти не в том порядке. Однако UDP обеспечивает более высокую скорость передачи данных. Разумнее было бы с точки зрения безопасности и надежности
     (что сообщение точно дойдет от одного клиента к другому) применить протокол TCP/IP, однако более подробное изучение применения этого протокола в библиотеке 
     socket сводится к ошибкам в работе - для корректной работы необходимо подключать acyncio Python, что повлекло бы за собой дополнительный расход времени на 
     изучение данного раздела. Наш чатик прост, без лишних перегрузок, является скорее тестовым вариант для изучения - для понимания основ работы с библиотекой
     socket, на мой взгляд, UDP достаточно. Были созданы два файла Python - один описывает работу сервера, другой работу клиента. Соответственно, при помощи socket 
     сервер на определенных хосте и порту слушает, ждет входящих подключений, клиентов. Клиент отправляется сообщение, сервер принимает сообщение и затем пересылает
     его другому нужному клиенту. Фактически, сервер регулирует передачу данных.
     2)  Для авторизации и регистрации пользователя, разумеется нужна локальная база данных. Поскольку СУБд MYsql многим начинающим программистам весьма известна,
     достаточно удобна, она и была выбрана в проекте, тем более, ранее уже приходилось работать с MySql, только на PHP. Была создана в оболочке MYsql Client при помощи простых запросов 
     необходимая для работы таблица для сохранения логина и пароля пользователя. Пароль в поле таблицы бд зарегистрированного пользователя сохраняется в 
     зашифрованном виде при помощи md5 - для обеспечения конфиденциальности, а также для уменьшения риска расхищения личных данных. Библиотека для md5 Python - 
     hashlib. Она содержит также и другие алгоритмы шифрования данных. 
     3) Для сохранения сообщения пользователей в чате в любое время (во время их отсутствия), либо же во время перезапуска сервера, была создана таблица в бд для сохранения
     текста сообщений, даты и времени т.д. Пользователь, в любой момент зашедший в чат, может увидеть осуществленную им и другими пользователями ранее переписку. В то же время,
     пока пользователь находится непосредственно в чате, он получает сообщения от других пользователей напрямую с сервера, посредством socket. 
     4) Для создания графического интерфейса приложения чата была использована библиотека PyQt5. Это обосновывается личным выбором - я уже имела малый опыт работы с ней, захотелось
     вспомнить и улучшить знания и навыки работы, тем более, она весьма удобна и интуитивно понятна. 
     5) Thread - потоки. Для бесперебойной работы нескольких клиентов без задержек и ожиданий друг друга(клиентов) нужны были простейшие потоки. Каждый клиент - отдельный поток.
     Клиентов может быть много, сервер один. 
     6) Написанием кода занималась в Ide Pycharm. Просто и удобно. 
     7) Весь код и работу приложения можно описать так: в отдельном Gui открывается сервер server.py, в нем можно отслеживать информацию о пользователях, однако форма спрятана от пользователя. 
     Если нужно отследить изменения, можно программно в коде закомментировать строку window.hide(). В другой форме main.py (последующие формы login.py, CharForm.py) открывается окошко регистрации и авторизации, 
     после этих действий открывается следующая форма непосредственно самого чата - она простая, без излишеств, предполагает окошко для созерцания пришедших и отправленных сообщений, текстовое поле для многострочного 
     ввода сообщения со стороны текущего пользователя и кнопку отправить. Так можно открыть несколько форм клиентов на одном хосте (пк), либо на разных пк по локалке. Программно сервер настроен на прослушку с разных хостов.
     Так клиенты могут общаться друг с другом. 
     
                                         Сложности, или, куда же без них?
     Освоение любой библиотеки, технологии, сценария требует времени, усилий, сноровки, работу над возникшими ошибками, концентрации на деле. 
     Разумеется, они были. Во-первых, ранее, до создания простейшего чата, я не работала с сокетами. Это помогло мне вспомнить основные протоколы сети, разобраться глубже
     во взаимодействии сервера-клиента. Во-вторых, бфли знания и опыт работы с sql, однако сочетания sql + Python было в новизну. С этим почти не было трудностей, библиотека для
     работы с MySql очень проста, в ней нет ничего лишнего. PyQt5 я ранее использовала, однако многое подзабылось, были проблемы с синхронизацией PyQt5 + Thread + socket. Однако 
     проблема нашла свое решение, пусть и не в кратчайшие сроки. Что касается библиотеки threading - изучала ранее в теории, было понимание, как и что работает, теперь же это было применено
     на практике. Алгоритм шифрования md5 был мне ранее знаком, потому нашла библиотеку для его использования в Python. А что же касается потраченного времени? Больше всего времени ушло на выяснения
     причины и устранения ошибок, то и дело сыпавшихся в PyCharm. На то удел новичков, учиться на ошибках. В общей сложности было потрачено 4 дня. 
     
                                              Источники информации
     Множество различных сайтов и сравнение информации друг с другом. Не все пишут правильные вещи, лишь документация верна. Потому оф. документация по Python - один из источников информации, ссылка
     https://www.python.org  Также пример работы с socket - https://www.youtube.com/watch?v=MPjgHxK8k68. Некоторую часть информации по sql почерпнула отсюда https://www.sql.ru/docs/  и еще много других 
     источников. 
                                              Дальнейшие доработки
     Рациональнее безопасная передача данных без возможных потерь - перевод на acyncio+tcp/ip. Сделать чат не только по локалке, но и через интернет, можно также сделать чат-форум через связку, например, 
     Python + Django. Улучшение качества кода. Улучшения возможностей самой переписки, со стороны GUI. Добавления поля почты при регистрации в бд и в форме, добавление кнопки "Забыли пароль", соответственно 
     добавления модуля работы в Python рассылки на почту кода для восстановления данных входа. И т.д.
                                              
                                             
