
import subprocess
import shlex
import os
import time


# CONFIGURATION INFORMATION
#############################
# Possible names of datasets: 'lendingSubset', 'bank', 'census' are included but you can
# use any arff based dataset you want.  Place it in the directory you run from.
# Example: name_of_dataset for 'census.arff' is 'census'
# experiment is a Weka experiment template (a Weka serialized XML experiment with a few pre-configured settings)
# included experiment templates are 'trees_and_boosted', 'mixed_classifiers', 'knn', 'neural_nets', 'svm'.  
# You can also create your own experiment templates.  Please note that in order to use 'svm' or experiments
# which make use of LibSVM, you need to point to both LibSVM.jar and libsvm.jar as is done below in 
# path_to_libsvm.  This is not necessary for the other experiments.  

name_of_dataset = 'spambase_scaled' #'spambase' #'bank'
experiment = 'neural_nets' # 'trees_and_boosted'

path_to_weka_jar = '/Users/Sylvan/weka-3-7-10/weka.jar'
path_to_libsvm = '/Users/Sylvan/weka-3-7-10/libsvm.jar:/Users/Sylvan/wekafiles/packages/LibSVM/LibSVM.jar'
path_to_experiments = 'templates/raw/'
#############################

#xmlprefix = 'templates/raw/bank_mixed_classifiers'

# Generate Experiment files from template
def generate_experiment_files():
	#xmlbase = os.path.basename(xmlprefix)
	cmd = './templates/xmlsetup.sh %s %s' % (name_of_dataset, experiment)
	cmd = shlex.split(cmd)
	output = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.STDOUT).communicate()[0]
	print output

# Run the Experiments through Weka
def run_experiments():
	weka_path = path_to_weka_jar + ":" + path_to_libsvm
	xmlprefix = path_to_experiments + name_of_dataset + "_" + experiment
	for i in range(10,100,10):
		exp_file = xmlprefix + str(i) + '.xml'
		cmd = 'java -Xmx1024m -cp %s weka.experiment.Experiment -l %s -r' % (weka_path, exp_file)
		cmd = shlex.split(cmd)
		print cmd

		start = time.time()
		output = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.STDOUT).communicate()[0]
		elapsed = time.time() - start	
		print output
		print "Elapsed experiment time %d is %d seconds." % (i, elapsed)


if __name__ == "__main__":
	generate_experiment_files()
	run_experiments()
