import unittest
from phone_finder import PhoneFinder
from async_downloader import async_download
from time import sleep

class TestDownloaderSearch(unittest.TestCase):
    def setUp(self):
        param = {
            'len_local_phone': 6,
            'local_code': '3532',
            'len_international_phone': 11,
            'international_code': '8',
        }
        self.phone_finder = PhoneFinder(**param)

        self.urls = [
            'https://repetitors.info/',
            'https://hands.ru/company/about/',
            'http://сакмарскийрайон.рф/',
            'http://сакмарскийрайон.рф/Pages.aspx?id=36',
            'http://сакмарскийрайон.рф/Pages.aspx?id=535',
            'http://www.uralakva.ru/index.php?a=iv&id=4&pg_id=4'
        ]



    def test_seach_1(self):
        
        expected_result = {
            'http://сакмарскийрайон.рф/Pages.aspx?id=535': {'83533121507', '83533121130', '83533121853'}, 
            'http://сакмарскийрайон.рф/': {'83533121507', '83533121130', '83532447544', '83533121853'}, 
            'http://www.uralakva.ru/index.php?a=iv&id=4&pg_id=4': {'83532733254', '83532401133'}, 
            'https://hands.ru/company/about/': {'84951370720'}, 
            'http://сакмарскийрайон.рф/Pages.aspx?id=36': {'83533121695', '83533121777', '83533121507', '83533121300', '83533122271', '83533121130', '83533121850', '83533121853'},
            'https://repetitors.info/': {'88005057283', '84955405676', '88005057284'},
        }
        result = async_download(self.urls)
        sleep(2)
        self.assertDictEqual(expected_result, result)

    

if __name__ == "__main__":
    unittest.main()