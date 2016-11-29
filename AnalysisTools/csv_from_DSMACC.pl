#!/usr/bin/perl
#use strict;
use warnings;

## Parses the Spec and rate files from the DSMACC model into csv-style files that can be read into pandas with read_csv. 
# chmod a+x the file, then run with files as arguments  
# can use multiple files:     ./csv_to_DSMACC.pl *.dat
# creates        .ropa       file with inital filename 
####################### Dan Ellis ####################

my $data;
my $len;
my $individual;

for my $arg (@ARGV) {
    
    open(my $fh, "<", $arg) or die "$!";

    @new = split(/\./,$arg);
    open(my $write, ">", $new[0].".ropa") or die "$!";

    
    while( <$fh> ) {
        
        s/\!/,/g;
        s/\s+//g;
        chop($_); #rm last 

                       
            
            
        print $write $_ . "\n";
        
        
    }
    close $fh or die "Error in closing the file ", __FILE__, " $!\n";
    close $write or die "Error in closing the file ", __FILE__, " $!\n";

print "Made ".$arg.".ropa";
}

