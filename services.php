<?php
 header("Content-type: text/xml");
 header("Connection: close");
 header("Expires: -1");
?>
<CiscoIPPhoneMenu>
  <Title>slacker.com services</Title>
  <Prompt>Choose a service</Prompt>

  <MenuItem>
    <Name> Order Some Food</Name>
    <URL>http://slacker.com/cisc0/food.php</URL>
  </MenuItem>

</CiscoIPPhoneMenu>
