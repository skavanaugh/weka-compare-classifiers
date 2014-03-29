import subprocess
import shlex
import csv
import time
import os
import runExperiment


# CONFIGURATION INFORMATION
#############################
# name_of_dataset = defined in runExperiment.py
# experiment = defined in runExperiment.py

#csvprefix = 'templates/raw/bank_mixed_classifiers'
createPNGs = False # If you set this to True, you need to have matplotlib
showGraphs = False # If you set this to True, you need to have matplotlib
runWekaExperiments = False # If you set this to True, make sure you have configured runExperiment.py

# This is a list of what you would like to measure in all your classifiers.  You can add or remove 
# from this list as long as you choose from the list of fields below.

studies = ['Percent_incorrect', 'Elapsed_Time_training', 'Elapsed_Time_testing', 
	'UserCPU_Time_training','UserCPU_Time_testing', 'F_measure'] # , 'measureNumLeaves']

#############################
csvprefix = runExperiment.path_to_experiments + runExperiment.name_of_dataset + "_" + runExperiment.experiment

"""
# This is a list of all the possible metrics that this utility can make.  Please choose numeric fields.
fields = ['Key_Dataset', 'Key_Run', 'Key_Scheme', 'Key_Scheme_options', 'Key_Scheme_version_ID', 
		'Date_time', 'Number_of_training_instances', 'Number_of_testing_instances', 'Number_correct', 
		'Number_incorrect', 'Number_unclassified', 'Percent_correct', 'Percent_incorrect', 'Percent_unclassified', 
		'Kappa_statistic', 'Mean_absolute_error', 'Root_mean_squared_error', 'Relative_absolute_error', 
		'Root_relative_squared_error', 'SF_prior_entropy', 'SF_scheme_entropy', 'SF_entropy_gain', 
		'SF_mean_prior_entropy', 'SF_mean_scheme_entropy', 'SF_mean_entropy_gain', 'KB_information', 
		'KB_mean_information', 'KB_relative_information', 'True_positive_rate', 'Num_true_positives', 
		'False_positive_rate', 'Num_false_positives', 'True_negative_rate', 'Num_true_negatives', 
		'False_negative_rate', 'Num_false_negatives', 'IR_precision', 'IR_recall', 'F_measure', 
		'Matthews_correlation', 'Area_under_ROC', 'Area_under_PRC', 'Weighted_avg_true_positive_rate', 
		'Weighted_avg_false_positive_rate', 'Weighted_avg_true_negative_rate', 'Weighted_avg_false_negative_rate', 
		'Weighted_avg_IR_precision', 'Weighted_avg_IR_recall', 'Weighted_avg_F_measure', 
		'Weighted_avg_matthews_correlation', 'Weighted_avg_area_under_ROC', 'Weighted_avg_area_under_PRC', 
		'Unweighted_macro_avg_F_measure', 'Unweighted_micro_avg_F_measure', 'Elapsed_Time_training', 
		'Elapsed_Time_testing', 'UserCPU_Time_training', 'UserCPU_Time_testing', 'Serialized_Model_Size', 
		'Serialized_Train_Set_Size', 'Serialized_Test_Set_Size', 'Coverage_of_Test_Cases_By_Regions', 
		'Size_of_Predicted_Regions', 'Summary', 'measureTreeSize', 'measureNumLeaves', 'measureNumRules']

"""

# helper function is_number (could have used isdigit())
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

#helper function average for lists
def average(strlist): # can blow up if len(l) == 0
	l = map(float,strlist)
	return (sum(l))/len(l)

def getClassifierNickName(k):
	
	if runExperiment.experiment == "neural_nets":
		nn_vals = ["1 HL=3 | 500 epochs", "2 HL=(3-3) | 200 epochs", "2 HL=(5-3) | 200 epochs", 
			"1 HL=3 | 200 epochs", "1 HL=2 | 100 epochs", "1 HL=3 | 100 epochs"]
		
		nn_base = 'weka.classifiers.functions.MultilayerPerceptron '
		nn_keys = ['-L 0.3 -M 0.2 -N 500 -V 0 -S 0 -E 20 -H 3', '-L 0.5 -M 0.2 -N 200 -V 0 -S 0 -E 20 -H \"3, 3\"',
			'-L 0.3 -M 0.2 -N 200 -V 0 -S 0 -E 20 -H \"5, 3\"', '-L 0.3 -M 0.2 -N 200 -V 0 -S 0 -E 20 -H 3',
			'-L 0.3 -M 0.2 -N 100 -V 0 -S 0 -E 20 -H 2', '-L 0.3 -M 0.2 -N 100 -V 0 -S 0 -E 20 -H 3']

		nn_keys = [nn_base + x for x in nn_keys]

		nn_dict = dict(zip(nn_keys, nn_vals))
	
		if k in nn_dict:
			return nn_dict[k]
		elif "5, 3" in k:  # hardcoded because having trouble recognizing this key
			return nn_vals[2]
		elif "3, 3" in k:  # hardcoded because having trouble recognizing this key
			return nn_vals[1]
		else:
			return "Neural Network"

	else:
		return "Classifier"


if runWekaExperiments:
	runExperiment.generate_experiment_files()
	runExperiment.run_experiments()

csvbase = os.path.basename(csvprefix)
outputCSVs = []
[outputCSVs.append(csvbase + '_' + s + '.csv') for s in studies]

for ii, s in enumerate(studies):
	csvfile = outputCSVs[ii]
	dataDict = {}		
	summaryDict = {}

	for i in range(10,100,10):
		with open(csvprefix + str(i) + '.csv', 'rbU') as f:
			reader = csv.DictReader(f, delimiter = ",", quotechar = "'")

			for row in reader:
				k = row['Key_Scheme'] + ' ' + row['Key_Scheme_options']
				if k not in dataDict and is_number(row[s]):
					dataDict[k] = {}		
					summaryDict[k] = {}
					dataDict[k]['AmtData'] = []
					summaryDict[k]['AmtData'] = []
					dataDict[k][s] = []
					summaryDict[k][s] = []
					
				if k in dataDict:
					dataDict[k]['AmtData'].append(i)
				#if is_number(row[s]): 
					dataDict[k][s].append(row[s])

	for key in dataDict:
		# prepend name of classifier. eventually this should be a classifier nickname for graphing.
		summaryDict[key]['AmtData'].append('')
		summaryDict[key][s].append(getClassifierNickName(key)) # nickname
		size = len(dataDict[key]['AmtData']) / 9 # 9 for 10, 20, 30, ... , 90

		for i in range(9):
			partListBeg = i * size
			partListEnd = (i + 1) * size
			summaryDict[key]['AmtData'].append(average(dataDict[key]['AmtData'][partListBeg:partListEnd]))
			summaryDict[key][s].append(average(dataDict[key][s][partListBeg:partListEnd]))

	with open(csvfile, 'wb') as f:
		writer = csv.writer(f, delimiter = ",", quotechar = "'")
		writer.writerow(summaryDict[key]['AmtData'])
		for key in summaryDict:
			writer.writerow(summaryDict[key][s])
		print "Created CSV file %s" % csvfile

	
	if showGraphs or createPNGs:
		import matplotlib.pyplot as plt

		classifierlist = []
		for key in summaryDict:
			plt.plot(summaryDict[key]['AmtData'][1:], summaryDict[key][s][1:])
			classifierlist.append(key)
			
		fig = plt.gcf()
		#fig.set_size_inches(10,8.5)
		plt.title(s)
		plt.legend(classifierlist, prop={'size':6})
		plt.xlabel("Percentage of Data used to Train")
		
		if createPNGs:
			plt.savefig(csvbase + "_" + s + ".png",dpi=100)

		if showGraphs:
			plt.show()

