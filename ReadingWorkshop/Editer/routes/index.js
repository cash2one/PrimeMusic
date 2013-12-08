
/*
 * GET home page.
 */

var DB = require('../node_modules/DB.js');

exports.index = function(req, res){
  res.render('index', { title: 'Express', });
};

exports.find = function(req, res){
    var word = req.body['word'];
    var db = new DB();
    db.find_word_group_list(word, function(document_list){
            console.log(word);
            console.log(document_list.length);
            res.render('wordgrouplist', {"wordgroups": document_list});
            });
};

exports.update = function(req, res){
    var wordgroup = req.body;
    var db = new DB();
    db.update_one_word_group(wordgroup, function(result){
            if (result == 0){
                res.send(200, 'err');
            }
            else{          
                res.send(200, 'success');
            }
            }); 
};

exports.delete = function(req, res){
    var wordgroup = req.body;
    var db = new DB();
    db.remove_one_word_group(wordgroup, function(result){
            if (result == 0){
                res.send(200, 'err');
            }
            else{          
                res.send(200, 'success');
            }
            }); 
};
