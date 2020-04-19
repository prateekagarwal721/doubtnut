
from io import BytesIO
from pdfdocument.document import PDFDocument

from .models import DUSerVideoSeen

@background(schedule=60*5)
def generate_pdf(video_seen_id,user_id):
    last_video_seen = DUSerVideoSeen.objects.filter(id=video_seen_id).first()
    latest_video_seen = DUSerVideoSeen.objects.filter(seen_by_id=last_video_seen.asked_by_id).order_by('-seen_at').first()

    if last_video_seen == latest_video_seen:
        catalog_question = CatalogQuestion.objects.filter(id=last_video_seen.catalog_question_id).first()
        question_json = catalog_question.similar_question

        f = BytesIO()
        pdf = PDFDocument(f)
        pdf.init_report()
        pdf.p(question_json)
        pdf.generate()
        return f.getvalue()