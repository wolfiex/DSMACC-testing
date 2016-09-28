#!/usr/local/bin/perl;
use warnings;
use strict;


my $string = '';

      local $/ = undef;
        open FILE, $ARGV[0] or die "Couldn't open file: $!";
            $string = <FILE>;
            close FILE;
        



$string =~ s/(.*RO2 =).*[\&\n].*(CALL mcm.*)/$1$2/g;

print $string;
        
