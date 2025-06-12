from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch

from predictions.models import Prediction


class PredictionViewSetTests(APITestCase):

    def setUp(self):
        # Create a sample prediction
        Prediction.objects.create(
            square_footage=1500,
            bedrooms=3,
            predicted_price=300000
        )

    def test_list_predictions(self):
        response = self.client.get("/predictions/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["square_footage"], 1500)

    @patch("predictions.views.regression_model")
    def test_predict_success(self, mock_model):
        mock_model.predict.return_value = [350000]

        payload = {
            "square_footage": 2000,
            "bedrooms": 4
        }

        response = self.client.post("/predictions/predict/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["square_footage"], 2000)
        self.assertEqual(response.data["predicted_price"], 350000)

    @patch("predictions.views.regression_model", None)
    def test_predict_model_unavailable(self):
        payload = {
            "square_footage": 2000,
            "bedrooms": 4
        }
        response = self.client.post("/predictions/predict/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("Regression model not available", response.data["detail"])

    def test_predict_missing_fields(self):
        response = self.client.post("/predictions/predict/", {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("square_footage and bedrooms are required", response.data["detail"])

    def test_predict_invalid_data(self):
        payload = {
            "square_footage": "large",
            "bedrooms": "many"
        }
        response = self.client.post("/predictions/predict/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("must be integers", response.data["detail"])
