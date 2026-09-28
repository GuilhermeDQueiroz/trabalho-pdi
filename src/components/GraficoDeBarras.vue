<template>
  <div id="chart" class="LStyleChartContainer">
    <apexchart
      type="bar"
      height="380"
      :options="chartOptions"
      :series="series"
      :key="countAtualizacao"
    ></apexchart>
  </div>
</template>

<script setup lang="ts">
// Vue
import { ref, watch } from 'vue'

interface PropTypes {
  valores?: number[] | string[]
  labels: string[]
  titulo?: string
  simboloAntesLabel?: string | null
  simbolosDepoisLabel?: string | null
}

const props = withDefaults(defineProps<PropTypes>(), {
  titulo: 'Histograma de Níveis de Cinza',
  simboloAntesLabel: null,
  simbolosDepoisLabel: null,
  valores: () => [],
  labels: () => []
})

const countAtualizacao = ref(0)

const series = ref([
  {
    name: 'Qtd Pixels',
    data: props.valores
  }
])

const chartOptions = ref({
  chart: {
    height: 380,
    type: 'bar',
    toolbar: {
      show: true,
      tools: {
        download: true,
        selection: true,
        zoom: true,
        zoomin: true,
        zoomout: true,
        pan: true,
        reset: true
      }
    },
    background: 'transparent'
  },
  theme: {
    mode: 'dark'
  },
  colors: ['#cccccc'],
  plotOptions: {
    bar: {
      borderRadius: 1,
      columnWidth: '95%'
    }
  },
  dataLabels: {
    enabled: false
  },
  xaxis: {
    categories: props.labels,
    title: {
      text: 'Nível de Cinza (0 = Preto ... 255 = Branco)',
      style: {
        color: '#a0a0a0',
        fontWeight: 'bold',
        fontSize: '13px'
      }
    },
    labels: {
      style: {
        colors: '#808080'
      },
      rotate: 0,
      formatter: function (val: string) {
        const num = Number(val)
        return num % 32 === 0 ? val : ''
      }
    },
    axisBorder: {
      color: '#333333'
    },
    axisTicks: {
      color: '#333333'
    }
  },
  yaxis: {
    title: {
      text: 'Frequência (Pixels)',
      style: {
        color: '#a0a0a0',
        fontWeight: 'bold',
        fontSize: '13px'
      }
    },
    labels: {
      style: {
        colors: '#808080'
      }
    }
  },
  tooltip: {
    theme: 'dark',
    y: {
      formatter: function (val: number) {
        return `${val} pixels`
      }
    }
  },
  grid: {
    borderColor: '#262626'
  }
})

watch(
  () => props.valores,
  (novosValores) => {
    series.value = [
      {
        name: 'Qtd Pixels',
        data: novosValores
      }
    ]
    countAtualizacao.value += 1
  }
)
</script>

<style scoped>
.LStyleChartContainer {
  background-color: #121212;
  border-radius: 6px;
  padding: 12px;
  border: 1px solid #2b2b2b;
}
</style>
