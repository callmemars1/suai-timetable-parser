from parser_class import Parser
import logging
import json
import re


class RaspParamParser(Parser):

    def __init__(self, url):
        super().__init__(url)
        self.g_param = self.soup.find('div', class_='form').find('select')
        self.p_param = self.g_param.find_next('select')
        self.b_param = self.p_param.find_next('select')
        self.r_param = self.b_param.find_next('select')
        self.g_param_table = self.unpack_param(self.g_param)
        self.p_param_table = self.unpack_param(self.p_param)
        self.b_param_table = self.unpack_param(self.b_param)
        self.r_param_table = self.unpack_param(self.r_param)

    @staticmethod
    def unpack_param(string):
        """
        Returns unpacked values

        :param string: str like <option value="19">1011</option> ... <option value="352">Агеев М.П. - ассистент</option>
        :return list with dictionaries that look like: {'value': value, 'text': text}
        :rtype list
        """
        table = []
        regexp = r'<option value="(.*)".*>(.*)<.*'
        for sub_string in string:
            match = (re.search(regexp, str(sub_string)))
            if match is not None:
                value = int(match.group(1))
                text = str(match.group(2))
                table.append(
                    {'value': value,
                     'text': text}
                )
        return table

    @staticmethod
    def save_list(table, table_path, indent=2, ensure_ascii=False):
        with open(table_path, 'w') as file:
            json.dump(table, file, indent=indent, ensure_ascii=ensure_ascii)


if __name__ == '__main__':
    parser = RaspParamParser('https://rasp.guap.ru/')

    parser.save_list(parser.g_param_table, 'g_param_table.json')
    parser.save_list(parser.p_param_table, 'p_param_table.json')
    parser.save_list(parser.b_param_table, 'b_param_table.json')
    parser.save_list(parser.r_param_table, 'r_param_table.json')
