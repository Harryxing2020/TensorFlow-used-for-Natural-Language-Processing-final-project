function showWordCloud(showdata, anchor, name) {


    am4core.ready(function() {
    
        // Themes begin
        am4core.useTheme(am4themes_animated);
        // Themes end
        
        // Create chart instance
        var chart = am4core.create(anchor, am4charts.XYChart);
        
        // Add data
        chart.data = showdata;
        
        // Use only absolute numbers
        chart.numberFormatter.numberFormat = "#.#s";
        
        // Create axes
        var categoryAxis = chart.yAxes.push(new am4charts.CategoryAxis());
        categoryAxis.dataFields.category = "tweet";
        categoryAxis.renderer.grid.template.location = 0;
        categoryAxis.renderer.inversed = true;
        
        var valueAxis = chart.xAxes.push(new am4charts.ValueAxis());
        valueAxis.extraMin = 0.1;
        valueAxis.extraMax = 0.1;
        valueAxis.renderer.minGridDistance = 40;
        valueAxis.renderer.ticks.template.length = 5;
        valueAxis.renderer.ticks.template.disabled = false;
        valueAxis.renderer.ticks.template.strokeOpacity = 0.4;
        valueAxis.renderer.labels.template.adapter.add("text", function(text) {
          return text == "Negitive" || text == "Positive" ? text : text + "%";
        })
        
        // Create series
        var Negitive = chart.series.push(new am4charts.ColumnSeries());
        Negitive.dataFields.valueX = "Negitive";
        Negitive.dataFields.categoryY = "tweet";
        Negitive.clustered = false;
        
        var NegitiveLabel = Negitive.bullets.push(new am4charts.LabelBullet());
        NegitiveLabel.label.text = "{valueX}%";
        NegitiveLabel.label.hideOversized = false;
        NegitiveLabel.label.truncate = false;
        NegitiveLabel.label.horizontalCenter = "right";
        NegitiveLabel.label.dx = -10;
        
        var Positive = chart.series.push(new am4charts.ColumnSeries());
        Positive.dataFields.valueX = "Positive";
        Positive.dataFields.categoryY = "tweet";
        Positive.clustered = false;
        
        var PositiveLabel = Positive.bullets.push(new am4charts.LabelBullet());
        PositiveLabel.label.text = "{valueX}%";
        PositiveLabel.label.hideOversized = false;
        PositiveLabel.label.truncate = false;
        PositiveLabel.label.horizontalCenter = "left";
        PositiveLabel.label.dx = 10;
        
        var NegitiveRange = valueAxis.axisRanges.create();
        NegitiveRange.value = -10;
        NegitiveRange.endValue = 0;
        NegitiveRange.label.text = "Negitive";
        NegitiveRange.label.fill = chart.colors.list[0];
        NegitiveRange.label.dy = 20;
        NegitiveRange.label.fontWeight = '600';
        NegitiveRange.grid.strokeOpacity = 1;
        NegitiveRange.grid.stroke = Negitive.stroke;
        
        var PositiveRange = valueAxis.axisRanges.create();
        PositiveRange.value = 0;
        PositiveRange.endValue = 10;
        PositiveRange.label.text = "Positive";
        PositiveRange.label.fill = chart.colors.list[1];
        PositiveRange.label.dy = 20;
        PositiveRange.label.fontWeight = '600';
        PositiveRange.grid.strokeOpacity = 1;
        PositiveRange.grid.stroke = Positive.stroke;

        
        var title = chart.titles.create();
        title.text = name;
        title.fontSize = 40;
        title.fontWeight = "800";
        
        });


};

function init() {

    d3.json(`/getattitudeData`, function (attitude) {

        console.log(attitude['Trumplist'].length)
        console.log(attitude['Bidenlist'].length)

        showWordCloud(attitude['Trumplist'].slice(0, 10), 'chartdivatt1', "Trump")
        showWordCloud(attitude['Bidenlist'].slice(0, 10), 'chartdivatt2', "Biden")

    });


};

init();
