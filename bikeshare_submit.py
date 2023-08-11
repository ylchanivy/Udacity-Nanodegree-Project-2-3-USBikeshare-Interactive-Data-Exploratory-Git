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
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    #city_list=['chicago','new york city','washington']
    
    
    city=''
    while city not in CITY_DATA.keys():        
        city=(input('Please select a city by typing in "chicago","new york city", or "washington"').lower()).strip()
        
        
        if city not in CITY_DATA.keys():     
            print('Please check and enter a valid city name')
        else:
            print('Selected city is {}.'.format(city))
    
                    


    # get user input for month (all, january, february, ... , june)
    month=''
    month_list=['all','january','february','march','april','may','june']
    while month not in month_list:
        month=(input('Please select month from january to june by typing the full name ie. "january" or type "all" for january to june. ').lower()).strip()
        
        
        if month not in month_list:
            print('Please check and enter a valid month')
        else:
            print('Selected month is {}.'.format(month))


    # get user input for day of week (all, monday, tuesday, ... sunday)
    day=''
    day_list=['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    while day not in day_list:
        day=(input('Please select day from monday to sunday by typing the full name ie. "monday" or type "all" for monday to sunday. ').lower()).strip()
        
        
        if day not in day_list:
            print('Please check and enter a valid day')
        else:
            print('Selected day is {}.'.format(day))
            


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
    df['start_hour']=df['Start Time'].dt.hour

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

    # display the most common month  
    popular_month =df['month'].mode()[0]
    print(f'Most common travel month of city is {popular_month} month.')


    # display the most common day of week
    popular_dow =df['day_of_week'].mode()[0]
    print('Most common travel week of day of city is {}.'.format(popular_dow))


    # display the most common start hour
    popular_hour=df['start_hour'].mode()[0]
    print('Most common travel week of hour of city is {}.'.format(popular_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station=df['Start Station'].mode()[0]
    print('Most common travel start station of city is {} station.'.format(popular_start_station))


    # display most commonly used end station
    popular_end_station=df['End Station'].mode()[0]
    print('Most common travel end station of city is {} station.'.format(popular_end_station))


    # display most frequent combination of start station and end station trip
    df['Start-End']=df['Start Station']+ df['End Station']
    popular_start_end=df['Start-End'].mode()[0]
    print('Most common travel trip is {}.'.format(popular_start_end))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time=df['Trip Duration'].sum()
    ttl_minute1,ttl_second=divmod(total_travel_time,60)
    ttl_hour,ttl_minute=divmod(ttl_minute1,60)
    print('Total travel duration is {} hours {} minutes and {} seconds.'.format (round(ttl_hour),round(ttl_minute),round(ttl_second)))


    # display mean travel time
    avg_travel_time=df['Trip Duration'].mean()
    avg_minute1,avg_second=divmod(avg_travel_time,60)
    avg_hour,avg_minute=divmod(avg_minute1,60)
    print('Average travel duration is {} hours {} minutes and {} seconds.'.format (round(avg_hour),round(avg_minute),round(avg_second)))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    # Chicago and New York City files also have the following two column:
    # gender , yob

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('The user types are : {}'.format(user_types))


    # Display counts of gender    
    
    try:
        gender_count=df['Gender'].value_counts()
        print('The repective gender counts are : {}'.format(gender_count))
        
    except(KeyError):
        print('No Gender counts as there\'s not Gender column in this city dataset ')
           
        

    # Display earliest, most recent, and most common year of birth
    try:
        oldest_age=int(df['Birth Year'].min())
        print('The oldest age : {}'.format(oldest_age))
    except(KeyError):
        print('No oldest age information as there\'s not Birth Year column in this city dataset')
    
    
    try:
        youngest_age=int(df['Birth Year'].max())
        print('The youngest age : {}'.format(youngest_age))
    except(KeyError):
        print('No youngest age information as there\'s not Birth Year column in this city dataset')
        
    try:    
        most_common_age=int(df['Birth Year'].mode()[0])
        print('The most common age : {}'.format(most_common_age))
    except(KeyError):
        print('No common age information as there\'s not Birth Year column in this city dataset')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def display_data(df):
    
    response=['yes','no']
    user_response=''
    
    last_index=(df.shape[0])-1
    remaining_rows=(df.shape[0])
    
    # keep asking for user_response if user's input is not valid
    # if user_response is yes then show them the first 5 row of data
    # if user_response is no then thanks them for their input and exit while loop
    while user_response not in response:
        user_response=(input('Do you want to view the raw data? Please enter "yes" or"no"').lower()).strip()        
        if user_response=='yes':
            print(df.head())
            
            print('Total number of rows for filtered data: {}'.format(df.shape[0]))
            print('Printed raw data from row {} to row {}.'.format(1,5))
            print('Remaining rows: {} rows.'.format(remaining_rows-5))
            
           
            # ask user if they would like to view subsequent(s) next 5 rows            
            index_counter=5
            
            while user_response=='yes'and index_counter<last_index : # when condition is met, it stopped              
                user_response_2=(input('Would you like to view the subsequent next 5 rows of raw data? Please enter"yes" or "no"').lower()).strip()

                
                if user_response_2=='yes':
                     
                    print('Printing the subsequent 5 rows')
                    print(df[index_counter:index_counter+5])

                    print('Printed raw data from row {} to row {}.'.format(index_counter+1,index_counter+5))
                    
                    
                    if remaining_rows-5-5<0: 
                    #or index_counter>=last_index :                        
                        print('Remaining rows:0')
                        print('Finished printing all filtered raw data.')
                        break
                    else:    
                        print('Remaining rows: {} rows.'.format(remaining_rows-5-5))
                        
                        index_counter+=5
                        remaining_rows-=5

                        #if index_counter>=last_index:                        
                        #    print('Finished printing all filtered raw data.')
                      
                elif user_response_2=='no':
                    print('Thank you for your input. Hope you have a great day')
                    break
                else:
                    print('Please check and enter a valid response "yes"or "no"')
                
        elif user_response=='no':
            print('Thank you for your input. Hope you have a great day')
        else:
            print('Please check and enter a valid response "yes"or "no"')
            
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = (input('\nWould you like to restart? Enter yes or no.\n').lower()).strip()
        if restart!= 'yes':
            break
if __name__ == "__main__":
    main()