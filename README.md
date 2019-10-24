# pandas-speed-test
This program comppares four different ways to "loop" through a dataframe:
1) a standard python for loop
2) a for loop using pandas iterrows function
3) a for loop using pandas itertuples function
3) using a pandas apply function
4) using a pandas cut function

The size of the loop is initially created by loading the seaborn 'iris' data set
into a dataframe (150 rows). There is a loop that will increase the size of the 
dataframe by a factor of 10 (this is the variable N that is initialized on 
line 132).

I've tried to document the program properly. Hopefully you can follow the logic.
