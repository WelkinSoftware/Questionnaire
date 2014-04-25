from django.db import models
class Student(models.Model):
		freshman = 'fr'
		sophomore = 'so'
		junior = 'jr'
		senior = 'sr'
		year_in_school_choices = (
			(freshman, 'Freshman'),
			(sophomore, 'Sophomore'),
			(junior, 'Junior'),
			(senior, 'Senior'),
		)
		
		class Meta:
			app_label = 'test'
			
		year_in_school = models.CharField(max_length=2,
			choices=year_in_school_choices,
			default=freshman)
		
		def is_upperclass(self):
			return self.year_in_school in (self.junior, self.senior)

