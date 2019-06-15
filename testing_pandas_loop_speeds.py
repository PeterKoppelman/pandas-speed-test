# Based on article How to Use Pandas Right by George Seif - Peter Koppelman May 25, 2019

import seaborn as sns
import pandas as pd
import time
import matplotlib.pyplot as plt

sns.set()


def main():
	def load_data(N, data):
		# take the current length of data and make it 10 times longer.		
		data2 = data
		for i in range(9):
			data = pd.concat([data, data2], ignore_index=True)
		return data


	def calc_times(data):
		# Calculate which bin to put the petal length in
		def compute_class(petal_length):
		    if petal_length <= 2:
		        return 1
		    elif 2 < petal_length < 5:
		        return 2
		    else:
		        return 3


		def std_loop(data):
		# Calculate time using a standard Python loop. This will
		# act as our baseline for the test. 
			start = time.time()
			class_list = []
			for i in range(len(data)):
			    petal_length = data.iloc[i]['petal_length']
			    class_num = compute_class(petal_length)
			    class_list.append(class_num)
			return time.time() - start


		def iter_func(data):
		# Use pandas iterrows() function in loop.
			start = time.time()
			class_list = []
			for index, data_row in data.iterrows():
			    petal_length = data_row['petal_length']
			    class_num = compute_class(petal_length)
			    class_list.append(class_num)
			return time.time() - start


		def apply_func(data):
		# Use the apply function in pandas - no more loops
			start = time.time()
			class_list = data.apply(lambda row: compute_class(row['petal_length']), axis=1)
			return time.time() - start


		def cut_func(data):
			# Use cut so we do not have to call the compute_class function.
			start = time.time()
			class_list = pd.cut(x=data.petal_length,
			                   bins=[0, 2, 5, 100],
			                   include_lowest=True,
			                   labels=[1, 2, 3]).astype(int)
			return time.time() - start


		# Run through each type of "loop"
		for_loop_time = std_loop(data)
		iter_loop_time = iter_func(data)
		apply_time = apply_func(data)
		cut_time = cut_func(data)
		return for_loop_time, iter_loop_time, apply_time, cut_time


	def print_results(df_time_series):
		# Print out the raw results.
		print('#' * 80)
		print(' ' * 24, end = '')
		print('Time to complete loops in Seconds')
		df_time_series = pd.DataFrame(speed_dict).T
		df_time_series.columns = ['For Loop', 'Iter Rows', 'Apply', 'Cut']
		df_time_series.index.name = 'Number of Loops'
		print(df_time_series)
		print()

		# Calculate the percentage time difference between all of the methods using the for loop
		# as a baseline
		df_time_series_pct = df_time_series.copy()
		df_time_series_pct['Iter Rows'] = df_time_series_pct['For Loop']/df_time_series_pct['Iter Rows']
		df_time_series_pct['Apply'] = df_time_series_pct['For Loop']/df_time_series_pct['Apply']
		df_time_series_pct['Cut'] = df_time_series_pct['For Loop']/df_time_series_pct['Cut']
		df_time_series_pct['For Loop'] = 1.000000
		print(' ' * 21, end = '')
		print('Percentage Speed Increase over For Loop')
		print(df_time_series_pct)

		# Show the results using a time series graph in seaborn
		time_series_plot(df_time_series)


	def print_interim_results(data):
		# Print interim results so that the user knows the program is working
		print(' Sample Test Size {:,} is complete'.format(len(data)))


	def time_series_plot(df_time_series):
		# Print a time series plot using seaborn.
		fig, ax = plt.subplots()
		ax.set_ylabel('Seconds')
		ax.set_title('Different ways to loop through data in Pandas')
		fig.set_size_inches(14,12)
		sns.lineplot(data = df_time_series)
		plt.show()

	'''Lets start the code. The first that that we will do is create an empty
	dictionary called speed_dict. We'll store the amount of rows (length of 
	data frame) as the key and the speed of each test for the length of the dataframe
	as a list that will be the value'''
	speed_dict = {}

	'''N is the number of loops that we will do.
	N = 1 is one loop with 150 rows
	N = 2 is two loops. One with 150 rows, one with 1,500 rows
	N = 3 is three loops. One with 150 rows, one with 1,500 rows and one with 15,000 rows
	You can change N to be any number that you wish, but watch out...the for loop will take
	some time.
	''' 
	N = 3
	'''Load the sample data set from seaborn'''
	data = sns.load_dataset('iris')

	for i in range(N):
		# No need to load data on the first go round. It's been done just above from seaborn 
		if i > 0:
			data = load_data(i, data)
		for_loop_time, iter_loop_time, apply_time, cut_time = calc_times(data)
		speed_dict[len(data)] = [for_loop_time, iter_loop_time, apply_time, cut_time]
		print_interim_results(data)

	df_time_series = pd.DataFrame(speed_dict)
	print_results(df_time_series)
	

if __name__ == '__main__':
	# Run the speed Test
	main()