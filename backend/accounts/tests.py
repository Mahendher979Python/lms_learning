from django.test import TestCase, override_settings
from django.urls import reverse


@override_settings(ALLOWED_HOSTS=['*'])
class AuthLegalLinksTests(TestCase):
    def test_register_page_uses_login_style_legal_panels(self):
        response = self.client.get('/register/', follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="terms-link"')
        self.assertContains(response, 'id="conditions-link"')
        self.assertContains(response, 'id="terms-panel"')
        self.assertContains(response, 'id="conditions-panel"')
        self.assertNotContains(response, f'href="{reverse("terms_page")}"')
        self.assertNotContains(response, f'href="{reverse("conditions_page")}"')

    def test_shared_footer_legal_links_use_working_routes(self):
        response = self.client.get(reverse('index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'<a href="{reverse("terms_page")}">Privacy Notice</a>')
        self.assertContains(response, f'<a href="{reverse("conditions_page")}">Cookies</a>')
        self.assertNotContains(response, 'href="#privacy-notice"')
        self.assertNotContains(response, 'href="#cookies"')

    def test_homepage_contains_blog_section_for_footer_link(self):
        response = self.client.get('/en/', follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="blog"')
        self.assertContains(response, 'From the Blog')
