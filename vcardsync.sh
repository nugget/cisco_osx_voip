#!/bin/sh

cd $HOME/Documents
echo Exporting vCards
ab2vcard -d vCards
chmod 755 $HOME/Documents/vCards
chmod 644 $HOME/Documents/vCards/*.vcf
echo Syncing to dazed
rsync -auz --delete $HOME/Documents/vCards/ nugget@dazed.slacker.com:/htdocs/cisc0/vCards/
echo Constructing CID inserts
ssh dazed.slacker.com /htdocs/cisc0/cidexport.pl > /tmp/cid.sh
chmod 755 /tmp/cid.sh
echo Copying insert script to suburbia
scp -qp /tmp/cid.sh suburbia.slacker.com:/tmp/cid.sh && rm /tmp/cid.sh
echo Performing inserts
ssh suburbia.slacker.com "setenv TERM vt100 && sudo /tmp/cid.sh | grep -ci success && rm /tmp/cid.sh"
echo Done!
