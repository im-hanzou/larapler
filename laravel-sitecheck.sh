#!/bin/bash
# Mass Laravel Site Checker
# Created By Im-Hanzou
# Using GNU Parallel
# Usage: bash file.sh list.txt thread 

yellow='\033[0;33m'
cat << "EOF"
  _                                _ 
 | |    __ _  _ _  __ _ __ __ ___ | |
 | |__ / _` || '_|/ _` |\ V // -_)| |
 |____|\__,_||_|  \__,_| \_/ \___||_|
                                     
EOF
printf "${yellow}Mass Laravel Site Checker\nGithub : im-hanzou\nUsage: bash file.sh list.txt thread\nExample: bash laravel-sitecheck.sh list.txt 50\n\n\n"

exploit(){	
classic='\033[0m'
red='\e[41m'
green='\e[42m'
target=$1
thread=$2

if [[ $(curl --silent --connect-timeout 10 --max-time 10 --insecure -o /dev/null -c - $target ) =~ 'XSRF-TOKEN' || $(curl --silent --connect-timeout 10 --max-time 10 --insecure -o /dev/null -c - $target ) =~ '_session' ]]; 
then
    printf "${green}[ Valid ]${classic} => [ $target | Laravel Site ] \n";
    printf "$target\n" >> laravel.txt
    else
    printf "${red}[ Not Valid ]${classic} => $target \n";
    printf "$target\n" >> notlaravel.txt
fi
}

export -f exploit
parallel -j $2 exploit :::: $1 

printf "\033[0;36mLaravel Site : laravel.txt\n";
printf "\033[0;36mNot Laravel Site : notlaravel.txt\n";
