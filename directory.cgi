#!/usr/bin/perl -Tw

$ENV{'PATH'} = '/bin:/usr/bin:/usr/local/bin';
$ENV{'BASH_ENV'} = '';

use strict;
use CGI;

&CGI::ReadParse;
my $q=CGI->new();
my $me = 'http://slacker.com/cisc0/directory.cgi';
my $vcd = '/htdocs/cisc0/vCards';

# $::in{'dn'} = 'David MCNETT';
if($::in{'st'}) {
  my @matches = search_names($::in{'st'});
  if(@matches == 1) {
    display_card($matches[0]);
  } else {
    display_menu(@matches);
  }
} elsif($::in{'dn'}) {
  display_card($::in{'dn'});
} else {
  display_form();
}

sub search_names {
  my ($search) = @_;
  my @retbuf;

  open NAMES, "cd $vcd && egrep -li '^TEL;' *.vcf|";
  while(<NAMES>) {
    if($_ =~ /(.*)\.vcf$/) {
      my $filename = $1;
      if(($filename =~ / $search/i) or ($filename =~ /^$search/i)) {
        $retbuf[@retbuf] = $filename;
      }
    }
  }

  return @retbuf;
}

sub display_menu {
  my @names = @_;

  display_header();

  print "<CiscoIPPhoneMenu>\n";
  print "<Title>Matching Contacts</Title>\n";
  print "<Prompt>Select a Contact</Prompt>\n";

  for(my $i=0; $i<@names; $i++) {
    my $urlname = $q->escape($names[$i]);
    print "<MenuItem>\n";
    print "<Name>" . $names[$i] . "</Name>\n";
    print "<URL>$me?dn=$urlname</URL>\n";
    print "</MenuItem>\n";
  }

  print "</CiscoIPPhoneMenu>\n";

}
sub display_card {
  my ($name) = @_;

  my @entries;
  my $pref_entry = 0;

  display_header();

  print "<CiscoIPPhoneDirectory>\n";
  print "<Title>$name</Title>\n";
  print "<Prompt>Select a Number</Prompt>\n";

  open CARD, $vcd . '/' . $name . '.vcf';
  while(<CARD>) {
    my $buf = $_;

    $buf =~ s/\r//;
    $buf =~ s/\n//;

    if($buf =~ /^(TEL|item\d+\.TEL)[;:]/) {
      my ($num,$label) = ('+1 317 555-1212','Unknown');

      if($buf =~ /^(item\d+)\.TEL[;:]/) {
        $label = $1;
      } elsif($buf =~ /type=([^:;]+)[:;]/) {
        $label = $1;
      }

      if($buf =~ s/type=pref//i) {
        $pref_entry = @entries;
      }

      if($buf =~ /:(.*)$/) {
        $num = $1;
      }

      $num =~ s/^sip://;
      $label = lc($label);

      $entries[@entries] .= "<DirectoryEntry>\n" . 
                            "<Name>$label</Name>\n" .
			    "<Telephone>" . $num . "</Telephone>\n" .
                            "</DirectoryEntry>\n";
    } elsif($buf =~ /^(item\d+)\.X-ABLabel:(.+)$/) {
      my ($itemnum,$itemlabel) = ($1,$2);
      for(my $i=0; $i<@entries; $i++) {
        $entries[$i] =~ s/<Name>$itemnum<\/Name>/<Name>$itemlabel<\/Name>/i;
      }
    }
  }
  close CARD;
  print $entries[$pref_entry];
  for(my $i=0; $i<@entries; $i++) {
    if($i != $pref_entry) {
      print $entries[$i];
    }
  }

  print "</CiscoIPPhoneDirectory>\n";

}


sub display_header {
print <<EOF;
Content-type: text/xml
Connection: close
Expires: -1

EOF
}

sub display_form {
display_header();
print <<EOF;
<CiscoIPPhoneInput>
<Title>Search for a Contact</Title>
<Prompt>Enter a search string</Prompt>
<URL>$me</URL>
<InputItem>
<DisplayName>Name</DisplayName>
<QueryStringParam>st</QueryStringParam>
<InputFlags>L</InputFlags>
<DefaultValue></DefaultValue>
</InputItem>
</CiscoIPPhoneInput>
EOF
}
