#-*- coding:utf-8 -*-

import xhtml2pdf.pisa as pisa
import cStringIO as StringIO
import cgi


def render_pdf(html):
    # Function to generate the pdf document and return it throught HttpResponse
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), mimetype='application/pdf')
    return HttpResponse('Error when generating the pdf: %s' % cgi.escape(html))
