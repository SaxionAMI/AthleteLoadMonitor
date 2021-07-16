<template>
  <v-container id="chart" class="pa-0">
    <v-layout justify-center align-center>
      <v-flex lg8 xl6>
        <apexchart
          type="bar"
          height="350"
          :options="chartOptions"
          :series="series"
          v-bind="setBar"
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
  name: 'ChartBar',
  props: ['playerData', 'training', 'chart', 'items', 'averages'],
  data() {
    return {
      playData: this.playerData,
      chartChoice: this.chart,
      dropdownItems: this.items,
      trainingData: this.training,
      series: [
        {
          name: 'Inflation',
          data: [],
        },
      ],
      chartOptions: {
        chart: {
          height: 350,
          type: 'bar',
        },
        plotOptions: {
          bar: {
            dataLabels: {
              position: 'top', // top, center, bottom,
            },
          },
        },
        dataLabels: {
          enabled: true,
          formatter: function(val) {
            return val
          },
          offsetY: -20,
          style: {
            fontSize: '12px',
            colors: ['#304758'],
          },
        },
        colors: ['#1b4350'],
        xaxis: {
          categories: ['Average', 'Actual', 'Predicted'],
          position: 'bottom',
          labels: {
            style: {
              fontSize: '14px',
              colors: ['#000', '#000', '#000'],
            },
          },
          axisBorder: {
            show: false,
          },
          axisTicks: {
            show: false,
          },
          crosshairs: {
            fill: {
              type: 'gradient',
              gradient: {
                colorFrom: '#D8E3F0',
                colorTo: '#BED1E6',
                stops: [0, 100],
                opacityFrom: 0.4,
                opacityTo: 0.5,
              },
            },
          },
          tooltip: {
            enabled: true,
            offsetY: -35,
          },
        },
        fill: {
          gradient: {
            shade: 'light',
            type: 'horizontal',
            shadeIntensity: 0.25,
            gradientToColors: undefined,
            inverseColors: true,
            opacityFrom: 1,
            opacityTo: 1,
            stops: [50, 0, 100, 100],
          },
        },
        yaxis: {
          axisBorder: {
            show: false,
          },
          axisTicks: {
            show: false,
          },
          labels: {
            show: false,
            formatter: function(val) {
              return val.toFixed(0)
            },
          },
        },
        title: {
          text: '',
          align: 'centre',
          style: {
            fontSize: '16px',
            color: '#000',
          },
        },
      },
    }
  },
  computed: {
    setBar() {
      console.log(this.averages)
      console.log(this.choice)
      var choice = this.chartChoice
      var training = this.trainingData
      var average = this.averages[choice.average]
      var actDate = new Date(training.timestamp).toLocaleString()

      this.chartOptions.title.text = choice.label
      this.series[0].data.push(average)
      this.series[0].data.push(training[choice.actual])
      var predChoice = choice.predicted
      if (training[predChoice]) {
        this.chartOptions.xaxis.categories = ['Average', 'Actual', 'Predicted']
        this.series[0].data.push(training[predChoice])
      } else {
        this.chartOptions.xaxis.categories = ['Average', 'Actual']
      }
      // for (let i = 0; i < predTrainings.length; i++) {
      //     var predDate = moment(predTrainings[i].Date).format("DD-MM-YYYY")
      //     if (actDate === predDate) {
      //         this.series[0].data.push(predTrainings[i][choice])
      //     }
      // }
    },
  },
}
</script>

<style scoped></style>
