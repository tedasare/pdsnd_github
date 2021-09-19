import time
from pprint import pprint
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
    city, month, day = '' , '', ''
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input('\nWhat city would you like to view data for: Chicago, New York City, Washington?\n')
            # removing whitespaces and converting to lowercase 
            city = city.strip().lower()
        except EOFError:
            city = ''

        if city in ['chicago', 'new york city', 'washington']:
            break
        else:
            print('Ooops! Please check your input and try again. Eg: New York City\n')


    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input('\nWhich month(s) would you like to view bikeshare data for: all, January, ..., June?\n')
            month = month.strip().lower()
        except EOFError:
            month = ''

        if month in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            break
        else:
            print('Ooops! Please try again. Enter a month from January to June or all. Eg: all or March\n')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input('\nWhich day(s) would you like to view data for: all, Monday, ..., Sunday?\n')
            day = day.strip().lower()
        except EOFError:
            day = ''

        if day in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday','sunday']:
            break
        else:
            print('Ooops! Please try again. Enter a day from Monday to Sunday or all. Eg: all or Wednesday\n')

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
        loaded_df - Pandas DataFrame containing data loaded from data file filtered by city, month, and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # make copy of DataFrame for raw trip data output
    loaded_df = df.copy()
    loaded_df.rename(columns = {'Unnamed: 0' : 'index'}, inplace = True)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week, and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

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

    # applying city, month, day filters to raw data dataframe
    loaded_df = loaded_df[loaded_df.index.isin(df.index)]

    return df, loaded_df


def data_viewer(df, chunk_size):
    """Displays raw data of descriptive statitics 5 lines at a time."""

    i = 0
    # chunk_size = 5
    while True:
        try:
            # error handling EOFError when taking input
            first_prompt = '\nWould you like to view trip data?\nEnter yes or y to view or any other key to continue program.\n'
            subsequent_prompt = '\nView some more trip data?\nEnter yes or y to view or any other key to continue program.\n'

            if i == 0:
                raw_data = input(first_prompt)
            else:
                raw_data = input(subsequent_prompt)
            print('\n')
        except EOFError:
            raw_data = ''    

        if raw_data.strip().lower() not in ['yes', 'y']:
                break
        else:
            # splitting rows of data into list of dictionaries
            trip_records = df.to_dict('records')

            # display raw data 5 lines of raw data
            if i < len(trip_records):
                subset = trip_records[i : i + chunk_size]
                for trip_data in subset:
                    pprint(trip_data)
                i += chunk_size
            else:
                # end of records
                print('\nNo more data to display\n')
                break


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()
    print('Most Common Month of Travel: ', popular_month.to_string(index = False))

    # display the most common day of week
    popular_day = df['day_of_week'].mode()
    print('Most Frequent Day of Travel: ', popular_day.to_string(index = False))

    # display the most common start hour
    popular_hour = df['hour'].mode()
    print('Most Frequent Start Hour: ', popular_hour.to_string(index = False))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()
    print('Most Popular Start Station: ', popular_start_station.to_string(index = False))

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()
    print('Most Commonly Used End Station: ', popular_end_station.to_string(index = False))

    # display most frequent combination of start station and end station trip
    df['station_combo'] = df['Start Station'] + ' to ' + df['End Station']
    popular_station_combo = df['station_combo'].mode()
    print('Most Frequent Combination of Start Station and End Station:\n', popular_station_combo.to_string(index = False))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def time_converter(seconds):
    """
    Converts time in seconds to days, hours, minutes and seconds.

    Args:
        (int) seconds - time in seconds to for conversion 
    Returns:
        (int) d - time in days only
        (int) h - time in hours only
        (int) m - time in minutes only
        (int/float) s - time in seconds only
    """

    m, s = seconds // 60, seconds % 60
    h, m = m // 60, m % 60
    d, h = h // 24, h % 24

    return int(d), int(h), int(m), s


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    total_d, total_h, total_m, total_s = time_converter(total_time)
    print('Total Travel Time: {} seconds or {} days {} hours {} minutes {} seconds'.format(total_time, total_d, total_h, total_m, total_s))

    # display mean travel time
    avg_time = df['Trip Duration'].mean()
    avg_d, avg_h, avg_m, avg_s = time_converter(avg_time)
    print('Average Travel Time: {} seconds or {} days {} hours {} minutes {:.1f} seconds'.format(avg_time, avg_d, avg_h, avg_m, avg_s))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # display counts of user types
    user_types = df['User Type'].value_counts()
    print('Counts of User Types:\n', user_types.to_string())

    try:
        # display counts of gender
        gender_types = df['Gender'].value_counts()
        print('\nCounts of Gender Types:\n', gender_types.to_string())
    except KeyError:
        print('\nBreakdown of Gender Types: Gender data unavailable for the selected city')

    try:
        # display earliest, most recent, and most common year of birth
        print('\nEarliest Year of Birth: ', int(df['Birth Year'].min()))
        print('Most Recent Year of Birth: ', int(df['Birth Year'].max()))
        print('Most Common Year of Birth: ', int(df['Birth Year'].mode()))
    except KeyError:
        print('\nEarliest, Most Recent and Common Years of Birth: Birth Year data unavailable for the selected city')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    """Calls other funtions to run the interactive program in a loop."""

    while True:
        try:
            city, month, day = get_filters()
            df, loaded_df = load_data(city, month, day)

            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            data_viewer(loaded_df, 5)

            try:
                # error handling EOFError when taking input
                restart = input('Would you like to restart?\nEnter yes or y to restart or any other key to exit.\n')
                print('\n\n')
            except EOFError:
                restart = ''

            if restart.strip().lower() not in ['yes', 'y']:
                    break

        except KeyboardInterrupt:
            # keyboard intterupts while the program is running will cause a force quit
            print('\n\nForce quit\nExiting program now...')
            break


if __name__ == "__main__":
        main()
