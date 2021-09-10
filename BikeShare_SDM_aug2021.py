#!/usr/bin/env python
# coding: utf-8

# In[ ]:



import os as os
import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_DATA = { 'all': "",'january': 1,'february': 2,'march': 3,'april': 4,'may': 5,'june': 6,'july': 7,'august': 8,'september': 9,'october': 10,'november': 11,'december': 12}

DAY_DATA = ['all', 'monday', 'tuesday', 'wednesday', 'friday', 'saturday', 'sunday']


def get_filters():
    """
    First - outputs CWD - as someone who uses multiple paths to run Jupyter notebook, this quick working directory note is usefull
    It then continues to  asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print('\n\nFirst, you should know your current directory is: ', os.getcwd(), '\n- if that is correct and the bikeshare CSVs are stored here then please continue by answering some questions\n\n')


    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs


    city = ''

    while city not in CITY_DATA:
        city = input("\nWhat is the name of the city to analyze data? (Input either chicago, new york city, washington)\n").lower()
        if city in CITY_DATA:
            break
        else:
            print('\nI am sorry but your input is invalid, please select chicago, new york city or washington ')


    # TO DO: get user input for month (all, january, february, ... , june)


    month = ''

    while month not in MONTH_DATA:
        month = input("\nWhich month would you like to analyze? (availible months are january, february, march, april, may, june or all \n").lower()
        if month in MONTH_DATA:
            break
        else:
            print('\nI am sorry but your input is invalid, please select a month or "all" ')


    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    day = ''

    while day not in DAY_DATA:
        day = input("\nWhich day of the week would you like to analyze? select monday throught to sunday or all \n").lower()
        if day in DAY_DATA:
            break
        else:
            print('\nI am sorry but your input is invalid, please select a day of the week or "all" ')

    print('\n','-'*30)
    print('\n you have made the following selections:', '\n city: ', city.upper(), '\n month: ', month.upper(), '\n and day: ', day.upper(), '\n\n')
    print('\n','-'*30)
    return city, month, day



def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city])

    df['Start Time']=pd.to_datetime(df['Start Time'])

    df['hour']= df['Start Time'].dt.hour
    df['year']= df['Start Time'].dt.year
    df['month']= df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()


    #user filter
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
        df = df[df['month']==month]
    if day != 'all':
        df = df[df['day_of_week']==day.title()]

    return df

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    #calculate most popular / mode

    popular_hour = df['hour'].mode()[0]
    popular_day = df['day_of_week'].mode()[0]
    popular_month = df['month'].mode()[0]


    # TO DO: display the most common month
    print('Most Frequent Start month:', popular_month)


    # TO DO: display the most common day of week
    print('Most Frequent Start day:', popular_day)

    # TO DO: display the most common start hour
    print('Most Frequent Start Hour:', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*30)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_stat= df['Start Station'].mode()[0]
    print("The most common start station is {}.\n".format(start_stat))


    # TO DO: display most commonly used end station
    end_stat= df['End Station'].mode()[0]
    print("The most common end station is {}.\n".format(end_stat))

    # TO DO: display most frequent combination of start station and end station trip
    combination = df.groupby(['Start Station', 'End Station']).size().nlargest()

    print('The most common start and end combinition is shown below: \n\n', combination.head(1))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time

    sum_time = df['Trip Duration'].sum()
    print('The total travel time for the filtered data was: ', round(sum_time/(60*60),2), ' hours \n')


    # TO DO: display mean travel time

    mean_time = df['Trip Duration'].mean()
    print('The average travel time for the filtered data was: ', round(mean_time/60,1), 'minutes')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users. Filters no user data"""

    print('\nCalculating User Stats...\n')
    start_time = time.time()


    if 'Gender' in df.columns:
        types = df['User Type'].unique()
        print('\nThe filtered data contains the following user types:\n', types)
        types = df['User Type'].value_counts()
        print('\nThe breakdown of these types are shown here:\n', types)
        gcount = df['Gender'].value_counts()
        print('\nThe gender split looks like:\n', gcount)
        early = df['Birth Year'].min()
        last = df['Birth Year'].max()
        common = df['Birth Year'].mode()
        print('\nThe oldest user was born in {}, whilst the youngest user was born in {}. The most common year of birth was {}'.format(int(early), int(last), int(common)))
    else:
        print('No user data can be calculated for this city filter')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """prompts user whether they would like to see 5 lines of raw data"""
    i=0
    raw_request=input('Would you like to see 5 lines of raw data? Enter yes or no')
    while raw_request.lower() == 'yes' and i+5 < df.shape[0]:
        print(df.iloc[i:i+5])
        i += 5
        raw_request = input('Would you like to see 5 more lines of data? Enter yes or no')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)
        restart = input('\nWell that was fun, would you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()


# In[ ]:





# In[ ]:
