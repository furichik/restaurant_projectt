from django.test import TestCase

class PostListTest(TestCase):
    def test_health_check(self):
        response=self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/index.html")

class PostModelTest(TestCase):
    def test_create_post(self):
        post=Post.objects.create
            