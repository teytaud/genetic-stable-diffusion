#!/bin/bash

cat archive_results_*.txt > archive_results.txt
(
echo '%%%% DO NOT MODIFY: AUTOMATICALLY GENERATED.'
echo '\begin{table}'
echo '\begin{tiny}'
echo '\begin{minipage}{.33\textwidth}'
echo '\begin{tabular}{|c|c|c|c|}'
echo '\hline'
echo 'Problem & Train & Tool & Acc.\\'
echo '\hline'
grep '^L' archive_results.txt | sed 's/ / \& /g' | sed 's/$/\\\\/g' | cut -c 3- | sed 's/_/-/g' | sort | awk '{ if ( $1 != prev ) { idx=idx+1 ; if (idx % 3 == 0 ) { print "\\hline" ; print "\\end{tabular}\\end{minipage} \\\\ \\begin{minipage}{.33\\textwidth}\\begin{tabular}{|c|c|c|c|}\\hline" } else { print "\\hline" ; print "\\end{tabular}\\end{minipage}  \\begin{minipage}{.33\\textwidth}\\begin{tabular}{|c|c|c|c|}\\hline" };} print $0; prev = $1 }' 
echo '\hline'
echo '\end{tabular}\end{minipage}'
echo '\end{tiny}'
echo '\caption{\label{acc}Accuracies when learning high-level features: accuracies are quite poor. Majority is a simple majority vote as a baseline.}'
echo '\end{table}'
echo '\begin{table}'
echo '\begin{tiny}'
echo '\begin{minipage}{.33\textwidth}'
echo '\begin{tabular}{|c|c|c|c|}'
echo '\hline'
echo 'Problem & Train set & Tool & Perf\\'
echo '\hline'
#grep '^O' archive_results.txt | sed 's/ / \& /g' | sed 's/$/\\\\/g' | cut -c 3- | sed 's/_/-/g' | sort | egrep 'MLP|major' |  awk '{ if ( $1 != prev ) { print "\\hline" ; print "\\end{tabular}\\end{minipage} \\\\ \\begin{minipage}{.33\\textwidth}\\begin{tabular}{|c|c|c|c|}\\hline" } print $0; prev = $1 }' | sed 's/majority/Random/g' | sed 's/$/\%\%Optim/g' 
grep '^O' archive_results.txt | sed 's/ / \& /g' | sed 's/$/\\\\/g' | cut -c 3- | sed 's/_/-/g' | sort | egrep '.|ajor|MLP' |egrep 'rand|MLPClassif-[23]|LogisticRe-[23]|maj' | awk '{ if ( $1 != prev ) { idx=idx+1 ; if (idx % 3 == 0 ) { print "\\hline" ; print "\\end{tabular}\\end{minipage} \\\\ \\begin{minipage}{.33\\textwidth}\\begin{tabular}{|c|c|c|c|}\\hline" } else { print "\\hline" ; print "\\end{tabular}\\end{minipage}  \\begin{minipage}{.33\\textwidth}\\begin{tabular}{|c|c|c|c|}\\hline" };} print $0; prev = $1 }'  | sed 's/$/\%\%Optim/g' 
echo '\hline'
echo '\end{tabular}'
echo '\end{minipage}'
echo '\end{tiny}'
echo '\caption{\label{opt}Frequency of success when optimizing the probability of failures $z\mapsto P(Quality(G(z))=Good)$. Results are positive (increased frequency of success), in spite of the poor accuracies in Table \ref{acc}. Random is the standard Vanilla StableDiffusion reroll as a baseline.}'
echo '\end{table}'
) > ltable.tex
sed -i.tmp 's/[0-9]\.[0-9][0-9]/&PROUTPROUT/g' ltable.tex
sed -i.tp 's/PROUTPROUT[0-9]*//g' ltable.tex


echo Everything:
grep Optim ltable.tex #| egrep 'Random|Dec'
echo My favorite:
grep Optim ltable.tex #| egrep 'Random|LogisticRe.6'

echo "open ltable.tex"

