<script>
  export default {
    data() {
      return {
        date: "...",
      }
    },
   	methods: {
      async getDate() {
        this.date = "loading ..."
        try {
          const res = await fetch("/api/date/")
          if (!res.ok) {
            this.date = "Error: Network response was not OK"
          }
          this.date = await res.text()
     	} catch(error) {
          this.date = `Error: ${error}`
        }
      }
    }
  }
</script>

<template>
  <button @click="getDate">Get date</button>
  <p>{{ date }}</p>
</template>
