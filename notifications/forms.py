import sys
import time

from django import forms
from django.conf import settings
from django.core.validators import validate_email
from django.core.mail import send_mail
from django.db import transaction
from django.forms import CharField
from django.forms import ModelChoiceField
from django.utils.html import strip_tags

from django_q.tasks import async, result

from bdr.settings import EMAIL_SENDER
from notifications import ACCEPTED_PARAMS
from notifications.models import Stage
from .models import (
    Company,
    Cycle,
    CycleEmailTemplate,
    CycleNotification,
    Person,
)


def set_values_for_parameters(person, company):
    params = {}
    for param, value in ACCEPTED_PARAMS.items():
        if value:
            params[param] = eval(value)
        else:
            params[param] = value
    return params


def format_body(body_html, person, company):
    params = set_values_for_parameters(person, company)
    email_body = body_html.format(**params)
    return email_body


def format_subject(subject, person, company):
    params = set_values_for_parameters(person, company)
    subject = subject.format(**params)
    return subject


def make_messages(persons, emailtemplate):
    emails = []
    for person in persons:
        subject = format_subject(emailtemplate.subject, person, person.company)
        email_body = format_body(emailtemplate.body_html, person, person.company)
        recipient_email = [person.email]

        emails.append((subject, recipient_email, email_body))

        cycle_notification = CycleNotification.objects.filter(
            email=person.email,
            emailtemplate=emailtemplate
        ).first()

        counter = 1
        if cycle_notification:
            counter = cycle_notification.counter + 1
            cycle_notification.delete()

        # store sent email
        CycleNotification.objects.create(
            subject=subject,
            email=person.email,
            body_html=email_body,
            emailtemplate=emailtemplate,
            counter=counter,
            person=person,
        )

        emailtemplate.is_triggered = True
        emailtemplate.save()
    return emails


def send_emails(sender, emailtemplate, people=None, is_test=False, data=None):
    with transaction.atomic() as atomic:
        if people:
            subject = emailtemplate.subject
            sender = EMAIL_SENDER
            emails = make_messages(people, emailtemplate)
        elif is_test:
            company = Company.objects.filter(name=data.get('company')).first()
            person = Person.objects.filter(name=data.get('contact')).first()
            values = set_values_for_parameters(person, company)
            email = [data['email'].strip()]
            body_html = emailtemplate.body_html.format(**values)
            subject = emailtemplate.subject.format(**values)
            emails = [(subject, email, body_html)]
        else:
            recipients = Person.objects.filter(
                company__group=emailtemplate.group).distinct()
            subject = emailtemplate.subject
            sender = EMAIL_SENDER
            emails = make_messages(recipients, emailtemplate)

        for subject, recipient_email, email_body in emails:
            plain_html = strip_tags(email_body)
            send_mail(subject, plain_html, sender, recipient_email,
                      fail_silently=False, html_message=email_body)


def send_mail_sender(task):
    # TODO implement mail
    print("Done")


class CycleAddForm(forms.ModelForm):
    class Meta:
        model = Cycle
        fields = ['year', 'closing_date']
        exclude = ('id',)


class CustomModelChoiceField(ModelChoiceField):
    """Workaround for https://code.djangoproject.com/ticket/30014"""
    def to_python(self, value):
        if isinstance(value, self.queryset.model):
            value = getattr(value, self.to_field_name or 'pk')
        return super().to_python(value)


class StageAddForm(forms.ModelForm):
    cycle = CustomModelChoiceField(Cycle.objects.all(), disabled=True)

    class Meta:
        model = Stage
        fields = ['cycle', 'title']

    def save(self, commit=True, *args, **kwargs):
        """When a new stage is added to a cycle create a template
        for each group.
        """
        kwargs['commit'] = False
        instance = super().save(*args, **kwargs)
        if commit:
            instance.save()
            instance.create_stage_templates()
        return instance


class CycleEmailTemplateEditForm(forms.ModelForm):
    class Meta:
        model = CycleEmailTemplate
        fields = ['subject', 'body_html']
        exclude = ('id', 'cycle', 'emailtemplate')


class CycleEmailTemplateTestForm(forms.Form):
    email = forms.CharField(validators=[validate_email])

    def send_email(self, emailtemplate):
        if not settings.ASYNC_EMAILS:  # TESTING
            send_emails(EMAIL_SENDER, emailtemplate, is_test=True, data=self.data)
        else:
            async(send_emails, *(EMAIL_SENDER, emailtemplate, None, True, self.data),
                  hook='notifications.forms.send_mail_sender')


class CycleEmailTemplateTriggerForm(forms.Form):

    def send_emails(self, emailtemplate, people):
        if not settings.ASYNC_EMAILS:  # TESTING
            send_emails(EMAIL_SENDER, emailtemplate, people)
        else:
            async(send_emails, *(EMAIL_SENDER, emailtemplate, people),
                  hook='notifications.forms.send_mail_sender')


class ResendEmailForm(forms.Form):

    def send_email(self, emailtemplate, person):
        send_emails(EMAIL_SENDER, emailtemplate, [person])
