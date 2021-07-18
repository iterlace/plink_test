from typing import Any, Optional

from rest_framework.renderers import JSONRenderer


class DetailedRenderer(JSONRenderer):
    def render(
        self,
        data: Any,
        accepted_media_type: Optional[Any] = None,
        renderer_context: Optional[dict] = None,
    ) -> str:
        status_code: int = renderer_context["response"].status_code  # type: ignore
        response = {
            "status": "success",
            "errors": None,
            "data": data,
        }

        if status_code < 200 or status_code >= 300:
            response["status"] = "error"
            response["data"] = None
            response["errors"] = data

        return super(DetailedRenderer, self).render(  # type: ignore
            response, accepted_media_type, renderer_context
        )
