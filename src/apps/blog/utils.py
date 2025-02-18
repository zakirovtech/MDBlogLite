import os
from logging import Logger

import markdown
from django.conf import settings
from weasyprint import HTML


class BioConvertMixin:
    def convert_md_to_pdf(self, text: str, logger: Logger):
        try:
            html = markdown.markdown(text)
            output_pdf_path = os.path.join(settings.MEDIA_ROOT, "pdf/cv.pdf")
            HTML(string=html).write_pdf(output_pdf_path)
        except Exception as e:
            logger.error(f"Failed convert bio to PDF format with error: [{e}]")
        else:
            logger.info(f"Successfully create PDF bio in: [{output_pdf_path}]")


class PostViewsCounterMixin:
    def get_client_address(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")


class CommonContextMixin:
    def get_common_context(self, *args, **kwargs):
        context = {"blogname": settings.BLOG_NAME}
        if args:
            context.update({"extra_args": args})
        if kwargs:
            context.update(**kwargs)
        return context
