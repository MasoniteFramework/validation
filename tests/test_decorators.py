from masonite.testing import TestCase
from masonite.routes import Get


class TestDecorators(TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        super().setUp()
        self.routes(
            only=[
                Get("/test", "PackageController@show"),
                Get("/validate", "PackageController@validate"),
            ]
        )

    def test_validation_decorator(self):
        self.assertFalse(self.get("/validate").contains("success"))
        self.get("/validate", {"name": "Joe"}).assertContains("success")
