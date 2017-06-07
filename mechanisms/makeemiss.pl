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
my $num= 0 ;  # counter for reaction labels in output file

## Temporary auxiliary arrays/variables
#  @lines:  lines read in from input file
#  @spl:    array with separated species and vd from input line
#  @idx:    index of current species in species/vd array

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
my $writefile;#output KPP file "depos.kpp"

########################################################################

# Define input data file:
if (exists $ARGV[1]) {
  $fdat = $ARGV[1];
} else {
  $fdat = '../InitCons/emiss.dat';
}
if (-f "$fdat") {
  print "\n\033[94mData file:         $fdat\n";
} elsif ($fdat eq "0" || $fdat eq '-') {
  print "\033[95m\nWarning! Option '$ARGV[1]':\n",
        "An empty KPP emissions file has been created!\033[0m\n\n";
  print "\n\033[94mOutput written to 'emiss.kpp'.\033[0m\n\n";
  open($writefile, ">","emiss.kpp")
  or die "Could not open file emiss.kpp: $!";
  print $writefile "//Currently no emissions.\n",
                   "//Template file with sample equation:\n\n",
                   "//{E1.} EMISS = CH4 : 9.62E+07;\n";
  close($writefile);
  exit;
} else {
  print "\033[95m\nWarning! File '$fdat' does not exist.\n",
        "An empty KPP emissions file has been created!\033[0m\n\n";
  print "\n\033[94mOutput written to 'emiss.kpp'.\033[0m\n\n";
  open($writefile, ">","emiss.kpp")
  or die "Could not open file emiss.kpp: $!";
  print $writefile "//Currently no emissions.\n",
                   "//Template file with sample equation:\n\n",
                   "//{E1.} EMISS = CH4 : 9.62E+07;\n";
  close($writefile);
  exit;
}

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
open($writefile, ">","emiss.kpp") or die "Could not open file emiss.kpp: $!";
print $writefile "#EQUATIONS\n";

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
        my @idx = grep { $dspc[$_] eq $mspc } 0 .. $#dspc; # find index in array
        print $writefile
        "\{D$num\.\} EMISS = $mspc :  $vd[$idx[-1]] ;\n" ;
        print "$mspc:\t$vd[$idx[-1]]\n";
# Otherwise use standard value:
  } } }

# Close all files
    close(FILE);
}
close($writefile);

if ($num ==0) {
  open($writefile, ">","emiss.kpp")
  or die "Could not open file emiss.kpp: $!";
  print $writefile "//Currently no emissions.\n",
             "//Template file with sample equation:\n\n",
             "//{E1.} EMISS = CH4 : 9.62E+07;\n";
  close($writefile);
  print "\n\033[95mWarning! No species in the data file\n",
        "matched the species in the current mechanism.\n",
        "An empty sample KPP emissions file has been created.\033[0m\n";
}

print "\n\033[94mOutput written to 'emiss.kpp'.\033[0m\n\n";

#######################################################################
