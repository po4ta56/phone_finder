import requests
import re

from typing import Set


class PhoneFinder:

    local_code = '495'
    international_code = '8'
    len_local_phone = 7
    len_international_phone = 11

    def find(self, content: str) -> Set[str]:
        '''
        parse content and return list of 'raw' phones
        '''
        pattern = self.__get_pattern()
        list_phones = list()
        matches = re.finditer(pattern, content, re.MULTILINE)
        for match in matches:
            for i in range(3, 5):
                raw_phone = match.group(i)
                if raw_phone:
                    list_phones.append(raw_phone)
        return set(list_phones)

    def __get_pattern(self) -> str:
        pattern = r'(>|^|\s)((\+?[78](?:[-() ]*\d){#len_international_phone#})|((?:[-]*\d){#len_local_phone#}))(<|$|\s)'
        pattern = pattern.replace(
                    '#len_international_phone#',
                    str(self.len_international_phone-1)
        )
        pattern = pattern.replace(
                    '#len_local_phone#',
                    str(self.len_local_phone)
        )

        return pattern

    def normalize(self, raw_phone: str) -> str:
        '''
        clear 'raw' phone
        '''
        self.__check_len()
        phone = ''
        only_digit = ''.join(filter(str.isdigit, raw_phone))
        if len(only_digit) == self.len_local_phone:
            phone = f'{self.international_code}{self.local_code}{only_digit}'
        elif len(only_digit) == self.len_international_phone-1:
            phone = f'{self.international_code}{only_digit}'
        elif len(only_digit) == self.len_international_phone:
            phone = f'{self.international_code}{only_digit[1:]}'
        else:
            raise ValueError('Wrong phone length!')

        return phone

    def __check_len(self):
        len_local = len(self.international_code) \
                    + len(self.local_code) \
                    + self.len_local_phone \

        if len_local != self.len_international_phone:
            raise ValueError('Wrong local code length!')

    def get_phones(self, content: str) -> Set[str]:
        '''
        return the list of found normalized phones
        '''
        return set(list(map(self.normalize, self.find(content))))


if __name__ == "__main__":

    list_of_url = [
        'https://repetitors.info/',
        'https://hands.ru/company/about/',
        'http://сакмарскийрайон.рф/',
        'http://сакмарскийрайон.рф/Pages.aspx?id=36',
        'http://сакмарскийрайон.рф/Pages.aspx?id=535',
        'http://www.uralakva.ru/index.php?a=iv&id=4&pg_id=4'
    ]

    pf = PhoneFinder()
    pf.len_local_phone = 6
    pf.local_code = '3532'

    for url in list_of_url:
        rs = requests.get(url)
        lsp = pf.get_phones(rs.text)
        print(url, lsp)
