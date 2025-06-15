<script setup>
defineProps(['title', 'description', 'creator', 'date', 'copyright'])
</script>

<template>
    <table>
        <tbody>
            <tr>
                <th>Description</th>
                <td>{{ description }}</td>
            </tr>
            <tr>
                <th>Creator</th>
                <td>{{ creator }}</td>
            </tr>
            <tr>
                <th>Date</th>
                <td>{{ date }}</td>
            </tr>
            <tr>
                <th>Copyright</th>
                <td>{{ copyright }}</td>
            </tr>
        </tbody>
    </table>
</template>

<style scoped>
table {
    width: 100%;
    border-spacing: 0 0.5rem; /* horizontal gap: 0, vertical gap: 1rem */
    border-collapse: separate;
    margin-top: 1rem;
}

th {
    text-align: left;
    vertical-align: top;
    font-weight: bold;
    white-space: nowrap; /* Prevent label wrapping */
    width: 1%; /* Shrink to fit content */
    padding-right: 1rem;
}

td {
    width: auto; /* Take remaining space */
    padding: 0;
}
</style>