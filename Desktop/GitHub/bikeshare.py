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
    cities = ['chicago', 'new york city', 'washington']
    city = input("Please Enter the name of the city you want to see its statistics [chicago, new york city, washington]").lower()
    while city not in cities:
            city = input("Please try to enter the city name again keeping in mind it should be the same like this 'chicago', 'new york city', 'washington' ")
            

    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    month = input("Please Enter the month you want to filter by.\n HINT: if you want to filter by all months, please type all.\n").lower()
    while month  not in months:
        month = input("Please try to enter the month again keeping in mind it should be the one of these names all, january, february, march, april, may, june").lower()
                  

    days = ['all', 'saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday']
    day = input("Please Enter the day you want to filter by.\n HINT: if you want to filter by all days, please type all.\n").lower()
    while day  not in days:
        day = input("Please try to enter the day again keeping in mind it should be the one of these names all, saturday, sunday, monday, tuesday, wednesday, thursday, friday").lower()

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
    df['day_of_week'] = df['Start Time'].dt.day_name()

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

    months = ['january', 'february', 'march', 'april', 'may', 'june']
    print("The most Common Month is: ", months[int(df["month"].value_counts().idxmax())-1])

    print("The most Common Day is: ", df["day_of_week"].value_counts().idxmax())

    df['hour'] = df['Start Time'].dt.hour
    print("The most Common hour is: ", df["hour"].value_counts().idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    print("The most Commonly used start station is: ", df["Start Station"].value_counts().idxmax())

    print("The most Commonly used end station is: ", df["End Station"].value_counts().idxmax())

    most_frequent_trip = df[['Start Station', 'End Station']].mode().loc[0]
    print("The most frequent trip is: ", most_frequent_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_duration = df['Trip Duration'].sum()
    print("total travel time in hours is: ", total_duration)

    mean_duration = df['Trip Duration'].mean()
    print("mean travel time in hours is: ", mean_duration)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts()
    print(user_types)
    if city != "washington":
        user_gender = df['Gender'].value_counts().idxmax()
        print(user_gender)
    else:
        print('Washington doesn\'t have such dataset')

    if city != "washington":
        earliest_year_of_birth = df['Birth Year'].min()
        most_recent_year_of_birth = df['Birth Year'].max()
        most_common_year_of_birth = df['Birth Year'].value_counts().idxmax()
        print("The earliest year of birth is:",earliest_year_of_birth,
            ", most recent one is:",most_recent_year_of_birth,
            "and the most common one is: ",most_common_year_of_birth)
    else:
        print('Washington doesn\'t have such dataset')
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

def display_data(df):
    """ This function is used to display sequential 5 rows of data if the user wanted this.
        Arguments:- (DataFrame)
        Return:- (None)
    """
    row = 0
    view_data = ''
    respon_list = ['yes','no']
    while view_data not in respon_list:
            view_data = input("Would you like to see the raw data? Type 'y' or 'n'.").lower()
            if (view_data == "y") and (row <= len(df.index)):
                print(df.loc[row:row+4,:])
                row += 5
            else:
                break
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
if __name__ == "__main__":
	main()
