function getText(str) {
    str = str.replace(/<\/?[^>]*>/g, '');
    str = str.replace(/[ | ]*\n/g, '\n');
    str = str.replace(/\n[\s| | ]*\r/g, '\n');
    return str;
}

function saveOption() {
    var arg = $(this).attr("name");
    var tableId = "table" + arg;
    var table = document.getElementById(tableId);
    var tbody = table.tBodies[0];
    
    var wordgroup = {};
    wordgroup["meaning"] = getText(tbody.rows[0].cells[1].innerHTML);
    wordgroup["paraphrase"] = getText(tbody.rows[1].cells[1].innerHTML);
    wordgroup["word_list"] = [];
    
    for (var i = 2; i < tbody.rows.length; i += 1){
        var row = tbody.rows[i];
        word = {};
        word["word"] = getText(row.cells[0].innerHTML);
        word["meaning_list"] = getText(row.cells[1].innerHTML).split("\n");
        if (word["word"] == "") {
            continue;
        }
        wordgroup["word_list"].push(word);
    }
    wordgroup["arg"] = arg;
    $.post("/update", wordgroup, function(data, status){
		    alert(data);
            var input_word = document.getElementById("input-word").value;
            $.post("/find", {word: input_word}, function(data, status){
			    $("#word-group-list").html(data);
                $(".save").click(saveOption);     
                $(".delete").click(deleteOption);     
                $(".add").click(addOption);     
                });     
            });
}

function deleteOption() {
    var arg = $(this).attr("name");
    var tableId = "table" + arg;
    var divId = "div" + arg;
    var table = document.getElementById(tableId);
    var tbody = table.tBodies[0];
    
    var wordgroup = {};
    wordgroup["meaning"] = getText(tbody.rows[0].cells[1].innerHTML);
    wordgroup["paraphrase"] = getText(tbody.rows[1].cells[1].innerHTML);
    wordgroup["word_list"] = [];
    
    for (var i = 2; i < tbody.rows.length; i += 1){
        var row = tbody.rows[i];
        word = {};
        word["word"] = getText(row.cells[0].innerHTML);
        word["meaning_list"] = getText(row.cells[1].innerHTML).split("\n");
        if (word["word"] == "") {
            continue;
        }
        wordgroup["word_list"].push(word);
    }
    wordgroup["arg"] = arg;
    $.post("/delete", wordgroup, function(data, status){
            alert(data);
            document.getElementById(divId).innerHTML="";
            });
}

function addOption(){
    var arg = $(this).attr("name");
    var tableId = "table" + arg;
    var table = document.getElementById(tableId);
    var tbody = table.tBodies[0];
    var tr = tbody.insertRow(2);
    var td_1 = tr.insertCell(0);
    td_1.innerHTML = "<div contenteditable='true'></div>";
    var td_2 = tr.insertCell(1);
    td_2.innerHTML = "<div contenteditable='true'></div>";
}

$(document).ready(function(){
    $("#search-word").click(function(){
		var input_word = document.getElementById("input-word").value;
		$.post("/find", {word: input_word}, function(data, status){
			$("#word-group-list").html(data);
			$(".save").click(saveOption);     
			$(".delete").click(deleteOption);     
			$(".add").click(addOption);     
		});     
	});     
});
