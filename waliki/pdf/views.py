import tempfile
from sh import rst2pdf
from django.shortcuts import get_object_or_404
from waliki.models import Page
from waliki.utils import send_file
from waliki.settings import WALIKI_PDF_INCLUDE_TITLE
from waliki.acl import permission_required


@permission_required('view_page')
def pdf(request, slug):
    page = get_object_or_404(Page, slug=slug)

    with tempfile.NamedTemporaryFile(suffix='.pdf') as output:
        outfile = output.name
    if WALIKI_PDF_INCLUDE_TITLE:
        line = "/" * len(page.title)
        title = "%s\n%s\n%s\n\n" % (line, page.title, line)
        with tempfile.NamedTemporaryFile(suffix='.rst', mode="w", delete=False) as infile:
            infile.file.write(title + page.raw)
            infile = infile.name
    else:
        infile = page.abspath
    rst2pdf(infile, o=outfile)
    filename = page.title.replace('/', '-').replace('..', '-')
    return send_file(outfile, filename="%s.pdf" % filename)
