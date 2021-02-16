from copy import copy
from unittest import TestCase
import os
import shutil
import DeDup
from pathlib import Path, PosixPath


class Test(TestCase):

    base = os.path.dirname(__file__)
    input = str(base) + '/photos/'
    output = str(base) + '/photos-deleted/'
    images = input + '/2006/'
    results = output + '/2006/'
    test_files = base + '/test-files/'

    def setUp(self):
        DeDup.args = {'input': self.input,
                      'output': self.output}
        os.makedirs(os.path.dirname(self.images), exist_ok=True)
        os.makedirs(os.path.dirname(self.output), exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.input)
        shutil.rmtree(self.output)
        pass

    def prepare(self, test1, test2, file1, file2):
        dup1 = Path(self.images, test1)
        dup2 = Path(self.images, test2)
        res1 = Path(self.results, test1)
        res2 = Path(self.results, test2)
        os.makedirs(dup1.parent, exist_ok=True)
        os.makedirs(dup2.parent, exist_ok=True)
        shutil.copy(self.test_files + file1, dup1)
        shutil.copy(self.test_files + file2, dup2)
        assert dup1.exists()
        assert dup2.exists()
        assert not res1.exists()
        assert not res2.exists()
        return [dup1, dup2], [res1, res2]

    def test_auto_check_size(self):
        test_dups, res = self.prepare('test1/large.jpg', 'test2/large.jpg',
                                      'large.jpg', 'small.jpg')
        orig_dups = copy(test_dups)
        result_dups = DeDup.auto_check(test_dups)
        assert orig_dups[0].exists()
        assert not orig_dups[1].exists()
        assert not res[0].exists()
        assert res[1].exists()
        assert result_dups == [PosixPath('/code/PicSorter/photos/2006/test1/large.jpg')]

    def test_remove_dups_same_image_2_locations(self):
        test_dups, res = self.prepare('test1/large.jpg', 'test2/large.jpg',
                                      'large.jpg', 'large.jpg')
        orig_dups = copy(test_dups)
        result_dups = DeDup.remove_dups(1, test_dups)
        assert orig_dups[0].exists()
        assert not orig_dups[1].exists()
        assert not res[0].exists()
        assert res[1].exists()
        assert result_dups == [PosixPath('/code/PicSorter/photos/2006/test1/large.jpg')]

    def test_check_response_0(self):
        test_dups, res = self.prepare('test1/large.jpg', 'test2/large.jpg',
                                      'large.jpg', 'large.jpg')
        orig_dups = copy(test_dups)
        result_dups = DeDup.check_response(ord('0'), test_dups)
        assert not orig_dups[0].exists()
        assert orig_dups[1].exists()
        assert res[0].exists()
        assert not res[1].exists()
        assert result_dups == [PosixPath('/code/PicSorter/photos/2006/test2/large.jpg')]

    def test_check_response_1(self):
        test_dups, res = self.prepare('test1/large.jpg', 'test2/large.jpg',
                                      'large.jpg', 'large.jpg')
        orig_dups = copy(test_dups)
        result_dups = DeDup.check_response(ord('1'), test_dups)
        assert orig_dups[0].exists()
        assert not orig_dups[1].exists()
        assert not res[0].exists()
        assert res[1].exists()
        assert result_dups == [PosixPath('/code/PicSorter/photos/2006/test1/large.jpg')]

    def test_check_response_3(self):
        test_dups, res = self.prepare('test1/large.jpg', 'test2/large.jpg',
                                      'large.jpg', 'large.jpg')
        orig_dups = copy(test_dups)
        result_dups = DeDup.check_response(ord('3'), test_dups)
        assert orig_dups[0].exists()
        assert orig_dups[1].exists()
        assert not res[0].exists()
        assert not res[1].exists()
        assert result_dups == [PosixPath('/code/PicSorter/photos/2006/test1/large.jpg'),
                               PosixPath('/code/PicSorter/photos/2006/test2/large.jpg')]

    def test_check_response_x(self):
        test_dups, res = self.prepare('test1/large.jpg', 'test2/large.jpg',
                                      'large.jpg', 'large.jpg')
        orig_dups = copy(test_dups)
        result_dups = DeDup.check_response(ord('x'), test_dups)
        assert orig_dups[0].exists()
        assert orig_dups[1].exists()
        assert not res[0].exists()
        assert not res[1].exists()
        assert result_dups == []

    def test_check_response_a(self):
        test_dups, res = self.prepare('test1/large.jpg', 'test2/large.jpg',
                                      'large.jpg', 'large.jpg')
        orig_dups = copy(test_dups)
        result_dups = DeDup.check_response(ord('a'), test_dups)
        assert not orig_dups[0].exists()
        assert not orig_dups[1].exists()
        assert res[0].exists()
        assert res[1].exists()
        assert result_dups == []
