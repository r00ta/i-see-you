import unittest

class TestRepoSetup(unittest.TestCase):

    def test_repo_setup(self):
        try:
            import iseeyou
        except:
            self.fail("Could not import iseeyou repo.")

