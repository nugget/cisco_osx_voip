#!/usr/bin/perl -Tw

$ENV{'PATH'} = '/bin:/usr/bin:/usr/local/bin';
$ENV{'BASH_ENV'} = '';

use strict;
use CGI;

my $vcd = '/htdocs/cisc0/vCards';

open NAMES, "cd $vcd && egrep -li '^TEL;' *.vcf|";
while(<NAMES>) {
  if($_ =~ /(.*)\.vcf$/) {
    my $filename = $1;
    extract_nums($filename);
  }
}
close NAMES;

sub extract_nums {
  my ($name) = @_;
  my $fn = $name . ".vcf";

  my @entries;
  my $pref_entry = 0;

  open CARD, $vcd . '/' . $fn;
  while(<CARD>) {
    my $buf = $_;

    $buf =~ s/\r//;
    $buf =~ s/\n//;

    if($buf =~ /^(TEL|item\d+\.TEL)[;:]/) {
      my ($num,$label) = ('3175551212','Unknown');

      if($buf =~ s/type=pref//i) {
        $pref_entry = @entries;
      }

      if($buf =~ /^(item\d+)\.TEL[;:]/) {
        $label = $1;
      } else {
        while($buf =~ s/type=([^:;]+)//i) {
          $label .= " " . $1;
        }
	$label =~ s/unknown //i;
      }


      if($buf =~ /:(.*)$/) {
        $num = $1;
      }

      $num =~ s/^sip://;

      if($num =~ /^\+(\d+) /) {
        if($1 != 1) {
          $num = "";
        }
      }

      $label =~ s/cell/mobile/i;
      $label = lc($label);
      $label =~ s/\b(\w)/\U$1/g;

      if($num =~ s/ ?x ?(\d+)$//) {
        $label .= " (x$1)";
      }

      $num =~ s/[^\d]//g;
      $num =~ s/^1//;

      if($num) {
        $entries[@entries] .= "asterisk -rx 'database put cidname $num " .
                              "\"$name ($label)\"'\n";
      }

    } elsif($buf =~ /^(item\d+)\.X-ABLabel:(.+)$/) {
      my ($itemnum,$itemlabel) = ($1,$2);
      if($itemlabel eq lc($itemlabel)) {
        $itemlabel =~ s/\b(\w)/\U$1/g;
      }
      for(my $i=0; $i<@entries; $i++) {
        $entries[$i] =~ s/\($itemnum\)/\($itemlabel\)/i;
      }
    }
  }
  close CARD;
  for(my $i=0; $i<@entries; $i++) {
    print $entries[$i];
  }
}
