from django.test import TestCase
from django.urls import resolve

from lists.models import Item
from lists.views import home_page


class HomePageTest(TestCase):
    def test_root_url_resolver_to_home_page_view(self) -> None:
        found = resolve("/")
        self.assertEqual(found.func, home_page)

    def test_only_saves_items_when_necessary(self) -> None:
        self.client.get("/")
        self.assertEqual(Item.objects.count(), 0)

    def test_home_page_returns_correct_html(self) -> None:
        response = self.client.get("/")

        html = response.content.decode("utf8")
        self.assertTrue(html.startswith("<html>"))
        self.assertIn("<title>To-Do lists</title>", html)
        self.assertTrue(html.strip().endswith("</html>"))

        self.assertTemplateUsed(response, "lists/home.html")

    def test_uses_home_template(self) -> None:
        response = self.client.get("/")
        self.assertTemplateUsed(response, "lists/home.html")

    def test_can_save_a_POST_request(self) -> None:
        self.client.post("/", data={"item_text": "A new list item"})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new list item")

    def test_redirects_after_POST(self) -> None:
        response = self.client.post("/", data={"item_text": "A new list item"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"], "/")

    def test_displays_all_list_items(self) -> None:
        Item.objects.create(text="itemey 1")
        Item.objects.create(text="itemey 2")

        response = self.client.get("/")

        self.assertIn("itemey 1", response.content.decode("utf8"))
        self.assertIn("itemey 2", response.content.decode("utf8"))


class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self) -> None:
        first_item = Item()
        first_item.text = "The first (even) list item"
        first_item.save()

        second_item = Item()
        second_item.text = "Item the second"
        second_item.save()

        saved_itens = Item.objects.all()
        self.assertEqual(saved_itens.count(), 2)

        first_saved_item = saved_itens[0]
        second_saved_item = saved_itens[1]
        self.assertEqual(first_saved_item.text, "The first (even) list item")
        self.assertEqual(second_saved_item.text, "Item the second")
