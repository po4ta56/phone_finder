import unittest
from phone_finder import PhoneFinder

class TestParser(unittest.TestCase):
    def setUp(self):
        param = {
            'len_local_phone': 6,
            'local_code': '3532',
            'len_international_phone': 11,
            'international_code': '8',
        }
        self.phone_finder = PhoneFinder(**param)

    def test_seach_local_1(self):
        content = '60-60-60'
        self.assertEqual(set([content,]), self.phone_finder.find(content))

    def test_seach_local_2(self):
        content = '606060'
        self.assertEqual(set([content,]), self.phone_finder.find(content))

    def test_seach_local_3(self):
        content = '606-060'
        self.assertEqual(set([content,]), self.phone_finder.find(content))

    def test_seach_local_4(self):
        content = ' 60-60-60 '
        self.assertEqual(set(['60-60-60',]), self.phone_finder.find(content))

    def test_seach_local_5(self):
        content = ''' some text
        fish 60-60-60 water
        some str
        '''
        self.assertEqual(set(['60-60-60',]), self.phone_finder.find(content))

    def test_seach_local_6(self):
        content = '<span>60-60-60 '
        self.assertEqual(set(['60-60-60',]), self.phone_finder.find(content))

    def test_seach_local_7(self):
        content = '60-60-60</span>'
        self.assertEqual(set(['60-60-60',]), self.phone_finder.find(content))
    
    def test_seach_local_8(self):
        content = '<span>60-60-60</span>'
        self.assertEqual(set(['60-60-60',]), self.phone_finder.find(content))
    
    def test_seach_local_9(self):
        content = '<span>60-60-60sometext'
        self.assertNotRegex(content, self.phone_finder.get_pattern())

    def test_seach_local_10(self):
        content = 'span60-60-60'
        self.assertNotRegex(content, self.phone_finder.get_pattern())

    def test_seach_local_11(self):
        content = '<span>60-6-60</span>'
        self.assertNotRegex(content, self.phone_finder.get_pattern())

    def test_seach_local_12(self):
        content = '<span>60 60 60</span>'
        self.assertNotRegex(content, self.phone_finder.get_pattern())

    def test_seach_international_1(self):
        content = '89876543210'
        self.assertEqual(set([content,]), self.phone_finder.find(content))

    def test_seach_international_2(self):
        content = '+79876543210'
        self.assertEqual(set([content,]), self.phone_finder.find(content))

    def test_seach_international_3(self):
        content = '79876543210'
        self.assertEqual(set([content,]), self.phone_finder.find(content))

    def test_seach_international_4(self):
        content = '7(987)6543210'
        self.assertEqual(set([content,]), self.phone_finder.find(content))

    def test_seach_international_5(self):
        content = '7(987)654 32 10'
        self.assertEqual(set([content,]), self.phone_finder.find(content))

    def test_seach_international_6(self):
        content = '7(987)654-32-10'
        self.assertEqual(set([content,]), self.phone_finder.find(content))

    def test_seach_international_7(self):
        content = '7(987)654-32-10<span'
        self.assertEqual(set(['7(987)654-32-10',]), self.phone_finder.find(content))
    
    def test_seach_international_8(self):
        content = 'span>8(987)654-32-10'
        self.assertEqual(set(['8(987)654-32-10',]), self.phone_finder.find(content))

    def test_seach_international_9(self):
        content = 'span8(987)654-32-10'
        self.assertNotRegex(content, self.phone_finder.get_pattern())

    def test_seach_international_10(self):
        content = 'span 8(987)654-32-100'
        self.assertNotRegex(content, self.phone_finder.get_pattern())


    def tearDown(self):
        pass


class TestNormalizer(unittest.TestCase):
    def setUp(self):
        param = {
            'len_local_phone': 6,
            'local_code': '3532',
            'len_international_phone': 11,
            'international_code': '8',
        }
        self.phone_finder = PhoneFinder(**param)

    def test_normalize_local_1(self):
        content = '60-60-60'
        self.assertEqual('83532606060', self.phone_finder.normalize(content))
    
    def test_normalize_local_2(self):
        content = '606060'
        phone_prefix = self.phone_finder.international_code+self.phone_finder.local_code
        self.assertEqual(phone_prefix+'606060', self.phone_finder.normalize(content))

    def test_normalize_local_3(self):
        content = '606-060'
        phone_prefix = self.phone_finder.international_code+self.phone_finder.local_code
        self.assertEqual(phone_prefix+'606060', self.phone_finder.normalize(content))

    def test_normalize_local_4(self):
        content = '60 60 60'
        phone_prefix = self.phone_finder.international_code+self.phone_finder.local_code
        self.assertEqual(phone_prefix+'606060', self.phone_finder.normalize(content))

    def test_normalize_local_5(self):
        content = '606060s'
        phone_prefix = self.phone_finder.international_code+self.phone_finder.local_code
        self.assertEqual(phone_prefix+'606060', self.phone_finder.normalize(content))

    def test_normalize_local_6(self):
        content = '60-60-600'
        self.assertRaises(ValueError, self.phone_finder.normalize, content)

    def test_normalize_international_1(self):
        content = '89876543210'
        self.assertEqual('89876543210', self.phone_finder.normalize(content))
    
    def test_normalize_international_2(self):
        content = '8-987-65-43-21-0'
        self.assertEqual('89876543210', self.phone_finder.normalize(content))

    def test_normalize_international_3(self):
        content = '8(987)654-32-10'
        self.assertEqual('89876543210', self.phone_finder.normalize(content))

    def test_normalize_international_4(self):
        content = '8(987)654 32 10'
        self.assertEqual('89876543210', self.phone_finder.normalize(content))

    def test_normalize_international_5(self):
        content = '+7(987)654 32 10'
        self.assertEqual('89876543210', self.phone_finder.normalize(content))

    def test_normalize_international_6(self):
        content = '7(987)654-32 10'
        self.assertEqual('89876543210', self.phone_finder.normalize(content))

    def test_normalize_international_7(self):
        content = 's7(987)654-32 10'
        self.assertEqual('89876543210', self.phone_finder.normalize(content))

    def test_normalize_international_8(self):
        content = 's7(987)654-32 10s'
        self.assertEqual('89876543210', self.phone_finder.normalize(content))

    def test_normalize_international_9(self):
        content = '7(987)654-32-100'
        self.assertRaises(ValueError, self.phone_finder.normalize, content)

if __name__ == "__main__":
    unittest.main()