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

    var referencesNodes = "references{ID}";
    var authorNodes = "authors{name}";
    var keywordNodes = "keywords{value}";
    var referenceNodes = "references{ID}";
    var projectNodes = "projects{name}";
    var hash = window.location.hash.substr(1);



    var searchButton = $("#searchButton");
    var authorsCheck = $("#authorsCheck");
    var keywordsCheck = $("#keywordsCheck");
    var projectsCheck = $("#projectsCheck");
    var referencesCheck = $("#referencesCheck");
    var queryParameterText = $('#queryParameter');
    var queryTypeSelect = $("#queryType");

    function do_qyuery() {
        var query_fields = fields.slice();
        if (authorsCheck.is(':checked')) {
            query_fields.push(authorNodes);
        }
        if (keywordsCheck.is(':checked')) {
            query_fields.push(keywordNodes);
        }
        if (projectsCheck.is(':checked')) {
            query_fields.push(projectNodes);
        }
        if (referencesCheck.is(':checked')) {
            query_fields.push(referenceNodes);
        }

        queryType = queryTypeSelect.val();
        if (queryType !== 'papers') {
            queryType += ' (parameter: "' + queryParameterText.val() + '")'
        }

        query_graph("{ " + queryType + " {" + query_fields.join(', ') + '} }');
    }

    searchButton.click(function(e) {
        do_qyuery();
    });


    function query_graph(query) {
        console.log(query);
        $.get('graphql?query=' + query, function(response) {
            papers = response.data[queryTypeSelect.val()];
            console.log(papers)

            var nodes = []
            var edges = []
            var keywordsContainer = {};
            var authorsContainer = {};
            var projectsContainer = {};
            if (papers !== undefined) {
                for (var i = 0; i < papers.length; i++) {
                    paper = papers[i];
                    node = {
                        id: paper.ID,
                        label: paper.title,
                        color: {
                            background: "green"
                        },
                    };
                    nodes.push(node);


                    var keywords = paper.keywords;
                    if (keywords !== undefined) {

                        for (var j = 0; j < keywords.length; j++) {
                            keyword = keywords[j];
                            edges.push({
                                from: paper.ID,
                                to: "kw_" + keyword.value,
                                arrows: "to",
                                //label: "has keyword"
                            })
                            if (keyword.value in keywordsContainer) {
                                continue;
                            }
                            keywordsContainer[keyword.value] = keyword.value;
                        }
                    }
                    var authors = paper.authors;
                    if (authors !== undefined) {
                        for (var j = 0; j < authors.length; j++) {
                            author = authors[j];
                            console.log(author);
                            edges.push({
                                from: paper.ID,
                                to: "author_" + author.name,
                                arrows: "from",
                                //label: "wrote"
                            })
                            if (author.name in authorsContainer) {
                                continue;
                            }
                            authorsContainer[author.name] = author.name;
                        }
                    }

                    var references = paper.references;
                    if (references !== undefined) {

                        for (var j = 0; j < references.length; j++) {
                            reference = references[j];
                            edges.push({
                                to: paper.ID,
                                from: reference.ID,
                                arrows: "from",
                                label: "cites"
                            });
                        }
                    }



                    var projects = paper.projects;
                    if (projects !== undefined) {
                        for (var j = 0; j < projects.length; j++) {
                            project = projects[j];
                            edges.push({
                                from: paper.ID,
                                to: "project_" + project.name,
                                arrows: "from",
                                //label: "wrote"
                            })
                            if (project.name in projectsContainer) {
                                continue;
                            }
                            projectsContainer[project.name] = project.name;
                        }
                    }
                }

                for (var prop in keywordsContainer) {
                    if (keywordsContainer.hasOwnProperty(prop)) {
                        nodes.push({
                            id: "kw_" + prop,
                            label: prop,
                            color: {
                                background: "blue"
                            },
                        });
                    }
                }

                for (var prop in authorsContainer) {
                    if (authorsContainer.hasOwnProperty(prop)) {
                        nodes.push({
                            id: "author_" + prop,
                            label: prop,
                            color: {
                                background: "purple"
                            },
                        });
                    }
                }

                for (var prop in projectsContainer) {
                    if (projectsContainer.hasOwnProperty(prop)) {
                        nodes.push({
                            id: "project_" + prop,
                            label: prop,
                            color: {
                                background: "purple"
                            },
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
                },
                edges: {
                    font: {
                        size: 9,
                        color: '#000'
                    }
                }
            };

            var container = document.querySelector('#myNetwork');

            var data = {
                nodes: nodes,
                edges: edges
            };

            var network = new vis.Network(container, data, options);

            // Interactions

            network.on("click", function (params) {
                params.event = "[original event]";
                document.getElementById('debug').innerHTML = '<h2>Click event:</h2>' + JSON.stringify(params, null, 4);
                console.log('click event, getNodeAt returns: ' + this.getNodeAt(params.pointer.DOM));
            });

            network.on("doubleClick", function (params) {
                params.event = "[original event]";
                document.getElementById('debug').innerHTML = '<h2>doubleClick event:</h2>' + JSON.stringify(params, null, 4);
                var node_id = this.getNodeAt(params.pointer.DOM);
                window.location.href = '/papers/' + node_id;
            });

        });
    }

    if( hash != 'noquery' ) {
        do_qyuery();
    }
    if (hash == 'debug') {
        $('#debug').show();
    }
});