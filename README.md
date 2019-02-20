# 1C-Retail-smoke-tests

Версия 0.30

1. Общие сведенья.
Программа для Windows писалась мной как учебная, ради удовольствия, для пробы своих возможностей на Питоне. Программа "пытается" поверхностно, автоматически тестировать(нажимать на кнопочки и гиперссылочки) 1C приложение (на примере 1С:Розницы), опубликованное в веб-клиенте. На других продуктах 1С программа может не работать совсем и требовать незначительных доработок .
Программа имеет 6 тестовых режимов работы: "savemenu", "open_forms", "scenario", "cursor", "go"," go_partial.

---

2. Подробно о режимах работы:
	"savemenu" - обходит меню 1С:Розницы, открывая и считывая подменю разделов. Выстроенную иерархию программа сериализует и сохраняет в свою папку с именем dict_main_elements.pickle.
	"open_forms" - читает файл dict_main_elements.pickle, затем обходит каждое подменю открывая и закрываю форму. После каждого нажатия пытается закрыть все открытое в 1С:Розница и затем снова открыть весь путь до следующего элемента в очереди. Делает скриншот если появилось окно 1С:Предприятие или сообщение пользователю. Пытается их закрыть и продолжить свой обход. Программу выгодно запускать под разными пользователями у которых разные профили 1С. 
	"cursor" - бесконечно выводит в консоль координаты браузера с открытой в нем 1С и координаты курсора мыши.
	"scenario" - (тестовый режим) примитивный способ создавать универсальные сценарии автотестирования. В каталоге с программой создаем текстовой файл с набором предопределенных команд и записанных координат курсора с помощью режима cursor. Пример создания примитивного сценария и описание доступных команд находится в файле example_scenario.txt.
После того как программа откроет 1С в браузере, нужно ввести в консольное окно имя файла со сценарием (должен быть в каталоге программы). 
При желании можно легко переписать данный режим для сценарного прощелкивания вообще чего угодно.
Хоть и убого, но вполне подходит для случаев когда нужно написать, что то быстро, что будет щелкать определенную последовательность в программе. Так же подходит(но нужно дорабатывать) если по каким то причинам не работают стандартные средства сценарного автотестирования.
	"go"  - пытается "прощелкивать" 1С:Розницу намного более глубоко чем режим "open_forms". Идет по меню разделов и каждый открывшийся раздел добавляет в очередь на детальное "прощелкивание".  Далее, если в каком то из разделов, гиперссылка или кнопочка, при нажатии на нее, открывает новое окно, так же добавляет его в очередь на "прощелкивание". Помнит путь из элементов которые нужно нажать что бы добраться до нужного окна. Будет работать пока не кончится список с найденными окнами. Сохраняет скриншоты так же как и в режиме "open_forms". Некоторые элементы формы может не найти из за фильтров отбора в коде, некоторые элементы может щелкать несколько раз из за недостатков того же фильтра. Использует в том числе и эмуляцию нажатий клавиатуры, поэтому тестирование можно легко сломать если набирать что то на компьютере одновременно с работой программы. Отлично находит системные ошибки для разных пользователей(профилей) когда спокойно работает на отдельном компьютере.
	"go_partial" - то же самое, что и go только при начале работы нужно указать раздел подменю по которому будет обход. Пример: Администрирование, Обслуживание("прощелкает" только его).
3. Подробнее о программе, ошибки в архитектуре.
Программа использует три зависимости: pywin32 для эмуляций нажатий мышью и тд., Pillow - участвует в создании скриншотов, Selenium - фреймворк для тестирования браузерных приложений. Все версии зависимостей указаны в файле requirements.txt.  
Программа написана по принципу: "выполняет свою функцию и ладно".
Ошибки, недоработки:
Один плохой класс на всю программу. 
Медленно.  (решено в версии: 0.30 - полностью переписан фильтр и способ обхода)
Неправильное использование "try/exception". 
Чрезмерно усложненная реализация. (упрощено  версия: 0.30)
Отсутствие юнит тестов.

Что бы я переделал:
Наметил бы архитектуру заранее.
Избавился бы от Pillow.
Реализовать запуск режима "scenario" на мониторе любого размера. Увеличить количество команд. Сделать так что бы сценарии были в отдельной папке и из одного сценария можно было вызывать другой сценарий. Сделать, что бы сценарий работал рекурсивно или повторялся. Сделать так что бы сценарий мог принимать параметры.
Искал более простые и универсальные способы отлавливать нужные окна.
Так же если бы речь шла о простом сайте, а не об 1С приложении - всего этого бы не понадобилось вообще. 
Достаточно было бы одного Селена. 
Так же и у 1С есть более удобные способы автотестирования своих приложений.
      
4. Для работы программы нужны:
Браузер chrome. 
Опубликованная на веб-сервере база 1С:Розницы.
 chromedriver.exe в папке с программой.
указать настройки в файле opt.txt (в папке с программой).
файл запуска: main.py. Для стабильной и быстрой работы, в 1С:Рознице должно быть включено отображение открытых вкладок в верхней части приложения.

Программа в своем коде много работает с "id" элементов html страницы. Поэтому, что бы использовать ее на других продуктах 1с или на сайтах - нужно проверить актуальны ли все "id" в коде для другого 1с или сайта. 
