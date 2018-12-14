$(document).ready(function() {
    // create a network
    // create an array with nodes
    var nodes = new vis.DataSet([]);

    // create an array with edges
    var edges = new vis.DataSet([]);

    // create a network
    var container = document.getElementById('myNetwork');

    // provide the data in the vis format
    var data = {
        nodes: nodes,
        edges: edges
    };

    var options = {
        interaction: {
            multiselect: true,
            dragNodes: true,
            dragView: true,
        },
        nodes: {
            shape: 'dot',
            size: 15,
            color: '#ECBF26', // select color
            font: {
                size: 10,
                color: '#000'
            }
        }
    };

    // initialize your network!
    var network = new vis.Network(container, data, options);


    console.log('Loaded')
    $("#search").click(function(e) {
        serialised_data = $('#form').serialize();
        $.get('api/papers/search?' + serialised_data, function(data) {

            var newNodes = []

            for (i = 0; i < data.length; i++) {
                paper = data[i];
                newNodes.push({
                    "id": paper.ID,
                    "label": paper.title
                });
            }


            var updatedIds = nodes.add(newNodes);
        })
    });


    $("#reference").click(function(e) {
        nodes = network.getSelectedNodes();
        if (nodes.length == 2) {
            referee = nodes[0];
            referenced = nodes[1];

            var message = prompt("Referencing " + referenced + " from " + referenced);
            var content = {
                comment: message
            };
            var url = "/api/references/" + referee + "/" + referenced;
            console.log(content)
            $.ajax({
                url: url,
                type: "POST",
                data: JSON.stringify(content),
                contentType: "application/json",
                success: function(result) {
                    alert("Success!");
                }
            });

        } else {
            alert("Select two papers!");
        }

    });

    $('#addEntry').click(function(e) {
        var entry = $('#entry').val();

        $.ajax({
            url: "/api/papers",
            type: "POST",
            data: entry,
            contentType: "text/plain",
            success: function(data) {
                alert("Inserted!");
            }
        })

    });

    $.get('/api/recent', function(data) {

        var newNodes = []
        for (i = 0; i < data.nodes.length; i++) {
            paper = data.nodes[i];
            newNodes.push({
                "id": paper.ID,
                "label": paper.title
            });
        }
        var updatedIds = nodes.add(newNodes);

        var newEdges = []
        for (i = 0; i < data.references.length; i++) {
            reference = data.references[i];
            reference.arrows = "to"
            newEdges.push(reference);
        }
        var updatedEdges = edges.add(newEdges);
    })
});