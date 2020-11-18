import unittest
import tempfile

from index import Index


class TestDocumentIndex(unittest.TestCase):

    def test_index(self):

        with tempfile.TemporaryDirectory() as td:
            with open(td + '/' + "1.hello.xml", "w") as f:
                f.writelines(["hello\n", "world\n", "thank you\n", "python"])
            with open(td + '/' + "2.goodbye.xml", "w") as f:
                f.writelines(["goodbye\n", "friends\n", "thank you\n", "python"])
            with open(td + '/' + "3.special.chars.xml", "w") as f:
                f.writelines(["zzz\n", "zzz...\n", "zZzZzZz...\n"])
            print(td)
            idx = Index.new(td)

        self.assertEqual(set(["1"]), idx.search("hello world"))
        self.assertEqual(set(["2"]), idx.search("goodbye friends"))
        self.assertEqual(set(), idx.search("hello goodbye"))
        self.assertEqual(set(["1", "2"]), idx.search("thank you python"))
        self.assertEqual(set(), idx.search("zzz zzzzzzz"))
        self.assertEqual(set(["3"]), idx.search("zzz zzzzzzz..."))


if __name__ == '__main__':
    unittest.main()
