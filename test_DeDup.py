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
        print('done...')
        shutil.rmtree(self.input)
        shutil.rmtree(self.output)
        pass

    def test_remove_dups_same_image_2_locations(self):
        print('going...')
        dup1 = Path(self.images, 'test1/large.jpg')
        dup2 = Path(self.images, 'test2/large.jpg')
        res = Path(self.results, 'test2/large.jpg')
        os.makedirs(dup1.parent, exist_ok=True)
        os.makedirs(dup2.parent, exist_ok=True)
        shutil.copy(self.test_files + 'large.jpg', dup1)
        shutil.copy(self.test_files + 'large.jpg', dup2)
        assert dup1.exists()
        assert dup2.exists()
        assert not res.exists()
        test_dups = [dup1, dup2]
        result_dups = DeDup.remove_dups(1, test_dups)
        assert dup1.exists()
        assert res.exists()
        assert not dup2.exists()
        assert result_dups == [PosixPath('/code/PicSorter/photos/2006/test1/large.jpg')]
