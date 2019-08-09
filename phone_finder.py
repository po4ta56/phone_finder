
import re

from typing import Set


class PhoneFinder:
    len_local_phone = None
    local_code = None
    len_international_phone = None
    international_code = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.__compiled = False

    def compile_regexp(self):
        pattern = self.get_pattern()
        self.__regex = re.compile(pattern, re.MULTILINE)
        self.__compiled = True

    def find(self, content: str) -> Set[str]:
        '''
        parse content and return list of 'raw' phones
        '''
        if not self.__compiled:
            self.compile_regexp()

        list_phones = list()
        matches = self.__regex.finditer(content)
        for match in matches:
            for i in range(3, 5):
                raw_phone = match.group(i)
                if raw_phone:
                    list_phones.append(raw_phone)
        return set(list_phones)

    def get_pattern(self) -> str:
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
        def check_len(self):
            len_local = len(self.international_code) \
                        + len(self.local_code) \
                        + self.len_local_phone \

            if len_local != self.len_international_phone:
                raise ValueError('Wrong local code length!')

        check_len(self)
        phone = ''
        only_digit = ''.join(filter(str.isdigit, raw_phone))
        if len(only_digit) == self.len_local_phone:
            phone = f'{self.international_code}{self.local_code}{only_digit}'
        elif len(only_digit) == self.len_international_phone-len(self.international_code):
            phone = f'{self.international_code}{only_digit}'
        elif len(only_digit) == self.len_international_phone:
            phone = f'{self.international_code}{only_digit[len(self.international_code):]}'
        else:
            raise ValueError('Wrong phone length!')

        return phone

    def get_phones(self, content: str) -> Set[str]:
        '''
        return the list of found normalized phones
        '''
        return set(map(self.normalize, self.find(content)))
