Описание
=======

Используется для автоматического тестирования миссиий на сервере через веб-сокеты.


Как пользоваться
======

    
1. Запуск
------

Для удобства работы эта утилита инкапсулированна в докер контенер, 
для начала использования нужно собрать докер образ или сказать существующий:

**docker pull checkio/editor-tester** - для скачивания

**./manage.sh build** – для сборки локально

Для запуска тестов необходимы два обязательный параметра: домен, ключ сессии, 
и один необязательный: ключ базовой авторизации, если тестируемый домен находится за сервером, 
на котором включена базовая авторизация.
 
 
Команда для запуска:
**./manage.sh run -d=\<alias_or_domain> -s=\<session_key> [-b=\<basic_auth_key>]**

*alias_or_domain* - может быть: master, test1, test2 или можно явно передать домен *test3.empireofcode.com*

*session_key* - ключ сессии пользователя, под которым будет выполнятся запуск миссии. 
ВАЖНО! так как под этим пользователем будут запскаться миссии, соответственно у него буду решены 
задачи и получены все ачивки.

Узнать этот ключ можно так:
 
1. Авторизоваться на сайте под пользователем с под которого будут проходить тесты

2. Открыть в браузере консоль разработчика

3. Во вкладке Resources, открыть cookie -> необзодимы домен, из списка выбрать строку с именем *sessionid*

и значение этой строки будет необходимое значение

*basic_auth_key* – этот трибут можно также получить в консоле разработчика:
во вкладке Network отркрыть информацию о запросе к документу и в параметрах *Request Headers*
должна присутствовать строка вида:

**Authorization:Basic ZW1waXJlOlkwdVNoYWxsTm90UGFz**

последовательность символов это и есть наш ключ.



Примеры запуска тестов:

**./manage.sh run -d=master -s=nvb6327fke8srrx9u1klyat0dgnm**

**./manage.sh run -d=test1 -s=d90u6xfwfm5d77f427fnczyzqfslhv3 -b=ZW1waXJlOlkwdVNoYWxsTm90UGFzcz**



2. Добоваление тестов
------

В папке *tests_data* для каждой миссии необходимо созать файт *\<mission_slug>.py*

Формат содежимого следующий:

    TESTS = [{
        'name': <some_name_for_test>,
        'mission_slug': '<mission_slug>',
        'code': <solution>,
        'success': <True or False>   
    },
    ...
    ]

Например:

    TESTS = [{
        'name': 'even_last__success',
        'mission_slug': 'even_last',
        'code': '''
    def even_last(array):
        return sum(array[::2]) * array[-1] if array else 0
    ''',
        'success': True
    },
    {
        'name': 'even_last__fail',
        'mission_slug': 'even_last',
        'code': '''
    def even_last(array):
        return 0
    ''',
        'success': False
    },
    ]
    