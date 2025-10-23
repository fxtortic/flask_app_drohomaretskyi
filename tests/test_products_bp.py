import unittest
from app import app

class ProductsBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        """Налаштування клієнта тестування перед кожним тестом."""
        app.config["TESTING"] = True
        self.client = app.test_client()
    
    def test_products_list(self):
        """Тест маршруту /products (редірект на /products/)"""
        response = self.client.get("/products/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Products", response.data)
        self.assertIn(b"Laptop", response.data)
    
    def test_product_detail(self):
        """Тест маршруту /products/<id>"""
        response = self.client.get("/products/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Laptop", response.data)
        self.assertIn(b"999.99", response.data)
    
    def test_product_not_found(self):
        """Тест неіснуючого продукту"""
        response = self.client.get("/products/999")
        self.assertEqual(response.status_code, 404)
    
    def test_product_api(self):
        """Тест API endpoint"""
        response = self.client.get("/products/api/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        data = response.get_json()
        self.assertEqual(data["name"], "Laptop")

if __name__ == "__main__":
    unittest.main()
