from rest_framework.versioning import NamespaceVersioning
from rest_framework.views import APIView


class HRentalVersions(NamespaceVersioning):
    default_version = "v1"
    allowed_versions = ["v1", "v2"]
    version_param = "version"


class ExampleView(APIView):
    versioning_class = HRentalVersions
