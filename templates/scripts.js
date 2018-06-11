$(document).ready(function(){

api_version = "r4"
scan_status={}
//function to make get requests
function make_cont_get(url,patt,flag,sites,index){
  $.get(url, function(data) {

    if (flag==0) {

      if (data.status.indexOf(patt) >= 0) {
        setTimeout(function (){
          make_cont_get(url,patt,0,sites,index);
        }, 10000);
      }
      else{
        $("#current_exec_stat").text("Collecting the Web Sites involved..");
        $("#show-progress").hide()
        list_domains_identified();
      }
    }
    else if (flag==1) {

      if (data.status.indexOf(patt) < 0) {
          make_cont_get(url,patt,1,sites,index);
          $("#current_exec_stat").text("Scanning "+sites[index]);
          $("#tjex-prog").attr("style", "width: "+data.status+"%");
          $("#tjex-prog").attr("class", "determinate amber lighten-1");
      }
      else{
        $("#tjex-prog").attr("style", "width: 100%");
        $("#current_exec_stat").text("Completed Scanning "+sites[index]);
        $("#list-alerts").append("<ul class=\"collapsible\"><li><div class=\"collapsible-header\"><i class=\"material-icons\">bug_report</i>"+sites[index]+"</div><div class=\"collapsible-body\"><ul id=\"domain-"+index+"\" class=\"collapsible\"></ul></div></li></ul>");
        console.log("Meen");
        console.log("#domain-"+index);
        $('.collapsible').collapsible();
        //show report
        ind=index
        $.get('/ess/api/'+api_version+'/zap/getscanresults/', function(rep) {

            if (rep.status=="Report fetched") {
              //add fetched report

                for (var i = 1; i <= rep.report.length; i++) {
                  if (rep.report[i-1]["url"].indexOf(sites[ind])>=0) {
                    if (rep.report[i-1]["risk"]=="Low") {
                      color=""
                      icon="panorama_fish_eye"
                    }

                    else if (rep.report[i-1]["risk"]=="Medium") {
                      color="orange-text"
                      icon="lens"
                    }

                    else if (rep.report[i-1]["risk"]=="High") {
                      color="red-text"
                      icon="lens"
                    }

                    fields=Object.keys(rep.report[i-1])

                    sub_code2=""
                    for (var j = 0; j < fields.length; j++) {
                      //if the field is not empty
                      if (rep.report[i-1][fields[j]]!="") {
                          sub_code2=sub_code2+"<p><b>"+fields[j]+": </b>"+_.escape(rep.report[i-1][fields[j]])+"</p>";
                      }
                    }
                    sub_code1="<li><div class = \"collapsible-header\"><i class = \"material-icons "+color+"\">"+icon+"</i>Alert "+i.toString()+"</div><div class = \"collapsible-body\">"
                    sub_code3="</div></li>"
                    $("#domain-"+ind).append(sub_code1+sub_code2+sub_code3);

                  }
                }


            }
            else{
              //show error
              $("#domain-"+index).text("Error fetching report")
            }
      })

        if (index+1<sites.length) {
          index=index+1
          make_condi_post("/ess/scan/start/",{"site":sites[index]},"started","ZAP Exception");
          make_cont_get("/ess/api/"+api_version+"/zap/getstatus/ascan/","100",1,sites,index);
        }
      }
    }
  });
}

//Function that lists the created secjob upon clicking the create button of the secjob
function tjob_exec_wait(){
  make_cont_get("/ess/tjob/execstatus/","not-called",0,"",0)
}

//Display the domains in the history
function list_domains_identified(){
  $.get("/ess/api/"+api_version+"/getsites/", function(data) {
    $("#list-domains").show();
    $("#progress-msg").show();
    $("#start-scan-btn").show();
    //$("#list-alerts").show();
    for (var i = 0; i < data.sites.length; i++) {
      $("#domains-follow").append("<div class=\"chip\">"+data.sites[i]+"<i class=\"close material-icons\">close</i></div>")
    }

    $("#current_exec_stat").text("Remove out-of-scope web sites and click the \"START SCAN\" button");

  });
}

function make_condi_post(url,body,scondition,fcondition){

  $.ajax({
        type: "POST",
        url: url,
        // The key needs to match your method's input parameter (case-sensitive).
        data: JSON.stringify(body),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(re){
        if(re.status==scondition){
          toast("Scan started",4000);
          //showScanStatus($("#start-scan"));
        }
        else if(re.status==fcondition){
          toast("Scan could not start due to ZAP Exception");
        }

            },
        failure: function(errMsg) {
      toast("Active Scanning Failed",4000);
      alert(errMsg);
        }
  });
}


    $("#progress-msg").hide();
    $("#list-alerts").hide();
    $("#start-scan-btn").hide();
    $( "#stop-scan-btn" ).hide()
    status=tjob_exec_wait();

    $( "#start-scan-btn" ).click(function() {
      $( "#stop-scan-btn" ).show()
      $("#current_exec_stat").text("Starting Scan");
      $("#tjex-prog").attr("style", "width:"+0+"%");
      domains=$("div.chip");
      if (domains.length>0) {
        $("#list-alerts").show();
      }
      sites=[]
      for (var i = 0; i < domains.length; i++) {
        sites.push(domains[i].firstChild.data.toString())
      }
      $("#show-progress").show()
      if (sites.length>0) {
        make_condi_post("/ess/scan/start/",{"site":sites[0]},"started","ZAP Exception");
        make_cont_get("/ess/api/"+api_version+"/zap/getstatus/ascan/","100",1,sites,0);

      }

    });

    $( "#stop-scan-btn" ).click(function() {
      $.get("/ess/api/"+api_version+"/stop/", function(data) {
        if (data.status== "stopped-ess") {
          toast("ESS Stopped")
        }
        else {
          toast("Error")
        }
      });
    });
//    get_pscan_results();
//    start_ascan();
});
