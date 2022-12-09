from django.test import TestCase
from rest_framework_simplejwt.tokens import RefreshToken
from cookiesAPI.models import Command, Cookie, User

class CookiesTest(TestCase):
    def setUp(self):
        self.cookie_1 = Cookie.objects.create(**{
            'name': 'Cookie Epautre Noix',
            'description': 'Very chewy and healthy cookie. Contains nuts et other stuff',
            'price': 3.0,
            'photo_main_page': 'images/Cookies-epeautre-chocolat-noir-pecan-detail.jpg',
            'photo_detail': 'images/Cookies-epeautre-chocolat-noir-pecan-main.jpg',
        },)

        self.user_1 = User.objects.create_user(**{"first_name": "string1", "last_name": "string1", "password": "string1", "email": "1.1@1.com", "username": "1.1@1.com"})
        self.user_2 = User.objects.create_user(**{"first_name": "string2", "last_name": "string2", "password": "string2", "email": "2.2@2.com", "username": "2.2@2.com"})
        
        self.create_command_by_view(self.user_1, quantity=3)
        self.create_command_by_view(self.user_2, quantity=5)

        self.command_user_1 = Command.objects.get(user=self.user_1)
        self.command_user_2 = Command.objects.get(user=self.user_2)

    def create_command_by_view(self, user, quantity=3):
        create_data = {
            "command_cookies": [
                {
                    "quantity": quantity,
                    "cookie": str(self.cookie_1.id)
                },
            ]
        }
        response = self.client.post("/commands/", create_data, content_type="application/json", HTTP_AUTHORIZATION=self.get_bearer_token(user))
        return response


    def get_bearer_token(self, user): 
        refresh = RefreshToken.for_user(user)
        return f'Bearer {refresh.access_token}'

    def test_create_user(self):
        response = self.client.post("/user/", {"first_name": "string", "last_name": "string", "password": "string", "email": "h.h@h.com"})
        self.assertEqual(response.status_code, 201)

        created_user = User.objects.get(username='h.h@h.com')
        self.assertEqual(created_user.first_name, "string")
        self.assertEqual(created_user.last_name, "string")
        self.assertEqual(created_user.email, "h.h@h.com")
        self.assertEqual(created_user.username, "h.h@h.com")
        self.assertEqual(created_user.is_superuser, False)
        self.assertEqual(created_user.is_staff, False)
        # TODO: tester que on peut pas créer 2 avec le même email !

    def test_update_user(self):
        def test_update_user(user_id, user, expected_status_code):
            request_data = {
                'username': '1.1@1.com',
                'email': '1.1@1.com', 
                'first_name': 'string1', 
                'last_name': 'string1', 
                'address_line': '10 avenue lala',
                'postal_code': '75017',
                'city': 'Paris',
                'country': 'France'
            }

            response = self.client.put(f"/user/{user_id}/", request_data, content_type="application/json", HTTP_AUTHORIZATION=self.get_bearer_token(user))
            self.assertEqual(expected_status_code, response.status_code)
        
            if expected_status_code == 200:
                print(response.json())
                self.assertDictEqual(
                    response.json(), 
                    {
                        'first_name': 'string1', 
                        'last_name': 'string1', 
                        'country': 'France', 
                        'city': 'Paris', 
                        'postal_code': '75017', 
                        'address_line': '10 avenue lala'
                    }
                )
        
        test_update_user(str(self.user_1.id), self.user_1, 200)
        test_update_user(str(self.user_2.id), self.user_1, 404)


    def test_get_cookies(self):
        response = self.client.get("/cookies/")
        self.assertEqual(response.status_code, 200)

        expected_data = response.json()
        expected_data[0].pop("id")
        photo_detail_url = expected_data[0].pop("photo_detail")
        photo_main_page_url = expected_data[0].pop("photo_main_page")

        self.assertListEqual(
            [{
                "name": "Cookie Epautre Noix",
                "description": "Very chewy and healthy cookie. Contains nuts et other stuff",
                "price": 3,
            }], 
            expected_data
        )

        self.assertEqual(photo_detail_url, 'http://testserver/images/Cookies-epeautre-chocolat-noir-pecan-main.jpg')
        self.assertEqual(photo_main_page_url, 'http://testserver/images/Cookies-epeautre-chocolat-noir-pecan-detail.jpg')
    
    def test_get_cookie(self):
        id = str(self.cookie_1.id)
        response = self.client.get(f"/cookies/{id}/")
        self.assertEqual(response.status_code, 200)

        expected_data = response.json()
        expected_data.pop("id")
        expected_data.pop("photo_detail")
        expected_data.pop("photo_main_page")

        self.assertDictEqual(
            {
                "name": "Cookie Epautre Noix",
                "description": "Very chewy and healthy cookie. Contains nuts et other stuff",
                "price": 3,
            }, 
            expected_data
        )

    def test_get_user(self):
        def get_user(id, user, expected_status_code):
            response = self.client.get(f"/user/{id}/", HTTP_AUTHORIZATION=self.get_bearer_token(user))
            self.assertEqual(expected_status_code, response.status_code)
        
            if expected_status_code == 200: 
                self.assertDictEqual(response.json(), 
                    {
                        'id': id, 
                        'username': '1.1@1.com',
                        'email': '1.1@1.com', 
                        'first_name': 'string1', 
                        'last_name': 'string1', 
                        'address_line': '',
                        'postal_code': '',
                        'city': '',
                        'country': ''
                    })
        
        get_user(str(self.user_1.id), self.user_1, 200)
        get_user(str(self.user_2.id), self.user_1, 404)


    def test_create_command(self):
        response = self.create_command_by_view(self.user_1)

        self.assertEqual(201, response.status_code)
        self.assertDictEqual(response.json(), 
            {
                "command_cookies": [
                    {
                        "total_cost": self.cookie_1.price * 3,
                        "quantity": 3,
                        "cookie": str(self.cookie_1.id)
                    },
                ]
            })


    def test_get_commands(self):
        def get_commands(user, expected_status_code, expected_data):
            response = self.client.get(f"/commands/", HTTP_AUTHORIZATION=self.get_bearer_token(user))
            self.assertEqual(expected_status_code, response.status_code)
        
            if expected_status_code == 200: 
                response_data = response.json()
                for command in response_data:
                    command.pop("created_at")
                
                self.assertListEqual(response.json(), expected_data)
        
        get_commands(self.user_1, 200, [{'id': self.command_user_1.id, 'command_cookies': [{'total_cost': 9, 'quantity': 3, 'cookie': str(self.cookie_1.id)}], 'total_cost_command': 9}])
        get_commands(self.user_2, 200, [{'id': self.command_user_2.id, 'command_cookies': [{'total_cost': 15, 'quantity': 5, 'cookie': str(self.cookie_1.id)}], 'total_cost_command': 15}])
        
    
    def test_get_command_detail(self):
        def test_get_command_detail(command_id, user, expected_status_code, expected_data=None):
            response = self.client.get(f"/commands/{command_id}/", HTTP_AUTHORIZATION=self.get_bearer_token(user))
            self.assertEqual(expected_status_code, response.status_code)
        
            if expected_status_code == 200:
                response_data = response.json()
                response_data.pop("created_at")
                self.assertDictEqual(response.json(), expected_data)

        test_get_command_detail(self.command_user_1.id, self.user_1, 200, expected_data={'id': self.command_user_1.id, 'command_cookies': [{'total_cost': 9, 'quantity': 3, 'cookie': str(self.cookie_1.id)}], 'total_cost_command': 9})
        test_get_command_detail(self.command_user_1.id, self.user_2, 404)
    


    
