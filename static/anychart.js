function myFunction() {
    var x = document.getElementById("year-select").value;
    document.getElementById("demo").innerHTML = "You selected: " + x;

    // Clear map container
    document.getElementById("container").innerHTML = ""; 
     

    //#container-map.html("");
    // load the data
    anychart.data.loadJsonFile(`/data/${x}`, function (data) {
        // console.log(data)

        // Variable to hold the data
        var geoData = data

        console.log(geoData)

        // // create a new array with the resulting data
        var data = [];

        // Go through the initial data
        for (var i = 0; i < geoData.length; i++) {

            // insert the resulting data in the array using the AnyChart keywords 
            data.push({ id: geoData[i].ISO2, value: geoData[i].Happiness_Score, title: geoData[i].Country })

        };

         console.log(data)

        // connect the data with the map
        var chart = anychart.map(data);

        chart.geoData(anychart.maps.world);

        // specify the chart type and set the series 
        var series = chart.choropleth(data);

        // set the chart title
        chart.title("Happiness Score by Country");

        // color scale ranges
        ocs = anychart.scales.ordinalColor([
            { less: 3.999 },
            { from: 4, to: 4.499 },
            { from: 4.5, to: 4.999 },
            { from: 5, to: 5.499 },
            { from: 5.50, to: 5.999 },
            { from: 6, to: 6.499 },
            { from: 6.50, to: 6.999 },
            { greater: 7 }
        ]);

        // set scale colors
        ocs.colors(["rgb(255, 0, 0)", "	rgb(255, 128, 0)", "rgb(255,255,0)", "rgb(0,255,0)", "rgb(0,255,255)", "rgb(0,128,255)", "rgb(0,0,255)", "rgb(128,0,255)"]);

        // tell the series what to use as a colorRange (colorScale)
        series.colorScale(ocs);

        // enable the legend
        chart.legend(true);

        // set the source mode of the legend and add styles
        chart.legend()
            .itemsSourceMode("categories")
            .position('right')
            .align('top')
            .itemsLayout('vertical')
            .padding(50, 0, 0, 20)
            .paginator(false);
            

        // set the container id
        chart.container('container');

        // draw the chart
        chart.draw();
    });


};

