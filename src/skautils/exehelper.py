import os

import toml


class CheckExeVersion:
    """
    Помогает сопоставить текущую версию файла и версию, записанную в toml file
    Если версия не совпадает, класс остановит выполнение кода под классом
    """

    exe_name: str
    version: str
    versions_toml_path: str
    exe_path: str
    creator_email: str
    open_exe_folder: bool

    def __init__(self, exe_name: str, version: str, versions_toml_path: str, exe_path: str, creator_email: str,
                 open_exe_folder: bool = False) -> None:
        """
        1. Инициализирует класс
        2. Проверяет версию
        3. Если версия совпадает, не делает ничего, иначе останавливает программу
        :param exe_name: название файла. Должно совпадать с названием, которое лежит в файле по адресу
                            versions_toml_path
        :param version: версия текущего файла
        :param versions_toml_path: путь к файлу, где прописаны последние версии
        :param exe_path: путь к exe
        :param creator_email: электронная почта создателя
        :param open_exe_folder: открывать или не открывать папку с exe
        """
        self.exe_name = exe_name
        self.version = version
        self.versions_toml_path = versions_toml_path
        self.exe_path = exe_path
        self.creator_email = creator_email
        self.open_exe_folder = open_exe_folder

        self.check_last_version()

    def __get_last_version_and_check(self) -> tuple[bool, str]:
        """
        Проверяет является ли self.version последней версией

        :raises KeyError: если наш файл не имеет версии в toml-файле с версиями

        :return:
            [0] - true, если версия в self.versions_toml_path == self.version
            [1] - версия из self.versions_toml_path
        """
        last_version: str
        is_last_version: bool = False

        parsed_toml = toml.loads(self.versions_toml_path)

        if self.exe_name not in parsed_toml:
            raise KeyError(f"{self.exe_name} не имеет версии")

        last_version = parsed_toml[self.exe_name]

        return is_last_version, last_version


    def __open_folder_with_new_exe(self) -> None:
        """
        Открывает папку с последней версией exe-файла
        :return:
        """
        os.startfile(self.exe_path)

    def __stop_program(self, last_version: str) -> None:
        """
        Останавливает работу программы
        :param last_version: последняя версия файла

        :raises RuntimeError: при вызове

        :return: ничего
        """
        raise RuntimeError(f"Текущая версия {self.version} файла не является последней. Последняя версия {last_version}"
                           f"\nПоследняя версия находится по пути: {self.exe_path}"
                           f"\nПри возникновении вопросов, обратитесь к разработчику: {self.creator_email}")

    def check_last_version(self) -> None:
        """
        Проверка последней версии
        Если версия последняя, ничего не произойдет

        :raises RuntimeError: если версия не последняя
        """

        last_version: str
        is_last_version: bool

        last_version, is_last_version = self.__get_last_version_and_check()

        if not is_last_version:
            if self.open_exe_folder:
                self.__open_folder_with_new_exe()
            self.__stop_program(last_version)