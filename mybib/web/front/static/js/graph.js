$(document).ready(function() {

    var fields = [
"ID",
"title",
"address",
"acmid",
"year",
"isbn",
"_bibtex",
"numpages",
"url",
"pages",
"series",
"ENTRYTYPE",
"publisher",
"location",
"booktitle",
"doi",
    ]

var referencesNodes =  "references{ID}";
var authorNodes = "authors{name}";
var keywordNodes = "keywords{value}";
var referenceNodes = "references{ID}";
var projectNodes = "projects{name}";




    var searchButton = $("#searchButton");
    var authorsCheck = $("#authorsCheck");
    var keywordsCheck = $("#keywordsCheck");
    var projectsCheck = $("#projectsCheck");
    var referencesCheck = $("#referencesCheck");

    searchButton.click(function(e) {
        var query_fields = fields.slice();
        if(authorsCheck.is(':checked')) {
            query_fields.push(authorNodes);
        }
        if(keywordsCheck.is(':checked')) {
            query_fields.push(keywordNodes);
        }
        if(projectsCheck.is(':checked')) {
            query_fields.push(projectNodes);
        }
        if(referencesCheck.is(':checked')){
            query_fields.push(referenceNodes);
        }

        console.log(query_fields.join(', '));

        query_graph("{ papers {" + query_fields.join(', ') + '} }');
    });


    function query_graph(query) {
    console.log(query);
    $.get('graphql?query=' + query, function(response) {
        papers = response.data.papers

        var nodes = []
        var edges = []
        var keywordsContainer = {};
        var authorsContainer = {};
        if(papers !== undefined) {
            for (var i = 0; i < papers.length; i++) {
              paper = papers[i];
              node = {
                id:paper.ID,
                label:paper.title,
                color:{background:"green"},
              };
              nodes.push(node);


              var keywords = paper.keywords;
              if(keywords !== undefined) {

                for (var j = 0; j < keywords.length; j++) {
                    keyword = keywords[j];
                    edges.push({
                        from:paper.ID,
                        to:"kw_"+keyword.value,
                        arrows:"to",
                        //label: "has keyword"
                    })
                    if(keyword.value in keywordsContainer) {
                        continue;
                    }
                    keywordsContainer[keyword.value] = keyword.value;
                }
              }
              var authors = paper.authors;
              if(authors !== undefined) {
                for (var j = 0; j < authors.length; j++) {
                    author = authors[j];
                    console.log(author);
                    edges.push({
                        from:paper.ID,
                        to:"author_"+author.name,
                        arrows:"from",
                        //label: "wrote"
                    })
                    if(author.name in authorsContainer) {
                        continue;
                    }
                    authorsContainer[author.name] = author.name;
                }
              }

                var references = paper.references;
              if(references !== undefined) {

                for (var j = 0; j < references.length; j++) {
                    reference = references[j];
                    edges.push({
                        from:paper.ID,
                        to:reference.ID,
                        arrows:"from",
                        //label: "references"
                    });
                }
              }
          }

            for (var prop in keywordsContainer) {
                if (keywordsContainer.hasOwnProperty(prop)) {
                    nodes.push({
                        id:"kw_" +prop,
                        label:prop,
                        color:{background:"blue"},
                    });
                }
            }

            for (var prop in authorsContainer) {
                if (authorsContainer.hasOwnProperty(prop)) {
                    nodes.push({
                        id:"author_" +prop,
                        label:prop,
                        color:{background:"purple"},
                    });
                }
            }

        }


    var options = {
        interaction: {
            multiselect: true,
            dragNodes: true,
            dragView: true,
        },
        nodes: {
            shape: 'dot',
            size: 15,
            font: {
                size: 10,
                color: '#000'
            }
        }
    };

        var container = document.querySelector('#myNetwork');

        var data = {
            nodes: nodes,
            edges: edges
        };

        network = new vis.Network(container, data, options);
    });
    }
});