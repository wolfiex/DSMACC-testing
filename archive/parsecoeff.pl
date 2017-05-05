#!/usr/bin/perl

## Parse rate files for constants. Ensures coefficents are save parameters. D.Ellis 2017

my $file = $ARGV[0];
print("parsing $file \n");

open my $in,  '<',  $file      or die "Can't read old file: $!";
open my $out, '>', "$file.def" or die "Can't write new file: $!";

print $out "# Add this line to the top\n";

while( <$in> )
    {
    s/(\s*[^!].+)=.*\n/REAL(dp):: $1 \n/g;
    print $out $_;
    }

close $out;
