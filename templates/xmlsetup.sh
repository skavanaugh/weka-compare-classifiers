#!/bin/bash

    # This script creates nine XML Weka experiment files from a Weka experiment file template
    # It accepts arguments $1 and $1, the name of the dataset (aarfprefix) and xmlprefix
    
    #aarfprefix="bank"
    #xmlprefix="mixed_classifiers"
    
    aarfprefix=$1
    xmlprefix=$2
    #experimentpath=$3
    #templatepath=$experimentpath | cut -d '/' -f1
  

    # Constants in the Weka experiment template files 
    temppercent=47
    tempcsv="template.csv"
    temparff="template.arff"


    for i in {1..9}
  	do
  		fileend="$(($i * 10))"
     	fl="templates/raw/$aarfprefix"_"$xmlprefix$fileend.xml"
      cp "templates/$xmlprefix.xml" $fl
      echo $fl" created."
      mv $fl $fl.temp
      sed s/$temparff/$aarfprefix.arff/g $fl.temp > $fl
      mv $fl $fl.temp
      sed s/$tempcsv/$aarfprefix'_'$xmlprefix$fileend.csv/g $fl.temp > $fl
      mv $fl $fl.temp
      sed s/$temppercent/$fileend/g $fl.temp > $fl
      rm -f $fl.temp
 	  done


    # for fl in adult*.xml 
    # do
    #   mv $fl $fl.old
    #   sed 's_/Users/sylvan/GeorgiaTech/data/a_a_g' $fl.old > $fl
    #   rm -f $fl.old
    # done


