import unittest
from listcondalic.liccheck_and_condameta_based import strip_version_info


class TestStripInfo(unittest.TestCase):
    def test_strip_whitespace(self):
        self.assertEqual(strip_version_info('python'), 'python')
        self.assertEqual(strip_version_info('python == 3'), 'python')
        self.assertEqual(strip_version_info('python = 3'), 'python')
        self.assertEqual(strip_version_info('python >= 3'), 'python')
        self.assertEqual(strip_version_info('python <= 3'), 'python')
        self.assertEqual(strip_version_info('python ~= 3'), 'python')
        self.assertEqual(strip_version_info('python != 3'), 'python')

    def test_strip_extra(self):
        self.assertEqual(strip_version_info('pythonas3'), 'pythonas3')
        self.assertEqual(strip_version_info('python == 3asd'), 'python')
        self.assertEqual(strip_version_info('python = 332efa'), 'python')
        self.assertEqual(strip_version_info('python >= 3s3as'), 'python')
        self.assertEqual(strip_version_info('python <= 34sfd3'), 'python')
        self.assertEqual(strip_version_info('python ~= 34f1r'), 'python')
        self.assertEqual(strip_version_info('python != 3er1'), 'python')

    def test_strip(self):
        self.assertEqual(strip_version_info('python'), 'python')
        self.assertEqual(strip_version_info('python==3'), 'python')
        self.assertEqual(strip_version_info('python=3'), 'python')
        self.assertEqual(strip_version_info('python>=3'), 'python')
        self.assertEqual(strip_version_info('python<=3'), 'python')
        self.assertEqual(strip_version_info('python~=3'), 'python')
        self.assertEqual(strip_version_info('python!=3'), 'python')
