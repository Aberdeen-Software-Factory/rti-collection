<script setup>
import TextInput from './TextInput.vue'
import TagsInput from './TagsInput.vue'
import LargeTextInput from './LargeTextInput.vue'
import SelectInput from './SelectInput.vue'

const metadata = defineModel()

const ccLicenseOptions = [
    { value: "CC BY",           text: "Attribution (CC BY)" },
    { value: "CC BY-SA",        text: "Attribution-ShareAlike (CC BY-SA)" },
    { value: "CC BY-ND",        text: "Attribution-NoDerivs (CC BY-ND)" },
    { value: "CC BY-NC",        text: "Attribution-NonCommercial (CC BY-NC)" },
    { value: "CC BY-NC-SA",     text: "Attribution-NonCommercial-ShareAlike (CC BY-NC-SA)" },
    { value: "CC BY-NC-ND",     text: "Attribution-NonCommercial-NoDerivs (CC BY-NC-ND)" },
]
</script>

<template>
    <TextInput label="Name" v-model="metadata.name"/>
    <TagsInput label="Language" v-model="metadata.language"/>
    <TagsInput label="Script/Writing System" v-model="metadata.script"/>
    <TagsInput label="Archeological Provenance" v-model="metadata.provenance"/>
    <TagsInput label="Current Location" v-model="metadata.location"/>
    <TagsInput label="Photographer(s)" v-model="metadata.photographer"/>
    <TextInput label="Date(s) of Imaging" v-model="metadata.date"/>
    <LargeTextInput label="Bibliography" v-model="metadata.bibliography"/>
    <LargeTextInput label="Notes" v-model="metadata.notes"/>
    <TagsInput label="Keywords" v-model="metadata.keywords"/>
    <SelectInput label="Copyright" :options="ccLicenseOptions" v-model="metadata.copyright"/>
</template>