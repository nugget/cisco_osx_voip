#!/usr/bin/perl -Tw

$ENV{'PATH'} = '/bin:/usr/bin:/usr/local/bin';
$ENV{'BASH_ENV'} = '';

use strict;
use CGI;

&CGI::ReadParse;
my $q=CGI->new();
my $me = 'http://slacker.com/cisc0/directory.cgi';

# $::in{'st'} = 'moo';
if(! $::in{'st'} ) {
  display_form();
  exit;
} else {
  my @matches = search_names($::in{'st'});
  if(@matches == 1) {
    display_card($matches[0]);
  } else {
    display_menu(@matches);
  }
}

sub search_names {
  my ($buf) = @_;

  my @retbuf;

  $retbuf[@retbuf] = 'David McNett';
  $retbuf[@retbuf] = 'Paul Followell';
  $retbuf[@retbuf] = 'Tom Neville';

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
    print "<URL>$me?name=$urlname</URL>\n";
    print "</MenuItem>\n";
  }

  print "</CiscoIPPhoneMenu>\n";

}
sub display_card {
  my ($name) = @_;

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
