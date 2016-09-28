#!/usr/bin/perl
use strict;
use warnings;

my $num= 0 ;
open(my $writefile, ">","depos.kpp") or die "Could not open file  $!";
#print $writefile "#DEFFIX\nDEPOS=IGNORE;\n";
print $writefile "#EQUATIONS\n";
for my $file ('inorganic','organic') {
    open( FILE, "<$file.kpp" )  or die("Couldn't open :$!\\n");

    while (<FILE>) {
        if (/.*\=\s*IGNORE.*/) {
            $num += 1            ;
            s/\s*([\d\D]*)\s*\=\sIGNORE.*/{$num.} $1 = DUMMY : DEPOS*(1.16D-5*EXP(0.\/TEMP)) ;/g ;
            print $writefile "$_" if $_ !~ /EMISS/;
         }}
    close(FILE);
}
close($writefile);
