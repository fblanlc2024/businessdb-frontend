from reportlab.pdfgen import canvas

c = canvas.Canvas("hello.pdf")
c.drawString(100, 750, "Hello, ReportLab!")
c.save()