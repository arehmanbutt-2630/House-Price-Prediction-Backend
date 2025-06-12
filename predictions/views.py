from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

import os
import pickle

from django.conf import settings

from .models import Prediction
from .serializers import PredictionSerializer

# Load the regression model
MODEL_PATH = os.path.join(settings.BASE_DIR, "predictions", "ml_model", "house_price_model.pkl")
try:
    with open(MODEL_PATH, "rb") as f:
        regression_model = pickle.load(f)
except Exception as e:
    regression_model = None
    print(f"Error loading model: {e}")

class PredictionViewSet(mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    """
    Only list existing predictions, and allow predictions via custom ('predict/') endpoint.
    """
    queryset = Prediction.objects.all()
    serializer_class = PredictionSerializer

    @action(detail=False, methods=["post"])
    def predict(self, request):
        if regression_model is None:
            return Response(
                {"detail": "Regression model not available on server."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        data = request.data
        sq_ft = data.get("square_footage")
        bedrooms = data.get("bedrooms")

        if sq_ft is None or bedrooms is None:
            return Response(
                {"detail": "square_footage and bedrooms are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            sq_ft = int(sq_ft)
            bedrooms = int(bedrooms)
        except (ValueError, TypeError):
            return Response(
                {"detail": "square_footage and bedrooms must be integers."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            predicted_price = regression_model.predict([[sq_ft, bedrooms]])[0]
        except Exception as e:
            return Response(
                {"detail": f"Prediction failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Save to DB
        record_data = {
            "square_footage": sq_ft,
            "bedrooms": bedrooms,
            "predicted_price": int(predicted_price),
        }

        serializer = self.get_serializer(data=record_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
