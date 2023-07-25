import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:
        city = input("Enter the city you would like to analyze data for: ").lower()
        if city not in CITY_DATA:
            print("Your input is not a valid city.")
        else:
            break  
    
    # TO DO: get user input for month (all, january, february, ... , june)

    while True:
        month = input("Please enter the month you would like to analyze data for, or type ALL for the entire period: ").lower()
        if month not in ('all','january','february','march','april','may','june'):
            print("Your input is not a valid month or ALL.")
        else:
            break  


    while True:
        day = input("Please enter the weekday you would like to analyze data for, or type ALL to not specify: ").lower()
        if day not in ('all','monday','tuesday','wednesday','thursday','friday','saturday','sunday'):
            print("Your input is not a valid weekday or ALL.")
        else:
            break
        
    print('-'*40)
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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()


    popular_month = df['month'].mode()[0]
    print('Most popular month of travel:', popular_month)

    popular_weekday = df['day_of_week'].mode()[0]
    print('Most popular day of the week:', popular_weekday)   



    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find and print the most common hour (from 0 to 23)
    popular_hour = df['hour'].mode()[0]
    print('Most popular starting hour:', popular_hour)   

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most popular start station:', popular_start_station)   

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most popular end station:', popular_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    df['Combination'] = df['Start Station'] + " , " + df['End Station']
    popular_combination = df['Combination'].mode()[0]
    print('Most popular combination of start and end station:', popular_combination)

    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Travel Time'] = df['End Time'] - df['Start Time']  
    total_travel_time = df['Travel Time'].sum()
    print('Total travel time:', total_travel_time)
    
    # TO DO: display mean travel time
    mean_travel_time = df['Travel Time'].mean()
    print('Mean travel time for each trip:', mean_travel_time)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Breakdown of user types:\n',user_types)

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print('\nBreakdown of gender:\n',gender)    

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_yob = df['Birth Year'].min()
        print('Earliest year of birth:', int(earliest_yob))
    
        recent_yob = df['Birth Year'].max()
        print('Most recent year of birth:', int(recent_yob))

        common_yob = df['Birth Year'].mode()
        print('Most common year of birth:', int(common_yob))
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def raw_data(df):    
    """Asks the user if raw data view is desired."""
    print('\nCalculating User Stats...\n')

    while len(df.index)>0:
        raw_view = input("Would you like to view 5 (more) rows of raw data? (y/n)").lower()
        if raw_view not in ('y','n'):
            print("I did not understand your response. Please state y or n.")
        elif raw_view == 'y':
            print(df.head()) 
            df.drop(index=df.index[:5], axis=0, inplace=True)
        else:
            break
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
