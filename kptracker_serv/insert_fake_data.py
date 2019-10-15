import sqlite3, random, datetime
from sqlite3 import Error


firstNames = ["Norris", "Erminia", "Amee", "Jacinda", "Jacinto", "Joeann", "Karen", "Manuel", "Cary", "Cheryll"]
lastNames = ["Tootle", "Benn", "Medal", "Maples", "Staub", "Luera", "Chiles", "Coplin", "Byers", "Sober"]

bowlingCenterNames = ["Warlington", "Ffestiniog", "Ardglass", "Laewaes", "Stamford", "Jarren's Outpost", "Lanercost", "Goldcrest", "Nantgarth", "Sharpton"]

minimumNumberOfLanes = 2
maximumNumberOfLanes = 12

hands = ["L", "R"]
designations = ["A"]
genders = ["M", "F"]
sanction_states = [True, False]

NUMBER_OF_BOWLER_PROFILES_TO_MAKE = 5
NUMBER_OF_BOWLING_CENTERS_TO_MAKE = 5
NUMBER_OF_GAMES_TO_MAKE = 5
NUMBER_OF_LEAGUES_TO_MAKE = 5
NUMBER_OF_LEAGUE_BOWLERS_TO_MAKE = 5
NUMBER_OF_LEAGUE_SCHEDULES_TO_MAKE = 5
NUMBER_OF_TEAMS_TO_MAKE = 5
NUMBER_OF_TEAM_ROSTERS_TO_MAKE = 5
NUMBER_OF_USER_PROFILES_TO_MAKE = 5
NUMBER_OF_WEEKLY_PAIRINGS_TO_MAKE = 5

def create_connection(db_file):
	conn = None
	try:
		conn = sqlite3.connect(db_file)
	except Error as e:
		print(e)
 
	return conn
  
def create_bowler_profile(conn, bowler_profile):
	sql = ''' INSERT INTO kpbt_bowlerprofile(date_of_birth,hand,designation,is_sanctioned,last_date_sanctioned,user_id) VALUES(?,?,?,?,?,?) '''
	cur = conn.cursor()
	cur.execute(sql, bowler_profile)
	return cur.lastrowid

def create_bowling_center(conn, bowling_center):
	sql = ''' INSERT INTO kpbt_bowlingcenter(name,num_lanes,manager_id) VALUES(?,?,?) '''
	cur = conn.cursor()
	cur.execute(sql, bowling_center)
	return cur.lastrowid

def create_game(conn, game):
	sql = ''' INSERT INTO kpbt_game(series_date,applied_average,game_one_score,game_two_score,game_three_score,bowler_id,league_id,team_id) VALUES(?,?,?,?,?,?,?,?) '''
	cur = conn.cursor()
	cur.execute(sql, game)
	return cur.lastrowid

def create_league(conn, league):
	sql = ''' INSERT INTO kpbt_league(name,num_teams,designation,gender,min_roster_size,max_roster_size,is_handicap,handicap_scratch,allow_substitutes,bye_team_point_threshold,absentee_score,game_point_value,series_point_value,bowling_center_id) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
	cur = conn.cursor()
	cur.execute(sql, league)
	return cur.lastrowid

def create_leaguebowler(conn, leaguebowler):
	sql = ''' INSERT INTO kpbt_leaguebowler(league_average,league_high_game,league_high_series,league_total_scratch,league_total_handicap,bowler_id,league_id) VALUES(?,?,?,?,?,?,?) '''
	cur = conn.cursor()
	cur.execute(sql, leaguebowler)
	return cur.lastrowid

def create_leagueschedule(conn, leagueschedule):
	sql = ''' INSERT INTO kpbt_leagueschedule(date_started,date_ending,num_weeks,start_time,league_id) VALUES(?,?,?,?,?) '''
	cur = conn.cursor()
	cur.execute(sql, leagueschedule)
	return cur.lastrowid

def create_team(conn, team):
	sql = ''' INSERT INTO kpbt_team(number,name,total_pinfall,total_handicap_pins,total_scratch_pins,team_points,league_id) VALUES(?,?,?,?,?,?,?) '''
	cur = conn.cursor()
	cur.execute(sql, team)
	return cur.lastrowid

def create_teamroster(conn, teamroster):
	sql = ''' INSERT INTO kpbt_teamroster(games_with_team,is_substitute,bowler_id,team_id) VALUES(?,?,?,?) '''
	cur = conn.cursor()
	cur.execute(sql, teamroster)
	return cur.lastrowid

def create_userprofile(conn, userprofile):
	sql = ''' INSERT INTO kpbt_userprofile(first_name,last_name,email,is_league_secretary,is_center_manager,user_id) VALUES(?,?,?,?,?,?) '''
	cur = conn.cursor()
	cur.execute(sql, userprofile)
	return cur.lastrowid

def create_weeklypairing(conn, weeklypairing):
	sql = ''' INSERT INTO kpbt_weeklypairing(league_id) VALUES(?) '''
	cur = conn.cursor()
	cur.execute(sql, weeklypairing)
	return cur.lastrowid

def main():
	database = r"D:\\Documents\\GitHub\\KPTracker\\kptracker_serv\\db.sqlite3"
 
	# create a database connection
	conn = create_connection(database)
	with conn: 		
		for _ in range(0, NUMBER_OF_BOWLER_PROFILES_TO_MAKE):
			bowler_profile = (datetime.datetime.strptime('{} {}'.format(random.randint(1, 366), random.randint(1800,2020)), '%j %Y'), random.choice(hands), random.choice(designations), random.choice(sanction_states), datetime.datetime.strptime('{} {}'.format(random.randint(1, 366), random.randint(1800,2020)), '%j %Y'),  _)
			create_bowler_profile(conn, bowler_profile)

		for _ in range(0, NUMBER_OF_BOWLING_CENTERS_TO_MAKE):
			bowling_center = (random.choice(bowlingCenterNames), random.randint(minimumNumberOfLanes, maximumNumberOfLanes), _)
			create_bowling_center(conn, bowling_center)

		for _ in range(0, NUMBER_OF_GAMES_TO_MAKE):
			game = (datetime.datetime.strptime('{} {}'.format(random.randint(1, 366), random.randint(1800,2020)), '%j %Y'), random.randint(1, 300), random.randint(1, 300), random.randint(1, 300), random.randint(1, 300), _, _, _)
			create_game(conn, game)

		for _ in range(0, NUMBER_OF_LEAGUES_TO_MAKE):
			league = (random.choice(bowlingCenterNames), random.randint(1,10), random.choice(designations), random.choice(genders), random.randint(1, 4), random.randint(5, 10), random.choice(sanction_states), random.randint(1, 200), random.choice(sanction_states), random.randint(1,10), random.randint(1,10), random.randint(1,10), random.randint(1,10), _)
			create_league(conn, league)

		for _ in range(0, NUMBER_OF_LEAGUE_BOWLERS_TO_MAKE):
			league_bowler = (random.randint(1, 300), random.randint(1, 300), random.randint(1, 300), random.randint(1, 200), random.randint(1, 200), _, _)
			create_leaguebowler(conn, league_bowler)

		# for _ in range(0, NUMBER_OF_LEAGUE_SCHEDULES_TO_MAKE):
		# 	league_schedule = (datetime.datetime.strptime('{} {}'.format(random.randint(1, 366), random.randint(1800,2020)), '%j %Y'), datetime.datetime.strptime('{} {}'.format(random.randint(1, 366), random.randint(1800,2020)), '%j %Y'), random.randint(1, 10), ????TIME???? , _)
		# 	create_leagueschedule(conn, league_schedule)

		for _ in range(0, NUMBER_OF_TEAMS_TO_MAKE):
			team = (_, random.choice(bowlingCenterNames), random.randint(1, 1000), random.randint(1, 1000), random.randint(1, 1000), random.randint(1, 1000), _)
			create_team(conn, team)

		for _ in range(0, NUMBER_OF_TEAM_ROSTERS_TO_MAKE):
			team_roster = (random.randint(1, 20), random.choice(sanction_states), random.randint(1, 10), random.randint(1, 10))
			create_teamroster(conn, team_roster)

		for _ in range(0, NUMBER_OF_USER_PROFILES_TO_MAKE):
			user_profile = (random.choice(firstNames), random.choice(lastNames), random.choice(firstNames) + "@" + random.choice(lastNames) + ".com", random.choice(sanction_states), random.choice(sanction_states), random.randint(1,10))
			create_userprofile(conn, user_profile)

		# for _ in range(0, NUMBER_OF_WEEKLY_PAIRINGS_TO_MAKE):
		# 	weekly_pairing = (random.choice(bowlingCenterNames), random.randint(minimumNumberOfLanes, maximumNumberOfLanes), _)
		# 	create_weeklypairing(conn, weekly_pairing)
 
if __name__ == '__main__':
	main()