from django.db import models
from gsheets import mixins
from uuid import uuid4


class BotUser(models.Model):
	user_id = models.IntegerField(unique=True)
	first_name = models.CharField(max_length=256, blank=True, null=True)
	tel_number = models.CharField(max_length=512, blank=True, null=True)
	active = models.BooleanField(default=False)
	permission = models.CharField(max_length=255, blank=True, null=True)
	language = models.CharField(max_length=255, blank=True, null=True)
	cr_on = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.first_name


class Candidate(mixins.SheetSyncableMixin, models.Model):
	user_id = models.CharField(max_length=255, blank=True, null=True)
	fullname = models.CharField(max_length=255, blank=True, null=True)
	age = models.CharField(max_length=10, blank=True, null=True)
	contact_number = models.CharField(max_length=255, blank=True, null=True)
	address = models.CharField(max_length=255, blank=True, null=True)
	education = models.CharField(max_length=255, blank=True, null=True)
	first_salary = models.CharField(max_length=255, blank=True, null=True)
	ex_workplace = models.CharField(max_length=255, blank=True, null=True)
	leisure_activities = models.CharField(max_length=255, blank=True, null=True)
	achievements = models.CharField(max_length=600, blank=True, null=True)
	ex_salary = models.CharField(max_length=255, blank=True, null=True)
	expected_salary = models.CharField(max_length=255, blank=True, null=True)
	start_salary = models.CharField(max_length=255, blank=True, null=True)
	salary_factor = models.CharField(max_length=600, blank=True, null=True) #kompaniya nima uchun pul tolaydi
	best_employee = models.CharField(max_length=255, blank=True, null=True)
	marital_status = models.CharField(max_length=255, blank=True, null=True)
	book = models.CharField(max_length=600, blank=True, null=True)
	bad_habit = models.CharField(max_length=600, blank=True, null=True)
	work_achievements = models.CharField(max_length=600, blank=True, null=True)
	ready_to_start = models.CharField(max_length=255, blank=True, null=True)
	step = models.IntegerField(default=0)
	on_process = models.BooleanField(default=False)
	filled_date = models.CharField(max_length=255)
	ads_type = models.CharField(max_length=255)

	class  Meta:
		verbose_name_plural = "Candidates"
 
	def __str__(self):
		return self.fullname


