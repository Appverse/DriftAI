import unittest
import re
from pathlib import Path

from optapp.utils import check_uri, compile_path_pattern
from test import testenv

class UtilsTest(unittest.TestCase):
    def test_check_false_uri(self):
        """
        Test check_uri with false URIs
        :return:
        None
        """
        # https://en.wikipedia.org/wiki/Uniform_Resource_Identifier
        # URI = scheme:[//authority]path[?query][#fragment]

        not_uri1 = r"./test"
        not_uri2 = testenv.TEST_PATH
        not_uris = [not_uri1, not_uri2]

        for not_uri in not_uris:
            self.assertFalse(check_uri(not_uri))

    def test_check_true_uri(self):
        """
        Test check_uri with true URIs
        :return:
        None
        """
        # https://en.wikipedia.org/wiki/Uniform_Resource_Identifier
        # URI = scheme:[//authority]path[?query][#fragment]

        not_uri1 = r"./test"
        not_uri2 = str(Path(r"./test").absolute())
        not_uris = [not_uri1, not_uri2]

        uri1 = r"file:///{}".format(testenv.TEST_PATH)
        uri2 = "https://en.wikipedia.org/wiki/Uniform_Resource_Identifier"
        uri3 = "http:/ en.wikipedia.org/wiki/Uniform_Resource_Identifier"
        uris = [uri1, uri2, uri3]

        #not yet accepted uris
        nyi_uri1 = "mongodb://{username}:{password}@{host}/{database}?{options}"
        nyi_uri2 = "mysql://{username}:{password}@{host}/{database}?{options}"
        nyi_uris = [nyi_uri1, nyi_uri2]

        for not_uri in not_uris:
            self.assertFalse(check_uri(not_uri))
        for uri in uris:
            self.assertTrue(check_uri(uri))
        for nyi_uri in nyi_uris:
            self.assertFalse(check_uri(nyi_uri))

    def test_check_true_uri_but_not_implemented_yet(self):
        """
        Test check_uri with true URIs but not yet implemented (should assert False)
        :return:
        None
        """
        # https://en.wikipedia.org/wiki/Uniform_Resource_Identifier
        # URI = scheme:[//authority]path[?query][#fragment]

        # not yet accepted uris
        nyi_uri1 = "mongodb://{username}:{password}@{host}/{database}?{options}"
        nyi_uri2 = "mysql://{username}:{password}@{host}/{database}?{options}"
        nyi_uris = [nyi_uri1, nyi_uri2]

        for nyi_uri in nyi_uris:
            self.assertFalse(check_uri(nyi_uri))

    def test_compile_path_pattern(self):
        """
        Test compile_path_pattern with some paths and patterns
        :return:
        None
        """

        patterns = [
            {
                "basepattern": str(Path("optapp_projects", "my_project", "data")),
                "pathpattern" : r"{{{}}}/{{{}}}-{{}}.{}",
                "labels" : ["label1", "label2"],
                "extension" : ["png", "jpg"]
            }
        ]   

        paths = [

        ]

        ext = "[{}]".format("|".join(patterns[0]["extension"]))
        cp = compile_path_pattern(patterns[0]["pathpattern"].format(*patterns[0]["labels"],ext), 
                                  basepattern=patterns[0]["basepattern"])
        values = ["fold1", "cat"]
        t = re.match(
            cp,
            str(Path("optapp_projects", "my_project", "data", "fold1", "cat-1110.png"))
        )
        self.assertIsNotNone(t)
        self.assertEqual(sorted(list(t.groupdict().values())), sorted(values))
        

if __name__ == '__main__':
    unittest.main()
