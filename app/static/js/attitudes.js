function showWordCloud(showdata, anchor, name) {


        am4core.ready(function() {
            if (name != 'Biden'){
                am4core.useTheme(am4themes_material);

            } 

            am4core.useTheme(am4themes_animated);
            // Themes end
            
            var iconPath = "M53.5,476c0,14,6.833,21,20.5,21s20.5-7,20.5-21V287h21v189c0,14,6.834,21,20.5,21 c13.667,0,20.5-7,20.5-21V154h10v116c0,7.334,2.5,12.667,7.5,16s10.167,3.333,15.5,0s8-8.667,8-16V145c0-13.334-4.5-23.667-13.5-31 s-21.5-11-37.5-11h-82c-15.333,0-27.833,3.333-37.5,10s-14.5,17-14.5,31v133c0,6,2.667,10.333,8,13s10.5,2.667,15.5,0s7.5-7,7.5-13 V154h10V476 M61.5,42.5c0,11.667,4.167,21.667,12.5,30S92.333,85,104,85s21.667-4.167,30-12.5S146.5,54,146.5,42 c0-11.335-4.167-21.168-12.5-29.5C125.667,4.167,115.667,0,104,0S82.333,4.167,74,12.5S61.5,30.833,61.5,42.5z"            
            var chart = am4core.create(anchor, am4charts.SlicedChart);
            chart.hiddenState.properties.opacity = 0; // this makes initial fade in effect
            
            chart.data = showdata;

            
            var series = chart.series.push(new am4charts.PictorialStackedSeries());
            series.dataFields.value = "value";
            series.dataFields.category = "name";
            series.alignLabels = true;
            
            series.maskSprite.path = iconPath;
            series.ticks.template.locationX = 1;
            series.ticks.template.locationY = 0.5;
            
            series.labelsContainer.width = 200;
            
            chart.legend = new am4charts.Legend();
            chart.legend.position = "left";
            chart.legend.valign = "bottom";

            var title = chart.titles.create();
            title.text = name;
            title.fontSize = 40;
            title.fontWeight = "800";
            
            });


};

function init() {

    d3.json(`/getattitudeData`, function (attitude) {
        mark = 1

        console.log(attitude)

        keys = Object.keys(attitude);


        for (j = 0; j < keys.length; j++) {
            showData = []

            att = attitude[keys[j]];
            showData.push({
                "category": 'Postive',
                "value": att*100, 
                "full": 100
            })

            showData.push({
                "category": 'Negative',
                "value": (1-att)*100, 
                "full": 100
            })

            console.log(showData)
            showWordCloud(showData, "chartdivatt" + mark, keys[j]);
            mark += 1;
        }


    });


};

init();
