from django.test import TestCase
from django.test import SimpleTestCase
from django.test import Client

# Create your tests here.


class TestViews(SimpleTestCase):
    """
    Tests for all views.
    """
    def test_landing_page_response(self):
        """
        Tests status code for landing page get request.
        """
        client = Client()
        response_code = client.get('').status_code
        self.assertEqual(response_code, 200)

    def test_landing_page_rendered_template(self):
        """
        Tests the correct template is rendered for a landing page url
        get request.
        """
        client = Client()
        response = client.get('')
        self.assertTemplateUsed(response, 'landing_page/landing_page.html')
        self.assertEqual(response.context['slogan'],
                         'Events & Activities Organised by You for You')
        self.assertEqual(response.context['page_id'], 'landing_page')
