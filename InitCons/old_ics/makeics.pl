#!/usr/bin/perl
use strict;
use warnings;

use POSIX;


my $file=$ARGV[0];
$file =~ s/(.*)\.(.*)/$1/g;

my $modified = POSIX::strftime( "%Y-%m-%d", localtime( ( stat "$file.csv" )[9]  ) );
print 'IC:', $file, ' last modified on ',  $modified ,"\n";


open( FILE, "<$file.csv" )  or die("Couldn't open IC :$!\\n");

my @data;
my $line;
my $counter=0;
my $description;
my $duration;
#get data from array
while ( $_ = <FILE> ) {
    s/\s//g;
    if ($counter < 4){
        if ($counter==0){ 
            $description = $_;
            $description =~ s/\n//g}
        
        if ($counter==3){ 
          
            s/(.*TIME,.*,)(-*\d+)(.*)/${2}/g;
            #s/([\s\w.,]*),([-\s]*\d*)([,\s.\D]*)/${2}/g;
            $duration = $_}
        $counter += 1;
    } else {   

        push @data, [split(",",$_)];
    }}
close(FILE);

# if failign do perl -pi-e 's/\r/\n/g'
my $n_species = $#data ;
my $n_runs = (0+@{$data[0]}) - 3;



#dsmacc filename use strftime $currentime = strftime "%y%m%d%H%M", localtime;
open(my $writefile, ">","Init_cons.dat") or die "Could not open file '$file' $!";

my $username = getpwuid( $< );
my $currenttime = strftime "%H:%M %e-%b-%y", gmtime;


print $writefile "$duration\n";

for my $col (1 .. $n_runs+2) {
    for my $row (0 ..$#data ) {
        my @columns = @{$data[$row] };
            if ($col < 3) {  
                printf $writefile "%15s!", $columns[$col] ;
            }else{
                printf $writefile "%15e!", $columns[$col] ;
            }}
   printf $writefile "\n";
    }

close("$file.ic");
print "Init Cons $file.ic created.\n\n" ;

