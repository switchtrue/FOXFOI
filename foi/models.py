from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class CaseManager(models.Manager):
    def create_case(self, title, user):
        case = self.create(title = title, created_date = timezone.now(), created_by = user)
        case.save()
        return case

class CommentManager(models.Manager):
    def create_comment(self, case, subject, body, user):
        comment = self.create(case = case, subject = subject, body = body, created_date = timezone.now(), created_by = user)
        comment.save()
        return comment

class AssessmentManager(models.Manager):
    def create_assessment(self, case):
        assessment = self.create(case = case)
        assessment.save()
        return assessment

class OutcomeManager(models.Manager):
    def create_outcome(self, case):
        outcome = self.create(case = case)
        outcome.save()
        return outcome

class InternalReviewManager(models.Manager):
    def create_internal_review(self, case):
        ir = self.create(case = case)
        ir.save()
        return ir

class InformationCommissionerAppealManager(models.Manager):
    def create_information_commissioner_appeal(self, case):
        ica = self.create(case = case)
        ica.save()
        return ica

class AdministrativeAppealsTribunalManager(models.Manager):
    def create_administrative_appeals_tribunal(self, case):
        aat = self.create(case = case)
        aat.save()
        return aat

class Case(models.Model):

    CORRESPONDENCE_METHOD = (
        ('EMAIL', 'Email'),
        ('LETTER', 'Letter'),
        ('PHONE', 'Phone'),
        ('FAX', 'Fax')
    )

    title = models.CharField(max_length = 100)
    subject = models.CharField(max_length = 250, blank = True, default = "")
    received_date = models.DateField(blank = True, null = True)
    enquiry_date = models.DateField(blank = True, null = True)
    enquiry_ref = models.CharField(max_length = 50, blank = True, default = "")
    enquiry_method = models.CharField(max_length = 20, choices = CORRESPONDENCE_METHOD, blank = True, default = "")
    response_method = models.CharField(max_length = 20, choices = CORRESPONDENCE_METHOD, blank = True, default = "")
    enquiry_description = models.CharField(max_length = 200, blank = True, default = "")
    urgent_flag = models.BooleanField(default = False)
    handling_instructions = models.CharField(max_length = 200, blank = True, default = "")
    addressee_name = models.CharField(max_length = 100, blank = True, default = "")
    created_date = models.DateTimeField()
    created_by = models.ForeignKey(User)

    def __unicode__(self):
        return self.title

    objects = CaseManager()

class Comment(models.Model):
    case = models.ForeignKey(Case)
    subject = models.CharField(max_length = 100)
    body = models.TextField()
    created_date = models.DateTimeField()
    created_by = models.ForeignKey(User)

    def __unicode__(self):
        return self.subject

    objects = CommentManager()

class Assessment(models.Model):

    THIRD_PARTY_CONSULTATION_REASON = (
        ('PERSON_BUSINESS', 'a person''s business or professional affairs'),
        ('ORGANISATION_BUSINESS', 'an organisation''s business or professional affairs'),
        ('PERSON_PERSONAL', 'an individual''s personal information'),
        ('GOVERNMENT', 'material originating or received from a State or Territory government'),
        ('FOREIGN', 'material originating or received from a foreign entity')
    )

    DOCUMENTS_ATTACHED_OR_DESCRIBED = (
        ('ATTACHED', 'Attached'),
        ('DESCRIBED', 'Described')
    )

    case = models.ForeignKey(Case)
    third_party_consultation = models.BooleanField(default = False)
    precedents = models.BooleanField(default = False)
    precedent_details = models.TextField(blank = True, null = True)

    # fee details
    fee_flag = models.BooleanField(default = False)
    search_and_retrieval_time = models.DecimalField(max_digits = 10, decimal_places = 2, blank = True, null = True)
    decision_making_time = models.DecimalField(max_digits = 10, decimal_places = 2, blank = True, null = True)
    photocopy_charges = models.DecimalField(max_digits = 10, decimal_places = 2, blank = True, null = True)
    other_access_time = models.DecimalField(max_digits = 10, decimal_places = 2, blank = True, null = True)
    postage_charges = models.DecimalField(max_digits = 10, decimal_places = 2, blank = True, null = True)
    initial_deposit = models.DecimalField(max_digits = 10, decimal_places = 2, blank = True, null = True)
    request_general_description = models.CharField(max_length = 100, blank = True)
    include_refine_request_flag = models.BooleanField(default = False)
    include_third_party_consultation_flag = models.BooleanField(default = False)
    request_concerning = models.CharField(max_length = 100, choices = THIRD_PARTY_CONSULTATION_REASON, blank = True)
    contact_name = models.CharField(max_length = 100, blank = True)
    contact_telephone = models.CharField(max_length = 30, blank = True)

    # fee metadata
    fee_notice_issued_flag = models.BooleanField(default = False)
    fee_notice_issued_date = models.DateField(blank = True, null = True)
    fee_payment_required_date = models.DateField(blank = True, null = True)
    fee_paid_flag = models.BooleanField(default = False)
    fee_received_date = models.DateField(blank = True, null = True)
    fee_limit_flag = models.BooleanField(default = False)

    # third party consultation data
    third_party_request_general_description = models.CharField(max_length = 100, blank = True, default = "")
    documents_attached_or_described = models.CharField(max_length = 100, choices = DOCUMENTS_ATTACHED_OR_DESCRIBED, blank = True)
    include_s47_flag = models.BooleanField(default = False)
    include_s47b_flag = models.BooleanField(default = False)
    include_s47f_flag = models.BooleanField(default = False)
    include_s47g_flag = models.BooleanField(default = False)
    respond_by_date = models.DateField(blank = True, null = True)
    third_party_contact_name = models.CharField(max_length = 100, blank = True, default = "")
    third_party_contact_telephone = models.CharField(max_length = 30, blank = True, default = "")

    # third party details
    third_party_title = models.CharField(max_length = 20, blank = True)
    third_party_name = models.CharField(max_length = 100, blank = True)
    third_party_department = models.CharField(max_length = 100, blank = True)
    third_party_organisation = models.CharField(max_length = 100, blank = True)
    third_party_address = models.CharField(max_length = 400, blank = True)
    third_party_postcode = models.CharField(max_length = 10, blank = True)

    def __unicode__(self):
        return self.case.title

    objects = AssessmentManager()

class Outcome(models.Model):

    FOI_OUTCOMES = (
        ('FULL_ACCESS', '1) Grant access in full'),
        ('PARTIAL_EXEMPTION', '2) Withhold some documents as exempt'),
        ('FULL_EXEMPTION', '3) Withhold all documents as exempt'),
        ('DEFER', '4) Defer access'),
        ('REDACTION', '5) Grant access with redactions'),
        ('DNE', '6) Documents do not exist or cannot be found'),
        ('NCND', '7) Neither confirm nor deny')
    )

    FOI_EXEMPTIONS = (
        ('CSR', 'Commonwealth-State Relations'),
        ('DPRAMF', 'Deliberative Processes Relating to Agencies'' or Ministers'' Functions'),
        ('FPIC', 'Financial and Property Interests of the Commonwealth'),
        ('OAM', 'Operations of Agencies Management'),
        ('PP', 'Personal Privacy'),
        ('BA', 'Business Affairs'),
        ('RCANU', 'Research by CSIRO or the Australian National University'),
        ('AE', 'Australia''s Economy')
    )

    FOI_CONDITIONAL_EXEMPTIONS = (
        ('CSR', 'Commonwealth-State Relations'),
        ('DPRAMF', 'Deliberative Processes Relating to Agencies'' or Ministers'' Functions'),
        ('FPIC', 'Financial and Property Interests of the Commonwealth'),
        ('OAM', 'Operations of Agencies Management'),
        ('PP', 'Personal Privacy'),
        ('BA', 'Business Affairs'),
        ('RCANU', 'Research by CSIRO or the Australian National University'),
        ('AE', 'Australia''s Economy')
    )

    DISCLOSURE_OUTCOMES = (
        ('GRANTED_IN_FULL', 'Granted In Full'),
        ('WITHHELD_IN_PART', 'Withheld In Part'),
        ('WITHHELD_IN_FULL', 'Withheld In Full')
    )

    CERTIFICATES = (
        ('National Security', 'National Security'),
        ('Defence', 'Defence'),
        ('International Relations', 'International Relations'),
        ('Relations with States', 'Relations with States'),
        ('Cabinet Documents', 'Cabinet Documents'),
        ('Executive Council Documents', 'Executive Council Documents'),
        ('Internal Working Documents', 'Internal Working Documents')
    )


    case = models.ForeignKey(Case)
    foi_outcomes = models.CharField(max_length = 100, choices = FOI_OUTCOMES, blank = True)
    foi_exemptions = models.CharField(max_length = 100, choices = FOI_EXEMPTIONS, blank = True)
    foi_conditional_exemptions = models.CharField(max_length = 100, choices = FOI_CONDITIONAL_EXEMPTIONS, blank = True)
    disclosure_outcomes = models.CharField(max_length = 100, choices = DISCLOSURE_OUTCOMES, blank = True)
    certificates = models.CharField(max_length = 100, choices = CERTIFICATES, blank = True)

    def __unicode__(self):
        return self.case.title

    objects = OutcomeManager()

class InternalReview(models.Model):
    case = models.ForeignKey(Case)
    requested_date = models.DateField(blank = True, null = True)
    review_held_date = models.DateField(blank = True, null = True)
    days_taken_to_hold_review = models.IntegerField(blank = True, null = True)
    review_members = models.TextField(blank = True, null = True)
    review_decision = models.TextField(blank = True, null = True)

    def __unicode__(self):
        return self.case.title

    objects = InternalReviewManager()

class InformationCommissionerAppeal(models.Model):
    case = models.ForeignKey(Case)
    contacted_date = models.DateField(blank = True, null = True)
    documents_provided_date = models.DateField(blank = True, null = True)
    decision_recieved_date = models.DateField(blank = True, null = True)
    decision = models.TextField(blank = True, null = True)
    decision_notice = models.CharField(max_length = 100, blank = True)

    def __unicode__(self):
        return self.case.title

    objects = InformationCommissionerAppealManager()

class AdministrativeAppealsTribunal(models.Model):
    case = models.ForeignKey(Case)
    contacted_date = models.DateField(blank = True, null = True)
    documents_provided_date = models.DateField(blank = True, null = True)
    decision_recieved_date = models.DateField(blank = True, null = True)
    decision = models.TextField(blank = True, null = True)
    decision_notice = models.CharField(max_length = 100, blank = True)

    def __unicode__(self):
        return self.case.title

    objects = AdministrativeAppealsTribunalManager()
