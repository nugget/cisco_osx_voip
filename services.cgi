#!/usr/bin/perl -Tw

$ENV{'PATH'} = '/bin:/usr/bin:/usr/local/bin';
$ENV{'BASH_ENV'} = '';

use strict;
use CGI;

&CGI::ReadParse;
my $q=CGI->new();
my $dir= 'http://slacker.com/cisc0';
my $me = $dir . '/services.cgi';

my @menu_main = (
  "CiscoIPPhoneMenu\tstyle",
  "slacker.com services\ttitle",
  "Choose an option\tprompt",
  "Phone Book\t$dir/directory.cgi",
  "Test Page\t$dir/test.cgi",
  "Food Delivery\t$me?item=food",
  "Berbee\thttp://phone-xml.berbee.com/menu.xml",
  "Flame\thttp://flame.tiefighter.org/fwd/xml/",
);

my @menu_food = (
  "CiscoIPPhoneDirectory\tstyle",
  "Local Food Delivery\ttitle",
  "Select a Restaurant\tprompt",
  "Papa John's\t+1 512 219-7272",
  "Pizza Hut\t+1 512 335-9444",
  "Dominos\t+1 512 331-7701",
  "Austins Pizza\t+1 512 506-8188",
);  

my @menu = @menu_main;
if($::in{'item'}) {
  if($::in{'item'} =~ /^([a-z0-9]+)$/) {
    my $evalstring =  '@menu = @menu_' . $1;
    eval $evalstring;
  }
}

display_header();
display_menu(@menu);

sub display_header {
print <<EOF;
Content-type: text/xml
Connection: close
Expires: -1

EOF
}

sub display_menu {
  my @menubuf = @_;
  my $style = 'menu';

  for(my $i=0; $i<@menubuf; $i++) {
    my $buf = $menubuf[$i];
    if($buf =~ /^([^\t]+)\tstyle$/i) {
      $style = $1;
      print "<" . $style . ">\n";
    } elsif($buf =~ /^([^\t]+)\ttitle$/i) {
      print "<Title>$1</Title>\n";
    } elsif($buf =~ /^([^\t]+)\tprompt$/i) {
      print "<Prompt>$1</Prompt>\n";
    } elsif($buf =~ /^([^\t]+)\t(.*)$/i) {
      display_item($style,$1,$2);
    }
  }
  print "</" . $style . ">\n";
}

sub display_item {
  my($style,$name,$target) = @_;
  if($style eq 'CiscoIPPhoneMenu') {
    print "<MenuItem>\n<Name> $name</Name>\n<URL>$target</URL>\n</MenuItem>\n";
  } elsif($style eq 'CiscoIPPhoneDirectory') {
    print "<DirectoryEntry>\n<Name> $name</Name>\n<Telephone>$target</Telephone>\n</DirectoryEntry>\n";
  }

}
