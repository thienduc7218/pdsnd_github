import time

import numpy as np
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv', 'new york': 'new_york_city.csv', 'washington': 'washington.csv' }

def collect_filters():
    """
    Collects user input for city, month, and day filters for exploring US bikeshare data.

    Returns:
        tuple: A tuple containing the selected city, month, and day filters.
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    city = input('\nWhich city data to see? : Chicago, New York, or Washington: ').lower()
    while city not in CITY_DATA:
        print('That\'s not a valid entry!')
        city = input('\nWhich city data to see? : Chicago, New York, or Washington: ').lower()

    filter = input('\nWould you like to filter by day or month? Please type day/month : ').lower()
    while filter not in ['day', 'month']:
        print('That\'s not a valid entry!')
        filter = input('\nWould you like to filter by day or month? Please type day/month : ').lower()

    if filter == 'day':
        day = input('\nwhich day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or all? Please type day name / all: ').lower()
        while day not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
            print('That\'s not a valid entry!')
            day = input('\nwhich day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or all ? please type day name / all: ').lower()
        month = 'all'
    else:
        month = input('\nWhich month? January, February, March, April, May, June or all? Please type month name / all: ').lower()
        while month not in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            print('That\'s not a valid entry!')
            month = input('\nWhich month? JJanuary, February, March, April, May, June or all? Please type month name / all: ').lower()
        day = 'all'

    print('='*100)
    return city, month, day

def consume_data(city, month, day):
    """
    Reads and filters bikeshare data based on the specified city, month, and day.

    Parameters:
    - city (str): The name of the city to retrieve data for.
    - month (str): The name of the month to filter data for. Use 'all' to include all months.
    - day (str): The name of the day of the week to filter data for. Use 'all' to include all days.

    Returns:
    - pandas.DataFrame: A DataFrame containing the filtered bikeshare data.

    """
    data = pd.read_csv(CITY_DATA[city])
    data['Start Time'] = pd.to_datetime(data['Start Time'])
    data['month'] = data['Start Time'].dt.month
    data['day_of_week'] = data['Start Time'].dt.day_name()
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        data = data[data['month'] == month]
    if day != 'all':
        data = data[data['day_of_week'] == day.title()]
    return data

def time_based_analyze(data):
    """
    Analyzes the most frequent times of travel based on the given data.

    Args:
        data (pandas.DataFrame): The data containing information about bike rides.

    Returns:
        Print out the result
    """
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    pop_month = data['month'].mode()[0]
    print('\nMost Common month is:', pop_month)
    pop_day = data['day_of_week'].mode()[0]
    print('\nMost Common day is:', pop_day)
    data['hour'] = data['Start Time'].dt.hour
    pop_hour = data['hour'].mode()[0]
    print('\nMost common hour is:', pop_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('='*100)

def station_based_analyze(data):
    """
    Analyzes the most popular stations and trips based on the given data.

    Args:
        data (pandas.DataFrame): The data containing information about bike trips.

    Returns:
        Print out the result
    """
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    start_station = data['Start Station'].mode()[0]
    print('\nMost Commonly used start station:', start_station)
    end_station = data['End Station'].value_counts().idxmax()
    print('\nMost Commonly used end station:', end_station)
    combination = data.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('\nMost Commonly used combination of start station and end station trip:', combination)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('='*100)

def trip_duration_based_analyze(data):
    """
    Analyzes the trip duration based on the provided data.

    Parameters:
        data (pandas.DataFrame): The data containing trip duration information.

    Returns:
        Print out the result
    """
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    total_travel_time = sum(data['Trip Duration'])
    print('\nTotal travel time is: ', total_travel_time/3600, " hours")
    average_travel_time = data['Trip Duration'].mean()
    print('\nAverage travel time is: ', average_travel_time/3600, " hours")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('='*100)

def user_based_analyze(data, city):
    """
    Analyzes user statistics based on the given data and city.

    Args:
        data (pandas.DataFrame): The data containing user information.
        city (str): The name of the city.

    Returns:
        Prints out the user types and, if the city is 'chicago' or 'new york', also prints the user gender,
        earliest year of birth, most recent year of birth, and most common year of birth.

    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    user_types = data['User Type'].value_counts()
    print(user_types)
    if city in ['chicago', 'new york']:
        user_gender = data['Gender'].value_counts()
        print(user_gender)
        earliest = int(data['Birth Year'].min())
        most_recent = int(data['Birth Year'].max())
        most_common = int(data['Birth Year'].mode()[0])
        print("\nThe earliest year of birth is: ", earliest)
        print("\nMost recent year of birth is: ", most_recent)
        print("\nThe most common year of birth is: ", most_common)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('='*100)

def display(data):
    """
    Displays 5 rows of individual trip data from a given DataFrame.

    Args:
        data (pandas.DataFrame): The DataFrame containing the trip data.

    Returns:
        None
    """
    while True:
        view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
        if view_data.lower() == 'yes':
            print('\nPlease stretch the width of your window to accomodate all colomuns in one horizontal row\n')
            break
        elif view_data.lower() == 'no':
            return
        else:
            print('That\'s not a valid entry !')

    position = 0
    while view_data == 'yes' and position <= (len(data.index)-5):
        try:
            print(data.iloc[position : position + 5])
            position += 5
            view_data = input("\nDo you wish to continue viewing more rows?: ").lower()
        except:
            print('That\'s not a valid entry !')

def main():
    """
    The main function of the bikeshare program.

    This function runs the main logic of the bikeshare program. It collects filters from the user,
    consumes data based on the filters, performs various analyses on the data, displays the results,
    and asks the user if they want to restart the program.

    Returns:
        None
    """
    while True:
        city, month, day = collect_filters()
        data = consume_data(city, month, day)
        time_based_analyze(data)
        station_based_analyze(data)
        trip_duration_based_analyze(data)
        user_based_analyze(data, city)
        display(data)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

main()
