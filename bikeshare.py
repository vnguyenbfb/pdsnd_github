import pandas as pd
import time

cities = {'Chicago': 'chicago.csv', 'Washington': 'washington.csv', 'New York': 'new_york_city.csv'}

def get_filters():
  
  city_list = list(cities.keys())
  
  """ GET CITY NAME """
  while True:
    city = str(input('Please enter a city name (Chicago, New York or Washington): '))
    city = city.title()
    if city not in city_list:
      print('Please enter a valid city name.')
    else:
      break
  
  """ GET THE FILTER """
  filter = input("Would you like to see by month (type 'month'), by day (type 'day') or both (type 'both')? Press any key if you do not want any filter. ")
  
  return city, filter 

def load_data(city, filter):

  months = ['January', 'February', 'March', 'April', 'May', 'June']
  month_dict = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6}

  df = pd.read_csv(cities[city])
  df['Start Time'] = pd.to_datetime(df['Start Time'])
  df['Month'] = df['Start Time'].dt.month
  df['Dayofweek'] = df['Start Time'].dt.dayofweek
  df['Hour'] = df['Start Time'].dt.hour

  if filter.lower() == 'month':
    while True:
      month_choice = str(input('Please enter full name of a month (January, February, March, April, May or June): '))
      if month_choice in months:
        break
      else:
        print('Please re-enter a valid month: ')
    df = df[(df['Month'] == month_dict.get(month_choice))]  

  elif filter.lower() == 'day':
    while True:
      dayofweek_choice = int(input('Please enter a number between 0 and 6 i.e 0 for Monday, 1 for Tuesday, ect: '))
      if dayofweek_choice in range (0, 7):
        break
      else:
        print('Please re-enter a valid number: ')  
    df = df[(df['Dayofweek'] == dayofweek_choice)]

  elif filter.lower() == 'both':
    while True:
      month_choice = str(input('Please enter full name of a month (January, February, March, April, May or June): '))
      if month_choice in months:
        break
      else:
        print('Please re-enter a valid month: ')
    while True:
      dayofweek_choice = int(input('Please enter a number between 0 and 6 i.e 0 for Monday, 1 for Tuesday, ect: '))
      if dayofweek_choice in range (0, 7):
        break
      else:
        print('Please re-enter a valid number: ')  
    df = df[(df['Month'] == month_dict.get(month_choice)) & (df['Dayofweek'] == dayofweek_choice)]
  
  else: 
    filter = 'None'
  return df, filter

def most_popular_time(df, city, filter):
  start_time = time.time()
  travel_time = df.groupby(['Hour'])['Hour'].count().reset_index(name='Count')
  most_travel_time =travel_time.loc[travel_time['Count'].idxmax()]
  runtime = time.time() - start_time 
  
  print('\n*********************************************')
  print('Calculating ... Popular times of travel')
  print('Filter: ', filter)
  print('City: ', city)
  print('\nMost_travel_time:\n', most_travel_time) 
  print('Runtime: ', runtime, 'seconds') 

def most_popular_trip(df, city, filter):
  start_time = time.time()
  df['Trip'] = df['Start Station'] + ' ' + df['End Station']
 
  popular_start_station = df.groupby(['Start Station'])['Start Station'].count().reset_index(name='Count')
  maxcount_start_station = popular_start_station.loc[popular_start_station['Count'].idxmax()]

  popular_end_station = df.groupby(['End Station'])['End Station'].count().reset_index(name='Count')
  maxcount_end_station = popular_end_station.loc[popular_end_station['Count'].idxmax()]

  popular_trip = df.groupby(['Trip'])['Trip'].count().reset_index(name='Count')
  maxcount_trip = popular_trip.loc[popular_trip['Count'].idxmax()]

  runtime = time.time() - start_time 

  print('\n*********************************************')
  print('Calculating ... Popular stations and trip')
  print('Filter: ', filter)
  print('City: ', city)
  print('\nMaxcount_start_station:\n', maxcount_start_station)
  print('\nMaxcount_end_station:\n', maxcount_end_station)
  print('\nMaxcount_trip:\n', maxcount_trip)
  print('Runtime: ', runtime, 'seconds')

def trip_duration(df, city, filter):
  start_time = time.time()
  total_travel_time = df['Trip Duration'].sum()
  average_travel_time = df['Trip Duration'].mean()
  
  runtime = time.time() - start_time 

  print('\n*********************************************')
  print('Calculating ... Trip duration')
  print('Filter: ', filter)
  print('City: ', city)
  print('\nTotal_travel_time: ', total_travel_time)
  print('Average_travel_time: ', average_travel_time)
  print('Runtime: ', runtime, 'seconds')

def user_info(df, city, filter):
  """ NO GENDER AND BIRTH YEAR DATA FOR WASHINGTON CITY """
  start_time = time.time()
  user_count = df.groupby(['User Type'])['User Type'].count().reset_index(name='Count')

  if city == 'Chicago' or city == 'New York':
    gender_count = df.groupby(['Gender'])['Gender'].count().reset_index(name='Count')
    earliest_birthyear = df['Birth Year'].min()
    most_recent_birthyear = df['Birth Year'].max() 
    birthyear_list = df.groupby(['Birth Year'])['Birth Year'].count().reset_index(name='Count')
    most_common_birthyear = birthyear_list.loc[birthyear_list['Count'].idxmax()]
    
  else:
    gender_count = 'No data for gender' 
    earliest_birthyear = 'No data for birth year'
    most_recent_birthyear = 'No data for birth year'
    most_common_birthyear = 'No data for birth year'
    
  runtime = time.time() - start_time 

  print('\n*********************************************')
  print('Calculating ... User info')
  print('Filter: ', filter)
  print('City: ', city)
  print('\nUser count by type:\n', user_count)
  print('\nGender count by type:\n', gender_count)
  print('\nEarliest birthyear: ', earliest_birthyear)
  print('\nMost recent birthyear: ', most_recent_birthyear) 
  print('\nMost common birthyear:\n', most_common_birthyear) 
  print('Runtime: ',runtime, 'seconds')

def show_raw_data(df):
  see_data = input('Would you like to see 5 lines of raw data? Type \'Y\' or \'N\' ')
  start_loc = 0
  while True:
    if see_data.upper() == 'N':
      break
    elif see_data.upper() == 'Y':
      print(df.iloc[:start_loc+5])
      start_loc += 5
      see_data = input('Would you like to see more raw data? Type \'Y\' or \'N\' ')
    else:
      print('Seems like there is an issue with your input. Please re-enter your answer.')
      see_data = input('Type \'Y\' or \'N\' ')

def main():
  while True:
    city, filter= get_filters()
    df, filter = load_data(city, filter)
    most_popular_time(df, city, filter)
    most_popular_trip(df, city, filter)
    trip_duration(df, city, filter)
    user_info(df, city, filter)
    show_raw_data(df)

    print('------------------------------------------------------------------------------')
    restart = input('Would you like to restart? Type \'Y\' or \'N\' ')
    while True:
      if restart.upper() == 'N':
        print('END OF REPORT')
        breaker = True
        break
      elif restart.upper() == 'Y':
        main()
      else:
        print('Seems like there is an issue with your input. Please re-enter your answer.')
        restart = input('Type \'Y\' or \'N\' ')
        continue
    if breaker == True:
      break

main()
