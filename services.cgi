#!/usr/bin/perl -Tw

$ENV{'PATH'} = '/bin:/usr/bin:/usr/local/bin';
$ENV{'BASH_ENV'} = '';

use strict;
use CGI;

&CGI::ReadParse;
my $q=CGI->new();
my $me = 'http://slacker.com/cisc0/services.cgi';
display_header();
display_menu(1);

sub display_header {
print <<EOF;
Content-type: text/xml
Connection: close
Expires: -1

EOF
}

sub display_menu {
print <<EOF;
<CiscoIPPhoneMenu>
<Title>slacker.com services</Title>
<Prompt>Choose a service</Prompt>
<MenuItem>
<Name> Phone Book</Name>
<URL>http://slacker.com/cisc0/directory.cgi</URL>
</MenuItem>
<MenuItem>
<Name> Food Delivery</Name>
<URL>http://slacker.com/cisc0/food.php</URL>
</MenuItem>
</CiscoIPPhoneMenu>
EOF
}
