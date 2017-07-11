#!/usr/bin/perl
use strict;
use warnings;

### Variable declarations
## Data arrays and variables
my @dspc;     # species with predefined deposition velocities
my @vd;       # deposition velocities
my $mspc;     # species used in current mechanism
my $vdstd;    # standard deposition velocitiy
              # (defined with key word "DEPOS" in depos.dat)
my $num= 0;   # counter for reaction labels in output file

## Temporary auxiliary arrays/variables
#  @lines:  lines read in from input file
#  @spl:    array with separated species and vd from input line
#  @idx:    index of current species in species/vd array

## Switch to extend standard value to all species in mechanism
#  (retrieved from 3rd script argument)
my $flstd = 1; # 0: use only values from data file
               # 1: extend standard value to all species (standard option)

## file handling
#  $dfu:       file unit for data file "depos.dat"
#              with predefined deposition velocities
my $fdat = "";#file name (and path) of data file
my $fout;#     name of output kpp file with depositon mechanism
#  $kfu:       input KPP files with definitions of species
#              used in current mechanism
my @fkpp;#     list of file names (and paths) of input KPP files
#              without file ending '.kpp'
#              In script argument, put list in quotes
#              and separate elements by whitespaces
my $writefile;#output KPP file "depos.kpp"

########################################################################
### Retrieval of script arguments

# Read in input kpp file(s) from 1st script argument
# or set default as inorganic/organic
if (exists $ARGV[0]) {
  my $targ = $ARGV[0];
  $targ =~ s/^\s+//;
  $targ =~ s/\s+$//;
  @fkpp = split(/\s+/, $targ);
} else {
  @fkpp = ('inorganic','organic');
}

# Read in input data file from 2nd script argument
# or ask for folder path and file name
if (exists $ARGV[1]) {
  $fdat = $ARGV[1];
} #else {
#   print "Enter folder path and name of data file: ";
#   $fdat = <STDIN>;
#   chomp $fdat;
#   print "$fdat\n";
# }

# Read in output kpp file from 3rd script argument
# or define default as "./mechanisms/depos_<data file name>.kpp"
if (exists $ARGV[2]) {
  $fout = $ARGV[2];
} elsif ($fdat eq "") {
  $fout = "";
} else {
  $fout = $fdat;
  $fout =~ s/\.\/InitCons\//\.\/mechanisms\/depos_/;
  $fout =~ s/\.dep/\.kpp/;
}

# Define use of standard value from third script argument
# or use as default
if (exists $ARGV[3]) {
  $flstd = $ARGV[3];
}

########################################################################

### Screen output and checks
if (-f "$fdat") {
  print "\n\033[94mData file:         $fdat\n";
} else {
  print "\033[95m\nWarning! No deposition scheme generated.\033[0m\n\n";
  exit;
}

print "KPP output file:   $fdat\n";
print "KPP input file(s): ", join(", ", @fkpp), "\n";
if ($flstd =~ 0) {
  print "Only deposition data from $fdat used.\033[0m\n";
} elsif ($flstd =~ 1) {
  print "Standard vd extended to all species in mechanism.\033[0m\n";
}

########################################################################

# Read in species and definitions of deposition velocities (vd)
# from data file "depos.dat"
open (my $dfu, '<', $fdat) or die "Could not open file $fdat: $!";
chomp(my @lines = <$dfu>);
close($dfu);

# Split array of input lines into array of species names and vd
# unless it is an empty line or comment line starting with '#'
print "\nPredefined deposition values\n----------------------------\n";
foreach (@lines) {
  $_  =~ s/\#.*//;
  if ($_ !~ /^\s*$/) {
    $_ =~ s/^\s+//;
    my @spl = split(/\s+/, $_);
    push @dspc, $spl[0];
    push @vd, $spl[1];
    print "$_\n" if $dspc[-1] !~ /DEPOS/;
} }

# Find standard value and save to vdstd.
# If no standard value is defined in input file, use 5.00d-6.
my @idx = grep { $dspc[$_] eq "DEPOS" } 0 .. $#dspc; # find index in array
if ($idx[-1] > 0) { # for double entries, always the last entry is used
  $vdstd = $vd[$idx[-1]];
} else {
  $vdstd = "5.00d-6"
}

if ($flstd =~ 1) {
  print "----------------------------\n",
        "\033[92m\e[1mvd(standard): ",$vdstd, "\033[0m\n",
        "----------------------------\n" ;
} else {
  print "----------------------------\n";
}


########################################################################

# Open output file and set KPP EQUATIONS variable
open(my $writefile, ">",$fout) or die "Could not open file $fout: $!";
print $writefile "#EQUATIONS\n";

# Loop over KPP files
for my $kfu (@fkpp) {
  open( FILE, "<./mechanisms/$kfu.kpp" )
  or die("Couldn't open file ./mechanisms/$kfu.kpp:$!\\n");
# Find lines with species definitions
  while (<FILE>) {
    if (/.*\=\s*IGNORE.*/) {
# Get species and store in $mspc
      s/\s*(\w)\s*\=\s*IGNORE.*/$1/g ;
      $mspc = $_ ;
      chomp $mspc ;

# Define experimental values:
      if (grep(/^$mspc$/, @dspc)) {
        $num += 1 if $mspc !~ /EMISS/; # Increase counter
        @idx = grep { $dspc[$_] eq $mspc } 0 .. $#dspc;
        print $writefile
        "\{D$num\.\} $mspc = DUMMY :  DEPOS*\($vd[$idx[-1]]\) ;\n" ;
# Otherwise use standard value:
      } elsif ($flstd =~ 1) {
        $num += 1 if $mspc !~ /EMISS/; # Increase counter
        @idx = grep { $dspc[$_] eq $mspc } 0 .. $#dspc;
        print $writefile
        "\{D$num\.\} $mspc = DUMMY :  DEPOS*\($vdstd\) ;\n"
        if $mspc !~ /EMISS/;
  } } }

# Close all files
    close(FILE);
}
close($writefile);

print "\n\033[94mOutput written to $fout.\033[0m\n\n";

#######################################################################
