from django.db import models
from django.contrib.auth.models import User
from kpbt.accounts.models import BowlerProfile
from kpbt.centers.models import BowlingCenter
from kpbt.teams.models import Team
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from kptracker.settings import SCHEDULEFILES_FOLDER as SCHEDULEDIR


from collections import deque
from itertools import islice
from dateutil import rrule
import datetime
import itertools


class League(models.Model):
	
	bowling_center = models.ForeignKey('BowlingCenter', on_delete=models.SET_NULL, null=True,
		related_name='leagues', verbose_name=('bowling center'))
	bowlers = models.ManyToManyField('BowlerProfile', through='LeagueBowler')
	
	name = models.CharField(max_length=32)
	
	def __str__(self):
		return self.bowling_center.name + ", " + self.name
		
	def set_center(self, center_name):
		try:
			center = BowlingCenter.objects.get(name=center_name)
		except ObjectDoesNotExist:
			print("Whoa")
		else:
			self.bowling_center = center
	
	def set_name(self, name):
		self.name = name
		
	def current_week(self):
		return self.schedule.current_week

class LeagueRules(models.Model):
	league = models.OneToOneField(League, on_delete=models.CASCADE)
	
	DESIGNATION = (
		('A', 'Adult'),
		('S', 'Senior'),
		('J', 'Junior')
	)
	
	GENDER = (
		('M', 'Men'),
		('W', 'Women'),
		('X', 'Mixed'),
	)
	
	num_teams = models.PositiveSmallIntegerField()
	designation = models.CharField(max_length=1, choices=DESIGNATION)
	gender = models.CharField(max_length=1, choices=GENDER)
	min_roster_size = models.PositiveSmallIntegerField()
	max_roster_size = models.PositiveSmallIntegerField()
	is_handicap = models.BooleanField(default=False)
	handicap_scratch = models.PositiveSmallIntegerField()
	allow_substitutes = models.BooleanField(default=False)
	bye_team_point_threshold = models.PositiveSmallIntegerField()
	absentee_score = models.PositiveSmallIntegerField()
	game_point_value = models.PositiveSmallIntegerField()
	series_point_value = models.PositiveSmallIntegerField()


class LeagueBowler(models.Model):
	bowler = models.ForeignKey(BowlerProfile, on_delete=models.CASCADE)
	league = models.ForeignKey(League, on_delete=models.CASCADE)
	
	league_average = models.PositiveSmallIntegerField()
	league_high_game = models.PositiveSmallIntegerField()
	league_high_series = models.PositiveSmallIntegerField()
	league_total_scratch = models.PositiveSmallIntegerField()
	league_total_handicap = models.PositiveSmallIntegerField()
	

class Schedule(models.Model):
	league = models.OneToOneField(League, on_delete=models.CASCADE)

	date_starting = models.DateField()
	date_ending = models.DateField()
	num_weeks = models.PositiveSmallIntegerField(default=0)
	start_time = models.TimeField()
	
	current_week = models.PositiveSmallIntegerField(default=1)
	
	def calc_num_weeks(self):
		weeks = rrule.rrule(rrule.WEEKLY, dtstart=self.date_starting, until=self.date_ending)
		self.num_weeks = weeks.count()
		
	
	def advance_week(self):
		current_week += 1
	
	
		
	def pairings(self, current_week=""):
		
		
		num_teams = self.league.leaguerules.num_teams
		num_weeks = self.num_weeks // 2
		
		if num_teams % 2:
			num_teams += 1
			
			
		filename = str(num_teams) + 'teams'
		filedir = SCHEDULEDIR + filename + '.csv'
		
		pairings = [None] * num_weeks
		with open(filedir) as schedule:
			
			schedule.readline() #skip first line to allow week number to align with list index
			
			for i in range(1, num_weeks):
				
				weekly_pairings = schedule.readline()
				
				weekly_pairing_list = weekly_pairings.strip('\n').split(',')
				pairings[i] = weekly_pairing_list
			
		
				
		
		if current_week:
		
			
			return [pairings[current_week]]
		else:
			return pairings
		
		
		
		
		"""this_league = self.league
		
		teams = list(range(1, this_league.leaguerules.num_teams+1))
		
		if len(teams) % 2:
			teams.append('Bye')
		
		mid = len(teams) // 2
		dq1 = deque(islice(teams, None, mid))
		dq2 = deque(islice(teams, mid, None))
		
		week_range = self.num_weeks - 1
		
		for _ in range(week_range):
			yield list(zip(dq1, dq2))
			start = dq1.popleft()
			dq1.appendleft(dq2.popleft())
			dq2.append(dq1.pop())
			dq1.appendleft(start)
		
		"""

"""		
	def shuffle(self, pairings):
		mod_base = len(pairings[0]) 
		mod_counter = mod_base - 1
		num_weeks = len(pairings)
		cur_week = 1
		
		for i in range(1, num_weeks):
			#print(mod_base, mod_counter)
			p_list = list(pairings[i])
			front_slice = ifilter(lambda x: x%2, p_list)
			back_slice = islice(lambda x: (x%2)+1, p_list)
			#slice = list(p_list[-(mod_counter)])
			#print(list(front_slice))
			#print(list(back_slice))
			new_list = list(itertools.chain(back_slice, front_slice))
			print(new_list)
			#slice.append(p_list)
			#print(slice)
			
			
			mod_counter -= 1
			if mod_counter < 0:
				mod_counter = mod_base - 1
			
			p_list = list(pairings[i])
			shifted_team = p_list.pop() #remove last team, insert it in front
			p_list.insert(0, shifted_team)
			print(p_list)
			
			print('Range is ' + i.__str__())
			if not cur_week % 2: #Every even week, reverse the order of each individual pairing
				#print('Cur week is ' + cur_week.__str__())
				reverse_list = []
				for j in pairings[cur_week]:
					j = tuple(reversed(j))
					reverse_list.append(j)
				#yield reverse_list
				
				for j in range(1, len(pairings[i])):
					swap = list(pairings[cur_week][j]) #convert tuple to list for swapping
					temp = swap[0]
					print(temp)
					swap[0] = swap[1]
					swap[1] = temp
					
					#, pairings[cur_week][j][1] = pairings[cur_week][j][1], pairings[cur_week][j][0]
					j =+ 2 # Move to the next pair
				
			
			cur_week += 1

					
"""				
			