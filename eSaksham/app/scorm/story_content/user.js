function ExecuteScript(strId)
{
  switch (strId)
  {
      case "6YNDNisn4m0":
        Script1();
        break;
  }
}

function Script1()
{
  var m_names = new Array("January", "February", "March",
"April", "May", "June", "July", "August", "September",
"October", "November", "December");
var today = new Date();
var dd = today.getDate();
var mm = today.getMonth();
var yyyy = today.getFullYear();
if(dd<10) { dd='0'+dd }
var date= m_names[mm]+' '+dd+', '+yyyy;
var player = GetPlayer();
player.SetVar("SystemDate",date);
}

