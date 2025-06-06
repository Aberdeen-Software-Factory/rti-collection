<script setup>
import ArtifactCard from './ArtifactCard.vue'
import artifactList from './data.js'


</script>

<template>
    <div class="main">
        <ArtifactCard v-bind:artifact="artifactList[0]"/>
        <ArtifactCard v-bind:artifact="artifactList[2]"/>
        <ArtifactCard v-bind:artifact="artifactList[3]"/>
    </div>
</template>

<style scoped>
.main {
  padding:10px;
  display:grid;
  grid-template-columns: 1fr;
  gap:10px;
}

@media (min-width:414px){
  .main{
    grid-template-columns: 1fr 1fr;
  }
}

@media (min-width:768px){
  .main{
    grid-template-columns: 1fr 1fr 1fr;
  }
}

@media (min-width:1200px){
  .main{
    grid-template-columns: 1fr 1fr 1fr 1fr;
  }
}
</style>