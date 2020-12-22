import time
import pandas as pd
import numpy as np
#list of cities with data wrangled by Udacity
cities = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def n_allstations(trip_value_counts):
    """
    Loops through a .value_counts pandas series and finds out the last index of a maxed value
    e.g.: a series with 5 counts of 13 most commom names, will return index 5 thus
          allowing to show the .value_counts table with all tied maxed values if there are some
    arg:
    (Series.value_counts) series with the .value_counts already applied
    use case:
        trip_value_counts.value_counts()[:n_allstations(trip_value_counts)].sort_values(ascending=False)
        this way the output will be a table showing all tied max count values
    """
    if trip_value_counts.value_counts().idxmax() == trip_value_counts.value_counts().idxmin():
        return len(trip_value_counts)
    else:
        for index, i in enumerate(trip_value_counts):
            if trip_value_counts[index+1] < trip_value_counts[index]:
                return(index+1)

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        valid = ['chicago', 'new york city', 'washington']
        city = input('Hello, which city would you like to see more information about Bikeshare? (chicago, new york city, washington)').lower()
        if city in valid:
            break
        else:
            print('It seems you have entered an incorrect input, please try again')

    # get user input for month (all, january, february, ... , june)
    while True:
        valid = ['all', 'jan', 'feb', 'mar', 'apr', 'may', 'jun']
        month = input('Would you like to see information about the whole database or a specific month? (all, jan, feb, mar, apr, may, jun)').lower()
        if month in valid:
            break
        else:
            print('It seems you have entered an incorrect input, please try again')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        valid = ['all', 'mon','tue', 'wed', 'thu', 'fry', 'sat', 'sun']
        day = input('Would you like information about a specific day of the week or about the whole database/ month? (all, sun, mon, tue, wed, thu, fry, sat)').lower()
        if day in valid:
            break
        else:
            print('It seems you have entered an incorrect input, please try again')
    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Reads the correct dataframe and apply filters from args:

    (str) city : Chicago, New York City or Washington - used as keys from the cities dict to read the .csv files
    (str) month : jan, feb, mar, apr, may, jun - names of the list months
    (str) day :
    """
    # read csv file according to the city passed as arg
    df = pd.read_csv(cities[city])

    # Convert Start Time and End Time columns to datetime format
    # This makes it possible to use datetime methods and use better functions to analise months, day and hours
    df['Start Time']= pd.to_datetime(df['Start Time'])
    df['End Time']= pd.to_datetime(df['End Time'])

    # Create new columns with just the Hour, Week and Month from the Start Time column
    # This way we can easily use simple pandas methods to analise our data
    df['hour'] = df['Start Time'].dt.hour
    df['week'] = df['Start Time'].dt.weekday #reading this way we can easily use an str input to filter
    df['month'] = df['Start Time'].dt.month

    # Filter the whole dataframe to contain only the wanted month
    if month != 'all':
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun'] # list with possible months inputs
        month = months.index(month) + 1 #since the datetime format uses months as numbers this way we can easily convert str to
                                        #the correct month
        df = df[df['month'] == month] #aplly the filter by month

    # Filter the whole dataframe by wanted day
    if day != 'all':
        # filter by day of week to create the new dataframe
        days = ['mon','tue', 'wed', 'thu', 'fry', 'sat', 'sun']
        day = days.index(day)
        df = df[df['week'] == day]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun'] # list with possible months inputs
    popular_month = df['month'].value_counts().idxmax()
    print("Most commom month: \n",months[popular_month-1])

    # display the most common day of week
    days = ['mon','tue', 'wed', 'thu', 'fry', 'sat', 'sun']
    popular_week = df['week'].value_counts().idxmax()
    print("Most commom week: \n",days[popular_week-1])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #find the most commom start station, end station and trip from start to end
    #here .idxmax() can have an issue since it only returns the first max id from the .value_counts() series
    #so if we have two or more stations with the same count only the first will be returned
    #to solve this we use the n_allstations function
    most_startstation = df['Start Station'].value_counts()
    most_startstation = df['Start Station'].value_counts()[:n_allstations(most_startstation)].sort_values(ascending=False)
    print('Most commom start station(s): \n',most_startstation)


    # display most commonly used end station
    most_endstation = df['End Station'].value_counts()
    most_endstation = df['End Station'].value_counts()[:n_allstations(most_endstation)].sort_values(ascending=False)
    print('\nMost commom end station(s): \n',most_endstation)

    # display most frequent combination of start station and end station trip
    most_commomtrip = (df['Start Station'] + " to " + df['End Station']).value_counts().idxmax()
    print('\nMost commom trip(s): \n',most_commomtrip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()/60 #total travel time in minutes
    print('Total travel time: \n',total_travel)


    # display mean travel time
    mean_travel = df['Trip Duration'].mean()/60 #average travel time in minutes
    print('Mean of travel time: \n',mean_travel)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].value_counts()
    print('Count of user types: \n', user_type)


    # Display counts of gender
    gender = "Gender" in df
    if gender is True:
        user_gender = df['Gender'].value_counts()
        print('Count of genders: \n',user_gender)

    else:
        print('This database does not have gender information')

    # Display earliest, most recent, and most common year of birth
    birth_year = 'Birth Year' in df
    if birth_year is True:
        earliest_yy_birth = df['Birth Year'].min()
        print('Earliest year of birth: \n',earliest_yy_birth)

        recent_yy_birth = df['Birth Year'].max()
        print('Most recent birth: \n',recent_yy_birth)

        commom_yy_birth = df['Birth Year'].value_counts().idxmax()
        print('Most commom birth: \n',commom_yy_birth)

    else:
        print('This database does not have birth year information')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):# shows user 5 lines of raw data at a time by request if possible.
    current_raw = 0
    valid = ['yes','no']
    while True:
        raw_data = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')

        if raw_data.lower() not in valid:
            print('\nIt seems you have entered an incorrect input, please try again\n')

        if raw_data.lower() == 'yes':
            try:
                print(df.iloc[ current_raw:current_raw+4 , : ])
                current_raw += 5
            except:
                print('\nWe have none or less than 5 rows left, moving to the next question\n')
                break

        elif raw_data.lower() == 'no':
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
