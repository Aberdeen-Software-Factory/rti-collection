<script setup>
import Collection from '@/components/Collection.vue';
import Header from '@/components/Header.vue';
</script>

<template>
    <Header :segments="[{ label: 'Collection' }]" title="Artifacts"/>
    <Collection/>
</template>

<style scoped>
</style>