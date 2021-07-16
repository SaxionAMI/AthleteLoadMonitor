<template>
  <v-container id="chart" class="pa-0">
    <v-layout justify-center align-center>
      <v-flex lg8 xl6>
        <apexchart
          type="line"
          :options="chartOptions"
          :series="series"
          v-bind="setChartData"
        />
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import Vue from 'vue'
import moment from 'moment'
import VueApexCharts from 'vue-apexcharts'

Vue.use(VueApexCharts)
Vue.component('apexchart', VueApexCharts)

export default {
  name: 'ChartPlayer',
  props: ['trainings', 'chart-choice', 'items', 'averages'],
  data() {
    return {
      series: [
        {
          name: 'Actual',
          // type: "bar",
          data: [],
        },
        {
          name: 'Average',
          data: [],
        },
        {
          name: 'Predicted',
          data: [],
        },
      ],
      chartOptions: {
        chart: {
          zoom: {
            enabled: true,
          },
          toolbar: {
            show: true,
            tools: {
              zoomin: false,
              zoomout: false,
              pan: true,
              download: false,
            },
          },
        },

        title: {
          text: '',
          align: 'center',
          style: {
            fontSize: '16px',
            color: '#000',
          },
        },
        dataLabels: {
          enabled: false,
        },
        colors: ['#4b7ea9', '#0c1532', '#979999'],
        stroke: {
          width: [2, 1, 1],
          curve: 'straight',
          dashArray: [4, 0, 4],
        },
        markers: {
          size: [3, 0, 3],
          hover: {
            sizeOffset: 6,
          },
        },
        xaxis: {
          categories: [],
          type: 'datetime',
          label: {
            formatter: function(value, timestamp, index) {
              return moment(new Date(timestamp)).format('DD-MM-YYYY, HH:mm')
            },
          },
        },
        yaxis: {
          labels: {
            formatter: value => {
              return value.toFixed(1)
            },
          },
        },
        tooltip: {
          y: [
            {
              title: {
                formatter: function(val) {
                  return val
                },
              },
            },
            {
              title: {
                formatter: function(val) {
                  return val + ' per training'
                },
              },
            },
            {
              title: {
                formatter: function(val) {
                  return val + ' per training'
                },
              },
            },
          ],
          x: {
            format: 'dd MMM yyyy HH:mm',
          },
        },
        grid: {
          borderColor: '#f1f1f1',
        },
      },
    }
  },
  computed: {
    setChartData() {
      var choice = this.chartChoice
      if (choice) {
        var trainings = this.trainings
        this.chartOptions.title.text = choice.label

        for (let i = 0; i < trainings.length; i++) {
          if(trainings[i][choice.actual]) { // only show positive values
            this.chartOptions.xaxis.categories.push(trainings[i].timestamp)
            this.series[0].data.push(
                    trainings[i][choice.actual] ? trainings[i][choice.actual] : 0
            )
            this.series[1].data.push(
                    this.averages[choice.average] ? this.averages[choice.average] : 0
            )
            if (trainings[i][choice.predicted]) {
              this.series[2].data.push(trainings[i][choice.predicted])
            }
          }
        }
      }
    },
  },
}
</script>

<style lang="scss"></style>
