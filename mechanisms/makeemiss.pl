#!/usr/bin/perl
use strict;
use warnings;
use List::MoreUtils qw(first_index); # to find first index of an entry in a list

### Variable declarations
## Data arrays and variables
my @dspc;     # species with predefined deposition velocities
my @vd;       # deposition velocities
my $mspc;     # species used in current mechanism
my $vdstd;    # standard deposition velocitiy
              # (defined with key word "DEPOS" in depos.dat)
my $num= 0 ;  # counter for reaction labels in output file

## Temporary auxiliary arrays/variables
#  @lines:  lines read in from input file
#  @spl:    array with separated species and vd from input line
#  $idx:    index of current species in species/vd array

## file handling
#  $dfu:       file unit for data file "depos.dat"
#              with predefined deposition velocities
my $fdat;#     file name (and path) of data file
#  $kfu:       input KPP files with definitions of species
#              used in current mechanism
my @fkpp;#     list of file names (and paths) of input KPP files
#              without file ending '.kpp'
#              In script argument, put list in quotes
#              and separate elements by whitespaces
#  $writefile: output KPP file "depos.kpp"

########################################################################

# Define input data file:
if (exists $ARGV[1]) {
  $fdat = $ARGV[1];
} else {
  $fdat = '../InitCons/emiss.dat';
}
print "\n\033[94mData file:         $fdat\n";

# Define input kpp files:
if (exists $ARGV[0]) {
  my $targ = $ARGV[0];
  $targ =~ s/^\s+//;
  $targ =~ s/\s+$//;
  @fkpp = split(/\s+/, $targ);
} else {
  @fkpp = ('inorganic','organic');
}
print "KPP input file(s): ", join(", ", @fkpp), "\033[0m\n\n";

########################################################################

# Read in species and definitions of deposition velocities (vd)
# from data file "depos.dat"
open (my $dfu, '<', $fdat) or die "Could not open file $fdat: $!";
chomp(my @lines = <$dfu>);
close($dfu);

# Split array of input lines into array of species names and vd
# unless it is an empty line or comment line starting with '#'
foreach (@lines) {
  $_  =~ s/\#.*//;
  if ($_ !~ /^\s*$/) {
    $_ =~ s/^\s+//;
    my @spl = split(/\s+/, $_);
    push @dspc, $spl[0];
    push @vd, $spl[1];
} }
print "\033[95mEmissions are only used for species included in the input ",
      "mechanisms.\nIF species are not listed here, but in $fdat, check for ",
      "their\npresence in the specified kpp files and possibly change the ",
      "kpp files.\033[0m\n",
      "\033[92mThe following emissions are used in the current scenario:\033[0m\n";


########################################################################

# Open output file and set KPP EQUATIONS variable
open(my $writefile, ">","emiss.kpp") or die "Could not open file emiss.kpp: $!";
print $writefile "#DEFFIX\nEMISS=IGNORE;\n#EQUATIONS\n";

# Loop over KPP files
for my $kfu (@fkpp) {
  open( FILE, "<$kfu.kpp" )  or die("Couldn't open file $kfu.kpp:$!\\n");
# Find lines with species definitions
  while (<FILE>) {
    if (/.*\=\s*IGNORE.*/) {
# Get species and store in $mspc
      s/\s*(\w)\s*\=\s*IGNORE.*/$1/g ;
      $mspc = $_ ;
      chomp $mspc ;

# Define experimental values:
      if (grep(/^$mspc$/, @dspc)) {
        $num += 1 ; # Increase counter
        my $idx = first_index { $_ eq $mspc } @dspc;
        print $writefile
        "\{D$num\.\} EMISS = $mspc :  $vd[$idx] ;\n" ;
        print "$mspc:\t$vd[$idx]\n"
# Otherwise use standard value:
  } } }

# Close all files
    close(FILE);
}
close($writefile);

print "\n\033[94mOutput written to 'emiss.kpp'.\033[0m\n\n"

#######################################################################
