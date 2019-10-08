import io

from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from .forms import GeneratorForm, EventForm
from .models import Event

# Create your views here.

class DashboardView(LoginRequiredMixin, TemplateView):

    template_name = "dashboard.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class EventDetailView(LoginRequiredMixin, DetailView):
    
    model = Event
    template_name = "event_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class EventListView(LoginRequiredMixin, ListView):
    
    model = Event
    template_name = "event_list.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class EventFormView(LoginRequiredMixin, FormView):

    template_name = "event_form.html"
    form_class = EventForm

    def form_valid(self, form):
        return super().form_valid(form)

class GeneratorView(LoginRequiredMixin, FormView):

    template_name = "generator.html"
    form_class = GeneratorForm

    def generate_pdf(self, cleaned_data):
        buffer = io.BytesIO()

        doc = SimpleDocTemplate(buffer,
                            pagesize=letter,
                            title=cleaned_data['title'],
                            rightMargin=30,
                            leftMargin=30,
                            topMargin=30,
                            bottomMargin=30)

        styles = getSampleStyleSheet()
    
        flowables = []
    
        # set form title
        styles['Title'].fontSize = 24
        title = Paragraph("Fiche Event n° ..........", style=styles["Title"])
        flowables.append(title)
        flowables.append(Spacer(0, 12))

        # set form association
        styles['Title'].fontSize = 18
        association = Paragraph("Organisé par l'association GConfs", style=styles["Title"])
        flowables.append(association)
        flowables.append(Spacer(0, 12))

        # set form table
        tablData = [['Nom de l\'Event', cleaned_data['title'], '', ''],
                    ['Date de l\'Event', '', 'Horaires', 'De __h__ à __h__'],
                    ['Récurrence', '', 'Si Oui', 'Fréquence (jours) :'],
                    ['', '', '', 'Jusqu\'au :'],
                    ['Responsable\nsur place', '', 'Tél', ''],
                    ['', '', 'Classe', ''],
                    ['Tuteur*\n(salarié IONIS)', '', 'Tél', ''],
                    ['', '', 'Poste / Ecole', ''],
                    ['Public attendu**', 'Etudiants Ionis (450 Max)', 'Membres', 'Externes (150 Max)'],
                    ['', '', '', '']]

        tabl = Table(tablData, [3.5*cm, 5.5*cm, 3.5*cm, 6.5*cm], 0.8*cm)

        tablStyle = TableStyle([('GRID',(0,0),(-1,-1),1.5,colors.black),
                                ('ALIGN',(0,0),(3,9),'CENTER'),
                                ('ALIGN',(3,2),(3,3),'LEFT'),
                                ('VALIGN',(0,0),(3,9),'MIDDLE'),
                                ('FONTSIZE',(0,0),(3,9), 11),
                                ('SPAN',(1,0),(3,0)),
                                ('SPAN',(0,2),(0,3)),
                                ('SPAN',(1,2),(1,3)),
                                ('SPAN',(2,2),(2,3)),
                                ('SPAN',(0,4),(0,5)),
                                ('SPAN',(1,4),(1,5)),
                                ('SPAN',(0,6),(0,7)),
                                ('SPAN',(1,6),(1,7)),
                                ('SPAN',(0,8),(0,9)),
                                ])
        tabl.setStyle(tablStyle)
        flowables.append(tabl)
        flowables.append(Spacer(0, 12))

        styles['Normal'].fontSize = 11
        # set form description
        description = Paragraph("Description de l'Event : ", style=styles["Normal"])
        flowables.append(description)
        flowables.append(Spacer(0, 12))

        # set form civil responsability
        civil = Paragraph("Avez-vous une assurance responsabilité civile ? ", style=styles["Normal"])
        flowables.append(civil)
        flowables.append(Spacer(0, 12))

        # set form rooms
        rooms = Paragraph("Salle(s) prévue(s) : ", style=styles["Normal"])
        flowables.append(rooms)
        flowables.append(Spacer(0, 12))

        # set form equipment
        equipment = Paragraph("Liste du matériel présent : ", style=styles["Normal"])
        flowables.append(equipment)
        flowables.append(Spacer(0, 12))

        # set form drinks
        drinks = Paragraph("Boisson(s) prévue(s) : ", style=styles["Normal"])
        flowables.append(drinks)
        flowables.append(Spacer(0, 12))

        # set form special
        special = Paragraph("Remarques spéciales concernant l'Event : ", style=styles["Normal"])
        flowables.append(special)
        flowables.append(Spacer(0, 12))

        # set form signature
        signData = ["Responsable sur place\n\nSigné le :\nSignature", "Président de l'association\n\nSigné le :\nSignature", "Tuteur\n\nSigné le :\nSignature", "Responsable des associations\n\nSigné le :\nSignature"],
        
        sign = Table(signData, 4.7*cm, 4.0*cm)

        signStyle = TableStyle([('GRID',(0,0),(-1,-1),1.5,colors.black),
                                ('FONTSIZE',(0,0),(3,0), 9),
                                ('VALIGN',(0,0),(3,0),'TOP'),
                                ])
        sign.setStyle(signStyle)
        flowables.append(sign)
        doc.build(flowables)

        pdf = buffer.getvalue()
        buffer.close()

        return pdf

    def form_valid(self, form):              
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="gconfs_event.pdf"'

        pdf = self.generate_pdf(form.cleaned_data)

        response.write(pdf)

        return response
