from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import subprocess


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def run_test1_view(request):
    try:
        result = subprocess.run(
            ["python", "manage.py", "run_test1"],
            capture_output=True,
            text=True
        )
        return Response({
            "status": "ok" if result.returncode == 0 else "error",
            "stdout": result.stdout,
            "stderr": result.stderr
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
